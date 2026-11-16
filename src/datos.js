/* ══ Datos: el banco oficial (data/pir.json, lo genera la GitHub Action) o, si aún no existe, un DEMO marcado como ficticio ══ */
const ASIGS_BASE = [
  ['psicopatologia', 'Psicopatología'], ['clinica_adultos', 'Trastornos mentales del adulto'], ['tratamientos', 'Tratamientos psicológicos'], ['psicoterapias', 'Psicoterapias'],
  ['infantil', 'Psicopatología y tratamiento infanto-juvenil'], ['salud', 'Psicología clínica de la salud'], ['evaluacion', 'Evaluación psicológica'], ['basica', 'Psicología básica'],
  ['metodologia', 'Estadística, psicometría y diseños'], ['etica', 'Ética, deontología y legislación'], ['personalidad', 'Psicología de la personalidad'], ['diferencial', 'Psicología diferencial'],
  ['psicobiologia', 'Psicobiología y neuropsicología'], ['psicofarmacologia', 'Psicofarmacología'], ['social', 'Psicología social'], ['evolutiva', 'Psicología evolutiva'],
  ['otras', 'Sin clasificar']
].map(([id, nombre]) => ({id, nombre}));

/* DEMO · preguntas ESCRITAS PARA LA DEMOSTRACIÓN (no son preguntas oficiales del PIR); sirven para probar la app sin datos */
const DEMO_PREG = [
  ['clinica_adultos', 'Según el DSM-5, ¿cuál es la duración mínima de los síntomas necesaria para diagnosticar un trastorno de ansiedad generalizada?', ['Un mes.', 'Tres meses.', 'Seis meses.', 'Doce meses.'], 3],
  ['tratamientos', '¿Qué técnica consiste en exponer gradualmente al paciente a una jerarquía de estímulos que le generan ansiedad mientras mantiene una respuesta incompatible como la relajación?', ['La inundación.', 'La desensibilización sistemática.', 'El moldeamiento.', 'El tiempo fuera.'], 2],
  ['basica', 'En el condicionamiento clásico, ¿cómo se denomina la desaparición gradual de la respuesta condicionada cuando el estímulo condicionado se presenta repetidamente sin el incondicionado?', ['Habituación.', 'Generalización.', 'Extinción.', 'Recuperación espontánea.'], 3],
  ['metodologia', '¿Qué coeficiente se usa habitualmente para estimar la consistencia interna de un test?', ['El coeficiente de correlación de Pearson.', 'El coeficiente alfa de Cronbach.', 'El coeficiente kappa de Cohen.', 'El coeficiente de determinación.'], 2],
  ['evolutiva', 'Según Piaget, ¿en qué estadio adquiere el niño la conservación de la cantidad y un pensamiento lógico aplicado a objetos concretos?', ['Sensoriomotor.', 'Preoperacional.', 'Operaciones concretas.', 'Operaciones formales.'], 3],
  ['psicofarmacologia', '¿Cuál es el mecanismo de acción principal de la fluoxetina?', ['Inhibición de la monoaminooxidasa.', 'Inhibición selectiva de la recaptación de serotonina.', 'Antagonismo de los receptores dopaminérgicos D2.', 'Agonismo de los receptores GABA-A.'], 2],
  ['personalidad', '¿Cuáles son las tres dimensiones del modelo de personalidad de Eysenck?', ['Extraversión, neuroticismo y psicoticismo.', 'Apertura, responsabilidad y amabilidad.', 'Búsqueda de novedad, evitación del daño y dependencia de la recompensa.', 'Afecto positivo, afecto negativo y restricción.'], 1],
  ['social', '¿Cómo se denomina la tendencia a explicar la conducta de los demás por sus disposiciones personales y a infravalorar la influencia de la situación?', ['Efecto de falso consenso.', 'Error fundamental de atribución.', 'Sesgo de autoservicio.', 'Efecto halo.'], 2],
  ['infantil', 'Según el DSM-5, ¿antes de qué edad deben haber estado presentes varios síntomas de inatención o hiperactividad-impulsividad para diagnosticar un TDAH?', ['Antes de los 7 años.', 'Antes de los 10 años.', 'Antes de los 12 años.', 'Antes de los 16 años.'], 3],
  ['etica', '¿Qué ley regula en España los derechos y obligaciones en materia de información y documentación clínica y la autonomía del paciente?', ['La Ley 14/1986, General de Sanidad.', 'La Ley 41/2002, básica reguladora de la autonomía del paciente.', 'La Ley 44/2003, de ordenación de las profesiones sanitarias.', 'La Ley Orgánica 3/2018, de protección de datos personales.'], 2],
  ['psicobiologia', 'Una lesión en el área de Broca produce típicamente:', ['Una afasia fluida con comprensión muy alterada.', 'Una afasia no fluida con comprensión relativamente conservada.', 'Una agnosia visual para objetos.', 'Una amnesia anterógrada.'], 2],
  ['evaluacion', '¿Cuál de estos instrumentos es una técnica proyectiva basada en láminas con manchas de tinta?', ['El MMPI-2.', 'La escala WAIS-IV.', 'El test de Rorschach.', 'El cuestionario 16PF.'], 3]
].map(([asig, enunciado, opciones, correcta], i) => ({id: 'demo-' + (i + 1), anio: 0, n: i + 1, asig, enunciado, opciones, correcta, anulada: false, imagen: false, demo: true}));

/* DEMO · recuentos FICTICIOS de 2015 a 2026 (no son datos reales): solo para ver la predicción funcionando */
function demoConteos() {
  const base = {clinica_adultos: 30, tratamientos: 28, infantil: 18, evaluacion: 16, psicopatologia: 14, basica: 14, salud: 12, metodologia: 12, psicoterapias: 10, psicobiologia: 10, personalidad: 8, etica: 6, psicofarmacologia: 6, social: 6, evolutiva: 6, diferencial: 4};
  const r = rng('demo-oraculopir'), c = {};
  for (let y = 2015; y <= 2026; y++) {
    c[y] = {};
    for (const k in base) { const tr = k === 'tratamientos' || k === 'psicofarmacologia' ? (y - 2015) * 0.35 : k === 'diferencial' || k === 'basica' ? -(y - 2015) * 0.25 : 0; c[y][k] = Math.max(0, Math.round(base[k] * 1.05 + tr + (r() - 0.5) * 5)); }
  }
  return c;
}

let DATA = {real: false, asignaturas: ASIGS_BASE, preguntas: DEMO_PREG, conteos: demoConteos(), examenes: [], generado: null};
const nombreAsig = id => t((DATA.asignaturas.find(a => a.id === id) || {nombre: id}).nombre);
/* Carga data/pir.json (mismo origen, en GitHub Pages). Abierta como fichero local o sin datos todavía → DEMO */
async function cargaDatos() {
  try {
    const r = await fetch('data/pir.json', {cache: 'no-cache'});
    if (!r.ok) throw 0;
    const j = await r.json();
    const ps = (j.preguntas || []).filter(q => q && q.enunciado && q.anio);
    if (ps.length < 100) throw 0;
    DATA = {real: true, asignaturas: j.asignaturas || ASIGS_BASE, preguntas: ps, conteos: conteos(ps), examenes: j.examenes || [], generado: j.generado || null, clasificacion: j.clasificacion || ''};
    try { const a = await (await fetch('data/asignaturas.json', {cache: 'no-cache'})).json(); DATA.kws = Object.fromEntries((a.asignaturas || []).map(x => [x.id, x.kw || []])); } catch { DATA.kws = {}; }
  } catch { /* se queda el DEMO */ }
  return DATA;
}
