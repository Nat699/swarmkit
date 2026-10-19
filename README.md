# swarmkit — SAMA Tail Amplification Analysis

Análise da assinatura geomagnética da Anomalia Magnética do Atlântico Sul (SAMA) em dados do Swarm (ESA).

## Achado Principal (Confirmado)

A SAMA apresenta uma **amplificação da cauda** na distribuição do campo magnético residual (\(F - 	ext{CHAOS(core+crust)}\)) durante tempestades geomagnéticas.

- **Efeito primário:** +0.119 (SE: 0.007, n = 151 tempestades)
- **Placebo (rótulos permutados):** nulo (-0.0003, IC95%: [-0.004, +0.004])
- **Especificidade:** O efeito é exclusivo da SAMA, não ocorrendo nas regiões controle (Pacífico Central, Índico Sul, Atlântico Leste).
- **Robustez:** Consistente entre satélites A e B e estável em leave-one-out.

## Metodologia

1. **Resíduo:** Subtração do campo interno (CHAOS-7 core + crust) do campo observado.
2. **Métrica:** Fração de amostras acima do limiar de calmaria (não skewness linear).
3. **Pareamento:** Cada tempestade é comparada com duas janelas de calmaria.
4. **Unidade Independente:** Tempestade (não janela).

## O que foi Refutado

A hipótese original de que a SAMA amplifica a **skewness** linear durante tempestades não se sustentou. O efeito está especificamente na cauda da distribuição do resíduo, não no terceiro momento global.

## Reprodução

O pipeline é 100% reprodutível (hashes SHA-256, seed fixa, 151 tempestades pareadas).

## Status

- Artigo em preparação para submissão ao *Annales Geophysicae*.
- Corpus e código abertos (MIT).
