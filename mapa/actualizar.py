#!/usr/bin/env python3
"""Capa 1 del mapa (automática, sin Claude).

Lee todo diario/, cuenta palabras y frases que se repiten y cuáles aparecen
juntas en un mismo pensamiento. Escribe:
  - mapa/palabras.json        (se guarda en el repo)
  - mapa/.export/*.json       (archivos listos para cargar en la página; no se suben)
Nunca toca diario/.
"""
import json, os, re, sys, unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations
from zoneinfo import ZoneInfo

RAIZ = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIARIO = os.path.join(RAIZ, "diario")
MAPA = os.path.join(RAIZ, "mapa")
EXPORT = os.path.join(MAPA, ".export")

STOP = set("""
a al algo algun alguna algunas alguno algunos ante antes aqui asi aun aunque bastante bien cada casi como con contra cual
cuales cualquier cuando cuanto de del desde donde dos el ella ellas ello ellos en entonces entre era eramos eran eras eres es
esa esas ese eso esos esta estaba estaban estabamos estamos estan estar estas este esto estos estoy fue fueron fui fuimos ha
habia habian han has hasta hay he hemos hice hizo igual la las le les lo los mas me mi mia mias mio mios mis mucho muchos muy
nada ni no nos nosotros o otra otras otro otros para pero poco por porque pues que quien quienes se sea sean ser si sido
siempre sin sobre solo son soy su sus tal tambien tan tanto te tenia tengo ti tiene tienen todo todos tu tus un una unas uno
unos usted vos y ya yo
che bueno boludo nose sea osea medio capaz digamos tipo onda viste sabes entendes ahi aca alla ok dale tipo cosa cosas vez veces
hacer hago hace hacen haces dije dice decis digo decir creo pienso siento sentia parece puede puedo podes ver veo ves voy va van
ir estar estuve estado tener tenes tenemos tuve hoy ahora despues luego mismo misma todavia nunca alguien nadie toda todas
cuenta parte forma manera momento algo onda bastante ganas lado tema
supongo quiero queria quiere queres tenga sabe sabia pasa pasaba paso pasan dentro varios literalmente acuerdo acuerdas seguro
principio realidad verdad tenido estan sido medio mucha muchas gente mientras tipo hecho""".split())

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def leer_entradas():
    entradas = []  # (fecha, hora, texto)
    if not os.path.isdir(DIARIO):
        return entradas
    for nombre in sorted(os.listdir(DIARIO)):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", nombre):
            continue
        fecha = nombre[:-3]
        texto = open(os.path.join(DIARIO, nombre), encoding="utf-8").read()
        partes = re.split(r"^## (\d{2}:\d{2})\s*$", texto, flags=re.M)
        for i in range(1, len(partes) - 1, 2):
            cuerpo = partes[i + 1].strip()
            if cuerpo:
                entradas.append((fecha, partes[i], cuerpo))
    return entradas

CLITICO = re.compile(r"^(.{3,}(?:ar|er|ir))(?:lo|la|los|las|le|les|me|se|nos)$")

def base(n):
    m = CLITICO.match(n)
    return m.group(1) if m else n

def tokens(texto):
    # conserva la forma original para mostrar; compara normalizado
    return re.findall(r"[a-záéíóúüñ]+", texto.lower())

def terminos_de(texto):
    toks = tokens(texto)
    ns = [base(norm(t)) for t in toks]
    # si se sacó un pronombre pegado ("cerrarlo"), se muestra el verbo ("cerrar")
    toks = [n if n != norm(t) else t for t, n in zip(toks, ns)]
    vistos = {}
    for i, n in enumerate(ns):
        if len(n) >= 4 and n not in STOP:
            vistos.setdefault(n, toks[i])
    # frases de 2-3 palabras que empiezan y terminan en palabra con contenido
    for largo in (2, 3):
        for i in range(len(ns) - largo + 1):
            seg = ns[i:i + largo]
            if seg[0] in STOP or seg[-1] in STOP or len(seg[0]) < 3 or len(seg[-1]) < 3:
                continue
            if largo == 3 and seg[1] not in ("de", "del", "a", "al", "y", "en", "con"):
                continue
            vistos.setdefault(" ".join(seg), " ".join(toks[i:i + largo]))
    return vistos  # normalizado -> forma visible

def main():
    entradas = leer_entradas()
    por_termino = defaultdict(list)
    forma = {}
    for fecha, hora, texto in entradas:
        for n, vis in terminos_de(texto).items():
            por_termino[n].append(f"{fecha} {hora}")
            forma.setdefault(n, vis)

    # palabras sueltas: desde 2 apariciones; frases: desde 2 apariciones
    terminos = [(n, refs) for n, refs in por_termino.items() if len(refs) >= 2]
    terminos.sort(key=lambda x: (-len(x[1]), x[0]))
    # si una frase aparece igual de seguido que su palabra, igual se muestran las dos
    top = terminos[:150]
    top_set = {n for n, _ in top}

    pares = Counter()
    for fecha, hora, texto in entradas:
        presentes = sorted(set(terminos_de(texto)) & top_set)
        for a, b in combinations(presentes, 2):
            if a in b or b in a:  # "ritual" dentro de "abrir el ritual"
                continue
            pares[(a, b)] += 1

    ahora = datetime.now(ZoneInfo("America/Argentina/Mendoza")).strftime("%Y-%m-%d %H:%M")
    palabras = {
        "generado": ahora,
        "total_entradas": len(entradas),
        "terminos": [{"id": n, "t": forma[n], "n": len(refs), "entradas": refs} for n, refs in top],
        "pares": [[a, b, c] for (a, b), c in pares.most_common(400) if c >= 2],
    }
    os.makedirs(MAPA, exist_ok=True)
    with open(os.path.join(MAPA, "palabras.json"), "w", encoding="utf-8") as f:
        json.dump(palabras, f, ensure_ascii=False, indent=1)

    # export para la página
    os.makedirs(EXPORT, exist_ok=True)
    with open(os.path.join(EXPORT, "palabras.json"), "w", encoding="utf-8") as f:
        json.dump(palabras, f, ensure_ascii=False)
    cpath = os.path.join(MAPA, "conceptos.json")
    if os.path.exists(cpath):
        with open(cpath, encoding="utf-8") as f, open(os.path.join(EXPORT, "conceptos.json"), "w", encoding="utf-8") as g:
            json.dump(json.load(f), g, ensure_ascii=False)
    dias = defaultdict(list)
    for fecha, hora, texto in entradas:
        dias[fecha].append({"hora": hora, "texto": texto})
    for fecha, lista in dias.items():
        with open(os.path.join(EXPORT, f"dia-{fecha}.json"), "w", encoding="utf-8") as f:
            json.dump({"fecha": fecha, "entradas": lista}, f, ensure_ascii=False)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # nunca bloquear la sesión
        print(f"mapa/actualizar.py falló: {e}", file=sys.stderr)
    sys.exit(0)
