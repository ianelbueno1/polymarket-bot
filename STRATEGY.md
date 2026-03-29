# Estrategia de Trading — Polymarket

## Filosofía (3 principios)

1. **El edge viene de sesgos humanos sistemáticos, no de predecir el futuro.** En política, los mercados son underconfident — un contrato a 70¢ tiene ~83% de probabilidad real (Le 2026, 292M trades). En sports/entertainment, el bias clásico se mantiene (favoritos ligeramente overpriced). La dirección del bias depende de la categoría.

2. **Ganar poco muchas veces > ganar mucho pocas veces.** Domer ganó $2.5M con 8,000 trades chicos de 10,000 totales. Joe Tay fue rentable con 34% win rate porque ganaba 3x más de lo que perdía. ATLAS: todos los agentes convergieron en cautela independientemente. El top 0.04% de wallets captura 70% de las ganancias — con ejecución consistente en 1-2 categorías.

3. **Cash es una posición válida.** Si no hay oportunidad clara, no tradear. El bot de DeepSeek perdió todo lo ganado por overtrading en mercado lateral. Los superforecasters de Tetlock casi nunca dicen "50%" como default — si no sabés, no tradeás, no tirás moneda.

---

## Fase actual: FASE 1 — Solo Favorite Compounder (primeras 4 semanas)

Objetivo: juntar 50+ trades resueltos para tener data estadísticamente significativa antes de cambiar cualquier cosa.

### Estrategia A: Favorite Compounder

**Base científica:**
- Le (2026): En política, contratos a 70¢ tienen ~83% de probabilidad real. Slope de calibración 1.31. Los favoritos están BARATOS.
- Reichenbach & Walther (2025, 124M trades): Precios de Polymarket trackean probabilidades reales y superan odds de bookmakers.
- PANews (112K wallets): Los que ganan tradean 1-2 categorías con expertise de dominio. Holds >7 días rinden 18% mejor que holds <24hs.

**Foco principal: POLÍTICA y GEOPOLÍTICA**
Esta es la categoría con más ineficiencia comprobada. El mercado es sistemáticamente underconfident en política (slope 1.31 vs 1.08 en sports). Razón: retail tradea con emociones políticas, no con probabilidades. Los trades grandes (>100 contratos) en política muestran slope de 1.74 — el smart money ve la underconfidence y la explota.

**Mecánica:**
1. Buscar mercados POLÍTICOS/GEOPOLÍTICOS donde un outcome tiene >80% de probabilidad implícita
2. **Descomponer la pregunta (Fermi — Tetlock):** ¿Qué tendría que pasar para YES? ¿Y para NO? Listar cada pathway.
3. **Base rate primero (Outside View — Tetlock):** ¿Con qué frecuencia pasan cosas así históricamente? Ese número es tu punto de partida.
4. **Ajustar con evidencia actual (Inside View):** Mover desde el base rate con updates chicos (3-5% por dato nuevo, como Tim Minto).
5. **Invertir la pregunta (Duke):** "¿Qué haría que estuviera equivocado?" Buscar activamente esa evidencia.
6. **Premortem (Duke):** "Imaginate que perdiste este trade. ¿Por qué fue?" Si la respuesta es obvia → no entrar.
7. Si después de todo esto la probabilidad real estimada es >90% y el mercado dice <88% → comprar el lado dominante.
8. Hold hasta resolución — no vender antes.

**Filtros obligatorios (todos deben pasar):**
- Probabilidad implícita del lado dominante: >80% (bajamos de 85% porque en política el bias es a favor nuestro)
- Volumen 24h: >$2,000
- Spread: <6%
- Resolución: >48 horas (no tradear en últimas 48hs — los bots dominan ahí)
- Liquidez: >$5,000
- Resolución criteria: clara y no ambigua (leer como abogado, no como periodista)
- Pasa el premortem: no hay razón obvia por la que perdería
- Pasa la inversión: busqué evidencia en contra y no la encontré (o es débil)

**Sizing:**
- $3 por trade, siempre, sin excepciones
- Foco en 10-20 mercados políticos/geopolíticos simultáneos
- Secundario: AI/Tech, Macro (cuando hay oportunidad clara)

**Rendimiento esperado (basado en data de Polymarket, no estimaciones genéricas):**
- En política: un contrato a 85¢ tiene ~93% de probabilidad real (slope 1.31)
- Win rate esperado: ~90%+ en política, ~85% en general
- Profit por trade ganador: $0.15-0.60 dependiendo del precio de entrada
- Loss por trade perdedor: -$3 completos (pero ocurre <10% del tiempo en política)
- Net esperado por ronda de 20 trades políticos: ~18 wins × $0.30 = $5.40, ~2 losses × $3 = $6.00
- Breakeven a ligeramente negativo hasta calibrar bien. Positivo cuando el edge de underconfidence se confirme.

**Categorías por prioridad:**
1. **Política** (slope 1.31 — mayor edge comprobado, foco principal)
2. **Geopolítica** (similar a política, alta emoción retail, resolución a veces ambigua — leer rules)
3. **AI/Tech** (gap entre realidad técnica y pricing narrativo)
4. **Macro/Economía** (solo cuando hay consenso extremo claro)

**Categorías de MENOR prioridad (poco edge):**
- Sports (slope 1.08 — casi eficiente, solo entrar con resolución 100% clara)
- Crypto (slope 1.05 — casi eficiente + territorio de bots)

**PROHIBIDAS:**
- Crypto price targets a fechas fijas (BTC a $X en marzo) — territorio de bots, lost $170+ acá
- Mercados con resolución ambigua (leer las rules de resolución ANTES de entrar)
- Mercados donde no podés hacer Fermi decomposition (si no podés descomponer → no entendés → no tradeás)

---

## Fase 2 (después de 50+ trades resueltos): Agregar Contrarian al 10%

Solo se activa cuando Fase 1 muestra edge positivo real.

### Estrategia B: Contrarian en pánico extremo

**Base científica:** Reflexividad de Soros (los precios crean realidad, loops de feedback se amplifican hasta romperse). Máximo consenso = máxima fragilidad (confirmado por ATLAS). En política específicamente, el mercado ya es underconfident — el contrarian tiene que ser en momentos de PÁNICO real donde el mercado overcorrige.

**Mecánica:**
1. Detectar mercados donde el precio se movió >20% en 24-48hs por una noticia
2. **Baseline pricing (Domer):** Estimar la probabilidad real SIN mirar el precio actual primero
3. **Fermi decomposition:** Descomponer la pregunta en sub-preguntas estimables
4. **Base rate:** ¿Con qué frecuencia overcorrecciones de este tipo se revierten?
5. **Premortem:** "Imaginate que este contrarian trade perdió. ¿Por qué?" Si es por algo fundamental (no pánico temporal) → no entrar
6. Solo entrar si edge >15% (mi estimación vs precio del mercado)
7. Comprar el lado impopular a precios bajos ($0.05-0.20)

**Filtros obligatorios:**
- Edge estimado: >15%
- Solo política/geopolítica (donde tenemos más edge + el underconfidence amplifica el snap-back)
- Resolución criteria 100% clara
- El evento debe tener un catalizador identificable, no ser "capaz que sí"
- Puedo explicar mi edge en 1 frase — si no puedo, no entro
- El premortem no muestra razón fundamental de pérdida

**Sizing:**
- $3 máximo, sin excepciones
- Max 10% del portfolio en contrarian
- Max 3 posiciones contrarian simultáneas

**R/R esperado:**
- Win rate bajo (~30-40%)
- Pero las ganancias son 3-5x las pérdidas (comprar a $0.10, cobrar $1 = 10:1)
- Estructura barbell de Taleb: muchas pérdidas chicas, ganancias grandes ocasionales

---

## Fase 3 (después de 100+ trades resueltos): Activar auto-research

Solo se activa cuando hay data estadísticamente significativa.

El agente puede proponer UN cambio por semana a esta estrategia, documentado en research_log.md con hipótesis y métricas pre-cambio. Si el cambio empeora resultados en 2 semanas → revertir.

Cambios deben evaluarse en batches de 20+ trades (Duke), nunca por resultados individuales.

---

## Protocolo de análisis por mercado (Tetlock + Duke + Domer)

Para CADA mercado que se evalúa, seguir estos pasos en orden:

### 1. Triage (Tetlock Commandment #1)
¿Esta pregunta es tradeble? Evitar preguntas demasiado fáciles (99% seguro, no hay edge) o demasiado difíciles (genuinamente 50/50, no hay edge). Buscar la zona Goldilocks: 65-90% donde hay tanto edge como resolución.

### 2. Descomposición Fermi
- ¿Qué tendría que ser verdad para YES?
- ¿Qué tendría que ser verdad para NO?
- Listar cada sub-componente con su probabilidad estimada
- Combinar matemáticamente, no intuitivamente

### 3. Outside View (Base Rate)
- ¿Con qué frecuencia pasan cosas así? Buscar datos históricos.
- Ese número es tu ANCLA. Todo lo demás ajusta desde ahí.
- Ejemplo: "¿Caerá el régimen de Iran?" → ¿Cuántos regímenes autoritarios cayeron en los últimos 50 años por presión externa? Base rate ~3% por año.

### 4. Inside View (Ajuste)
- ¿Qué es específico de ESTA situación que mueve el base rate?
- Updates chicos (3-5% por dato, como Tim Minto con sus 34 updates)
- Nunca hacer un salto de >15% por una sola noticia a menos que sea definitiva

### 5. Inversión (Duke)
- Argumentar seriamente el lado opuesto
- Si no podés construir un argumento decente en contra → posiblemente estás en confirmation bias
- Si el argumento en contra es fuerte → reducir confianza o no entrar

### 6. Premortem (Duke)
- "Es 2 semanas después y perdí este trade. ¿Qué pasó?"
- Si la respuesta es obvia y predecible → no entrar
- Si la respuesta requiere un evento improbable → entrar con más confianza

### 7. Resolución Check (Domer)
- Leer las reglas de resolución palabra por palabra
- ¿Hay tecnicidades que el mercado no está priceando?
- ¿Hay ambigüedad que podría causar disputa UMA?
- Si hay ambigüedad → no entrar (a menos que la ambigüedad favorezca tu posición)

### 8. Granularidad (Tetlock)
- Expresar tu probabilidad como número exacto (72%, no "alrededor de 70%")
- Comparar con el precio del mercado
- Calcular edge: tu estimación - precio del mercado
- Si edge < threshold (15% contrarian, ~7% favorite compounder) → no

---

## Reglas de hierro (no negociables, aplican siempre)

1. **Max $5 por trade.** Los trades de "alta convicción" con sizing grande son los que más te destruyen. BTC $80K con $100 fue el 35% de la pérdida total.

2. **Foco en 1-2 categorías con expertise.** El top 0.04% de wallets gana tradeando 1-2 categorías. Diversificar entre categorías correlaciona con más pérdidas (PANews, 112K wallets).

3. **Max 20 posiciones abiertas.** Más de eso no se puede monitorear con calidad.

4. **NO promediar para abajo.** Si una posición va mal, la tesis estaba equivocada o el timing fue malo. No tirar más plata.

5. **NO escalar posiciones.** Ganar 3 trades seguidos no significa que el próximo va a ganar. Sizing fijo siempre. "Resulting" (Duke): juzgar la decisión por el proceso, no por el resultado.

6. **Resolución >48hs.** No entrar en mercados que resuelven pronto — los bots dominan los últimos minutos. 15-20% de mercados crypto cortos resuelven por movimientos en los últimos 10 segundos.

7. **Leer resolución criteria como abogado.** Domer ($2.5M profit) dijo que su edge real era entender las reglas mejor que el mercado. UMA nunca overrideó una clarificación de Polymarket — las clarificaciones son binding.

8. **Evaluar en batches, no individualmente.** Un trade que pierde no es un error — es el 10-15% pasando. Evaluar performance cada 20+ trades (Duke). Con menos de 20 → no tenés data suficiente para cambiar nada.

9. **Hold >7 días.** Traders con holds >7 días rinden 18% mejor que holds <24hs (PANews data). En mercados binarios, el precio intermedio es ruido. Hold hasta resolución.

---

## Pre-trade protocol (60 segundos)

Esto no es opcional. Evidencia: +23% profitability (estudio Dartmouth), +45% adherencia a risk management, -38% decisiones emocionales con visualización.

1. **3 respiraciones lentas** — activa sistema nervioso parasimpático
2. **Rating emocional 1-5** — ¿estoy neutral?
3. **Si >3 → no tradear.** Sin excepciones.
4. **"Wanna Bet?" test (Duke):**
   - ¿Cuánto estoy dispuesto a perder? (debe ser $3, si querés más → estás emocional)
   - ¿Cuál es mi estimación de probabilidad EXACTA? (no "creo que sí", un número)
   - ¿Qué evidencia tengo? (no narrativa, datos)
   - ¿Qué evidencia en contra busqué? (si no buscaste → no entrar)
   - ¿Hice el premortem? (imaginar la pérdida antes de entrar)
   - ¿Pasó todos los filtros obligatorios? (uno por uno)
5. **Si dudás → no.** La duda es información.

---

## Kill rules

- **3 losses seguidos → pausa 24hs.** No revenge trading. "Tilt" (Duke) destruye más capital que malas estrategias.
- **Win rate <30% después de 30 trades → pausar 1 semana** y revisar todo.
- **Drawdown >15% → solo Estrategia A** hasta recuperar.
- **Drawdown >20% → full stop.** Revisar toda la estrategia desde cero.
- **Alpha decay check mensual:** Comparar Brier score de los últimos 20 trades vs los 20 anteriores. Si empeoró → el mercado cambió de régimen.
- **Calibration check mensual (Tetlock):** Plotear curva de calibración. ¿Cuando digo 80%, pasa ~80% del tiempo? Si hay desviación sistemática → ajustar.

---

## Lo que NO hago (Via Negativa)

- Crypto price targets a fechas fijas (BTC a $X en marzo) — perdí $170 acá
- Mercados 50/50 sin edge claro (moneda al aire) — nunca usar 50% como "no sé" (Tetlock: los peores forecasters abusan del 50%)
- FOMO porque un mercado se movió y "me lo perdí"
- Promediar para abajo sin información nueva
- Escalar sizing después de ganar
- Tradear por aburrimiento o por "hacer algo"
- Mercados con <$2K volumen diario o spread >6%
- Mercados con resolución ambigua o que dependen de interpretación
- Juzgar trades individuales como "errores" — evaluar en batches de 20+ (Duke)
- Confundir suerte con skill después de ganar (self-serving bias — Duke)
- Dejar que opiniones políticas/ideológicas contaminen estimaciones (Tetlock: los que confunden hechos con valores forecatean peor)

---

## Modelos mentales de referencia

**Tetlock (Superforecasting):** Base rate primero, ajustar con evidencia en updates chicos (3-5%), Fermi decomposition, granularidad (72% no "alrededor de 70%"), foxes > hedgehogs, perpetual beta.

**Duke (Thinking in Bets):** Separar calidad de decisión de calidad de resultado. Premortem. "Wanna Bet?" test. Evaluar en batches no individualmente. Resulting es el enemigo.

**Dalio:** No predecir, prepararse para cualquier escenario. 15-20 posiciones no correlacionadas. La economía es una máquina con ciclos.

**Paul Tudor Jones:** "Defense wins championships." Solo 5:1 R/R mínimo. "I'm always thinking about losing money."

**Soros:** Los precios crean realidad. Máximo consenso = máxima fragilidad. Probe small, press when confirmed, exit decisively.

**Livermore:** "It never was my thinking that made the big money. It was my sitting." Hold hasta resolución.

**Taleb:** Barbell — 90% ultra-seguro, 10% asimétrico. Antifragile: ganar cuando lo inesperado pasa. Fat tails existen — los eventos extremos pasan más seguido de lo que los modelos normales predicen.

**Seykota:** Los traders pierden porque inconscientemente buscan emoción, no profit. El agente autónomo elimina la emoción.

---

## Contexto científico

### Biología y psicología
- **Favorite-longshot bias** existe porque el cerebro sobrepondera eventos raros (cableado evolutivo, Prospect Theory, Kahneman Nobel 2002)
- **Estacionalidad** es real: menos luz solar → menos serotonina → más aversión al riesgo → precios más bajos en otoño/invierno (Lambert 2002, The Lancet). Hemisferio sur: patrón invertido.
- **Overconfidence** es el sesgo más universal — la gente consistentemente cree que sabe más de lo que sabe (Tetlock: 15,000+ predicciones de expertos, accuracy peor que monos tirando dardos)

### Mercados y sistemas
- **Alpha decay** es inevitable (~12 meses half-life). Red Queen hypothesis: tenés que evolucionar constantemente. Auto-research no es un lujo, es supervivencia.
- **Régimen changes** rompen todo. En crisis, los loops de auto-mejora son demasiado lentos (ATLAS: 0% éxito en COVID, -30% en rate tightening). Si hay crisis → cash.
- **Self-Organized Criticality:** Los crashes no son proporcionales a sus triggers. Tensión se acumula gradualmente, un evento menor puede desencadenar colapso. Implicación: no podés predecir crashes, pero sí detectar acumulación de tensión.

### Data empírica de Polymarket (papers y análisis)
- **Le 2026 (292M trades):** Política underconfident (slope 1.31), sports near-calibrated (1.08), crypto mild (1.05). Trades grandes en política: slope 1.74.
- **Reichenbach & Walther 2025 (124M trades):** No hay longshot bias general a nivel de mercado. Solo 30% de traders son rentables, decreciendo con el tiempo.
- **McCullough Dune data:** Brier score 0.058 a 12hs. 95.2% accuracy a 4hs. ~91% accuracy a 1 mes.
- **PANews (112K wallets):** 87.3% pierden plata. Top 0.04% captura 70% de ganancias. Expertise de nicho + ejecución consistente = la fórmula.
- Solo 7.6% de wallets son rentables. 14 de los 20 top wallets son bots.
- 41% de condiciones tienen oportunidades de arbitraje.
- Los spreads se comprimieron de 4.2¢ (ene 2025) a 2.4¢ (ago 2025) — el mercado se vuelve más eficiente cada mes.

---

## Post-trade review (después de cada batch de 20 trades resueltos)

### Por trade individual (log rápido):
1. ¿Seguí el protocolo de análisis completo?
2. ¿Cuál fue mi estimación vs el precio del mercado?
3. ¿Resultado: win/loss?

### Por batch de 20 (análisis profundo — Duke + Tetlock):
1. **Calibración:** Cuando dije 85%, ¿pasó ~85% del tiempo? Plotear curva.
2. **Brier score** del batch vs batch anterior. ¿Mejorando o empeorando?
3. **Resulting check:** ¿Estoy cambiando la estrategia por un mal resultado, o por un mal proceso?
4. **¿Qué trades ganaron y por qué?** Categoría, tipo, timing.
5. **¿Qué trades perdieron y por qué?** ¿Era predecible? ¿El premortem lo habría detectado?
6. **¿Hubo "lucky wins"?** Trades que gané pero con mal razonamiento → son red flags, no éxitos.
7. **¿Hubo "unlucky losses"?** Trades que perdí con buen razonamiento → mantener la estrategia.
8. **Alpha decay:** ¿El edge se está comprimiendo? ¿Los últimos 20 trades tienen menos edge que los 20 anteriores?
