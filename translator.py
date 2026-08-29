"""
ArgosTranslate Offline Translation Helper Module with Idiomatic Context Engine
Provides seamless 100% offline translation using installed model packages,
enhanced with Speech-to-Text typo correction and natural German/Portuguese idiomatic expressions.
"""

import sys
import re
import logging
from gemini_helper import get_gemini_api_key

logger = logging.getLogger(__name__)

_ARGOS_AVAILABLE = False
try:
    import argostranslate.package
    import argostranslate.translate
    _ARGOS_AVAILABLE = True
except ImportError:
    _ARGOS_AVAILABLE = False

# -------------------------------------------------------------------------
# IDIOMATIC PHRASE DICTIONARY & STT CORRECTIONS
# -------------------------------------------------------------------------

PT_TYPO_CORRECTIONS = [
    (r"\bdemais alguma coisa\b", "de mais alguma coisa"),
    (r"\bgostaria demais alguma coisa\b", "gostaria de mais alguma coisa"),
    (r"\bgostaria demais\b", "gostaria de mais"),
    (r"\bmais alguma coisa\b", "mais alguma coisa"),
]

IDIOMATIC_EXPRESSIONS_PT_TO_DE = [
    (r"gostaria (?:de )?mais alguma coisa\??", "Möchten Sie sonst noch etwas?"),
    (r"você gostaria (?:de )?mais alguma coisa\??", "Möchten Sie sonst noch etwas?"),
    (r"mais alguma coisa\??", "Sonst noch etwas?"),
    (r"deseja algo mais\??", "Möchten Sie sonst noch etwas?"),
    (r"muito obrigado", "Vielen Dank!"),
    (r"de nada", "Bitte schön!"),
    (r"bom dia", "Guten Tag!"),
    (r"boa tarde", "Guten Tag!"),
    (r"boa noite", "Guten Abend!"),
    (r"com licença", "Entschuldigung!")
]

def check_argos_status():
    """Checks if ArgosTranslate is imported and returns status + installed languages."""
    if not _ARGOS_AVAILABLE:
        return {
            "available": False,
            "installed_languages": [],
            "message": "Biblioteca ArgosTranslate não encontrada."
        }
    
    try:
        installed_languages = argostranslate.translate.get_installed_languages()
        lang_codes = [lang.code for lang in installed_languages]
        return {
            "available": True,
            "installed_languages": lang_codes,
            "message": f"ArgosTranslate pronto offline. Idiomas instalados: {', '.join(lang_codes) if lang_codes else 'Nenhum pacote instalado ainda'}"
        }
    except Exception as e:
        return {
            "available": False,
            "installed_languages": [],
            "message": f"Erro ao inicializar ArgosTranslate: {str(e)}"
        }


def preprocess_speech_text(text: str, lang: str = "pt") -> str:
    """Fixes common speech-to-text typos (e.g. 'demais alguma coisa' -> 'de mais alguma coisa')."""
    if not text:
        return text

    clean_text = text.strip()
    if lang == "pt":
        for pattern, replacement in PT_TYPO_CORRECTIONS:
            clean_text = re.sub(pattern, replacement, clean_text, flags=re.IGNORECASE)
            
    return clean_text


def translate_text(text: str, from_code: str = "en", to_code: str = "pt") -> dict:
    """
    Translates text from source language to target language.
    Applies idiomatic phrase corrections (e.g. 'gostaria de mais alguma coisa' -> 'Möchten Sie sonst noch etwas?').
    """
    if not text or not text.strip():
        return {"success": False, "error": "Texto vazio.", "translated_text": ""}

    # 1. Clean up STT typos
    clean_input = preprocess_speech_text(text, from_code)

    # 2. Check Idiomatic Dictionary for direct 100% natural translation
    if from_code == "pt" and to_code == "de":
        # Check if text contains prices e.g. "1,75 você gostaria de mais alguma coisa"
        price_match = re.search(r"(\d+[\,\.]\d{2})", clean_input)
        price_str = price_match.group(1).replace(",", ".") if price_match else ""

        for pattern, idiom_de in IDIOMATIC_EXPRESSIONS_PT_TO_DE:
            if re.search(pattern, clean_input, re.IGNORECASE):
                if price_str:
                    final_translated = f"{price_str} €. {idiom_de}"
                else:
                    final_translated = idiom_de
                    
                return {
                    "success": True,
                    "translated_text": final_translated,
                    "error": None
                }

    if not _ARGOS_AVAILABLE:
        return {
            "success": False,
            "error": "ArgosTranslate não está disponível.",
            "translated_text": clean_input
        }

    try:
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = next((l for l in installed_languages if l.code == from_code), None)
        to_lang = next((l for l in installed_languages if l.code == to_code), None)

        if not from_lang or not to_lang:
            return {
                "success": False,
                "error": f"Pacote de idiomas '{from_code}' -> '{to_code}' não instalado localmente.",
                "translated_text": clean_input,
                "requires_download": True
            }

        translation = from_lang.get_translation(to_lang)
        result = translation.translate(clean_input)

        # Post-process literal translation bugs in German
        if to_code == "de":
            result = result.replace("etwas zu viel?", "sonst noch etwas?")
            result = result.replace("gostaria demais", "möchten Sie sonst noch etwas")

        return {
            "success": True,
            "translated_text": result,
            "error": None
        }
    except Exception as e:
        logger.error(f"Erro na tradução: {e}")
        return {
            "success": False,
            "error": str(e),
            "translated_text": clean_input
        }
