# OráculoPIR

Qué asignaturas caerán en el PIR 2027 (sábado 23 de enero de 2027), estimado a partir de los exámenes PIR oficiales, con simulacros de preguntas oficiales y un generador de preguntas nuevas revisadas por varios agentes de IA. Aplicación web de un solo fichero.

**Usar la app:** https://fborrasumh.github.io/oraculopir/
**Idiomas:** español (por defecto), inglés y portugués. Se cambia en el selector de la barra superior o con `?lang=en` / `?lang=pt` en la URL. Las preguntas del PIR se muestran siempre en español.

## Qué hace

1. **Predicción por asignatura.** Cuenta cuántas preguntas ha tenido cada asignatura (Farmacología, Bioquímica, Fisiología, Microbiología, Fisicoquímica, Técnicas instrumentales, etc.) en cada PIR, las convierte en proporción del examen y estima cuántas tendrá en 2027 sobre 200, con un intervalo del 80 %.
   - Método: media ponderada en la que los años recientes pesan más (semivida de 4 años), más la mitad de la tendencia lineal.
2. **Cuánto fiarse.** Se hace una validación a ciegas en los tres últimos PIR: cada uno se predice solo con los años anteriores y se compara con lo que salió.
   - El método se mide frente a dos referencias sencillas: repetir el año anterior y la media de todos los años.
   - Si no las mejora, la app lo dice y recomienda usar el resultado solo como orden de prioridad.
3. **Simulacro probable.** Usa preguntas oficiales en la proporción que predice el modelo, cada una con la respuesta de la plantilla definitiva.
   - Puntúa como el PIR: +3 por acierto, −1 por fallo, 0 en blanco, y calcula la neta.
   - Reloj opcional al ritmo del PIR: 270 minutos para 210 preguntas.
   - Gratis y sin clave.
4. **Reto diario.** Diez preguntas oficiales, las mismas para todo el mundo cada día.
   - Racha de días seguidos.
   - Resultado en emojis para compartir sin desvelar las respuestas.
5. **Generador con un panel de cinco agentes** (inspirado en [DiagnostIA](https://fborrasumh.github.io/diagnostia/)), con la clave de IA de cada persona:
   - **Agente 1** redacta preguntas nuevas de la asignatura elegida. Recibe tres preguntas oficiales solo como muestra de estilo.
   - **Agentes 2 y 3** resuelven a ciegas, cada uno con las opciones barajadas de otra forma. Si hay clave de un segundo proveedor, se usa por defecto para resolver y revisar: modelos distintos se equivocan menos a la vez.
   - **Agente 4, el Contradictor**, ve la clave y solo busca razones para que la pregunta esté mal (clave errónea, dos opciones defendibles, falta de datos, guía cambiada).
   - **Agente 5, la Lista de control**, revisa la redacción con ocho normas habituales de preguntas de examen.
   - **El código** comprueba el formato (4 opciones distintas, clave entre 1 y 4, sin «todas/ninguna de las anteriores») y descarta las preguntas que se parecen demasiado a una oficial. También mira el estilo: que la correcta no sea mucho más larga que las demás y que los absolutos («siempre», «nunca») no estén solo en los distractores.
   - Una pregunta solo se **acepta** si los dos resolutores eligen la respuesta del redactor y el Contradictor, la Lista y el estilo no ponen pegas. Si un resolutor discrepa o hay una pega menor queda **dudosa**; si discrepan los dos, o el Contradictor la da por mala, se **descarta**. La Lista de control nunca descarta: sus pegas dejan la pregunta en dudosa, porque en la medición marcaba como malas demasiadas preguntas oficiales buenas.
   - **Medición de la fiabilidad:** el panel se prueba con 100 preguntas oficiales, cada una dos veces: con su respuesta oficial y con una respuesta errónea puesta a propósito. Así se publica cuántas buenas acepta y cuántas erróneas deja pasar, con solo los resolutores y con el panel completo (`data/calibracion.json`, pantalla «Cómo se valida»). Cada persona puede repetirla con su clave.
   - Las preguntas aceptadas se exportan a Word, CSV y Moodle (GIFT).

6. **Examen PIR 2027 completo con IA** (paso 4): 25, 50, 100 o 200 preguntas nuevas, repartidas por asignatura según la predicción.
   - Cada tanda pasa por el panel completo (redactor, 2 resolutores a ciegas, Contradictor, Lista de control) y las comprobaciones del código, y no repite preguntas dentro del mismo examen.
   - Se puede continuar si se corta. Lo que los agentes descartan se completa, si se quiere, con preguntas oficiales marcadas.
   - Se hace como simulacro con reloj y puntuación PIR, y se descarga en Word o Moodle (GIFT).
   - 200 preguntas cuestan unas 150 llamadas con la clave de cada persona; la app lo estima antes de empezar.
   - **Mis generadas:** todos los exámenes y las preguntas sueltas generados se guardan en el navegador (IndexedDB), sin servidor. Se pueden volver a hacer como simulacro, continuar, exportar a Word o Moodle, borrar, y guardar o recuperar en una copia JSON.
   - **Tu clave de IA:** guía paso a paso para conseguir la clave con límite de gasto (OpenAI, Gemini o Claude), qué cuesta y en qué se diferencia de una suscripción al chatbot.
7. **«¿Por qué?» en cada pregunta corregida**, con la clave de IA de cada persona. La IA explica la respuesta **oficial** y no puede cambiarla; si con las guías actuales le parece discutible, lo dice aparte. La explicación se guarda para no pagarla dos veces.
8. **Mi estudio:**
   - **Repaso espaciado de fallos:** cada fallo vuelve a salir al día siguiente y, si se acierta, a los 1, 3, 7, 21 y 60 días.
   - **Plan «dónde ganas más puntos»:** preguntas esperadas en 2027 × tu porcentaje de fallo en cada asignatura.
9. **Banco y exámenes:** el PIR de un año concreto completo (también con enlace `?anio=2019`) y un buscador por palabras, asignatura y año.
10. **Estructuras y figuras:** el PIR no tiene cuadernillo de imágenes; las estructuras químicas van dibujadas dentro del cuaderno y el texto extraído las pierde. `scripts/pir_figuras.py` localiza cada dibujo (líneas, curvas o imágenes incrustadas), lo asigna a la pregunta en cuya zona cae y guarda la pregunta entera como imagen: 33 preguntas de 2024, 2025 y 2026 se ven con su estructura.
11. **Avisar de un error** desde cada pregunta: abre una incidencia de GitHub ya rellenada.
12. **Instalable y sin conexión** (manifest + service worker): una vez abierta, funciona sin internet.
13. **Página «Cómo se valida»**, con el cotejo de cada examen frente a lo publicado.

## Lo que no hace (límites reales)

- **No predice preguntas concretas**, solo cuántas tendrá cada asignatura. El simulacro entrena el formato y el ritmo; no adivina el examen.
- **El PIR no tiene asignaturas oficiales.** Las 24 asignaturas (`data/asignaturas.json`) son una clasificación propia, parecida a la de las academias. Cada pregunta la asigna `gpt-6-luna` (`scripts/pir_clasifica_ia.py`, secreto `OPENAI_API_KEY`); sin clave, se usan palabras clave, que se equivocan en algunas preguntas.
- **Que el panel apruebe una pregunta no garantiza que sea correcta.** Reduce los errores, pero varios modelos pueden equivocarse a la vez; la medición dice cuántos se cuelan con preguntas oficiales, y las generadas pueden comportarse algo distinto. Las únicas respuestas con respaldo oficial son las de las preguntas oficiales.
- **Las anuladas y las preguntas cuya imagen no se tiene no entran en los simulacros.**
- Herramienta independiente, sin relación con el Ministerio de Sanidad.

## Datos que hay ahora

| Años | Cuaderno | Respuestas |
|---|---|---|
| 2022-2026 | Portal FSE del Ministerio (API de su web. titulación Farmacia «F». versión 0) | Hoja de respuestas definitiva oficial |
| 2009. 2016-2019. 2021 | Copias de los PDF oficiales que enlaza [La Chuleta del PIR](https://www.lachuletadelfir.com/examenes-pir-de-anos-anteriores/) | Plantilla definitiva copiada |
| 2020 | Ídem | Plantilla definitiva versión 0 publicada por consalud.es; las 5 anuladas coinciden con las publicadas (40. 57. 89. 96 y 166) |
| 2010-2015 | Ídem | Las plantillas que hay están escaneadas y no se leen. Las respuestas se cruzan **por texto** con la transcripción de [oposicionesgratis.com](https://oposicionesgratis.com/pir/examenes). que declara venir de la plantilla definitiva. Antes se valida esa fuente con los seis años que sí tienen plantilla oficial: coincide en 1.212 de 1.212 respuestas. Las preguntas que no casan con seguridad (y las anuladas) quedan sin respuesta y no entran en los simulacros |

Todo lo que no viene del portal se marca en la app como «tomada de una copia del cuaderno oficial».

El PIR ha cambiado de tamaño: 250 + 10 preguntas con 5 opciones hasta 2012. 225 + 10 de 2013 a 2019 (con 4 opciones desde 2016). 175 + 10 en 2020-2021 y 200 + 10 desde 2022. El número esperado de cada año se lee de la portada del propio cuaderno. y la predicción trabaja con proporciones.

Comprobaciones antes de aceptar un año copiado:
- El año del examen se toma del propio cuaderno: «PRUEBAS SELECTIVAS 2019» es el PIR de enero de 2020.
- El cuaderno debe ser de Farmacia y de la versión 0 si su portada dice la versión; la plantilla. del mismo año.
- No se puede usar el mismo fichero para dos años.
- No se admiten más de 15 anuladas.
- La plantilla debe cubrir al menos el 90 % de las preguntas.

La pregunta 210 de 2022 (de reserva) no tiene texto en el PDF y falta.

En total hay 4.104 preguntas de 18 exámenes; 3.820 se pueden usar en simulacros. La asignatura de cada pregunta la asigna `gpt-6-luna`.

## Datos: cómo se traen los exámenes al repositorio

El flujo **Actions → «Datos PIR» → Run workflow** (`.github/workflows/datos-pir.yml`) hace estos pasos:

1. `scripts/pir_fetch.py --api` abre el portal FSE con Chromium para obtener su token anónimo y pide a su API, convocatoria a convocatoria, el cuaderno de la versión 0 y la hoja de respuestas definitiva.
2. `scripts/pir_externos.py` completa los años que el portal ya no ofrece con las URL de `data/fuentes_externas.json`. Comprueba que cada cuaderno sea un PDF de Farmacia, de la versión 0, con las preguntas que anuncia su portada y que la plantilla cubra al menos el 90 % de ellas.
3. `scripts/pir_datos.py` extrae el texto (también de páginas a dos columnas), separa preguntas y opciones (4 o 5, según el año), lee la respuesta oficial, clasifica cada pregunta y escribe `data/pir.json` (lo que lee la app) y `data/informe.md` (año a año: preguntas, respuestas leídas, anuladas y huecos).

Con el paso `calibrar`, `scripts/pir_calibracion.py` abre la propia app en Chromium con el secreto `OPENAI_API_KEY` (en memoria, sin escribirlo en disco), mide el panel de agentes con 100 preguntas oficiales y guarda `data/calibracion.json`.

El portal es una aplicación web sin lista pública de enlaces, así que el descubrimiento es heurístico. Si algún año falla:

- Mira las capturas del portal en el artefacto `portal-debug` de la ejecución.
- Escribe a mano la URL en `data/fuentes.json` con `"origen": "manual"`.
- Relanza el flujo con el paso `descargar`.

**Revisa a mano al menos 20 preguntas por año contra el PDF antes de dar los datos por buenos.** Mientras no exista `data/pir.json`, la app funciona en **modo demostración**: recuentos ficticios y 12 preguntas escritas para la demo, ambos marcados como tales.

## Privacidad

- La predicción, los simulacros, el reto diario, la racha y la clave de IA se quedan en el navegador.
- El generador envía al proveedor elegido la asignatura y unas preguntas oficiales de ejemplo, nunca datos de la persona. Antes del primer envío muestra lo que va a salir.
- Cada tanda son cinco llamadas a la IA, que cada persona paga con su propia clave.

## Para que se difunda (diseño)

- **Gratis y sin registro:** predicción, simulacros y reto no piden clave. La fricción de la clave solo aparece en el generador.
- **Reto diario igual para todos**, con resultado en emojis (estilo Wordle) y racha: da algo que comparar cada día en los grupos de WhatsApp de la promoción.
- **«Te reto con este mismo examen»:** el enlace `?sim=<semilla>&n=<n>` reproduce exactamente el mismo simulacro en otro móvil.
- **Imagen de la predicción** (1080×1350), lista para Instagram y X, con el enlace de la app.
- **Cuenta atrás** hasta el 23 de enero en la portada.
- **Honestidad como argumento:** la tarjeta «¿Cuánto fiarse?» enseña el acierto a ciegas en lugar de prometer.

## Desarrollo y pruebas

```bash
python3 scripts/i18n_fuente.py     # regenera src/i18n.js (diccionarios en/pt)
python3 build.py                   # monta index.html
node tests/test_nucleo.js          # predicción, validación, muestreo, puntuación, comprobaciones del generador
python3 tests/test_datos.py        # extracción de cuadernos y plantillas (textos de prueba)
python3 tests/smoke_test.py        # app completa en Chromium con IA simulada
```

## Autoría

- Fernando Borrás Rocher (Universidad Miguel Hernández de Elche) · ORCID [0000-0002-5519-4573](https://orcid.org/0000-0002-5519-4573)

Basada en OráculoMIR y OráculoEIR, adaptada al examen PIR.

Fuente de las preguntas oficiales: cuadernos de examen y plantillas definitivas de respuestas publicados por el Ministerio de Sanidad (portal de Formación Sanitaria Especializada).

## Cómo citar

Borrás Rocher, F. (2026). *OráculoPIR* (v1.0.0) [Software]. https://github.com/fborrasumh/oraculopir (DOI en trámite)

## Licencia

Código: MIT. Véase [LICENSE](LICENSE). Las preguntas oficiales pertenecen a su fuente (Ministerio de Sanidad) y se reproducen citándola.
