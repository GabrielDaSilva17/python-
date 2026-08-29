"""
LEO Pocket Dictionary & Mobile Face-to-Face Split-Screen Translator - 100% Pure Python FastHTML Application
Supports 2-Person Live Conversation Translation (Person A upside down 180deg / Person B right side up) + Piper TTS + Flexionstabelle.
"""

import os
from fasthtml.common import (
    fast_app, serve, Title, Meta, Main, Div, Span, H1, H2, H3, P, A,
    Button, Form, Input, Textarea, Response, RedirectResponse, FileResponse
)
from starlette.staticfiles import StaticFiles

from components import (
    get_app_styles, get_app_scripts,
    render_leo_navbar, render_search_hero, render_all_category_tables,
    render_flexionstabelle_modal, render_gemini_key_modal,
    render_conversation_split_screen
)
from dictionary import search_leo, get_verb_conjugation
from gemini_helper import explain_word_with_gemini, save_gemini_api_key
from translator import translate_text
from tts_helper import render_piper_audio_player, AUDIO_DIR

# Initialize FastHTML App with 100% Pure Python Header
app, rt = fast_app(
    pico=False,
    hdrs=[
        Meta(charset="UTF-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"),
        Title("LEO Translator ~ Conversação Frente a Frente & Dicionário"),
        get_app_styles(),
        get_app_scripts()
    ]
)

# Mount static directory for 100% reliable static audio & asset serving
os.makedirs(AUDIO_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------------

@rt("/")
def home():
    """Main LEO Dictionary & Face-to-Face Conversation Translator Dashboard."""
    default_results = search_leo("")
    
    return Main(
        render_leo_navbar(),
        Div(
            Div(
                render_search_hero(),
                Div(
                    render_all_category_tables(default_results),
                    id="leo-results-container"
                ),
                id="dictionary-section",
                style="display: block;"
            ),
            render_conversation_split_screen(),
            cls="container"
        ),
        Div(id="flexion-modal-container"),
        render_gemini_key_modal()
    )


@rt("/api/live-translate-speech")
def api_live_translate_speech(person: str, text: str, lang: str = "de"):
    """
    Handles live speech translation for 2-person face-to-face mode:
    - If Person A speaks ('de' or 'en'), translates to 'pt' for Person B & plays Piper PT voice!
    - If Person B speaks ('pt'), translates to 'de' for Person A & plays Piper DE voice!
    """
    if person == "a":
        # Person A (German) spoke -> Translate to Portuguese for Person B
        res = translate_text(text, from_code=lang, to_code="pt")
        translated_text = res.get("translated_text", text) if res["success"] else text
        target_lang = "pt"
        speak_text = translated_text
        div_id = "transcript-person-a"
        sender_title = f"Pessoa A (Ficou registrado em {lang.upper()}):"
    else:
        # Person B (Portuguese) spoke -> Translate to German for Person A
        res = translate_text(text, from_code="pt", to_code="de")
        translated_text = res.get("translated_text", text) if res["success"] else text
        target_lang = "de"
        speak_text = translated_text
        div_id = "transcript-person-b"
        sender_title = "Pessoa B (Ficou registrado em PT):"

    audio_player = render_piper_audio_player(speak_text, target_lang)

    return Div(
        Div(
            P(sender_title, style="font-size: 0.75rem; font-weight: 700; color: var(--text-muted);"),
            P(f'"{text}"', style="font-size: 0.85rem; color: #94a3b8; font-style: italic;"),
            P("Tradução Real:", style="font-size: 0.75rem; font-weight: 700; color: var(--accent-cyan); margin-top: 0.4rem;"),
            P(translated_text, style="font-size: 1.05rem; font-weight: 700; color: var(--text-primary);"),
            audio_player,
            cls="speech-bubble",
            style="margin-bottom: 0.5rem;"
        ),
        id=div_id,
        cls="transcript-box"
    )


@rt("/api/piper-tts")
def api_piper_tts(text: str, lang: str = "de"):
    """Generates real human voice audio file and returns FastHTML Audio Player."""
    return render_piper_audio_player(text, lang)


@rt("/api/search-leo")
def api_search_leo(query: str = "", pair: str = "de-pt"):
    """Live search endpoint for LEO dictionary."""
    results = search_leo(query, pair)
    return render_all_category_tables(results)


@rt("/api/flexion")
def api_flexion(verb: str):
    """Returns German Verb Conjugation Modal (Flexionstabelle)."""
    verb_data = get_verb_conjugation(verb)
    return render_flexionstabelle_modal(verb_data)


@rt("/api/gemini-explain")
def api_gemini_explain(word: str):
    """Generates detailed linguistic explanation using Gemini AI."""
    res = explain_word_with_gemini(word)
    
    if res["success"]:
        return Div(
            Div("✨ Explicação Gemini AI:", style="font-weight: 700; color: var(--accent-gold); margin-bottom: 0.5rem; font-size: 0.85rem;"),
            Div(res["explanation"], style="color: #cbd5e1; font-size: 0.875rem; white-space: pre-wrap; line-height: 1.6;"),
            style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); padding: 1rem; border-radius: var(--radius-md); font-family: var(--font-sans);"
        )
    else:
        return Div(
            Div("📌 Análise do Termo (API Key ausente/inativa):", style="font-weight: 700; color: var(--accent-amber); margin-bottom: 0.5rem; font-size: 0.85rem;"),
            Div(res["explanation"], style="color: #cbd5e1; font-size: 0.85rem; white-space: pre-wrap;"),
            style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); padding: 1rem; border-radius: var(--radius-md);"
        )


@rt("/api/save-gemini-key")
def api_save_gemini_key(gemini_key: str):
    """Saves GEMINI_API_KEY into .env."""
    save_gemini_api_key(gemini_key)
    return RedirectResponse("/", status_code=303)


if __name__ == "__main__":
    serve(port=5001)