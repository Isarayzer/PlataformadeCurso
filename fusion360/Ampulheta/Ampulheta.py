# -*- coding: utf-8 -*-
"""
Ampulheta paramétrica para impressão 3D (Fusion 360 - Script Python)

Cria/atualiza:
  - Parâmetros de usuário nomeados (Modify > Change Parameters)
  - Componente "Corpo_Ampulheta"  (revolução 360 + roscas + chanfros)
  - Componente "Tampa_Superior"   (rosca fêmea, canal de O-ring, estrias)
  - Componente "Tampa_Inferior"   (idêntica, girada 180 graus)
  - Esboço de corte "Secao_XZ_Validacao" e relatório de validação
  - (opcional) exportação STL / 3MF de cada componente

Fluxo paramétrico:
  1. Rode o script (Utilities > Add-Ins > Scripts > Ampulheta > Run).
  2. Altere valores em Modify > Change Parameters.
  3. Rode o script de novo: ele LÊ os valores atuais dos parâmetros
     (não os sobrescreve) e regenera os três componentes.
  Os filetes usam a expressão "Raio_Filete" e atualizam sem rodar de novo.
  Veja README.md para o motivo (API do Fusion não cria Coil paramétrico).

Unidades: o módulo de geometria trabalha em mm; a API do Fusion em cm.
"""

import adsk.core
import adsk.fusion
import traceback
import math
import os
import sys
import importlib

_AQUI = os.path.dirname(os.path.abspath(__file__))
if _AQUI not in sys.path:
    sys.path.insert(0, _AQUI)
import ampulheta_geom as G   # noqa: E402
importlib.reload(G)

MM = 0.1   # mm -> cm

NOMES_COMPONENTES = ('Corpo_Ampulheta', 'Tampa_Superior', 'Tampa_Inferior')

_app = None
_ui = None


# ---------------------------------------------------------------------------
# Parâmetros
# ---------------------------------------------------------------------------

def garantir_parametros(design):
    """Cria os parâmetros que faltam e devolve G.Parametros com os valores
    ATUAIS do documento (o usuário pode tê-los alterado)."""
    up = design.userParameters
    padrao = G.Parametros()
    valores = padrao.como_dict()
    criados = []
    for nome, valor in valores.items():
        unid = G.UNIDADES.get(nome, 'mm')
        if up.itemByName(nome) is None:
            if nome == 'Parede_Gargalo':
                expr = 'Parede'          # acompanha a parede até você decidir reforçar
            elif unid == '':
                expr = str(int(valor))
            else:
                expr = '%g %s' % (valor, unid)
            up.add(nome, adsk.core.ValueInput.createByString(expr), unid,
                   G.COMENTARIOS.get(nome, ''))
            criados.append(nome)

    p = G.Parametros()
    for nome in valores:
        unid = G.UNIDADES.get(nome, 'mm')
        v = up.itemByName(nome).value
        if unid == 'mm':
            v = v / MM
        elif unid == 'deg':
            v = math.degrees(v)
        elif nome == 'Numero_Estrias':
            v = int(round(v))
        setattr(p, nome, v)
    return p, criados


# ---------------------------------------------------------------------------
# Utilidades de esboço / features
# ---------------------------------------------------------------------------

def P3(x, y, z):
    return adsk.core.Point3D.create(x * MM, y * MM, z * MM)


def _ponto_mais_proximo(entidade, alvo):
    a = entidade.startSketchPoint
    b = entidade.endSketchPoint
    da = a.geometry.distanceTo(alvo)
    db = b.geometry.distanceTo(alvo)
    return a if da <= db else b


def desenhar_laco(sketch, segs, flip=False, z_off=0.0):
    """Desenha um laço fechado (r, z) no esboço do plano XZ.
    flip=True aplica a rotação de 180 graus em torno de X (z -> -z)."""
    sketch.isComputeDeferred = True

    def S(pt):
        r, z = pt
        z = z + z_off
        if flip:
            z = -z
        return sketch.modelToSketchSpace(P3(r, 0.0, z))

    linhas = sketch.sketchCurves.sketchLines
    arcos = sketch.sketchCurves.sketchArcs
    ents = []
    for s in segs:
        if s[0] == 'line':
            ents.append(linhas.addByTwoPoints(S(s[1]), S(s[2])))
        else:
            ents.append(arcos.addByThreePoints(S(s[1]), S(s[2]), S(s[3])))
    # une os pontos coincidentes entre entidades consecutivas
    n = len(ents)
    for i in range(n):
        alvo = S(segs[i][-1])
        pa = _ponto_mais_proximo(ents[i], alvo)
        pb = _ponto_mais_proximo(ents[(i + 1) % n], alvo)
        if pa != pb:
            try:
                pa.merge(pb)
            except Exception:
                pass
    sketch.isComputeDeferred = False
    return ents


def maior_perfil(sketch):
    melhor, area = None, -1.0
    for i in range(sketch.profiles.count):
        pr = sketch.profiles.item(i)
        a = pr.areaProperties(adsk.fusion.CalculationAccuracy.MediumCalculationAccuracy).area
        if a > area:
            melhor, area = pr, a
    if melhor is None:
        raise RuntimeError('Esboço "%s" não gerou perfil fechado.' % sketch.name)
    return melhor


def revolver(comp, segs, nome, operacao, corpos=None, flip=False):
    sk = comp.sketches.add(comp.xZConstructionPlane)
    sk.name = nome
    desenhar_laco(sk, segs, flip=flip)
    prof = maior_perfil(sk)
    ri = comp.features.revolveFeatures.createInput(prof, comp.zConstructionAxis, operacao)
    ri.setAngleExtent(False, adsk.core.ValueInput.createByString('360 deg'))
    if corpos:
        ri.participantBodies = corpos
    f = comp.features.revolveFeatures.add(ri)
    f.name = nome
    return f


def filete_helicoidal(comp, perfil_local, hel, nome, flip=False):
    """Varre o perfil local (r, v) ao longo de uma hélice direita, como
    corpo novo. flip aplica a rotação de 180 graus em torno de X, que
    preserva o sentido da rosca (as duas extremidades ficam rosca direita)."""
    # hélice: esboço no plano XY (espaço do esboço = espaço do modelo)
    skh = comp.sketches.add(comp.xYConstructionPlane)
    skh.name = nome + '_Helice'
    skh.isComputeDeferred = True
    pts = adsk.core.ObjectCollection.create()
    for (x, y, z) in G.pontos_helice(hel['r'], hel['z0'], hel['voltas'], hel['passo']):
        if flip:
            y, z = -y, -z
        pts.add(skh.modelToSketchSpace(P3(x, y, z)))
    spline = skh.sketchCurves.sketchFittedSplines.add(pts)
    skh.isComputeDeferred = False

    # perfil no plano XZ, no início da hélice (ângulo 0)
    skp = comp.sketches.add(comp.xZConstructionPlane)
    skp.name = nome + '_Perfil'
    desenhar_laco(skp, perfil_local, flip=flip, z_off=hel['z0'])
    prof = maior_perfil(skp)

    caminho = comp.features.createPath(spline, False)
    si = comp.features.sweepFeatures.createInput(
        prof, caminho, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    si.orientation = adsk.fusion.SweepOrientationTypes.PerpendicularOrientationType
    sw = comp.features.sweepFeatures.add(si)
    sw.name = nome
    return sw.bodies.item(0)


def checar_filete(corpo, hel, meia_largura, flip=False):
    """Confere se o perfil não 'torceu' ao longo da hélice: pontos logo
    dentro dos flancos devem estar dentro do sólido e pontos logo fora,
    fora — no início, no meio e no fim da hélice."""
    dentro = adsk.fusion.PointContainment.PointInsidePointContainment
    erros = []
    for frac in (0.15, 0.5, 0.9):
        th = 2 * math.pi * hel['voltas'] * frac
        x = hel['r'] * math.cos(th)
        y = hel['r'] * math.sin(th)
        zc = hel['z0'] + hel['passo'] * th / (2 * math.pi)
        for dv, deve in ((0.0, True), (meia_largura - 0.15, True), (-(meia_largura - 0.15), True),
                         (meia_largura + 0.2, False), (-(meia_largura + 0.2), False)):
            yy, zz = (y, zc + dv)
            if flip:
                yy, zz = -yy, -zz
            esta = corpo.pointContainment(P3(x, yy, zz)) == dentro
            if esta != deve:
                erros.append('frac=%.2f dv=%.2f' % (frac, dv))
    return erros


def combinar(comp, alvo, ferramenta, operacao, nome):
    ferr = adsk.core.ObjectCollection.create()
    ferr.add(ferramenta)
    ci = comp.features.combineFeatures.createInput(alvo, ferr)
    ci.operation = operacao
    ci.isKeepToolBodies = False
    f = comp.features.combineFeatures.add(ci)
    f.name = nome
    return f


def arestas_circulares(corpo, raio_mm, z_mm, tol_mm=0.02):
    sel = adsk.core.ObjectCollection.create()
    for e in corpo.edges:
        g = e.geometry
        if g.objectType != adsk.core.Circle3D.classType():
            continue
        if abs(g.radius / MM - raio_mm) < tol_mm and abs(g.center.z / MM - z_mm) < tol_mm \
                and abs(g.center.x) < 1e-6 and abs(g.center.y) < 1e-6:
            sel.add(e)
    return sel


def filetar(comp, arestas, expr, nome):
    if arestas.count == 0:
        raise RuntimeError('Arestas para "%s" não encontradas.' % nome)
    fi = comp.features.filletFeatures.createInput()
    raio = adsk.core.ValueInput.createByString(expr)
    try:
        fi.edgeSetInputs.addConstantRadiusEdgeSet(arestas, raio, False)
    except AttributeError:          # API antiga
        fi.addConstantRadiusEdgeSet(arestas, raio, False)
    f = comp.features.filletFeatures.add(fi)
    f.name = nome
    return f


def novo_componente(design, nome):
    root = design.rootComponent
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = nome
    return occ


def remover_componentes_antigos(design):
    root = design.rootComponent
    removidos = 0
    for i in range(root.occurrences.count - 1, -1, -1):
        occ = root.occurrences.item(i)
        if occ.component.name in NOMES_COMPONENTES:
            occ.deleteMe()
            removidos += 1
    for i in range(root.sketches.count - 1, -1, -1):
        if root.sketches.item(i).name == 'Secao_XZ_Validacao':
            root.sketches.item(i).deleteMe()
    return removidos


# ---------------------------------------------------------------------------
# Construção
# ---------------------------------------------------------------------------

def construir_corpo(design, p, avisos):
    occ = novo_componente(design, 'Corpo_Ampulheta')
    comp = occ.component
    OP = adsk.fusion.FeatureOperations
    segs, info = G.perfil_corpo(p)
    hm, _ = G.helices(p)

    rev = revolver(comp, segs, 'Perfil_Corpo_Revolucao', OP.NewBodyFeatureOperation)
    corpo = rev.bodies.item(0)
    corpo.name = 'Corpo_Ampulheta'

    # concordância colar / ombro externo (parâmetro Raio_Filete, ao vivo)
    zoc = info['zoc']
    ar = arestas_circulares(corpo, p.r_raiz, zoc)
    for e in arestas_circulares(corpo, p.r_raiz, -zoc):
        ar.add(e)
    if info['canto_cubo']:
        rh, zh = info['canto_cubo']
        for z in (zh, -zh):
            for e in arestas_circulares(corpo, rh, z):
                ar.add(e)
    filetar(comp, ar, 'Raio_Filete', 'Filete_Colar_Ombro')
    corpo = comp.bRepBodies.item(0)

    # roscas macho (duas extremidades, ambas rosca direita) + chanfros de entrada
    perfil = G.perfil_filete_macho(p)
    meia = p.Crista_Rosca / 2.0 + p.Profundidade_Rosca / 2.0
    for flip, rotulo in ((False, 'Sup'), (True, 'Inf')):
        fil = filete_helicoidal(comp, perfil, hm, 'Rosca_Macho_' + rotulo, flip)
        err = checar_filete(fil, hm, meia, flip)
        if err:
            avisos.append('Rosca_Macho_%s: perfil possivelmente torcido no sweep (%s)'
                          % (rotulo, ', '.join(err)))
        combinar(comp, corpo, fil, OP.JoinFeatureOperation, 'Unir_Rosca_' + rotulo)
        corpo = comp.bRepBodies.item(0)
        revolver(comp, G.perfil_chanfro_rosca(p), 'Chanfro_Entrada_' + rotulo,
                 OP.CutFeatureOperation, [corpo], flip=flip)
        corpo = comp.bRepBodies.item(0)
    corpo.name = 'Corpo_Ampulheta'
    return occ, corpo, info


def construir_tampa(design, p, nome, flip, avisos):
    occ = novo_componente(design, nome)
    comp = occ.component
    OP = adsk.fusion.FeatureOperations
    _, hf = G.helices(p)
    sinal = -1.0 if flip else 1.0

    rev = revolver(comp, G.perfil_tampa(p), 'Perfil_Tampa_Revolucao',
                   OP.NewBodyFeatureOperation, flip=flip)
    tampa = rev.bodies.item(0)

    # rosca fêmea: ferramenta = filete macho deslocado radialmente de Folga_Rosca
    ferr = filete_helicoidal(comp, G.perfil_ferramenta_femea(p), hf, 'Rosca_Femea', flip)
    # a ferramenta é o filete macho transladado: mesma largura no raio médio
    meia = p.Crista_Rosca / 2.0 + p.Profundidade_Rosca / 2.0
    err = checar_filete(ferr, hf, meia, flip)
    if err:
        avisos.append('%s: ferramenta da rosca possivelmente torcida (%s)' % (nome, ', '.join(err)))
    combinar(comp, tampa, ferr, OP.CutFeatureOperation, 'Cortar_Rosca_Femea')
    tampa = comp.bRepBodies.item(0)

    # filete na aresta externa da saia (Raio_Filete, ao vivo)
    zb = p.z_aro - p.Comprimento_Saia
    filetar(comp, arestas_circulares(tampa, p.r_tampa, sinal * zb),
            'Raio_Filete', 'Filete_Saia')
    tampa = comp.bRepBodies.item(0)

    # estrias de pega (verticais -> imprimíveis sem suporte)
    n = int(p.Numero_Estrias)
    if n > 0:
        planos = comp.constructionPlanes
        pi = planos.createInput()
        pi.setByOffset(comp.xYConstructionPlane,
                       adsk.core.ValueInput.createByReal(sinal * (zb - 1.0) * MM))
        plano = planos.add(pi)
        plano.name = 'Plano_Estrias'
        sk = comp.sketches.add(plano)
        sk.name = 'Estrias'
        sk.isComputeDeferred = True
        rc = p.r_tampa + p.Raio_Estria - p.Profundidade_Estria
        for i in range(n):
            a = 2 * math.pi * i / n
            ctr = sk.modelToSketchSpace(P3(rc * math.cos(a), rc * math.sin(a), sinal * (zb - 1.0)))
            sk.sketchCurves.sketchCircles.addByCenterRadius(ctr, p.Raio_Estria * MM)
        sk.isComputeDeferred = False
        profs = adsk.core.ObjectCollection.create()
        for i in range(sk.profiles.count):
            profs.add(sk.profiles.item(i))
        comp_estria = p.Comprimento_Saia + p.Espessura_Tampa - 1.0 + 1.0
        ei = comp.features.extrudeFeatures.createInput(profs, OP.CutFeatureOperation)
        ext = adsk.fusion.DistanceExtentDefinition.create(
            adsk.core.ValueInput.createByReal(comp_estria * MM))
        direcao = (adsk.fusion.ExtentDirections.NegativeExtentDirection if flip
                   else adsk.fusion.ExtentDirections.PositiveExtentDirection)
        ei.setOneSideExtent(ext, direcao)
        ei.participantBodies = [tampa]
        f = comp.features.extrudeFeatures.add(ei)
        f.name = 'Estrias_Pega'
        tampa = comp.bRepBodies.item(0)

    tampa.name = nome
    return occ, tampa


# ---------------------------------------------------------------------------
# Validação
# ---------------------------------------------------------------------------

def validar(design, p, occs, info, avisos):
    linhas = []
    root = design.rootComponent
    fora = adsk.fusion.PointContainment.PointOutsidePointContainment

    for occ in occs:
        comp = occ.component
        for b in comp.bRepBodies:
            vol = b.physicalProperties.volume  # cm3
            linhas.append('%s: solido=%s, shells=%d, faces=%d, volume=%.2f cm3'
                          % (b.name, b.isSolid, b.shells.count, b.faces.count, vol))
            if not b.isSolid:
                avisos.append('%s NÃO é sólido.' % b.name)
            if comp.bRepBodies.count != 1:
                avisos.append('%s tem %d corpos (esperado 1).' % (comp.name, comp.bRepBodies.count))

    # canal aberto: eixo inteiro fora do corpo
    corpo = occs[0].component.bRepBodies.item(0)
    bloq = 0
    N = 400
    for i in range(N + 1):
        z = -p.z_aro + 2 * p.z_aro * i / N
        if corpo.pointContainment(P3(0, 0, z)) != fora:
            bloq += 1
    linhas.append('Canal central: %d de %d pontos do eixo bloqueados' % (bloq, N + 1))
    if bloq:
        avisos.append('Canal central obstruído!')

    # interferência entre corpo e tampas na posição montada
    try:
        col = adsk.core.ObjectCollection.create()
        for o in occs:
            col.add(o)
        ii = design.createInterferenceInput(col)
        ii.areCoincidentFacesIncluded = False
        res = design.analyzeInterference(ii)
        vol_int = 0.0
        for i in range(res.count):
            vol_int += res.item(i).interferenceBody.volume
        linhas.append('Interferência corpo x tampas: %d ocorrência(s), %.4f mm3'
                      % (res.count, vol_int * 1000.0))
        if vol_int * 1000.0 > 1e-3:
            avisos.append('Há interferência entre peças (%.4f mm3).' % (vol_int * 1000.0))
    except Exception as ex:
        linhas.append('Interferência: não foi possível analisar (%s)' % ex)

    # esboço de corte no plano XZ (complementa o Section Analysis)
    try:
        sk = root.sketches.add(root.xZConstructionPlane)
        sk.name = 'Secao_XZ_Validacao'
        ents = []
        for o in occs:
            for b in o.component.bRepBodies:
                ents.append(b.createForAssemblyContext(o))
        sk.intersectWithSketchPlane(ents)
        sk.isVisible = False
    except Exception as ex:
        linhas.append('Esboço de seção não criado (%s)' % ex)

    r = G.resumo(p)
    linhas.append('')
    linhas.append('Altura total montada: %.2f mm | corpo: %.2f mm' % (r['altura_total'], r['altura_corpo']))
    linhas.append('Diâmetro máximo: %.2f mm | cintura externa: %.2f mm'
                  % (r['diametro_max'], r['diametro_cintura_externa']))
    linhas.append('Gargalo: Ø%.2f mm x %.2f mm' % (p.Diametro_Gargalo, p.Altura_Gargalo))
    linhas.append('Parede do reservatório: %.2f mm (offset exato)' % p.Parede)
    linhas.append('Rosca: trapezoidal 90° (flancos 45°), passo %.2f mm, macho Ø%.2f/Ø%.2f, '
                  'fêmea Ø%.2f/Ø%.2f' % (p.Passo_Rosca, r['rosca_macho_maior'], r['rosca_macho_menor'],
                                        r['rosca_femea_maior'], r['rosca_femea_menor']))
    linhas.append('Folga radial %.2f mm | normal no flanco %.3f mm | axial total %.2f mm'
                  % (p.Folga_Rosca, r['folga_normal_flanco'], r['folga_axial_total']))
    linhas.append('Volume de cada reservatório: %.1f ml' % r['volume_reservatorio_ml'])
    return linhas


def exportar(design, occs, pasta):
    em = design.exportManager
    feitos = []
    for occ in occs:
        nome = occ.component.name
        stl = os.path.join(pasta, nome + '.stl')
        o = em.createSTLExportOptions(occ, stl)
        o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        em.execute(o)
        feitos.append(stl)
        try:
            f3 = os.path.join(pasta, nome + '.3mf')
            o3 = em.createC3MFExportOptions(occ, f3)
            em.execute(o3)
            feitos.append(f3)
        except Exception:
            pass
    return feitos


# ---------------------------------------------------------------------------
# Entrada
# ---------------------------------------------------------------------------

def run(context):
    global _app, _ui
    try:
        _app = adsk.core.Application.get()
        _ui = _app.userInterface
        design = adsk.fusion.Design.cast(_app.activeProduct)
        if not design:
            _ui.messageBox('Abra um design (workspace DESIGN) antes de rodar o script.')
            return
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType

        root = design.rootComponent
        existentes = [root.occurrences.item(i).component.name for i in range(root.occurrences.count)
                      if root.occurrences.item(i).component.name in NOMES_COMPONENTES]
        if existentes:
            r = _ui.messageBox(
                'Já existem componentes da ampulheta neste design.\n\n'
                'Regenerar com os valores ATUAIS dos parâmetros?\n'
                '(os componentes antigos serão substituídos; os parâmetros são mantidos)',
                'Ampulheta', adsk.core.MessageBoxButtonTypes.YesNoButtonType)
            if r != adsk.core.DialogResults.DialogYes:
                return

        p, criados = garantir_parametros(design)
        try:
            G.perfil_corpo(p)
            G.perfil_tampa(p)
            G.perfil_filete_macho(p)
            G.perfil_ferramenta_femea(p)
        except (G.ErroGeometria, ValueError) as ex:
            _ui.messageBox('Combinação de parâmetros inválida:\n\n%s\n\nNada foi alterado.' % ex)
            return

        remover_componentes_antigos(design)
        avisos = []
        occ_c, corpo, info = construir_corpo(design, p, avisos)
        adsk.doEvents()
        occ_s, _ = construir_tampa(design, p, 'Tampa_Superior', False, avisos)
        adsk.doEvents()
        occ_i, _ = construir_tampa(design, p, 'Tampa_Inferior', True, avisos)
        adsk.doEvents()

        occs = [occ_c, occ_s, occ_i]
        linhas = validar(design, p, occs, info, avisos)
        texto = '\n'.join(linhas)
        if criados:
            texto = 'Parâmetros criados: %d\n\n' % len(criados) + texto
        if avisos:
            texto += '\n\nATENÇÃO:\n- ' + '\n- '.join(avisos)
        else:
            texto += '\n\nValidação: OK'
        _ui.messageBox(texto, 'Ampulheta - validação')

        r = _ui.messageBox('Exportar STL e 3MF de cada componente?', 'Ampulheta',
                           adsk.core.MessageBoxButtonTypes.YesNoButtonType)
        if r == adsk.core.DialogResults.DialogYes:
            dlg = _ui.createFolderDialog()
            dlg.title = 'Pasta para exportação'
            if dlg.showDialog() == adsk.core.DialogResults.DialogOK:
                arquivos = exportar(design, occs, dlg.folder)
                _ui.messageBox('Exportado:\n' + '\n'.join(arquivos))
    except Exception:
        if _ui:
            _ui.messageBox('Falha:\n{}'.format(traceback.format_exc()))
