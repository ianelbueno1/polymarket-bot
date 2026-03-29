# Estrategia de Trading — Polymarket Paper Trader

## Filosofía Core

**Contrarian + Trend Following**
- Comprar cuando el mercado entra en pánico PERO la tendencia macro acompaña
- Vender cuando el mercado está en euforia irracional
- NUNCA ir contra la tendencia macro de fondo

"Be fearful when others are greedy, greedy when others are fearful" — Buffett
"The trend is your friend until the end" — Ed Seykota

---

## Checklist de Análisis por Mercado

### 1. Identificar la tendencia macro
- ¿Cuál es la dirección de largo plazo? (BTC bull cycle? Tensiones geopolíticas escalando? Elecciones acercándose?)
- Si la macro dice UP → solo buscar oportunidades de compra en dips
- Si la macro dice DOWN → solo buscar shorts en rallies
- Si no hay tendencia clara → NO OPERAR

### 2. Detectar pánico o euforia
- ¿El precio se movió bruscamente en las últimas horas/días?
- ¿Hay una noticia que causó sobrerreacción emocional?
- ¿El volumen 24h subió mucho? (señal de pánico/euforia)
- ¿El precio está lejos de lo que sería "racional"?

### 3. Medir el edge
- ¿Cuál creo que es la probabilidad REAL del evento?
- ¿Cuánto se desvía el precio del mercado de mi estimación?
- Solo entrar si mi estimación difiere >8% del precio del mercado
- Ejemplo: si creo que BTC tiene 60% de chance de llegar a $80K pero el mercado dice 40% → edge de 20%

### 4. Doble confirmación
- ¿Las wallets top están tomando la misma posición? (cuando tengamos tracking)
- ¿Hay smart money entrando o saliendo?
- ¿El sentimiento en redes es contrario a lo racional?

---

## Categorías y Cómo Analizarlas

### Crypto (Bitcoin, ETH, etc.)
- Macro: ciclo post-halving, ETF flows, política monetaria Fed
- Pánico: crashes repentinos, FUD de regulación, hacks
- Euforia: pumps sin fundamento, FOMO retail
- Indicadores clave: precio actual vs targets del mercado, proximidad temporal

### Geopolítica (Iran, Israel, Rusia, China)
- Macro: dirección de escalación o desescalación
- Pánico: ataques sorpresa, declaraciones agresivas
- Euforia: optimismo de paz sin fundamento real
- Clave: los mercados sobrereaccionan a noticias de guerra y subestiman diplomacia lenta

### Política (elecciones, nominaciones)
- Macro: tendencias de encuestas, incumbency advantage
- Pánico: escándalos, gaffes virales
- Euforia: rallies post-debate, endorsements
- Clave: candidatos meme siempre están overpriced (la gente apuesta por diversión, no por lógica)

### Sports / Esports
- Macro: rankings, forma reciente, head-to-head
- Pánico: equipo pierde primer set/mapa → odds colapsan
- Euforia: racha ganadora → favorito overpriced
- Clave: los upsets son más probables de lo que el mercado cree

### Fed / Economía
- Macro: dot plot, comunicados previos, datos de empleo/inflación
- Raramente hay edge aquí — el mercado es muy eficiente
- Solo operar cuando hay consenso extremo (>95%) que podría estar equivocado

---

## Gestión de Riesgo

### Sizing
- Trades normales: $3-5 USDC por trade
- Trades de alta convicción: máximo $10
- Lottery tickets (muy baja probabilidad, alto payout): $1-2 max
- NUNCA más de $10 por trade hasta tener data de win rate real
- Máximo 20% del portfolio por categoría (crypto, geopolítica, política, sports)

### Límites
- Máximo 40% del portfolio en posiciones abiertas
- Máximo 15 posiciones simultáneas
- No más de 20-30% en una sola categoría
- Stop loss diario: -$50 (para no seguir metiendo trades si el día viene mal)
- NUNCA promediar para abajo sin info nueva (Livermore)

### Mercado binario — NO hay stops tradicionales
- Polymarket paga $1 o $0. No hay "stop loss" como en acciones
- Si compraste a $0.30, tu downside es $0.30 y tu upside es $0.70 — ya sabés el riesgo al entrar
- NO vender porque el precio bajó — eso es vender el pánico que querías comprar
- Solo salir ANTES de resolución si: (1) tu tesis cambió por info nueva, (2) necesitás el capital para mejor oportunidad
- El sizing al entrar ES tu gestión de riesgo — cuánto ponés = cuánto podés perder

### Asymmetric R/R natural del mercado
- Comprar a $0.10 → riesgo $0.10, reward $0.90 (9:1)
- Comprar a $0.30 → riesgo $0.30, reward $0.70 (2.3:1)
- Comprar a $0.50 → riesgo $0.50, reward $0.50 (1:1)
- Por eso preferimos comprar en rangos bajos (0.05-0.40) donde el R/R es naturalmente asimétrico
- "It's not whether you're right or wrong, but how much you make when right" — Soros

### Kelly Criterion (simplificado)
- Bet size = (edge / odds) * bankroll * factor_conservador
- Factor conservador = 0.25 (quarter Kelly)
- Nunca apostar más del 5% del bankroll en un solo trade

---

## Dato clave: Solo 7.6% de wallets en Polymarket son rentables

Esto significa que el 92.4% pierde plata. Las razones principales:
1. Sin gestión de riesgo (apuestas grandes sin stops)
2. Trading emocional (FOMO, pánico)
3. Tratar Polymarket como apuesta deportiva en vez de probabilidades
4. Operar mercados eficientes (Fed, elecciones grandes) donde no hay edge
5. Overconfidence después de ganar → agrandan posiciones → pierden todo

Nuestro edge: análisis con Claude (sin emociones) + sizing disciplinado + stops asimétricos.

## Favorite-Longshot Bias (validado académicamente)
- Los longshots (precios bajos) están SISTEMÁTICAMENTE overpriced
- Los favoritos (precios altos) también están LIGERAMENTE overpriced
- Esto significa: comprar NO en favoritos extremos (>90c) y comprar YES selectivo en longshots tiene edge matemático
- Pero cuidado: no todos los longshots son iguales — necesitan análisis real

## Sesgos a Evitar

1. **Confirmation bias** — No buscar solo info que confirme mi tesis
2. **Recency bias** — No pesar demasiado lo que pasó ayer
3. **Sunk cost** — Si una posición va mal, cortarla. No promediar para abajo sin razón nueva
4. **Overconfidence** — Mi estimación también puede estar equivocada
5. **FOMO** — Si no hay oportunidad clara, NO OPERAR. Cash es una posición válida
6. **Gambler's fallacy** — Que haya perdido 3 trades seguidos no significa que el próximo va a ganar

---

## Checklist Pre-Trade (hacer ANTES de cada trade)

1. **Inversión (Munger):** ¿Cómo pierdo acá? Si no tenés respuesta clara → NO ENTRAR
2. **Circle of Competence (Buffett):** ¿Puedo explicar en 2 minutos por qué está mispriced? Si no → NO ENTRAR
3. **Si dudás, no (Naval):** Si no es obvio → NO ENTRAR. La duda es información
4. **Margin of Safety (Buffett):** ¿Hay colchón grande entre mi estimación y el precio? Si el edge es <8% → NO ENTRAR
5. **Antifragile (Taleb):** ¿Gano si pasa algo inesperado, o necesito que todo salga perfecto? Si necesitás que todo salga bien → NO ENTRAR
6. **Test and Scale (Soros):** Empezar con $3. Si la tesis se confirma (precio se mueve a favor), subir a $5-10

## Trades que NUNCA hacer (Via Negativa — Taleb)

- Mercados 50/50 sin edge claro (moneda al aire)
- Mercados ultra eficientes (Fed rate decisions con >95% consenso)
- FOMO porque un mercado se movió y "me lo perdí"
- Promediar para abajo sin info nueva
- Más de $10 por trade hasta tener win rate real
- Más de 20% del portfolio en una categoría
- Cualquier trade que no pase el checklist de arriba

## Post-Trade Review (Pain + Reflection — Dalio)

Después de cada trade que resuelve (win o loss), anotar:
- ¿Qué asumí que era cierto?
- ¿Lo era?
- ¿Lo repetiría sabiendo lo que sé ahora?
- ¿Qué regla nueva sale de esto?

## Formato del Análisis Diario

Cada sesión Claude debe:

1. **Status check**: Precio actual de cada posición, P&L, si hay que cerrar algo
2. **Mercados nuevos**: Top 10 oportunidades rankeadas por edge estimado
3. **Para cada trade propuesto**:
   - Mercado y pregunta
   - Side (YES/NO) y precio actual
   - Mi estimación de probabilidad real vs precio del mercado
   - Tendencia macro que respalda
   - Señal contrarian (qué pánico/euforia estoy explotando)
   - Monto sugerido y por qué
   - Riesgo principal (qué podría salir mal)
4. **Resumen**: trades propuestos en tabla para aprobación rápida
