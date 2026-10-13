# Ampulheta paramétrica — Fusion 360 / Bambu Lab P2S / PETG translúcido

Script Python do Fusion 360 que cria uma ampulheta funcional (165 × 55 mm) com
corpo translúcido de parede 1,20 mm, duas extremidades rosqueáveis, tampas
removíveis com canal para O-ring e gargalo central paramétrico.

```
Ampulheta/
├── Ampulheta.py            script do Fusion 360 (cria parâmetros, componentes, validação, export)
├── Ampulheta.manifest
├── ampulheta_geom.py       geometria (matemática pura, mm) usada pelo script
└── verificacao/
    ├── verificar_cadquery.py   reconstrói a MESMA geometria em OpenCASCADE e valida
    └── saida/                  resultado da verificação (relatório, corte, STL/3MF/STEP de referência)
```

## Como usar no Fusion 360

1. Copie a pasta `Ampulheta/` inteira (o `.py`, o `.manifest` e o `ampulheta_geom.py`).
2. Fusion 360 → **Utilities → Add-Ins → Scripts and Add-Ins** → **+** (ícone verde) → selecione a pasta.
3. Abra um design novo e clique em **Run**.
4. O script cria os parâmetros, os três componentes, valida e oferece exportar STL/3MF.

### Alterar dimensões

1. **Modify → Change Parameters** → edite qualquer parâmetro (ex.: `Diametro_Gargalo`).
2. Rode o script de novo → responda **Sim** em “Regenerar”.
   O script **lê** os valores atuais (não volta aos padrões) e reconstrói os
   três componentes. Combinações inválidas são recusadas com uma mensagem
   explicando o motivo, e nada é alterado.

**Limitação da API, sem rodeios:** a API do Fusion não consegue criar um
*Coil* (hélice paramétrica) e não existe hélice dirigida por parâmetro em
esboço. Por isso a geometria é calculada a partir dos parâmetros e
regenerada pelo script. Os filetes usam a expressão `Raio_Filete` e mudam
ao vivo, sem precisar rodar o script de novo. Todo o resto muda com uma nova
execução, que leva poucos segundos. Os parâmetros ficam sempre no
documento.

## Parâmetros

Os parâmetros pedidos (todos editáveis):

| Parâmetro | Valor |
|---|---|
| `Altura_Total` | 165 mm |
| `Diametro_Maximo` | 55 mm |
| `Parede` | 1.20 mm |
| `Diametro_Gargalo` | 4.0 mm |
| `Altura_Gargalo` | 5.0 mm |
| `Folga_Rosca` | 0.30 mm (radial) |
| `Altura_Rosca` | 8 mm |
| `Espessura_Tampa` | 3 mm |
| `Raio_Filete` | 1 mm |

Os parâmetros auxiliares abaixo são necessários para definir a geometria sem
números “escondidos” no código:

| Parâmetro | Valor | Função |
|---|---|---|
| `Parede_Gargalo` | `= Parede` | parede ao redor do canal (ver **Problema 1**) |
| `Angulo_Funil` | 60° | inclinação interna do funil (≥ 45° obrigatório) |
| `Angulo_Ombro` | 50° | inclinação interna do ombro junto ao colar (≥ 45°) |
| `Raio_Entrada_Gargalo` | 3 mm | concordância canal → funil |
| `Raio_Colar_Interno` | 3 mm | concordância ombro → colar |
| `Diametro_Rosca` | 42 mm | diâmetro maior da rosca macho |
| `Passo_Rosca` | 3 mm | |
| `Profundidade_Rosca` | 1.0 mm | |
| `Crista_Rosca` | 0.5 mm | |
| `Raio_Raiz_Rosca` | 0.3 mm | arredondamento de raiz e crista |
| `Chanfro_Rosca` | 0.5 mm | chanfro de entrada no aro |
| `Parede_Colar` | 3.5 mm | reforço local do colar rosqueado |
| `Diametro_Tampa` | 48 mm | |
| `Diametro_Vedacao_Interno` | 34 mm | = DI do O-ring |
| `Largura_Vedacao` / `Profundidade_Vedacao` | 2.0 / 1.1 mm | canal do O-ring 1,5 mm |
| `Numero_Estrias` / `Profundidade_Estria` / `Raio_Estria` | 30 / 0.5 / 0.75 mm | pega |
| `Chanfro_Tampa` | 0.6 mm | aresta do topo da tampa |

## Construção

* **Corpo:** um único perfil 2D fechado no plano XZ e um *Revolve* de 360°.
  O perfil interno é uma cadeia contínua e tangente: canal cilíndrico →
  arco de entrada R3 → funil reto a 60° → arco do reservatório (vertical no
  equador, Ø55) → ombro a 50° → arco R3 → colar. O perfil externo é o
  **offset exato** de `Parede` (linhas paralelas e arcos concêntricos), então
  a espessura vale exatamente 1,200 mm do gargalo até o ombro. Não é usado
  *Shell*, e não há duas esferas unidas.
* **Colar rosqueado:** reforço local (parede de 3,5 mm + filete) só nos
  últimos cerca de 13 mm de cada extremidade, com concordância `Raio_Filete`
  para o corpo transparente.
* **Roscas:** filete macho varrido em hélice (*Sweep*) e unido ao colar. A
  rosca fêmea é cortada na tampa por uma ferramenta igual ao filete macho,
  deslocada radialmente de `Folga_Rosca`. As duas extremidades são rosca
  **direita**: a parte de baixo é uma rotação de 180° em X, e não um
  espelhamento. Por isso as duas tampas são idênticas e intercambiáveis.
* **Vedação:** o aro plano do colar encosta no disco da tampa. O canal do
  O-ring fica no disco da tampa, inteiramente sobre o aro.
* **Validação no Fusion:** sólido/shells/volume de cada corpo, 401 pontos ao
  longo do eixo (o canal precisa estar livre), *Interference* entre as peças
  montadas, checagem de torção das hélices e o esboço `Secao_XZ_Validacao`
  (interseção dos corpos com o plano XZ).

---

## Relatório final

Os valores abaixo foram **medidos** na reconstrução OpenCASCADE
(`verificacao/saida/relatorio_cadquery.txt`), não apenas calculados.

### 1. Dimensões finais
| | |
|---|---|
| Altura total montada | **165,00 mm** |
| Altura do corpo (aro a aro) | 159,00 mm |
| Diâmetro máximo (equador) | **55,00 mm**, a z = ±51,4 mm do centro |
| Diâmetro das tampas | 48,0 mm |
| Cintura externa | 6,40 mm (ver Problema 1) |
| Abertura de abastecimento | Ø33,0 mm (cada extremidade) |
| Volume de cada reservatório | 86 ml (encha no máximo cerca de 50–60%) |
| Volume de material | corpo 29,1 cm³; cada tampa 8,8 cm³ |

### 2. Parâmetros criados
Os 9 pedidos e os 20 auxiliares listados acima.

### 3. Diâmetro real do gargalo
**Ø4,00 mm** cilíndrico ao longo de 5,0 mm, centrado no eixo, com entrada
concordada R3 → funil 60° dos dois lados. O canal foi verificado aberto: 0
de 1001 pontos do eixo bloqueados.

### 4. Espessura mínima da parede
* Reservatórios (funil + arco + equador): **1,200 mm** (mín = máx, medido).
* Transição ombro → colar: 1,2 → 3,5 mm, só nos 4 mm finais.
* Colar rosqueado: 3,5 mm até a raiz da rosca.
* Saia da tampa: 2,7 mm até o fundo da rosca fêmea (2,5 mm no alívio do topo; menos 0,5 mm nas estrias).
* Disco da tampa: 3,0 mm; 1,9 mm sob o canal do O-ring.

### 5. Tipo e passo da rosca
Trapezoidal com **flancos a 45° (90° incluso)**, rosca direita, **passo
3,0 mm**, profundidade 1,0 mm, crista 0,5 mm, raiz e crista arredondadas
R0,3. Macho Ø42,0 / Ø40,0. Fêmea Ø42,6 / Ø40,6. São cerca de 2,7 voltas em
8 mm úteis, com chanfro de entrada de 45° no aro.

> **Por que não Tr (30°)?** Os flancos da trapezoidal ISO ficam a 15° da
> horizontal quando a peça é impressa em pé. É um overhang de 75° em cada
> filete, que sai caído no PETG. Com 45°, a rosca imprime sem suporte e
> continua sendo um perfil trapezoidal robusto. Se preferir 30°, é só
> trocar o ângulo em `perfil_filete_macho`, mas não recomendo.

### 6. Folga aplicada à rosca
`Folga_Rosca` = **0,30 mm radial**, exatamente como pedido (a ferramenta é
deslocada radialmente). Isso resulta em:
* 0,212 mm normal ao flanco (medido: folga mínima corpo × tampa = 0,212 mm);
* 0,60 mm de folga axial total;
* engajamento radial de 0,70 mm;
* interferência de 0,000 mm³.

### 7. Orientação recomendada para impressão
| Peça | Orientação | Suporte |
|---|---|---|
| Corpo | **em pé** (eixo vertical, aro inferior na mesa) | nenhum. As superfícies internas e externas ficam todas ≥ 45° da horizontal |
| Tampa superior | **disco na mesa**, saia para cima | nenhum |
| Tampa inferior | **disco na mesa**, saia para cima (a peça é idêntica) | nenhum |

Configuração sugerida no Bambu Studio para o corpo: **3 paredes** (largura
de linha 0,40–0,42), camada de 0,12–0,16 mm (melhora as roscas e o escoamento
interno), suporte desligado, *Brim* de 5 mm, *Elephant foot compensation*
de 0,15 mm, costura (*seam*) alinhada atrás. Seque o PETG antes de imprimir.

### 8. Pontos de dificuldade na P2S

**Problema 1. Cintura de 6,4 mm (não alterado, aguardando sua decisão).**
Com `Parede` = 1,2 mm aplicada também ao gargalo, a cintura externa fica
com Ø6,4 mm. Esse trecho:
* sustenta os 80 mm do reservatório superior durante a impressão (pode
  vibrar com o arraste do bico);
* é exatamente o plano mais fraco da peça (adesão entre camadas sob
  flexão), então uma queda da mesa pode quebrar ali.

*Menor alteração proposta:* `Parede_Gargalo = 3 mm`. A cintura passa a
Ø10 mm, com concordância `Raio_Filete` para o funil. Os reservatórios
continuam com 1,2 mm e o canal continua Ø4. O parâmetro já existe; hoje ele
vale `= Parede` para respeitar o que você especificou.

**Problema 2. Forma do reservatório (decisão de projeto, explicada aqui).**
Um bulbo esférico teria superfícies quase horizontais perto do gargalo. Isso
**prende areia** (o ângulo de repouso fica entre 30° e 35°) e **exige
suporte interno** impossível de remover. Por isso o lado do gargalo é um
funil reto a 60° e só depois o bulbo se arredonda. O resultado é um
reservatório em “gota”, com o maior diâmetro mais perto das tampas. As
proporções principais (165 × 55) foram mantidas.

**Problema 3. Escoamento e tempo.** Com Ø4 mm, uma estimativa por Beverloo
(apenas orientativa) para areia de 0,15–0,3 mm dá cerca de 2–2,4 g/s, ou
seja, de 30 a 50 s para 70–100 g de areia. Para chegar a minutos, o gargalo
precisa ficar em torno de Ø2–2,5 mm:

| Ø gargalo | areia 0,15 mm | areia 0,30 mm |
|---|---|---|
| 2,0 mm | ~0,36 g/s | ~0,26 g/s |
| 2,5 mm | ~0,67 g/s | ~0,52 g/s |
| 3,0 mm | ~1,1 g/s | ~0,9 g/s |
| 4,0 mm | ~2,4 g/s | ~2,0 g/s |

Regras práticas: grão ≤ 1/5 do gargalo; areia seca e peneirada.

**Outros pontos de atenção**
* **Camadas no funil interno:** em 60° os degraus são pequenos, mas com
  camada de 0,28 mm a areia escorre pior. Use 0,12–0,16 mm.
* **Aro inferior na mesa:** é uma coroa de 3 mm de largura. Use *Brim*,
  porque o PETG em peça alta e estreita pode descolar.
* **Translucidez:** PETG impresso fica translúcido, não transparente.
  Paredes de 3 voltas, sem infill na parede, velocidade de parede externa
  reduzida e temperatura cerca de 5 °C acima do normal aumentam a clareza.
* **Fim do filete macho:** a ponta inferior da hélice termina em face plana.
  Isso não prejudica, mas é a única aresta não concordada da rosca.
* **Overhangs detectados na malha:** 4,6 mm² no corpo e 0,6 mm² em cada
  tampa, abaixo de 45°, nas pontas de saída das hélices junto ao chanfro.
  É irrelevante e imprime sem suporte.
* **Vedação:** O-ring **34 × 1,5 mm** (NBR ou silicone), ou um anel de TPU
  impresso de 34 × 38 × 1,5 mm. A compressão é de cerca de 27% com a tampa
  encostada no aro.

## Verificação offline (sem Fusion)

```
pip install cadquery trimesh manifold3d matplotlib lxml networkx
python verificacao/verificar_cadquery.py
```

Gera `relatorio_cadquery.txt`, `section_analysis_XZ.png` e STEP/STL/3MF
de referência de cada peça.

**Importante:** o script do Fusion **não pôde ser executado aqui** (não
existe Fusion 360 neste ambiente). A geometria, os booleanos, as folgas e
a manifoldness foram validados com o mesmo módulo `ampulheta_geom.py`
no OpenCASCADE. Se o Fusion acusar algo na primeira execução, a
mensagem de erro aparece em uma caixa de diálogo com o traceback completo.
