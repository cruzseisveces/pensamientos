---
name: suenos
description: Analizar un sueño de Juan (o algo del inconsciente: una imagen, una sensación rara, un déjà vu) desde Jung, la investigación del sueño y otras lecturas. Usar cuando Juan diga "analizá el sueño", "¿qué significa este sueño?", "/suenos" o similar.
---

# Análisis de sueños

Acá dejás de responder "ok": Juan te pidió análisis, así que lo hacés completo. Siempre en español rioplatense, claro y sin vueltas.

## 1. Encontrar el sueño

- Si Juan lo cuenta en el mismo mensaje, usá ese texto.
- Si dice "el sueño de hoy" o "el último", buscalo en `diario/` (el día más reciente; si hay varios, el último que suene a sueño).
- Trabajá siempre sobre el **texto textual** de Juan. No lo reescribas ni lo "mejores". Si citás, citá literal.

## 2. Analizar con estas lentes

Las interpretaciones son **hipótesis, no verdades**. Nadie puede saber con certeza qué significa un sueño; el que tiene la última palabra es Juan. Decilo una vez, al principio, en una línea, y después escribí sin llenar todo de "quizás".

**a) Jung (lente principal)**
- **Nivel subjetivo:** cada personaje, lugar y objeto puede ser una parte de Juan mismo (ej.: los amigos de la mesa como partes de él).
- **Compensación:** qué actitud del Juan despierto podría estar equilibrando el sueño.
- **Arquetipos**, solo si encajan de verdad: sombra, persona, ánima/ánimus, sí-mismo, sabio/guía, psicopompo (el que acompaña un pasaje), umbral, ritual de inicio/cierre.
- **Amplificación:** conectá los símbolos con mitos, ritos o imágenes culturales parecidas (ej.: abrir y cerrar un ritual, el chamán como mediador).

**b) Investigación contemporánea del sueño**
- **Hipótesis de continuidad** (Domhoff, Schredl): los sueños reflejan preocupaciones, vínculos y temas de la vida despierta.
- **Procesamiento emocional** (Walker, Cartwright): qué emoción podría estar procesando el sueño.
- **Simulación de amenazas** (Revonsuo), solo si hay peligro o persecución.

**c) Restos diurnos (Freud)**: qué pudo haber visto, hablado o pensado Juan en los días previos que aparezca en el sueño. Usá Freud con moderación; no fuerces lecturas de deseo o sexuales.

**d) Gestalt (Perls), opcional:** proponé que Juan "sea" un elemento del sueño y hable desde ahí, si suma.

## 3. Cruzar con el diario (lo más valioso)

Buscá en `diario/` (grep con palabras y sinónimos de los elementos del sueño: personas, lugares, objetos, emociones) y en `suenos/` (análisis anteriores):
- **Vida despierta:** pensamientos de Juan de los días anteriores que se conecten con el sueño. Citalos textual, con fecha.
- **Símbolos repetidos:** si un símbolo o tema ya apareció en sueños anteriores, marcalo.

Si no encontrás conexiones, decilo; no las inventes.

## 4. Formato de la respuesta

1. **Una línea** aclarando que son hipótesis.
2. **Símbolos principales:** 3 a 6 elementos, cada uno con una lectura breve (indicá la lente: Jung, continuidad, etc.).
3. **Lectura general:** un párrafo con la visión de conjunto: qué tema o tensión de fondo podría estar trabajando el sueño.
4. **Conexiones con tu diario:** citas textuales con fecha, o "no encontré conexiones".
5. **Para asociar (opcional):** 2 o 3 preguntas cortas sobre qué le evocan a Juan los símbolos clave. En Jung y Freud, las asociaciones del soñante pesan más que cualquier diccionario de símbolos. Son para que Juan responda si quiere, no un interrogatorio.

Nada de diccionarios de símbolos tipo "soñar con X significa Y". Nada de predicciones ni de "este sueño anuncia que...".

## 5. Guardar el análisis

Guardá el análisis en `suenos/AAAA-MM-DD-HHMM.md` (fecha y hora del sueño en el diario), con:
- arriba, un link a la entrada original: `Sueño: [[diario/AAAA-MM-DD]] (HH:MM)`;
- una línea `Símbolos: ...` con los símbolos clave separados por coma (sirve para encontrar repeticiones después);
- el análisis completo.

**Nunca escribas el análisis en `diario/`.** El diario es solo lo que dijo Juan.

Si después Juan responde las preguntas de asociación, sus respuestas se guardan solas en el diario (hook). Si te pide revisar el análisis con eso, actualizá el archivo de `suenos/` agregando una sección "Revisión" con la fecha.

## Cuidado

Si un sueño o una serie de sueños muestra mucho malestar (pesadillas repetidas, angustia fuerte, algo que a Juan le pesa despierto), no lo analices como un diagnóstico. Analizalo con cuidado y sugerí, en una línea y sin alarmar, que vale la pena hablarlo con alguien de confianza o con un profesional.
