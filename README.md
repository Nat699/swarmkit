# swarmkit — SAMA 2D Structure Analysis

Análise da assinatura geomagnética da Anomalia Magnética do Atlântico Sul (SAMA) em dados do Swarm (ESA), medida **durante** tempestades geomagnéticas.

## Achado Principal
A SAMA apresenta uma **estrutura 2D anisotrópica interna** documentada por 1.788 passagens do Swarm (2015–2024):
- **Pico em S-Centro:** skew +1.158 [IC 95%: 1.120–1.223]
- **Vale em S-Oeste:** skew +0.435 [IC 95%: 0.395–0.902]
- **Classificação (SAMA vs Controles):** AUC = 1.0000 (6 features). Skewness sozinha = 0.9817.

## O que NÃO foi confirmado (Refutação)
Testes de amplificação durante tempestades (threshold em DST ≈ −49 nT) **não se sustentaram**:
- r(skew, DST) dentro da SAMA: +0.05 (p = 0.49)
- Modelo combinado: DST t = +0.16 (n.s.)
- Conclusão: O efeito é geográfico (campo interno), não modulado por tempestade.

## Status
- Paper original (GRL 2026GL127373) **retirado**.
- Relatório Técnico disponível para INPE/EMBRACE.
- Paper em preparação para *Annales Geophysicae*.
