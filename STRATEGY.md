# Estrategia de Trading — Polymarket

## Filosofía (3 principios)

1. **El edge viene de sesgos humanos sistemáticos, no de predecir el futuro.** Los mercados sobreprecian certeza (favoritos rinden 84% cuando el mercado dice 90%) y sobreprecian longshots. Esto está probado académicamente (NBER, Kahneman/Tversky Nobel 2002, estudio de 3,587 mercados).

2. **Ganar poco muchas veces > ganar mucho pocas veces.** Domer ganó $2.5M con 8,000 trades chicos de 10,000 totales. Joe Tay fue rentable con 34% win rate porque ganaba 3x más de lo que perdía. ATLAS: todos los agentes convergieron en cautela independientemente.

3. **Cash es una posición válida.** Si no hay oportunidad clara, no tradear. El bot de DeepSeek perdió todo lo ganado por overtrading en mercado lateral. "Death by a thousand cuts" mata más que los crashes.

---

## Fase actual: FASE 1 — Solo Favorite Compounder (primeras 4 semanas)

Objetivo: juntar 50+ trades para tener data estadísticamente significativa antes de cambiar cualquier cosa.

### Estrategia A: Favorite Compounder

**Base científica:** Favorite-longshot bias (NBER). Eventos >80% probabilidad ocurren solo 84% del tiempo. Los mercados sobreprecian certeza porque los humanos sobreestiman riesgos raros (Prospect Theory, cableado evolutivo — el cerebro prioriza amenazas de baja probabilidad).

**Mecánica:**
- Buscar mercados donde un outcome tiene >85% de probabilidad implícita
- Verificar que la probabilidad real es >90% (basado en datos, no narrativa)
- Comprar el lado dominante (usualmente NO en longshots, o YES en favoritos claros)
- Hold hasta resolución — no vender antes

**Filtros obligatorios (todos deben pasar):**
- Probabilidad implícita del lado dominante: >85%
- Volumen 24h: >$2,000
- Spread: <6%
- Resolución: >48 horas (no tradear en últimas 48hs — los bots dominan ahí)
- Liquidez: >$5,000
- Resolución criteria: clara y no ambigua (leer como abogado, no como periodista)

**Sizing:**
- $3 por trade, siempre, sin excepciones
- Diversificar en 10-20 mercados simultáneos en categorías distintas

**Rendimiento esperado:**
- ~85% win rate (basado en data de 3,587 mercados)
- ~5-15% profit por trade ganador ($0.15-0.45 por trade de $3)
- El riesgo es perder $3 completos en un black swan (~15% del tiempo)
- Compounding: con 20 trades activos, 17 ganan ~$0.30 = $5.10, 3 pierden $3 = $9.00
- Net esperado por ronda: -$3.90 ... PERO los trades perdedores no pierden $3 completos
- Pérdida real promedio en favoritos que fallan: ~$0.45-0.90 (el precio no va a $0, baja a $0.70-0.85)
- Net esperado ajustado: positivo si la calibración se mantiene

**Categorías permitidas:**
- Política y geopolítica (más ineficiencia, retail emocional)
- AI/Tech (gap entre realidad técnica y pricing narrativo)
- Macro/Economía (cuando hay consenso extremo)
- Sports (solo cuando resolución es 100% clara)

**Categorías PROHIBIDAS:**
- Crypto price targets a fechas fijas (BTC a $X en marzo) — territorio de bots, lost $170+ acá
- Mercados con resolución ambigua (leer las rules de resolución ANTES de entrar)

---

## Fase 2 (después de 50+ trades): Agregar Contrarian al 10%

Solo se activa cuando Fase 1 muestra edge positivo real.

### Estrategia B: Contrarian en pánico extremo

**Base científica:** Reflexividad de Soros (los precios crean realidad, loops de feedback se amplifican hasta romperse). Máximo consenso = máxima fragilidad (confirmado por ATLAS).

**Mecánica:**
- Detectar mercados donde el precio se movió >20% en 24-48hs por una noticia
- Baseline pricing: estimar la probabilidad real SIN mirar el precio actual primero
- Solo entrar si edge >15% (mi estimación vs precio del mercado)
- Comprar el lado impopular a precios bajos ($0.05-0.20)

**Filtros obligatorios:**
- Edge estimado: >15% (no 8% como antes — los pros usan 15-20%)
- Solo categorías que entiendo profundamente
- Resolución criteria 100% clara
- El evento debe tener un catalizador identificable, no ser "capaz que sí"
- Puedo explicar mi edge en 1 frase — si no puedo, no entro

**Sizing:**
- $3 máximo, sin excepciones
- Max 10% del portfolio en contrarian
- Max 3 posiciones contrarian simultáneas

**R/R esperado:**
- Win rate bajo (~30-40%)
- Pero las ganancias son 3-5x las pérdidas (comprar a $0.10, cobrar $1 = 10:1)
- Estructura barbell de Taleb: muchas pérdidas chicas, ganancias grandes ocasionales

---

## Fase 3 (después de 100+ trades): Activar auto-research

Solo se activa cuando hay data estadísticamente significativa.

El agente puede proponer UN cambio por semana a esta estrategia, documentado en research_log.md con hipótesis y métricas pre-cambio. Si el cambio empeora resultados en 2 semanas → revertir.

---

## Reglas de hierro (no negociables, aplican siempre)

1. **Max $5 por trade.** Los trades de "alta convicción" con sizing grande son los que más te destruyen. BTC $80K con $100 fue el 35% de la pérdida total.

2. **Max 15% del portfolio en una categoría.** Diversificación = supervivencia. Dalio: 15-20 posiciones no correlacionadas.

3. **Max 20 posiciones abiertas.** Más de eso no se puede monitorear.

4. **NO promediar para abajo.** Si una posición va mal, la tesis estaba equivocada o el timing fue malo. No tirar más plata.

5. **NO escalar posiciones.** Ganar 3 trades seguidos no significa que el próximo va a ganar. Sizing fijo siempre.

6. **Resolución >48hs.** No entrar en mercados que resuelven pronto — los bots dominan los últimos minutos con latency arbitrage.

7. **Leer resolución criteria como abogado.** Domer ($2.5M profit) dijo que su edge real era entender las reglas mejor que el mercado. Si la resolución depende de una tecnicidad → ahí hay edge. Si es ambigua → no entrar.

---

## Pre-trade protocol (60 segundos)

Esto no es opcional. Evidencia: +23% profitability (estudio Dartmouth), +45% adherencia a risk management.

1. **3 respiraciones lentas** — activa sistema nervioso parasimpático
2. **Rating emocional 1-5** — ¿estoy neutral?
3. **Si >3 → no tradear.** Sin excepciones.
4. **¿Pasa todos los filtros obligatorios?** Repasar uno por uno.
5. **¿Puedo explicar mi edge en 1 frase?** Si no → no.
6. **Si dudás → no.** La duda es información. "La certeza de que no hay que entrar."

---

## Kill rules

- **3 losses seguidos → pausa 24hs.** No revenge trading.
- **Win rate <30% después de 30 trades → pausar 1 semana** y revisar todo.
- **Drawdown >15% → solo Estrategia A** hasta recuperar.
- **Drawdown >20% → full stop.** Revisar toda la estrategia desde cero.
- **Alpha decay check mensual:** ¿mis últimos 20 trades son mejores o peores que los 20 anteriores? Si peores → algo cambió en el mercado.

---

## Lo que NO hago (Via Negativa)

- Crypto price targets a fechas fijas (BTC a $X en marzo) — perdí $170 acá
- Mercados 50/50 sin edge claro (moneda al aire)
- Mercados ultra eficientes (Fed rate decisions con >95% consenso, elecciones con data abrumadora)
- FOMO porque un mercado se movió y "me lo perdí"
- Promediar para abajo sin información nueva
- Escalar sizing después de ganar
- Tradear por aburrimiento o por "hacer algo"
- Mercados con <$2K volumen diario o spread >6%
- Mercados con resolución ambigua o que dependen de interpretación

---

## Modelos mentales de referencia

**Dalio:** No predecir, prepararse para cualquier escenario. 15-20 posiciones no correlacionadas.

**Paul Tudor Jones:** "Defense wins championships." Solo 5:1 R/R mínimo. "I'm always thinking about losing money."

**Soros:** Los precios crean realidad. Máximo consenso = máxima fragilidad. Probe small, press when confirmed, exit decisively.

**Livermore:** "It never was my thinking that made the big money. It was my sitting." Hold hasta resolución.

**Taleb:** Barbell — 90% ultra-seguro, 10% asimétrico. Ser antifragile: ganar cuando lo inesperado pasa.

**Seykota:** Los traders pierden porque inconscientemente buscan emoción, no profit. El agente autónomo elimina la emoción.

---

## Contexto biológico (por qué funciona)

- **Favorite-longshot bias** existe porque el cerebro sobrepondera eventos raros (cableado evolutivo, Prospect Theory)
- **Estacionalidad** es real: menos luz solar → menos serotonina → más aversión al riesgo → precios más bajos en otoño/invierno (Lambert 2002, The Lancet). Esto aplica al hemisferio del trader.
- **Alpha decay** es inevitable (~12 meses half-life). Toda estrategia muere. Red Queen hypothesis: tenés que evolucionar constantemente solo para mantener tu posición. Auto-research no es un lujo, es supervivencia.
- **Régimen changes** rompen todo. En crisis, los loops de auto-mejora son demasiado lentos (ATLAS: 0% éxito en COVID, -30% en rate tightening). Si hay crisis → cash.

---

## Datos de Polymarket

- Solo 7.6% de wallets son rentables
- 14 de los 20 top wallets son bots
- 41% de condiciones tienen oportunidades de arbitraje
- Política y geopolítica tienen más ineficiencia (info asimétrica, retail emocional, resolución ambigua)
- Time decay toward 50% en contratos lejanos (edge en largo plazo)
- Los spreads se comprimieron de 4.2¢ (ene 2025) a 2.4¢ (ago 2025) — el mercado se vuelve más eficiente cada mes

---

## Post-trade review (después de cada trade que resuelve)

1. ¿Qué asumí que era cierto?
2. ¿Lo era?
3. ¿Seguí las reglas de hierro?
4. ¿Lo repetiría sabiendo lo que sé ahora?
5. ¿Sale alguna regla nueva de esto?
