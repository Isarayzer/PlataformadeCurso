# -*- coding: utf-8 -*-
"""
Geometria da ampulheta (matemática pura, sem dependência do Fusion 360).

Todas as medidas em milímetros e graus. Sistema de coordenadas:
  - eixo Z = eixo da ampulheta (vertical)
  - z = 0 no centro do gargalo
  - perfis descritos no semiplano (r, z) com r >= 0

Este módulo é usado:
  - pelo script do Fusion 360 (Ampulheta.py), que converte para cm;
  - pelo script de verificação offline (verificacao/verificar_cadquery.py).

Cada segmento de perfil é uma tupla:
  ('line', p0, p1)            linha reta
  ('arc',  p0, pm, p1)        arco por três pontos (início, meio, fim)
"""

import math
from dataclasses import dataclass, asdict


# ---------------------------------------------------------------------------
# Parâmetros
# ---------------------------------------------------------------------------

@dataclass
class Parametros:
    # --- Parâmetros principais pedidos -----------------------------------
    Altura_Total: float = 165.0
    Diametro_Maximo: float = 55.0
    Parede: float = 1.20
    Diametro_Gargalo: float = 4.0
    Altura_Gargalo: float = 5.0
    Folga_Rosca: float = 0.30          # radial
    Altura_Rosca: float = 8.0
    Espessura_Tampa: float = 3.0
    Raio_Filete: float = 1.0

    # --- Parâmetros auxiliares (necessários para definir a geometria) ----
    Parede_Gargalo: float = 1.20       # = Parede por padrão (ver relatório)
    Angulo_Funil: float = 60.0         # parede interna x horizontal, lado do gargalo
    Angulo_Ombro: float = 50.0         # parede interna x horizontal, lado da tampa
    Raio_Entrada_Gargalo: float = 3.0  # concordância canal -> funil
    Raio_Colar_Interno: float = 3.0    # concordância ombro -> colar (interno)

    Diametro_Rosca: float = 42.0       # diâmetro maior da rosca macho (corpo)
    Passo_Rosca: float = 3.0
    Profundidade_Rosca: float = 1.0
    Crista_Rosca: float = 0.5          # largura axial da crista do macho
    Raio_Raiz_Rosca: float = 0.3
    Chanfro_Rosca: float = 0.5         # chanfro de entrada no aro do colar
    Parede_Colar: float = 3.5          # parede do colar (raiz da rosca -> furo)

    Diametro_Tampa: float = 48.0
    Diametro_Vedacao_Interno: float = 34.0   # = diâmetro interno do O-ring
    Largura_Vedacao: float = 2.0
    Profundidade_Vedacao: float = 1.1
    Numero_Estrias: int = 30
    Profundidade_Estria: float = 0.5
    Raio_Estria: float = 0.75
    Chanfro_Tampa: float = 0.6         # aresta externa do topo (face que vai na mesa)

    # Constantes de construção (não expostas como parâmetro de usuário)
    _sobreposicao_raiz: float = 0.3    # quanto o perfil do filete penetra no colar
    _mergulho_raiz: float = 0.05       # deslocamento do arco de raiz para dentro do colar

    # ----- grandezas derivadas -------------------------------------------
    @property
    def z_aro(self):
        """Altura (z) da face de encosto (aro do colar) da metade superior."""
        return self.Altura_Total / 2.0 - self.Espessura_Tampa

    @property
    def r_crista(self):
        return self.Diametro_Rosca / 2.0

    @property
    def r_raiz(self):
        return self.r_crista - self.Profundidade_Rosca

    @property
    def r_abertura(self):
        return self.r_raiz - self.Parede_Colar

    @property
    def r_equador_int(self):
        return self.Diametro_Maximo / 2.0 - self.Parede

    @property
    def r_canal(self):
        return self.Diametro_Gargalo / 2.0

    @property
    def Comprimento_Saia(self):
        return self.Altura_Rosca + 1.0

    @property
    def Comprimento_Colar(self):
        return self.Altura_Rosca + 2.5

    @property
    def r_tampa(self):
        return self.Diametro_Tampa / 2.0

    @property
    def meia_base_dente(self):
        # flancos a 45 graus: base = crista + 2*profundidade
        return self.Crista_Rosca / 2.0 + self.Profundidade_Rosca

    def como_dict(self):
        d = asdict(self)
        return {k: v for k, v in d.items() if not k.startswith('_')}


# Unidade de cada parâmetro (para criação no Fusion)
UNIDADES = {
    'Angulo_Funil': 'deg',
    'Angulo_Ombro': 'deg',
    'Numero_Estrias': '',
}

COMENTARIOS = {
    'Altura_Total': 'Altura total montada (corpo + 2 tampas)',
    'Diametro_Maximo': 'Diametro externo maximo dos reservatorios',
    'Parede': 'Espessura da parede translucida dos reservatorios',
    'Diametro_Gargalo': 'Diametro do canal central (controla o tempo)',
    'Altura_Gargalo': 'Comprimento do trecho cilindrico do canal',
    'Folga_Rosca': 'Folga radial entre rosca macho e femea',
    'Altura_Rosca': 'Altura util rosqueada',
    'Espessura_Tampa': 'Espessura do disco da tampa',
    'Raio_Filete': 'Raio dos filetes de acabamento',
    'Parede_Gargalo': 'Parede ao redor do canal (reforco opcional da cintura)',
    'Angulo_Funil': 'Inclinacao interna do funil (min 45 p/ imprimir sem suporte)',
    'Angulo_Ombro': 'Inclinacao interna do ombro junto ao colar (min 45)',
    'Raio_Entrada_Gargalo': 'Concordancia entre canal e funil',
    'Raio_Colar_Interno': 'Concordancia interna entre ombro e colar',
    'Diametro_Rosca': 'Diametro maior da rosca macho do corpo',
    'Passo_Rosca': 'Passo da rosca',
    'Profundidade_Rosca': 'Altura do filete (radial)',
    'Crista_Rosca': 'Largura da crista do filete macho',
    'Raio_Raiz_Rosca': 'Arredondamento de raiz/crista do filete',
    'Chanfro_Rosca': 'Chanfro de entrada da rosca no aro',
    'Parede_Colar': 'Parede reforcada do colar rosqueado',
    'Diametro_Tampa': 'Diametro externo da tampa',
    'Diametro_Vedacao_Interno': 'Diametro interno do canal do O-ring (= DI do O-ring)',
    'Largura_Vedacao': 'Largura do canal do O-ring',
    'Profundidade_Vedacao': 'Profundidade do canal do O-ring',
    'Numero_Estrias': 'Numero de estrias de pega na tampa',
    'Profundidade_Estria': 'Profundidade das estrias',
    'Raio_Estria': 'Raio das estrias',
    'Chanfro_Tampa': 'Chanfro da aresta do topo da tampa (lado da mesa)',
}


# ---------------------------------------------------------------------------
# Utilidades 2D
# ---------------------------------------------------------------------------

def _add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _mul(a, s):
    return (a[0] * s, a[1] * s)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def _norm(a):
    return math.hypot(a[0], a[1])


def _unit(a):
    n = _norm(a)
    return (a[0] / n, a[1] / n)


def _arc_mid(c, p0, p1, raio, sentido_hint=None):
    """Ponto médio do arco menor de centro c entre p0 e p1."""
    a0 = math.atan2(p0[1] - c[1], p0[0] - c[0])
    a1 = math.atan2(p1[1] - c[1], p1[0] - c[0])
    da = a1 - a0
    while da > math.pi:
        da -= 2 * math.pi
    while da < -math.pi:
        da += 2 * math.pi
    am = a0 + da / 2.0
    return (c[0] + raio * math.cos(am), c[1] + raio * math.sin(am))


def arco(c, raio, p0, p1):
    return ('arc', p0, _arc_mid(c, p0, p1, raio), p1)


def linha(p0, p1):
    return ('line', p0, p1)


def espelhar_z(segs):
    """Espelha (r, z) -> (r, -z) e inverte a ordem/sentido da cadeia."""
    out = []
    for s in reversed(segs):
        if s[0] == 'line':
            out.append(('line', (s[2][0], -s[2][1]), (s[1][0], -s[1][1])))
        else:
            out.append(('arc', (s[3][0], -s[3][1]), (s[2][0], -s[2][1]),
                        (s[1][0], -s[1][1])))
    return out


def poligono_com_raios(vertices):
    """
    vertices: lista de ((x, y), raio) formando um polígono fechado.
    Retorna segmentos (linhas + arcos tangentes) com os cantos arredondados.
    """
    n = len(vertices)
    cantos = []
    Ls = []
    for i in range(n):
        v, rr = vertices[i]
        a = vertices[i - 1][0]
        b = vertices[(i + 1) % n][0]
        if rr <= 0:
            cantos.append((v, v, None))
            Ls.append(0.0)
            continue
        d1 = _unit(_sub(a, v))
        d2 = _unit(_sub(b, v))
        cosang = max(-1.0, min(1.0, _dot(d1, d2)))
        meio = math.acos(cosang) / 2.0
        L = rr / math.tan(meio)
        t1 = _add(v, _mul(d1, L))
        t2 = _add(v, _mul(d2, L))
        bis = _unit(_add(d1, d2))
        c = _add(v, _mul(bis, rr / math.sin(meio)))
        cantos.append((t1, t2, ('arc', t1, _arc_mid(c, t1, t2, rr), t2)))
        Ls.append(L)
    for i in range(n):
        j = (i + 1) % n
        lado = _norm(_sub(vertices[j][0], vertices[i][0]))
        if Ls[i] + Ls[j] > lado + 1e-9:
            raise ValueError('Raios de canto grandes demais no lado %r -> %r'
                             % (vertices[i][0], vertices[j][0]))
    segs = []
    for i in range(n):
        t1, t2, arc = cantos[i]
        if arc is not None:
            segs.append(arc)
        prox_t1 = cantos[(i + 1) % n][0]
        if _norm(_sub(prox_t1, t2)) > 1e-9:
            segs.append(('line', t2, prox_t1))
    return segs


# ---------------------------------------------------------------------------
# Perfil do corpo
# ---------------------------------------------------------------------------

class ErroGeometria(Exception):
    pass


def resolver_corpo(p: Parametros):
    """
    Resolve os pontos notáveis da metade superior do perfil interno.

    Cadeia interna (de baixo para cima):
      canal vertical r = r_canal  (z de 0 a Altura_Gargalo/2)
      arco de entrada (raio Raio_Entrada_Gargalo)  -> tangente a Angulo_Funil
      linha do funil  (Angulo_Funil em relação à horizontal)
      arco do reservatório (tangente ao funil, vertical no equador,
                            tangente ao ombro)
      linha do ombro (Angulo_Ombro)
      arco do colar (raio Raio_Colar_Interno)
      cilindro interno do colar r = r_abertura até o aro

    O perfil externo é o offset exato de Parede (linhas paralelas e arcos
    concêntricos), portanto a espessura nos reservatórios é constante.
    """
    a = math.radians(p.Angulo_Funil)
    b = math.radians(p.Angulo_Ombro)
    t = p.Parede
    rg = p.r_canal
    z1 = p.Altura_Gargalo / 2.0
    Re = p.Raio_Entrada_Gargalo
    Rc = p.Raio_Colar_Interno
    req = p.r_equador_int
    rab = p.r_abertura
    rraiz = p.r_raiz
    zaro = p.z_aro
    zoc = zaro - p.Comprimento_Colar   # onde o ombro externo encontra o colar

    if not (45.0 <= p.Angulo_Funil < 90.0 and 45.0 <= p.Angulo_Ombro < 90.0):
        raise ErroGeometria('Angulo_Funil e Angulo_Ombro devem estar entre 45 e 90 graus '
                            '(abaixo de 45 a parede interna exige suporte).')
    if Re <= t + 0.3:
        raise ErroGeometria('Raio_Entrada_Gargalo deve ser maior que Parede + 0.3 mm.')

    # Arco de entrada
    Ce = (rg + Re, z1)
    dlt = math.pi / 2 - a
    P2 = (Ce[0] - Re * math.cos(dlt), Ce[1] + Re * math.sin(dlt))
    u1 = (math.cos(a), math.sin(a))
    n1 = (-math.sin(a), math.cos(a))        # normal para dentro da cavidade

    # Ombro: linha externa passa por O = (r_raiz, zoc), direção u2
    u2 = (-math.cos(b), math.sin(b))
    n2 = (-math.sin(b), -math.cos(b))       # normal para dentro da cavidade
    O = (rraiz, zoc)
    Q = _add(O, _mul(n2, t))                # ponto da linha interna do ombro

    # Centro do arco do reservatório C = (req - R, cz):
    #  (C - P2).n1 = R   e   (C - Q).n2 = R
    # Linear em (R, cz).
    # eq1: (req - R - P2r)(-sa) + (cz - P2z) ca = R
    #   -> R(sa - 1) + cz*ca = -(req - P2r)(-sa) + P2z*ca
    sa, ca = math.sin(a), math.cos(a)
    sb, cb = math.sin(b), math.cos(b)
    A11, A12 = (sa - 1.0), ca
    B1 = (req - P2[0]) * sa + P2[1] * ca
    # eq2: (req - R - Qr)(-sb) + (cz - Qz)(-cb) = R
    #   -> R(sb - 1) - cz*cb = (req - Qr)*sb - Qz*cb
    A21, A22 = (sb - 1.0), -cb
    B2 = (req - Q[0]) * sb - Q[1] * cb
    det = A11 * A22 - A12 * A21
    if abs(det) < 1e-12:
        raise ErroGeometria('Sistema do reservatório degenerado.')
    Rb = (B1 * A22 - A12 * B2) / det
    cz = (A11 * B2 - B1 * A21) / det
    Cb = (req - Rb, cz)
    if Rb <= 2.0 * t:
        raise ErroGeometria('Raio do reservatório resultou pequeno demais (%.2f mm).' % Rb)

    P3 = _add(Cb, _mul((sa, -ca), Rb))      # tangência funil / reservatório
    Peq = (req, cz)
    P4 = _add(Cb, _mul((sb, cb), Rb))       # tangência reservatório / ombro

    # Arco do colar: centro (rab + Rc, zc), tangente ao ombro interno
    # (Cc - Q).n2 = -Rc
    zc = Q[1] + (Rc - (rab + Rc - Q[0]) * sb) / cb
    Cc = (rab + Rc, zc)
    P5 = _add(Cc, _mul(n2, Rc))             # tangência ombro / arco do colar
    P6 = (rab, zc)

    # Verificações de consistência da cadeia
    s_funil = _dot(_sub(P3, P2), u1)
    s_ombro = _dot(_sub(P5, P4), u2)
    erros = []
    if s_funil <= 0.5:
        erros.append('funil sem comprimento (aumente a altura ou o Angulo_Funil)')
    if s_ombro <= 0.2:
        erros.append('ombro sem comprimento (reduza Raio_Colar_Interno ou Diametro_Rosca)')
    if not (P3[1] < cz < P4[1]):
        erros.append('equador fora do arco do reservatório')
    if not (P6[1] < zaro - 1.0):
        erros.append('colar interno sem altura')
    if _dot(_sub(O, Q), n2) > 0:
        erros.append('orientação do ombro inválida')
    if rab <= rg + 2:
        erros.append('abertura muito pequena')
    if erros:
        raise ErroGeometria('; '.join(erros))

    return dict(Ce=Ce, Re=Re, P2=P2, u1=u1, n1=n1, P3=P3, Cb=Cb, Rb=Rb, Peq=Peq,
                P4=P4, u2=u2, n2=n2, O=O, Q=Q, P5=P5, Cc=Cc, Rc=Rc, P6=P6,
                z1=z1, zoc=zoc, zaro=zaro, s_funil=s_funil, s_ombro=s_ombro)


def perfil_corpo(p: Parametros):
    """
    Perfil fechado (semiplano r >= 0) do corpo inteiro, pronto para revolução.
    Retorna (segmentos, info) onde info tem pontos úteis para seleção de arestas.
    """
    g = resolver_corpo(p)
    t = p.Parede
    rg = p.r_canal
    z1 = g['z1']
    zaro = g['zaro']
    rab = p.r_abertura
    rraiz = p.r_raiz

    # ---------- cadeia interna, metade superior, do aro até (rg, z1) -------
    interna_sup = [
        linha((rab, zaro), g['P6']),
        arco(g['Cc'], g['Rc'], g['P6'], g['P5']),
        linha(g['P5'], g['P4']),
        arco(g['Cb'], g['Rb'], g['P4'], g['Peq']),
        arco(g['Cb'], g['Rb'], g['Peq'], g['P3']),
        linha(g['P3'], g['P2']),
        arco(g['Ce'], g['Re'], g['P2'], (rg, z1)),
    ]

    # ---------- cadeia externa, metade superior, de z = 0 até o aro --------
    sa = math.sin(math.radians(p.Angulo_Funil))
    ca = math.cos(math.radians(p.Angulo_Funil))
    off1 = (sa, -ca)                     # normal para fora no funil
    P2o = _add(g['P2'], _mul(off1, t))
    P3o = _add(g['P3'], _mul(off1, t))
    Reo = g['Re'] - t
    Rbo = g['Rb'] + t
    sb = math.sin(math.radians(p.Angulo_Ombro))
    cb = math.cos(math.radians(p.Angulo_Ombro))
    P4o = _add(g['Cb'], _mul((sb, cb), Rbo))
    Peqo = (g['Peq'][0] + t, g['Peq'][1])
    O = g['O']

    rh = rg + max(p.Parede_Gargalo, t)
    externa_sup = []
    canto_cubo = None
    if p.Parede_Gargalo <= t + 1e-6:
        externa_sup.append(('cubo', (rg + t, z1)))   # marcador; vira linha depois
        externa_sup.append(arco(g['Ce'], Reo, (rg + t, z1), P2o))
        externa_sup.append(linha(P2o, P3o))
    else:
        # cubo de reforço: cilindro r = rh até cruzar o arco/linha do funil
        if rh < P2o[0] - 1e-6:
            dx = rh - g['Ce'][0]
            zh = g['Ce'][1] + math.sqrt(max(Reo ** 2 - dx ** 2, 0.0))
            externa_sup.append(('cubo', (rh, zh)))
            externa_sup.append(arco(g['Ce'], Reo, (rh, zh), P2o))
            externa_sup.append(linha(P2o, P3o))
        else:
            zh = P2o[1] + (rh - P2o[0]) * math.tan(math.radians(p.Angulo_Funil))
            if zh >= P3o[1] - 1.0:
                raise ErroGeometria('Parede_Gargalo grande demais para o funil.')
            externa_sup.append(('cubo', (rh, zh)))
            externa_sup.append(linha((rh, zh), P3o))
        canto_cubo = (rh, zh)
    externa_sup += [
        arco(g['Cb'], Rbo, P3o, Peqo),
        arco(g['Cb'], Rbo, Peqo, P4o),
        linha(P4o, O),
        linha(O, (rraiz, zaro)),
    ]
    if _dot(_sub(O, P4o), g['u2']) <= 0.2:
        raise ErroGeometria('O ombro externo não alcança o colar (Diametro_Rosca grande '
                            'demais ou Comprimento_Colar curto).')

    r_cubo, z_cubo = externa_sup[0][1]
    externa_sup = externa_sup[1:]

    # ---------- montagem do laço fechado ----------------------------------
    segs = []
    segs += interna_sup                                   # aro sup -> (rg, z1)
    segs.append(linha((rg, z1), (rg, -z1)))               # canal inteiro
    segs += espelhar_z(interna_sup)                       # (rg,-z1) -> aro inf
    segs.append(linha((rab, -zaro), (rraiz, -zaro)))      # aro inferior
    ext_inf = espelhar_z(externa_sup)                     # aro inf -> cubo inf
    segs += ext_inf
    segs.append(linha((r_cubo, -z_cubo), (r_cubo, z_cubo)))  # cintura externa
    segs += externa_sup                                   # cubo sup -> aro sup
    segs.append(linha((rraiz, zaro), (rab, zaro)))        # aro superior

    info = dict(g)
    info.update(dict(P2o=P2o, P3o=P3o, P4o=P4o, Peqo=Peqo, Rbo=Rbo, Reo=Reo,
                     canto_cubo=canto_cubo, r_cintura_ext=r_cubo,
                     canto_colar=(rraiz, g['zoc'])))
    _checar_fechado(segs)
    return segs, info


def _checar_fechado(segs, tol=1e-6):
    for i, s in enumerate(segs):
        fim = s[-1]
        ini = segs[(i + 1) % len(segs)][1]
        if _norm(_sub(fim, ini)) > tol:
            raise ErroGeometria('Perfil não fechado entre segmentos %d e %d: %r != %r'
                                % (i, i + 1, fim, ini))


# ---------------------------------------------------------------------------
# Rosca
# ---------------------------------------------------------------------------

def perfil_filete_macho(p: Parametros):
    """
    Perfil do filete macho em coordenadas locais (r, v), v = axial relativo
    ao ponto da hélice. Trapezoidal com flancos a 45 graus (90 graus incluso),
    cristas arredondadas e raízes concordadas que penetram levemente no colar.
    """
    rr, rc = p.r_raiz, p.r_crista
    c2 = p.Crista_Rosca / 2.0
    bb = p.meia_base_dente
    rho = p.Raio_Raiz_Rosca
    d = p._mergulho_raiz
    e = p._sobreposicao_raiz
    tang = rho * math.tan(math.radians(22.5))
    vc = -d - bb - tang                  # fim do arco de raiz (inferior)
    vs = vc - 0.03
    if abs(vs) >= p.Passo_Rosca / 2.0 - 0.02:
        raise ErroGeometria('Filete largo demais para o passo (aumente Passo_Rosca ou '
                            'reduza Crista_Rosca/Profundidade_Rosca/Raio_Raiz_Rosca).')
    if 2 * tang >= p.Crista_Rosca:
        raise ErroGeometria('Raio_Raiz_Rosca grande demais para a crista.')
    verts = [
        ((rr - e, vs), 0.0),
        ((rr - d, vs), 0.0),
        ((rr - d, -d - bb), rho),        # raiz inferior (côncavo)
        ((rc, -c2), rho),                # crista inferior (convexo)
        ((rc, c2), rho),                 # crista superior
        ((rr - d, d + bb), rho),         # raiz superior
        ((rr - d, -vs), 0.0),
        ((rr - e, -vs), 0.0),
    ]
    return poligono_com_raios(verts)


def perfil_ferramenta_femea(p: Parametros):
    """
    Ferramenta de corte da rosca fêmea: filete macho deslocado RADIALMENTE
    de Folga_Rosca (folga radial exata pedida). Fundo do sulco arredondado.
    """
    f = p.Folga_Rosca
    rr, rc = p.r_raiz + f, p.r_crista + f
    c2 = p.Crista_Rosca / 2.0
    bb = p.meia_base_dente
    rho = p.Raio_Raiz_Rosca
    k = 0.1      # o flanco continua 0.1 mm para dentro do furo antes de virar
    verts = [
        ((rr - 0.5, -(bb + k)), 0.0),
        ((rr - k, -(bb + k)), 0.0),
        ((rc, -c2), rho),
        ((rc, c2), rho),
        ((rr - k, bb + k), 0.0),
        ((rr - 0.5, bb + k), 0.0),
    ]
    if 2 * (bb + k) >= p.Passo_Rosca - 0.1:
        raise ErroGeometria('Ferramenta da rosca fêmea larga demais para o passo.')
    return poligono_com_raios(verts)


def helices(p: Parametros):
    """
    Hélices (metade superior, rosca direita). Ambas com o mesmo "zero" de fase,
    portanto macho e fêmea ficam sincronizados com a tampa fechada.
    Retorna dicts com r (raio do caminho), z0 (z inicial, ângulo 0) e voltas.
    """
    P = p.Passo_Rosca
    zaro = p.z_aro
    bb = p.meia_base_dente
    ext_dente = bb + p._mergulho_raiz + p.Raio_Raiz_Rosca * math.tan(math.radians(22.5))
    # macho: a borda inferior do filete termina em z_aro - Altura_Rosca
    z0m = zaro - p.Altura_Rosca + ext_dente
    z1m = zaro + 1.5                         # passa do aro e é aparado pelo chanfro
    voltas_m = (z1m - z0m) / P
    # fêmea: começa abaixo da saia (sai da peça) com a mesma fase
    z_min_f = zaro - p.Comprimento_Saia - 2.0
    k = math.ceil((z0m - z_min_f) / P)
    z0f = z0m - k * P
    z1f = zaro - (bb + 0.1) - 0.15           # não toca o disco da tampa
    voltas_f = (z1f - z0f) / P
    rm = p.r_raiz + p.Profundidade_Rosca / 2.0
    rf = rm + p.Folga_Rosca
    return (dict(r=rm, z0=z0m, voltas=voltas_m, passo=P),
            dict(r=rf, z0=z0f, voltas=voltas_f, passo=P))


def pontos_helice(r, z0, voltas, passo, pts_por_volta=36):
    n = max(8, int(math.ceil(voltas * pts_por_volta)))
    out = []
    for i in range(n + 1):
        th = 2 * math.pi * voltas * i / n
        out.append((r * math.cos(th), r * math.sin(th), z0 + passo * th / (2 * math.pi)))
    return out


def perfil_chanfro_rosca(p: Parametros):
    """Região (r, z) removida por revolução: apara o filete acima do aro e
    cria o chanfro de entrada a 45 graus. Metade superior."""
    zaro = p.z_aro
    r0 = p.r_raiz - p.Chanfro_Rosca
    r1 = p.r_crista + 0.6
    return [
        linha((r0, zaro), (r1, zaro - (r1 - r0))),
        linha((r1, zaro - (r1 - r0)), (r1, zaro + 6.0)),
        linha((r1, zaro + 6.0), (r0, zaro + 6.0)),
        linha((r0, zaro + 6.0), (r0, zaro)),
    ]


# ---------------------------------------------------------------------------
# Tampa
# ---------------------------------------------------------------------------

def perfil_tampa(p: Parametros):
    """Perfil (r, z) da tampa SUPERIOR na posição montada (fechada)."""
    zaro = p.z_aro
    tc = p.Espessura_Tampa
    R = p.r_tampa
    f = p.Folga_Rosca
    rfuro = p.r_raiz + f           # crista da fêmea
    # alívio no topo da saia: 0.2 mm além do fundo da fêmea (evita faces
    # coincidentes com a crista da ferramenta da rosca no booleano)
    ralivio = p.r_crista + f + 0.2
    L = p.Comprimento_Saia
    ch = p.Chanfro_Tampa
    ch_in = 0.8                    # chanfro de entrada da saia
    ri = p.Diametro_Vedacao_Interno / 2.0
    ro = ri + p.Largura_Vedacao
    hv = p.Profundidade_Vedacao

    if R - ralivio < 2.0:
        raise ErroGeometria('Parede da tampa < 2 mm (aumente Diametro_Tampa).')
    if hv > tc - 1.2:
        raise ErroGeometria('Canal do O-ring profundo demais para Espessura_Tampa.')
    if not (p.r_abertura < ri and ro < p.r_raiz - p.Chanfro_Rosca):
        raise ErroGeometria('Canal de vedação não cai inteiramente sobre o aro do colar.')

    pts = [
        (0.0, zaro + tc),
        (R - ch, zaro + tc),
        (R, zaro + tc - ch),
        (R, zaro - L),
        (rfuro + ch_in, zaro - L),
        (rfuro, zaro - L + ch_in),
        (rfuro, zaro - 2.0 - (ralivio - rfuro)),
        (ralivio, zaro - 2.0),       # cone de 45 graus (imprimível)
        (ralivio, zaro),
        (ro, zaro),
        (ro, zaro + hv),
        (ri, zaro + hv),
        (ri, zaro),
        (0.0, zaro),
    ]
    segs = []
    for i in range(len(pts)):
        segs.append(linha(pts[i], pts[(i + 1) % len(pts)]))
    return segs


# ---------------------------------------------------------------------------
# Relatórios analíticos
# ---------------------------------------------------------------------------

def volume_cavidade_meia(p: Parametros, n=4000):
    """Volume (ml) de UM reservatório (z de 0 ao aro) por integração numérica."""
    segs, info = perfil_corpo(p)
    # amostra r_interno(z) para z em [0, z_aro]
    g = info
    zs = [i * p.z_aro / n for i in range(n + 1)]

    def r_int(z):
        rg = p.r_canal
        if z <= g['z1']:
            return rg
        # arco de entrada
        Ce, Re = g['Ce'], g['Re']
        if z <= g['P2'][1]:
            return Ce[0] - math.sqrt(max(Re ** 2 - (z - Ce[1]) ** 2, 0))
        if z <= g['P3'][1]:
            P2, u1 = g['P2'], g['u1']
            return P2[0] + (z - P2[1]) / u1[1] * u1[0]
        if z <= g['P4'][1]:
            Cb, Rb = g['Cb'], g['Rb']
            return Cb[0] + math.sqrt(max(Rb ** 2 - (z - Cb[1]) ** 2, 0))
        if z <= g['P5'][1]:
            P4, u2 = g['P4'], g['u2']
            return P4[0] + (z - P4[1]) / u2[1] * u2[0]
        if z <= g['P6'][1]:
            Cc, Rc = g['Cc'], g['Rc']
            return Cc[0] - math.sqrt(max(Rc ** 2 - (z - Cc[1]) ** 2, 0))
        return p.r_abertura

    vol = 0.0
    for i in range(n):
        zm = 0.5 * (zs[i] + zs[i + 1])
        vol += math.pi * r_int(zm) ** 2 * (zs[i + 1] - zs[i])
    return vol / 1000.0


def resumo(p: Parametros):
    segs, info = perfil_corpo(p)
    hm, hf = helices(p)
    return dict(
        altura_corpo=2 * p.z_aro,
        altura_total=p.Altura_Total,
        diametro_max=2 * (info['Peq'][0] + p.Parede),
        z_equador=info['Peq'][1],
        raio_reservatorio_int=info['Rb'],
        diametro_cintura_externa=2 * info['r_cintura_ext'],
        diametro_abertura=2 * p.r_abertura,
        rosca_macho_maior=2 * p.r_crista,
        rosca_macho_menor=2 * p.r_raiz,
        rosca_femea_maior=2 * (p.r_crista + p.Folga_Rosca),
        rosca_femea_menor=2 * (p.r_raiz + p.Folga_Rosca),
        folga_normal_flanco=p.Folga_Rosca * math.sin(math.radians(45)),
        folga_axial_total=2 * p.Folga_Rosca,
        engajamento_radial=p.Profundidade_Rosca - p.Folga_Rosca,
        voltas_macho=hm['voltas'],
        volume_reservatorio_ml=volume_cavidade_meia(p),
    )


if __name__ == '__main__':
    p = Parametros()
    for k, v in resumo(p).items():
        print('%-28s %10.3f' % (k, v))
