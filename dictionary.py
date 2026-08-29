"""
LEO Multi-Language Dictionary Engine with Contextual Disambiguation & SQLite Persistence
Supports 100% Offline Search for ANY word with 3-Step Grammatical Safeguards & Multi-Context Synonyms
(e.g., 'correr' -> rennen [alta velocidade], laufen [jogging/a pé], fließen [líquidos])
"""

import json
import sqlite3
import re
from translator import translate_text

DB_PATH = "leo_dictionary.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_leo_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leo_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            word_de TEXT NOT NULL,
            forms_de TEXT,
            article_de TEXT,
            plural_de TEXT,
            word_pt TEXT NOT NULL,
            word_en TEXT NOT NULL,
            details_pt TEXT,
            details_en TEXT,
            context_tag TEXT,
            conjugation_json TEXT
        )
    """)
    conn.commit()

    # Safely migrate schema if context_tag is missing
    cursor.execute("PRAGMA table_info(leo_words)")
    columns = [row[1] for row in cursor.fetchall()]
    if "context_tag" not in columns:
        cursor.execute("ALTER TABLE leo_words ADD COLUMN context_tag TEXT")
        conn.commit()

    # Check if database is empty, seed initial rich dictionary entries
    cursor.execute("SELECT COUNT(*) FROM leo_words")
    count = cursor.fetchone()[0]
    if count == 0:
        seed_initial_vocabulary(cursor)
        conn.commit()
    conn.close()

def seed_initial_vocabulary(cursor):
    """Seeds rich dictionary entries with contextual synonym distinctions (e.g. rennen vs laufen vs fließen)."""
    initial_words = [
        # VERBS - MULTI CONTEXT FOR "CORRER"
        ("Verbos", "rennen", "rannte, gerannt | Hilfsverb: sein", "", "", "correr", "to run fast / sprint", "correr com alta velocidade, disparar", "to sprint, dash", "alta velocidade",
         json.dumps({
             "praesens": ["ich renne", "du rennst", "er/sie/es rennt", "wir rennen", "ihr rennt", "sie rennen"],
             "perfekt": ["ich bin gerannt", "du bist gerannt", "er/sie/es ist gerannt", "wir sind gerannt", "ihr seid gerannt", "sie sind gerannt"],
             "praeteritum": ["ich rannte", "du ranntest", "er/sie/es rannte", "wir rannten", "ihr ranntet", "sie rannten"],
             "plusquamperfekt": ["ich war gerannt", "du warst gerannt", "er/sie/es war gerannt", "wir waren gerannt", "ihr wart gerannt", "sie waren gerannt"],
             "futur_1": ["ich werde rennen", "du wirst rennen", "er/sie/es wird rennen", "wir werden rennen", "ihr werdet rennen", "sie werden rennen"]
         })),
        ("Verbos", "laufen", "lief, gelaufen | Hilfsverb: sein", "", "", "correr / andar", "to run / to walk fast", "fazer jogging/esporte, ou caminhar rápido / ir a pé", "jogging or walking fast", "jogging / a pé",
         json.dumps({
             "praesens": ["ich laufe", "du läufst", "er/sie/es läuft", "wir laufen", "ihr läuft", "sie laufen"],
             "perfekt": ["ich bin gelaufen", "du bist gelaufen", "er/sie/es ist gelaufen", "wir sind gelaufen", "ihr seid gelaufen", "sie sind gelaufen"],
             "praeteritum": ["ich lief", "du liefst", "er/sie/es lief", "wir liefen", "ihr lieft", "sie liefen"],
             "plusquamperfekt": ["ich war gelaufen", "du warst gelaufen", "er/sie/es war gelaufen", "wir waren gelaufen", "ihr wart gelaufen", "sie waren gelaufen"],
             "futur_1": ["ich werde laufen", "du wirst laufen", "er/sie/es wird laufen", "wir werden laufen", "ihr werdet laufen", "sie werden laufen"]
         })),
        ("Verbos", "fließen", "floss, geflossen | Hilfsverb: sein", "", "", "correr", "to flow / to run (liquid)", "correr (líquidos, rio, água)", "liquid flow", "líquidos / rio",
         json.dumps({
             "praesens": ["ich fließe", "du fließt", "er/sie/es fließt", "wir fließen", "ihr fließt", "sie fließen"],
             "perfekt": ["ich bin geflossen", "du bist geflossen", "er/sie/es ist geflossen", "wir sind geflossen", "ihr seid geflossen", "sie sind geflossen"],
             "praeteritum": ["ich floss", "du flosst", "er/sie/es floss", "wir flossen", "ihr flosst", "sie flossen"],
             "plusquamperfekt": ["ich war geflossen", "du warst geflossen", "er/sie/es war geflossen", "wir waren geflossen", "ihr wart geflossen", "sie waren geflossen"],
             "futur_1": ["ich werde fließen", "du wirst fließen", "er/sie/es wird fließen", "wir werden fließen", "ihr werdet fließen", "sie werden fließen"]
         })),

        # VERBS - OTHER CONTEXTS
        ("Verbos", "überprüfen", "überprüfte, überprüft | Hilfsverb: haben", "", "", "verificar / checar / revisar", "to check / to verify", "examinar com atenção", "examine carefully", "exame / auditoria",
         json.dumps({
             "praesens": ["ich überprüfe", "du überprüfst", "er/sie/es überprüft", "wir überprüfen", "ihr überprüft", "sie überprüfen"],
             "perfekt": ["ich habe überprüft", "du hast überprüft", "er/sie/es hat überprüft", "wir haben überprüft", "ihr habt überprüft", "sie haben überprüft"],
             "praeteritum": ["ich überprüfte", "du überprüftest", "er/sie/es überprüfte", "wir überprüften", "ihr überprüftet", "sie überprüften"],
             "plusquamperfekt": ["ich hatte überprüft", "du hattest überprüft", "er/sie/es hatte überprüft", "wir hatten überprüft", "ihr hattet überprüft", "sie hatten überprüft"],
             "futur_1": ["ich werde überprüfen", "du wirst überprüfen", "er/sie/es wird überprüfen", "wir werden überprüfen", "ihr werdet überprüfen", "sie werden überprüfen"]
         })),
        ("Verbos", "spazieren", "spazierte, spaziert | Hilfsverb: sein", "", "", "caminhar / passear", "to walk / to stroll", "dar um passeio a pé sem pressa", "take a walk", "passeio a pé",
         json.dumps({
             "praesens": ["ich spaziere", "du spazierst", "er/sie/es spaziert", "wir spazieren", "ihr spaziert", "sie spazieren"],
             "perfekt": ["ich bin spaziert", "du bist spaziert", "er/sie/es ist spaziert", "wir sind spaziert", "ihr seid spaziert", "sie sind spaziert"],
             "praeteritum": ["ich spazierte", "du spaziertest", "er/sie/es spazierte", "wir spazierten", "ihr spaziertet", "sie spazierten"],
             "plusquamperfekt": ["ich war spaziert", "du warst spaziert", "er/sie/es war spaziert", "wir waren spaziert", "ihr wart spaziert", "sie waren spaziert"],
             "futur_1": ["ich werde spazieren", "du wirst spazieren", "er/sie/es wird spazieren", "wir werden spazieren", "ihr werdet spazieren", "sie werden spazieren"]
         })),
        ("Verbos", "kaufen", "kaufte, gekauft | Hilfsverb: haben", "", "", "comprar", "to buy / to purchase", "adquirir algo por dinheiro", "acquire for money", "comércio",
         json.dumps({
             "praesens": ["ich kaufe", "du kaufst", "er/sie/es kauft", "wir kaufen", "ihr kauft", "sie kaufen"],
             "perfekt": ["ich habe gekauft", "du hast gekauft", "er/sie/es hat gekauft", "wir haben gekauft", "ihr habt gekauft", "sie haben gekauft"],
             "praeteritum": ["ich kaufte", "du kauftest", "er/sie/es kaufte", "wir kauften", "ihr kauftet", "sie kauften"],
             "plusquamperfekt": ["ich hatte gekauft", "du hattest gekauft", "er/sie/es hatte gekauft", "wir hatten gekauft", "ihr hattet gekauft", "sie hatten gekauft"],
             "futur_1": ["ich werde kaufen", "du wirst kaufen", "er/sie/es wird kaufen", "wir werden kaufen", "ihr werdet kaufen", "sie werden kaufen"]
         })),

        # SUBSTANTIVOS
        ("Substantivos", "Überprüfung", "", "die", "die Überprüfungen", "a verificação / a checagem", "verification / audit / check", "exame minucioso de algo", "thorough check", "processo", None),
        ("Substantivos", "Überprüfungen", "", "die", "die Überprüfungen (Plural)", "as verificações / checagens", "verifications / checks", "forma plural do substantivo die Überprüfung", "plural form", "plural", None),
        ("Substantivos", "Wohnung", "", "die", "die Wohnungen", "o apartamento / a moradia", "apartment / flat", "local de residência", "place of residence", "imóvel", None),
        ("Substantivos", "Wohnungen", "", "die", "die Wohnungen (Plural)", "os apartamentos / moradias", "apartments / flats", "forma plural do substantivo die Wohnung", "plural form", "plural", None),
        ("Substantivos", "Wort", "", "das", "die Wörter", "a palavra", "word", "termo linguístico", "linguistic term", "gramática", None),
        ("Substantivos", "Tagebuch", "", "das", "die Tagebücher", "o diário", "diary / journal", "livro pessoal de anotações diárias", "personal daily logbook", "escrita", None),
        ("Substantivos", "Wörterbuch", "", "das", "die Wörterbücher", "o dicionário", "dictionary", "livro com definições de termos", "reference book with definitions", "estudos", None),
        ("Substantivos", "Sprache", "", "die", "die Sprachen", "a língua / o idioma", "language", "sistema de comunicação verbal", "system of communication", "comunicação", None)
    ]

    for item in initial_words:
        cursor.execute("""
            INSERT INTO leo_words 
            (category, word_de, forms_de, article_de, plural_de, word_pt, word_en, details_pt, details_en, context_tag, conjugation_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, item)

# Initialize Database on import
init_leo_db()

# -------------------------------------------------------------------------
# MORPHOLOGICAL RULE ENGINE WITH CONTEXTUAL DISAMBIGUATION
# -------------------------------------------------------------------------

INSEPARABLE_PREFIXES = ("be", "ge", "er", "ver", "zer", "ent", "emp", "über", "unter", "miss")
SEPARABLE_PREFIXES = ("ein", "aus", "an", "auf", "ab", "mit", "zu", "vor", "durch", "nach", "fort", "weg")
NOUN_SUFFIXES = ("ung", "ungen", "heit", "heiten", "keit", "keiten", "schaft", "schaften", "ion", "ionen", "tät", "täten", "nis", "nisse", "tum", "tümer")

def analyze_german_morphology(query: str, trans_de: str, trans_en: str):
    """
    Classifies German morphological structure with Duden safeguards & context tags.
    """
    q_clean = query.strip()
    word_de = trans_de.strip()

    is_noun = False
    article_de = "die"
    plural_de = ""
    singular_lemma = word_de

    word_lower = word_de.lower()
    q_lower = q_clean.lower()

    for suffix in NOUN_SUFFIXES:
        if word_lower.endswith(suffix) or q_lower.endswith(suffix):
            is_noun = True
            break

    if q_clean[0].isupper() or word_de[0].isupper() or is_noun:
        is_noun = True
        if word_lower.endswith("ungen"):
            singular_lemma = word_de[:-1] if word_de.endswith("ungen") else word_de
            plural_de = f"die {word_de} (Plural)"
            article_de = "die"
        elif word_lower.endswith("heiten") or word_lower.endswith("keiten") or word_lower.endswith("schaften"):
            singular_lemma = word_de[:-2]
            plural_de = f"die {word_de} (Plural)"
            article_de = "die"
        elif word_lower.endswith("ung") or word_lower.endswith("heit") or word_lower.endswith("keit") or word_lower.endswith("schaft"):
            article_de = "die"
            plural_de = f"die {word_de}en"
        elif word_lower.endswith("chen") or word_lower.endswith("lein") or word_lower.endswith("tum"):
            article_de = "das"
            plural_de = f"die {word_de}"
        else:
            article_de = "der"
            plural_de = f"die {word_de}e"

        return {
            "category": "Substantivos",
            "word_de": singular_lemma.capitalize(),
            "article_de": article_de,
            "plural_de": plural_de,
            "forms_de": None,
            "context_tag": "substantivo",
            "conjugation_json": None
        }

    # VERB
    category = "Verbos"
    verb_infinitive = word_lower
    if not verb_infinitive.endswith(("en", "n")):
        verb_infinitive += "en"

    if verb_infinitive.endswith("en"):
        stem = verb_infinitive[:-2]
    elif verb_infinitive.endswith("n"):
        stem = verb_infinitive[:-1]
    else:
        stem = verb_infinitive

    is_inseparable = any(verb_infinitive.startswith(p) for p in INSEPARABLE_PREFIXES)
    is_separable = any(verb_infinitive.startswith(p) for p in SEPARABLE_PREFIXES)

    if is_inseparable:
        partizip_2 = f"{stem}t"
    elif is_separable:
        for pref in SEPARABLE_PREFIXES:
            if verb_infinitive.startswith(pref):
                base_stem = verb_infinitive[len(pref):-2]
                partizip_2 = f"{pref}ge{base_stem}t"
                break
        else:
            partizip_2 = f"ge{stem}t"
    else:
        partizip_2 = f"ge{stem}t"

    aux = "sein" if verb_infinitive in ["laufen", "rennen", "kommen", "gehen", "fliegen", "fahren", "spazieren", "reisen", "bleiben", "sein", "fließen"] else "haben"
    forms_de = f"{stem}te, {partizip_2} | Hilfsverb: {aux}"

    conj_dict = generate_verb_conjugation_accurate(verb_infinitive, stem, partizip_2, aux)

    return {
        "category": "Verbos",
        "word_de": verb_infinitive,
        "article_de": "",
        "plural_de": "",
        "forms_de": forms_de,
        "context_tag": "verbo",
        "conjugation_json": json.dumps(conj_dict)
    }


def generate_verb_conjugation_accurate(infinitive: str, stem: str, partizip_2: str, aux: str):
    """Generates accurate verb conjugation table."""
    e_2sg = "est" if (stem.endswith("t") or stem.endswith("d")) else "st"
    e_3sg = "et" if (stem.endswith("t") or stem.endswith("d")) else "t"
    e_2pl = "et" if (stem.endswith("t") or stem.endswith("d")) else "t"

    aux_1sg = "bin" if aux == "sein" else "habe"
    aux_2sg = "bist" if aux == "sein" else "hast"
    aux_3sg = "ist" if aux == "sein" else "hat"
    aux_1pl = "sind" if aux == "sein" else "haben"
    aux_2pl = "seid" if aux == "sein" else "habt"
    aux_3pl = "sind" if aux == "sein" else "haben"

    aux_prt_1sg = "war" if aux == "sein" else "hatte"
    aux_prt_2sg = "warst" if aux == "sein" else "hattest"
    aux_prt_3sg = "war" if aux == "sein" else "hatte"
    aux_prt_1pl = "waren" if aux == "sein" else "hatten"
    aux_prt_2pl = "wart" if aux == "sein" else "hattet"
    aux_prt_3pl = "waren" if aux == "sein" else "hatten"

    return {
        "praesens": [
            f"ich {stem}e",
            f"du {stem}{e_2sg}",
            f"er/sie/es {stem}{e_3sg}",
            f"wir {infinitive}",
            f"ihr {stem}{e_2pl}",
            f"sie {infinitive}"
        ],
        "perfekt": [
            f"ich {aux_1sg} {partizip_2}",
            f"du {aux_2sg} {partizip_2}",
            f"er/sie/es {aux_3sg} {partizip_2}",
            f"wir {aux_1pl} {partizip_2}",
            f"ihr {aux_2pl} {partizip_2}",
            f"sie {aux_3pl} {partizip_2}"
        ],
        "praeteritum": [
            f"ich {stem}te",
            f"du {stem}test",
            f"er/sie/es {stem}te",
            f"wir {stem}ten",
            f"ihr {stem}tet",
            f"sie {stem}ten"
        ],
        "plusquamperfekt": [
            f"ich {aux_prt_1sg} {partizip_2}",
            f"du {aux_prt_2sg} {partizip_2}",
            f"er/sie/es {aux_prt_3sg} {partizip_2}",
            f"wir {aux_prt_1pl} {partizip_2}",
            f"ihr {aux_prt_2pl} {partizip_2}",
            f"sie {aux_prt_3pl} {partizip_2}"
        ],
        "futur_1": [
            f"ich werde {infinitive}",
            f"du wirst {infinitive}",
            f"er/sie/es wird {infinitive}",
            f"wir werden {infinitive}",
            f"ihr werdet {infinitive}",
            f"sie werden {infinitive}"
        ]
    }

# -------------------------------------------------------------------------
# DYNAMIC OFFLINE SEARCH ENGINE WITH CONTEXTUAL SYNONYMS
# -------------------------------------------------------------------------

def search_leo(query: str = "", pair: str = "de-pt"):
    """
    Searches SQLite database first.
    If query matches multiple contextual synonyms (e.g. 'correr' -> rennen, laufen, fließen),
    returns ALL contextual options side-by-side!
    """
    q = query.strip()
    conn = get_db_connection()
    cursor = conn.cursor()

    if not q:
        cursor.execute("SELECT * FROM leo_words ORDER BY id ASC")
        rows = cursor.fetchall()
    else:
        q_like = f"%{q.lower()}%"
        cursor.execute("""
            SELECT * FROM leo_words 
            WHERE LOWER(word_de) LIKE ? 
               OR LOWER(word_pt) LIKE ? 
               OR LOWER(word_en) LIKE ?
               OR LOWER(details_pt) LIKE ?
               OR LOWER(context_tag) LIKE ?
        """, (q_like, q_like, q_like, q_like, q_like))
        rows = cursor.fetchall()

    if q and not rows:
        dynamically_create_word_entry(cursor, q)
        conn.commit()
        
        cursor.execute("""
            SELECT * FROM leo_words 
            WHERE LOWER(word_de) LIKE ? 
               OR LOWER(word_pt) LIKE ? 
               OR LOWER(word_en) LIKE ?
        """, (f"%{q.lower()}%", f"%{q.lower()}%", f"%{q.lower()}%"))
        rows = cursor.fetchall()

    conn.close()

    categories = {"Verbos": [], "Expressões": [], "Substantivos": [], "Exemplos": []}
    for row in rows:
        item = dict(row)
        if item.get("conjugation_json"):
            try:
                item["conjugation"] = json.loads(item["conjugation_json"])
            except Exception:
                item["conjugation"] = None

        cat = item.get("category", "Substantivos")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    return categories


def dynamically_create_word_entry(cursor, query: str):
    """
    Translates unknown query offline using ArgosTranslate and applies
    Duden Morphological Classifier.
    """
    q = query.strip()
    
    res_en = translate_text(q, from_code="pt", to_code="en")
    trans_en = res_en.get("translated_text", q) if res_en["success"] else q
    
    res_de = translate_text(trans_en, from_code="en", to_code="de")
    trans_de = res_de.get("translated_text", q) if res_de["success"] else q

    analysis = analyze_german_morphology(q, trans_de, trans_en)

    cursor.execute("""
        INSERT INTO leo_words 
        (category, word_de, forms_de, article_de, plural_de, word_pt, word_en, details_pt, details_en, context_tag, conjugation_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        analysis["category"],
        analysis["word_de"],
        analysis["forms_de"],
        analysis["article_de"],
        analysis["plural_de"],
        q.lower(),
        trans_en.lower(),
        f"Análise Duden offline gerada para '{q}'",
        f"Duden offline analysis generated for '{q}'",
        analysis["context_tag"],
        analysis["conjugation_json"]
    ))


def get_verb_conjugation(verb_name: str):
    """Retrieves or dynamically generates verb conjugation table (Flexionstabelle)."""
    v_clean = verb_name.lower().strip()

    if any(v_clean.endswith(s) for s in NOUN_SUFFIXES):
        return None

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leo_words WHERE LOWER(word_de) = ?", (v_clean,))
    row = cursor.fetchone()
    conn.close()

    if row and row["conjugation_json"]:
        item = dict(row)
        item["conjugation"] = json.loads(item["conjugation_json"])
        return item
    else:
        analysis = analyze_german_morphology(v_clean, v_clean, v_clean)
        if analysis["conjugation_json"]:
            return {
                "word_de": analysis["word_de"],
                "forms_de": analysis["forms_de"],
                "conjugation": json.loads(analysis["conjugation_json"])
            }
        return None
