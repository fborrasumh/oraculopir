#!/usr/bin/env python3
"""Respuestas de los años sin plantilla legible, cruzando NUESTRO cuaderno con la transcripción de
oposicionesgratis.com/pir/examenes/<año> (que declara venir de la plantilla definitiva del Ministerio).

1. Abre cada página con Chromium, pulsa «Ver las N preguntas» y guarda las respuestas JSON y __NEXT_DATA__
   en data/raw/<año>/sondeo/ (para poder revisarlas).
2. Busca en ese JSON una lista de preguntas con enunciado, opciones y respuesta correcta.
3. Empareja por TEXTO, no por número (así da igual la versión del cuaderno): enunciado con Jaccard ≥ 0,6 y sin
   empate; la opción correcta, por texto (≥ 0,7) contra nuestras opciones.
4. VALIDA la fuente con los años que sí tienen plantilla oficial (respuestas.json del portal o plantilla.txt):
   solo si coincide en al menos el 97 % de las preguntas emparejadas se escribe data/raw/<año>/respuestas_cruce.json
   para los años SIN plantilla, y se anota en origen.txt.
    python3 scripts/pir_cruce_og.py 2010 2011 … [--validar 2016 2017 …]"""
import json, re, sys, time, pathlib, unicodedata
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import pir_datos as M
R = pathlib.Path(__file__).resolve().parent.parent; RAW = R / 'data' / 'raw'
URL = 'https://oposicionesgratis.com/pir/examenes/{}'


def toks(s):
    s = unicodedata.normalize('NFD', str(s).lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return set(re.findall(r'[a-zñ0-9]{3,}', s))


def jac(a, b):
    A, B = toks(a), toks(b); return len(A & B) / max(1, len(A | B))


def sondea(anio):
    from playwright.sync_api import sync_playwright
    dst = RAW / str(anio) / 'sondeo'; dst.mkdir(parents=True, exist_ok=True); trozos = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(locale='es-ES'); resp = []
        pg.on('response', lambda r: resp.append(r) if 'json' in (r.headers.get('content-type') or '') or '_rsc' in r.url else None)
        pg.goto(URL.format(anio), wait_until='networkidle', timeout=90000); time.sleep(2)
        for sel in ('text=/Ver las \\d+ preguntas/', 'text=Ver las', 'text=Consultar', 'text=Ver respuestas'):
            try: pg.click(sel, timeout=4000); pg.wait_for_load_state('networkidle', timeout=60000); time.sleep(3); break
            except Exception: pass
        html = pg.content(); nd = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
        if nd: trozos.append(nd.group(1))
        for x in re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html, re.S):   # carga en streaming (app router)
            try: trozos.append(json.loads('"' + x + '"'))
            except Exception: pass
        for r in resp:
            try: trozos.append(r.text())
            except Exception: pass
        (dst / 'og_pagina.txt').write_text(pg.inner_text('body')[:20000], encoding='utf-8')
        b.close()
    (dst / 'og_crudo.txt').write_text('\n\n=====\n\n'.join(trozos), encoding='utf-8')
    return trozos


def _jsons(texto):
    """Todos los objetos JSON que se puedan leer dentro de un texto (también escapados dentro de cadenas)."""
    for t in (texto,):
        dec = json.JSONDecoder(); i = 0
        while True:
            j = min([k for k in (t.find('{', i), t.find('[', i)) if k >= 0], default=-1)
            if j < 0: break
            try: o, fin = dec.raw_decode(t, j); yield o; i = fin
            except Exception: i = j + 1


TXT = ('enunciado', 'pregunta', 'question', 'stem', 'texto', 'text', 'statement', 'title')
OPS = ('opciones', 'options', 'answers', 'respuestas', 'alternativas', 'choices')
OK = ('correcta', 'correct', 'respuesta_correcta', 'correctAnswer', 'correct_answer', 'answer', 'solucion', 'rc', 'correctIndex')


def _pregunta(d):
    if not isinstance(d, dict): return None
    k_t = next((k for k in d if k.lower() in TXT and isinstance(d[k], str) and len(d[k]) > 15), None)
    k_o = next((k for k in d if k.lower() in OPS and isinstance(d[k], list) and 3 <= len(d[k]) <= 5), None)
    if not k_t or not k_o: return None
    ops, cor = [], None
    for i, o in enumerate(d[k_o]):
        if isinstance(o, str): ops.append(o)
        elif isinstance(o, dict):
            t = next((o[k] for k in o if k.lower() in TXT + ('label', 'value', 'opcion') and isinstance(o[k], str)), '')
            ops.append(t)
            if any(o.get(k) is True for k in o if k.lower() in ('correcta', 'correct', 'is_correct', 'iscorrect')): cor = ('txt', t)
    k_c = next((k for k in d if k in OK or k.lower() in OK), None)
    if cor is None and k_c is not None:
        v = d[k_c]
        if isinstance(v, bool): return None
        if isinstance(v, int) or (isinstance(v, str) and v.strip().isdigit()): cor = ('num', int(v))
        elif isinstance(v, str) and len(v.strip()) == 1 and v.strip().upper() in 'ABCDE': cor = ('num1', 'ABCDE'.index(v.strip().upper()) + 1)
        elif isinstance(v, str) and len(v) > 3: cor = ('txt', v)
    anul = any(d.get(k) for k in d if k.lower() in ('anulada', 'annulled', 'void', 'cancelled'))
    if cor is None and not anul: return None
    return {'enunciado': d[k_t], 'opciones': ops, 'cor': cor, 'anulada': bool(anul)}


def preguntas_og(trozos):
    mejor = []
    def anda(o):
        nonlocal mejor
        if isinstance(o, list):
            ps = [x for x in (_pregunta(e) for e in o) if x]
            if len(ps) > len(mejor): mejor = ps
            for e in o: anda(e)
        elif isinstance(o, dict):
            for v in o.values(): anda(v)
    for t in trozos:
        for o in _jsons(t): anda(o)
    return mejor


def cruza(anio, G, base):
    """{nº nuestro: opción 1..n | 0 anulada}, dudas. base: cómo leer «cor» numérico (0 = índice desde 0, 1 = desde 1)."""
    d = RAW / str(anio); qs, nopt = M.mejor_cuaderno((d / 'cuaderno.txt').read_text(encoding='utf-8'))
    res, dudas = {}, 0
    for g in G:
        sc = sorted(((jac(q['enunciado'], g['enunciado']), q) for q in qs), key=lambda x: -x[0])
        s, q = sc[0]
        if s < 0.6 or (len(sc) > 1 and sc[1][0] > s - 0.1): dudas += 1; continue
        if g['anulada']: res[q['n']] = 0; continue
        tipo, v = g['cor']
        if tipo == 'txt': txt = v
        else:
            i = v - (1 if tipo == 'num1' else base)
            if not 0 <= i < len(g['opciones']): dudas += 1; continue
            txt = g['opciones'][i]
        so = sorted(((jac(o, txt), k + 1) for k, o in enumerate(q['opciones'])), key=lambda x: -x[0])
        if so[0][0] < 0.7 or (len(so) > 1 and so[1][0] > so[0][0] - 0.15): dudas += 1; continue
        if q['n'] in res and res[q['n']] != so[0][1]: res.pop(q['n']); dudas += 1; continue
        res[q['n']] = so[0][1]
    return res, dudas, len(qs)


def oficiales(anio):
    d = RAW / str(anio)
    if (d / 'respuestas.json').exists(): return M.parse_respuestas_json(json.loads((d / 'respuestas.json').read_text(encoding='utf-8')))
    if (d / 'plantilla.txt').exists():
        qs, nopt = M.mejor_cuaderno((d / 'cuaderno.txt').read_text(encoding='utf-8'))
        return M.parse_plantilla((d / 'plantilla.txt').read_text(encoding='utf-8'), max(q['n'] for q in qs), nopt)
    return None


def main():
    args = sys.argv[1:]; val = []
    if '--validar' in args: i = args.index('--validar'); val = [int(a) for a in args[i + 1:]]; args = args[:i]
    objetivo = [int(a) for a in args]
    G = {}
    for y in objetivo + val:
        if not (RAW / str(y) / 'cuaderno.txt').exists(): print(f'{y}: sin cuaderno'); continue
        try: G[y] = preguntas_og(sondea(y))
        except Exception as e: print(f'{y}: no se pudo abrir la página ({e})'); continue
        print(f'{y}: {len(G[y])} preguntas leídas de oposicionesgratis' + (f' · ejemplo: {json.dumps(G[y][0], ensure_ascii=False)[:300]}' if G[y] else ' · revisa data/raw/%d/sondeo/og_crudo.txt' % y))
    # validación: con qué base numérica coincide más con las plantillas oficiales
    mejor = None
    for base in (0, 1):
        ac = tot = 0
        for y in val:
            of = oficiales(y)
            if not of or not G.get(y): continue
            res, _, _ = cruza(y, G[y], base)
            comun = [n for n in res if n in of and of[n] != 0 and res[n] != 0]
            ac += sum(1 for n in comun if res[n] == of[n]); tot += len(comun)
        if tot and (mejor is None or ac / tot > mejor[1]): mejor = (base, ac / tot, ac, tot)
    if not mejor: print('Sin años de validación con datos: no se escribe nada.'); sys.exit(1)
    base, pct, ac, tot = mejor
    print(f'VALIDACIÓN con plantillas oficiales {val}: {ac} de {tot} coinciden ({pct:.1%}), índice desde {base}')
    if pct < 0.97: print('La fuente no es lo bastante fiable: no se escribe nada.'); sys.exit(1)
    for y in objetivo:
        if not G.get(y): continue
        if oficiales(y): print(f'{y}: ya tiene plantilla oficial; no se toca'); continue
        res, dudas, n = cruza(y, G[y], base)
        print(f'{y}: {len(res)} respuestas de {n} preguntas ({sum(1 for v in res.values() if v == 0)} anuladas) · sin emparejar con seguridad: {dudas}')
        if len(res) < 0.70 * n: print(f'{y}: cubre menos del 70 %: no se escribe'); continue   # las que no casan se quedan sin respuesta (no entran en simulacros)
        d = RAW / str(y); (d / 'respuestas_cruce.json').write_text(json.dumps({str(k): v for k, v in sorted(res.items())}, indent=0), encoding='utf-8')
        o = d / 'origen.txt'; L = o.read_text(encoding='utf-8').splitlines() if o.exists() else []
        lin = f'plantilla: {URL.format(y)} (cruce por texto con el cuaderno; fuente validada con las plantillas oficiales de {", ".join(map(str, val))}: {pct:.1%} de coincidencia)'
        o.write_text('\n'.join([l for l in L if not l.startswith('plantilla: ')] + [lin]) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
