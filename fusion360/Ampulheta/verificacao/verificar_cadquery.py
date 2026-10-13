# -*- coding: utf-8 -*-
"""
Verificação offline da geometria da ampulheta com CadQuery (OpenCASCADE).

Reconstrói EXATAMENTE a mesma geometria do script do Fusion 360 (a partir do
mesmo módulo ampulheta_geom.py) e verifica:
  - sólidos válidos e fechados (manifold / watertight);
  - interferência zero entre corpo e tampas montados;
  - canal central aberto ao longo de todo o eixo;
  - folga das roscas;
  - espessura da parede dos reservatórios;
  - overhangs na orientação de impressão;
  - exporta STEP/STL/3MF e uma vista de corte (Section Analysis) em PNG.

Uso:
  pip install cadquery trimesh manifold3d matplotlib
  python verificar_cadquery.py [pasta_saida]
"""

import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

import cadquery as cq                      # noqa: E402
import ampulheta_geom as G                 # noqa: E402


def wire_de_segmentos(segs, z_off=0.0, flip=False):
    """Workplane XZ (x local = X, y local = Z) com o laço fechado."""
    def P(pt):
        r, z = pt
        z = z + z_off
        return (r, -z if flip else z)
    wp = cq.Workplane('XZ').moveTo(*P(segs[0][1]))
    for s in segs:
        if s[0] == 'line':
            wp = wp.lineTo(*P(s[2]))
        else:
            wp = wp.threePointArc(P(s[2]), P(s[3]))
    return wp.close()


def revolver(segs, flip=False):
    return wire_de_segmentos(segs, flip=flip).revolve(360, (0, 0, 0), (0, 1, 0))


def filete_helicoidal(perfil_local, hel, flip=False):
    """Varre o perfil (r, v) ao longo da hélice (rosca direita)."""
    altura = hel['voltas'] * hel['passo']
    helice = cq.Wire.makeHelix(hel['passo'], altura, hel['r'],
                               center=cq.Vector(0, 0, hel['z0']))
    perfil = wire_de_segmentos(perfil_local, z_off=hel['z0'])
    solido = perfil.sweep(cq.Workplane().add(helice), isFrenet=True)
    if flip:
        solido = solido.rotate((0, 0, 0), (1, 0, 0), 180)
    return solido


def aresta_circular(solido, raio, z, tol=0.02):
    sel = []
    for e in solido.edges().vals():
        if e.geomType() != 'CIRCLE':
            continue
        c = e.Center()
        if abs(e.radius() - raio) < tol and abs(c.z - z) < tol:
            sel.append(e)
    return sel


def construir(p):
    segs, info = G.perfil_corpo(p)
    hm, hf = G.helices(p)

    # ---------------- corpo ----------------
    corpo = revolver(segs)
    zoc = info['zoc']
    arestas = aresta_circular(corpo, p.r_raiz, zoc) + aresta_circular(corpo, p.r_raiz, -zoc)
    if info['canto_cubo']:
        rh, zh = info['canto_cubo']
        arestas += aresta_circular(corpo, rh, zh) + aresta_circular(corpo, rh, -zh)
    assert len(arestas) >= 2, 'arestas do colar não encontradas'
    corpo = corpo.newObject(arestas).fillet(p.Raio_Filete)

    macho = G.perfil_filete_macho(p)
    chanfro = G.perfil_chanfro_rosca(p)
    for flip in (False, True):
        corpo = corpo.union(filete_helicoidal(macho, hm, flip))
        corpo = corpo.cut(revolver(chanfro, flip))

    # ---------------- tampas ----------------
    femea = G.perfil_ferramenta_femea(p)
    tampas = []
    for flip in (False, True):
        t = revolver(G.perfil_tampa(p))
        t = t.cut(filete_helicoidal(femea, hf))
        # filete na aresta externa da saia
        zb = p.z_aro - p.Comprimento_Saia
        ed = aresta_circular(t, p.r_tampa, zb)
        t = t.newObject(ed).fillet(p.Raio_Filete)
        # estrias de pega
        n = int(p.Numero_Estrias)
        rcentro = p.r_tampa + p.Raio_Estria - p.Profundidade_Estria
        comp = p.Comprimento_Saia + p.Espessura_Tampa - 1.0
        for i in range(n):
            a = 2 * math.pi * i / n
            cil = (cq.Workplane('XY', origin=(0, 0, zb - 1.0))
                   .center(rcentro * math.cos(a), rcentro * math.sin(a))
                   .circle(p.Raio_Estria).extrude(comp + 1.0))
            t = t.cut(cil)
        if flip:
            t = t.rotate((0, 0, 0), (1, 0, 0), 180)
        tampas.append(t)
    return corpo, tampas[0], tampas[1], info


def espessuras_reservatorio(p, info, n=400):
    """Distância de pontos do perfil interno (funil, reservatório, ombro)
    até o perfil externo, amostrado densamente."""
    segs, _ = G.perfil_corpo(p)

    def amostrar(s, k=200):
        if s[0] == 'line':
            (x0, y0), (x1, y1) = s[1], s[2]
            return [(x0 + (x1 - x0) * i / k, y0 + (y1 - y0) * i / k) for i in range(k + 1)]
        # arco por 3 pontos -> centro
        (ax, ay), (bx, by), (cx, cy) = s[1], s[2], s[3]
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
        uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
        r = math.hypot(ax - ux, ay - uy)
        a0 = math.atan2(ay - uy, ax - ux)
        am = math.atan2(by - uy, bx - ux)
        a1 = math.atan2(cy - uy, cx - ux)
        def norm(x):
            while x - a0 > math.pi: x -= 2 * math.pi
            while x - a0 < -math.pi: x += 2 * math.pi
            return x
        am, a1 = norm(am), norm(a1)
        if not (min(a0, a1) <= am <= max(a0, a1)):
            a1 = a1 + (2 * math.pi if a1 < a0 else -2 * math.pi)
        return [(ux + r * math.cos(a0 + (a1 - a0) * i / k), uy + r * math.sin(a0 + (a1 - a0) * i / k)) for i in range(k + 1)]

    # perfil interno: pontos com z entre P2 e P5 (metade superior), lado interno
    z_lo, z_hi = info['P2'][1], info['P5'][1]
    # classificar: interno = pontos sobre a cadeia interna
    interna = []
    for s in segs[:7]:
        interna += amostrar(s, 400)
    externa = []
    for s in segs:
        if s in segs[:7]:
            continue
        externa += amostrar(s, 400)
    esp = []
    for (r, z) in interna:
        if z_lo + 0.5 <= z <= z_hi - 0.5:
            esp.append(min(math.hypot(r - a, z - b) for (a, b) in externa
                           if abs(b - z) < 6))
    return esp


def detalhar_overhang(mm, crit, log, nome):
    if not crit.any():
        return
    c = mm.triangles_center[crit]
    r = (c[:, 0] ** 2 + c[:, 1] ** 2) ** 0.5
    log('    regiões: r %.1f..%.1f mm, z %.1f..%.1f mm'
        % (r.min(), r.max(), c[:, 2].min(), c[:, 2].max()))


def secao(malhas, p, saida, log):
    """Section Analysis: corte no plano XZ do conjunto montado."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    cores = {'Corpo_Ampulheta': '#5aa9e6', 'Tampa_Superior': '#e07a5f',
             'Tampa_Inferior': '#e07a5f'}
    fig, axs = plt.subplots(1, 3, figsize=(16, 11),
                            gridspec_kw={'width_ratios': [1.1, 1, 1]})
    for ax, (titulo, zlim, xlim) in zip(axs, [
            ('Corte XZ - conjunto montado', None, None),
            ('Detalhe: rosca, vedação e tampa', (p.z_aro - 14, p.z_aro + 4), (12, 26)),
            ('Detalhe: gargalo', (-10, 10), (-8, 8))]):
        for nome, m in malhas.items():
            sec = m.section(plane_origin=[0, 0, 0], plane_normal=[0, 1, 0])
            if sec is None:
                continue
            for ent in sec.entities:
                pts = sec.vertices[ent.points]
                ax.plot(pts[:, 0], pts[:, 2], color=cores[nome], lw=0.9)
        ax.set_aspect('equal')
        ax.set_title(titulo)
        ax.grid(alpha=0.25)
        if zlim:
            ax.set_ylim(*zlim)
        if xlim:
            ax.set_xlim(*xlim)
        ax.set_xlabel('X [mm]')
        ax.set_ylabel('Z [mm]')
    fig.tight_layout()
    fn = os.path.join(saida, 'section_analysis_XZ.png')
    fig.savefig(fn, dpi=130)
    log('Corte salvo em %s' % fn)


def main():
    saida = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, 'saida')
    os.makedirs(saida, exist_ok=True)
    p = G.Parametros()
    corpo, tsup, tinf, info = construir(p)

    rel = []

    def log(s=''):
        print(s)
        rel.append(s)

    log('=== Verificação geométrica (CadQuery/OpenCASCADE) ===')
    pecas = {'Corpo_Ampulheta': corpo, 'Tampa_Superior': tsup, 'Tampa_Inferior': tinf}
    for nome, w in pecas.items():
        s = w.val()
        bb = s.BoundingBox()
        log('%-16s valido=%s  solidos=%d  shells=%d  volume=%.2f cm3  '
            'bbox X[%.2f, %.2f] Z[%.2f, %.2f]'
            % (nome, s.isValid(), len(w.solids().vals()), len(s.Shells()),
               s.Volume() / 1000, bb.xmin, bb.xmax, bb.zmin, bb.zmax))

    # interferência
    for nome, t in (('Tampa_Superior', tsup), ('Tampa_Inferior', tinf)):
        inter = corpo.intersect(t)
        v = sum(x.Volume() for x in inter.solids().vals()) if inter.solids().vals() else 0.0
        log('Interferência corpo x %s: %.6f mm3' % (nome, v))

    # canal aberto: pontos no eixo devem estar fora do corpo
    solido = corpo.val()
    bloqueados = 0
    for i in range(0, 1001):
        z = -p.z_aro + 2 * p.z_aro * i / 1000.0
        if solido.isInside(cq.Vector(0, 0, z), 1e-4):
            bloqueados += 1
    log('Pontos do eixo bloqueados (de 1001): %d' % bloqueados)

    # altura total montada
    zmax = tsup.val().BoundingBox().zmax
    zmin = tinf.val().BoundingBox().zmin
    log('Altura total montada: %.3f mm' % (zmax - zmin))
    log('Diâmetro máximo do corpo: %.3f mm' % (2 * solido.BoundingBox().xmax))

    # folga real das roscas: distância entre a tampa e o corpo abaixo do aro
    # (o aro encosta no disco da tampa de propósito -> excluído)
    for nome, t, sinal in (('Tampa_Superior', tsup, 1), ('Tampa_Inferior', tinf, -1)):
        h = p.Comprimento_Saia + 2.0
        zc = sinal * (p.z_aro - 0.3 - h / 2.0)
        caixa = cq.Workplane('XY').box(80, 80, h).translate((0, 0, zc))
        trecho = corpo.intersect(caixa)
        d = trecho.val().distance(t.val())
        log('Folga mínima medida corpo x %s (zona da rosca): %.3f mm' % (nome, d))

    # espessura da parede dos reservatórios (perfil interno x externo)
    esp = espessuras_reservatorio(p, info)
    log('Espessura reservatório (funil/esfera/ombro): min %.3f  max %.3f mm'
        % (min(esp), max(esp)))
    log('Diâmetro externo da cintura: %.2f mm' % (2 * info['r_cintura_ext']))

    # exportação
    import trimesh
    malhas = {}
    for nome, w in pecas.items():
        cq.exporters.export(w, os.path.join(saida, nome + '.step'))
        stl = os.path.join(saida, nome + '.stl')
        cq.exporters.export(w, stl, tolerance=0.01, angularTolerance=0.1)
        m = trimesh.load(stl)
        malhas[nome] = m
        log('%-16s malha: watertight=%s  winding_consistente=%s  corpos=%d  euler=%d'
            % (nome, m.is_watertight, m.is_winding_consistent,
               len(m.split(only_watertight=False)), m.euler_number))
        try:
            m.export(os.path.join(saida, nome + '.3mf'))
        except Exception as ex:
            log('aviso: 3MF %s: %s' % (nome, ex))

    # overhangs na orientação de impressão recomendada
    import numpy as np
    orient = {
        'Corpo_Ampulheta': None,                  # em pé, como modelado
        'Tampa_Superior': (math.pi, [1, 0, 0]),   # disco na mesa
        'Tampa_Inferior': None,                   # já está com o disco embaixo
    }
    for nome, m in malhas.items():
        mm = m.copy()
        if orient[nome]:
            mm.apply_transform(trimesh.transformations.rotation_matrix(
                orient[nome][0], orient[nome][1]))
        zmin = mm.bounds[0][2]
        n = mm.face_normals
        cz = mm.triangles_center[:, 2]
        fora_mesa = cz > zmin + 0.05
        # ângulo da face em relação à horizontal (0 = teto horizontal)
        ang = np.degrees(np.arcsin(np.clip(np.sqrt(n[:, 0] ** 2 + n[:, 1] ** 2), 0, 1)))
        para_baixo = n[:, 2] < -1e-6
        a = mm.area_faces
        crit = para_baixo & fora_mesa & (ang < 44.0)
        log('%-16s overhang < 45 graus da horizontal (precisa suporte): %.2f mm2; '
            'pior ângulo: %.1f graus'
            % (nome, a[crit].sum(),
               ang[para_baixo & fora_mesa].min() if (para_baixo & fora_mesa).any() else 90))
        detalhar_overhang(mm, crit, log, nome)

    secao(malhas, p, saida, log)

    with open(os.path.join(saida, 'relatorio_cadquery.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rel) + '\n')
    return p, info


if __name__ == '__main__':
    main()
