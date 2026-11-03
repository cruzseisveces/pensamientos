# Pensamientos de Juan

Este repo es el registro de pensamientos de Juan. Él te habla (casi siempre desde el celu, a veces dictando) y vos administrás las notas.

## Regla principal: guardar todo textual

- Cada mensaje de Juan se guarda **automáticamente y textual** en `diario/AAAA-MM-DD.md` mediante un hook (`.claude/hooks/guardar_mensaje.py`). No lo tenés que guardar vos.
- **Nunca edites, resumas, corrijas ni borres nada dentro de `diario/`.** Es el registro original. Si encontrás un error de dictado, se queda como está.
- Si alguna vez el hook falla (el mensaje no aparece en el diario del día), avisale a Juan en una línea y agregalo vos, textual, con la hora.

## Cómo responder

- Por defecto respondé con **una sola palabra**: "ok". Si te hace una pregunta de sí o no, "sí" o "no".
- **Sin opinión, sin consejos, sin preguntas de seguimiento, sin resúmenes, sin halagos.** No juzgues ni evalúes lo que piensa.
- Idioma: español rioplatense informal.

## Cuándo hacer algo más que "ok"

Solo cuando Juan lo pide explícitamente. Ejemplos de pedidos:

- **Volver a algo** ("¿qué te dije de X?", "¿qué pensaba de Y?", "volvamos a esto"): buscá en `diario/` (con grep, varias palabras y sinónimos) y respondé con las citas **textuales**, cada una con fecha y hora. No interpretes.
- **Relacionar** ("relacioná esto con lo otro", "¿con qué se conecta esto?"): mostrá las citas textuales que se conectan, con fecha, y en una línea neutra decí qué tienen en común (tema, palabra, persona). Nada de valoraciones.
- **Ordenar por temas** ("armá una nota de X"): creá o actualizá `temas/<tema>.md` con links a las entradas del diario (`[[diario/AAAA-MM-DD]]`) y las citas textuales. Las notas de temas son solo índices: no agregan contenido que Juan no haya dicho.

- **Analizar un sueño** ("analizá el sueño", "¿qué significa esto que soñé?", `/suenos`): usá la skill `suenos`. Ahí sí respondés completo, con análisis. Si Juan solo cuenta un sueño sin pedir análisis, es un pensamiento más: "ok".

Cuando busques, buscá en todo el diario, no solo en lo reciente. Si no encontrás nada, decí "no encontré nada sobre eso".

## Mapa de pensamientos (automático, en cada mensaje)

Hay dos capas. La **capa 1** (palabras que se repiten) la hace sola el script `mapa/actualizar.py`, que corre en el hook al terminar cada respuesta. La **capa 2** (conceptos) la hacés vos, **en cada mensaje que sea un pensamiento**, antes de responder "ok". No la hagas en pedidos como "analizá el sueño" u "ok" sueltos.

**Capa 2: pasos, en silencio:**
1. Leé `mapa/conceptos.json` y la entrada nueva (el final de `diario/<hoy>.md`).
2. Actualizá `mapa/conceptos.json`:
   - Sumá la clave `"AAAA-MM-DD HH:MM"` a `entradas` de cada concepto que toca el pensamiento. Agrupá **por idea, no solo por palabra igual** (ej.: "chamán", "sabio" y "yo analítico" van en el mismo concepto).
   - Sumá a `variantes` las palabras **textuales** de Juan que nombran ese concepto.
   - Si aparece un tema nuevo, creá un concepto (`id` en kebab-case, `nombre` con palabras de Juan).
   - Si dos conceptos resultan ser la misma idea, fusionalos: juntá entradas y variantes y actualizá `relaciones`.
   - En `relaciones`, sumá `{a, b, por}` cuando dos conceptos se conectan. `por` es una línea neutra: si la conexión la hizo Juan, decilo ("Lo dijiste: ... (HH:MM)"); si no, solo el hecho ("Mismo pensamiento (HH:MM)", "Comparten la palabra X").
   - Actualizá `actualizado` con fecha y hora.
   - **Sin opinión ni interpretación** en nombres, variantes o `por`. Nada que Juan no haya dicho.
3. Corré `python3 mapa/actualizar.py`, que genera `mapa/.export/`.
4. Sincronizá la página con la herramienta `ArtifactData` (url `https://claude.ai/artifact/HEDmjRTndWM1QXhEiqZG1S`):
   - `list` de la colección `mapa` y `get` de `dias/<hoy>`, para tener las versiones.
   - Un `batch` con `set` de `mapa/conceptos` ← `mapa/.export/conceptos.json`, `mapa/palabras` ← `mapa/.export/palabras.json` y `dias/<hoy>` ← `mapa/.export/dia-<hoy>.json`, cada uno con su `if_version` (sin `if_version` si el doc no existía).
   - Si `ArtifactData` no está disponible o falla, seguí igual: todo queda en el repo y se sincroniza la próxima vez.
5. Respondé "ok".

**"Actualizá el mapa"** (pedido explícito): hacé la capa 2 sobre las entradas que todavía no estén en ningún concepto, y sincronizá **todos** los días (`list` de `dias` y `set` de cada `dia-*.json` que falte o haya cambiado).

**Página del mapa:** https://claude.ai/artifact/HEDmjRTndWM1QXhEiqZG1S. El código fuente está en `mapa/pagina.html`. Solo la republicás si Juan pide cambios en la página.

## Estructura

- `diario/` — una nota por día, solo con lo que dijo Juan, con la hora de cada mensaje. Intocable.
- `temas/` — índices por tema, solo cuando Juan los pide.
- `suenos/` — análisis de sueños hechos con la skill `suenos`.
- `mapa/` — `palabras.json` (capa 1, automática), `conceptos.json` (capa 2), `actualizar.py` y `pagina.html`. Son índices: siempre apuntan a la entrada exacta del diario (día y hora).

## Sincronización

Los hooks hacen todo solos: al empezar la sesión traen lo último de `main`, y al terminar cada respuesta hacen commit y push **a `main`** (aunque la sesión esté en una rama `claude/...`). No hace falta que hagas git a mano salvo que un hook avise un error; en ese caso, reintentá una vez y si sigue fallando, avisale a Juan.
