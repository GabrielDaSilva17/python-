"""
100% Pure Python FastHTML UI Components - LEO Multi-Language Dictionary & Mobile Split-Screen Face-to-Face Translator
No HTML, CSS, or JS files - Everything rendered directly via FastHTML!
Supports Mobile Face-to-Face 2-Person Live Voice Translation (Person A upside down 180deg / Person B right side up) + Piper TTS + Flexionstabelle.
"""

from fasthtml.common import (
    Div, Span, H1, H2, H3, H4, P, A, Button, Form, Input, Textarea, Select, Option,
    Pre, Code, Header, Nav, Footer, Label, Table, Tr, Th, Td, Tbody, Thead, Style, Script, ft
)
from dictionary import search_leo, get_verb_conjugation
from gemini_helper import get_gemini_api_key

# -------------------------------------------------------------------------
# PURE PYTHON CSS DESIGN SYSTEM
# -------------------------------------------------------------------------

def get_app_styles():
    """Returns FastHTML Style element with LEO.org Inspired Theme & Mobile Split-Screen Translator."""
    return Style("""
        :root {
            --bg-dark: #0a0e17;
            --bg-card: #121929;
            --bg-table-header: #1a233a;
            --bg-table-row: #0f1624;
            --bg-table-alt: #141c2e;
            
            --border-color: rgba(255, 255, 255, 0.08);
            --border-leo: rgba(245, 158, 11, 0.4);
            --border-highlight: rgba(99, 102, 241, 0.4);
            
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            
            --accent-amber: #f59e0b;
            --accent-gold: #fbbf24;
            --accent-cyan: #06b6d4;
            --accent-indigo: #6366f1;
            --accent-emerald: #10b981;
            --accent-pink: #ec4899;

            --gradient-leo: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            --gradient-card: linear-gradient(180deg, #121929 0%, #0c121e 100%);
            --gradient-person-a: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            --gradient-person-b: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);

            --font-sans: 'Poppins', 'Montserrat', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --font-mono: 'IBM Plex Mono', 'Fira Code', monospace;

            --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 14px;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background-color: var(--bg-dark);
            color: var(--text-primary);
            font-family: var(--font-sans);
            line-height: 1.6;
            min-height: 100vh;
            background-image: radial-gradient(at 0% 0%, rgba(245, 158, 11, 0.08) 0px, transparent 50%);
        }

        .container {
            width: 100%;
            max-width: 1280px;
            margin: 0 auto;
            padding: 1rem;
        }

        /* LEO Navbar */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.85rem 1.25rem;
            background: rgba(18, 25, 41, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            margin-bottom: 1.5rem;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: var(--text-primary);
        }

        .brand-logo {
            width: 40px;
            height: 40px;
            background: var(--gradient-leo);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 1.1rem;
            color: #000;
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
        }

        .brand-title { font-size: 1.25rem; font-weight: 800; color: var(--accent-amber); }
        .brand-subtitle { font-size: 0.7rem; color: var(--text-secondary); }

        .nav-actions { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }

        .mode-tab-btn {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
            padding: 0.4rem 0.85rem;
            border-radius: var(--radius-md);
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        .mode-tab-btn.active {
            background: var(--accent-amber);
            color: #000;
            border-color: var(--accent-amber);
            font-weight: 700;
        }

        /* 📱 MOBILE SPLIT-SCREEN FACE-TO-FACE CONVERSATION LAYOUT */
        .split-screen-container {
            display: flex;
            flex-direction: column;
            height: calc(100vh - 120px);
            min-height: 580px;
            max-width: 500px;
            margin: 0 auto;
            border: 2px solid var(--accent-amber);
            border-radius: 24px;
            overflow: hidden;
            background: #090d16;
            box-shadow: var(--shadow-lg);
            position: relative;
        }

        /* Top Half: Person A (Rotated 180 degrees) */
        .person-a-screen {
            flex: 1;
            transform: rotate(180deg);
            background: var(--gradient-person-a);
            border-bottom: 2px solid rgba(245, 158, 11, 0.3);
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        /* Bottom Half: Person B (Normal orientation 0deg) */
        .person-b-screen {
            flex: 1;
            background: var(--gradient-person-b);
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        /* Center Divider Bar */
        .conversation-divider {
            height: 32px;
            background: var(--accent-amber);
            color: #000;
            font-size: 0.75rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .person-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .person-label { font-size: 0.85rem; font-weight: 700; display: flex; align-items: center; gap: 0.4rem; }

        .transcript-box {
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 0.85rem;
            flex: 1;
            margin: 0.75rem 0;
            overflow-y: auto;
            font-size: 0.9rem;
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        .speech-bubble {
            background: rgba(255, 255, 255, 0.08);
            padding: 0.5rem 0.75rem;
            border-radius: var(--radius-md);
            font-size: 0.875rem;
        }
        .speech-translated {
            color: var(--accent-cyan);
            font-weight: 600;
            font-size: 0.95rem;
        }

        .talk-btn-large {
            width: 100%;
            padding: 0.85rem;
            border-radius: var(--radius-md);
            font-size: 0.95rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            cursor: pointer;
            border: none;
            transition: transform 0.15s, box-shadow 0.15s;
        }
        .talk-btn-person-a {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        }
        .talk-btn-person-b {
            background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        }
        .talk-btn-large:active { transform: scale(0.97); }

        /* Search Section */
        .search-hero {
            background: var(--gradient-card);
            border: 1px solid var(--border-leo);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-lg);
        }

        .search-box-large { display: flex; gap: 0.75rem; margin-top: 1rem; }

        .search-input-large {
            flex: 1;
            padding: 0.75rem 1rem;
            background: rgba(9, 13, 22, 0.9);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            color: var(--text-primary);
            font-size: 1rem;
            outline: none;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.4rem;
            padding: 0.55rem 1rem;
            font-size: 0.85rem;
            font-weight: 600;
            border-radius: var(--radius-md);
            border: 1px solid transparent;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            font-family: inherit;
        }

        .btn-leo { background: var(--gradient-leo); color: #000; font-weight: 700; }
        .btn-secondary { background: rgba(255, 255, 255, 0.05); color: var(--text-primary); border-color: var(--border-color); }
        .btn-emerald { background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); border-color: rgba(16, 185, 129, 0.3); }
        .btn-sm { padding: 0.3rem 0.6rem; font-size: 0.75rem; }

        .leo-cat-block { margin-bottom: 2rem; }
        .leo-cat-header {
            background: var(--accent-amber);
            color: #000;
            font-size: 0.9rem;
            font-weight: 800;
            padding: 0.5rem 1rem;
            border-radius: var(--radius-md) var(--radius-md) 0 0;
            text-transform: uppercase;
        }

        .leo-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 0 0 var(--radius-md) var(--radius-md);
        }
        .leo-table tr { border-bottom: 1px solid var(--border-color); }
        .leo-table td { padding: 0.75rem 1rem; vertical-align: middle; }

        .col-left { width: 50%; color: var(--text-primary); }
        .col-right { width: 50%; color: var(--accent-cyan); font-weight: 600; }

        .term-de { font-weight: 700; color: #38bdf8; }
        .forms-de { font-size: 0.8rem; color: var(--text-muted); font-weight: 400; margin-left: 0.4rem; }
        .article-tag { font-size: 0.75rem; font-weight: 700; padding: 0.1rem 0.4rem; border-radius: var(--radius-sm); margin-right: 0.4rem; }
        .art-das { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
        .art-die { background: rgba(236, 72, 153, 0.2); color: #f472b6; }
        .art-der { background: rgba(16, 185, 129, 0.2); color: #34d399; }

        .context-pill {
            display: inline-flex;
            align-items: center;
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent-amber);
            border: 1px solid rgba(245, 158, 11, 0.3);
            padding: 0.15rem 0.5rem;
            border-radius: var(--radius-sm);
            font-size: 0.75rem;
            font-weight: 700;
            margin-left: 0.4rem;
        }

        .row-actions { display: flex; gap: 0.4rem; margin-top: 0.4rem; flex-wrap: wrap; }

        .modal-overlay {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(8px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999;
            padding: 1rem;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.25s ease;
        }
        .modal-overlay.active { opacity: 1; pointer-events: auto; }

        .flexion-box {
            background: #111827;
            border: 2px solid var(--accent-amber);
            border-radius: var(--radius-lg);
            width: 100%;
            max-width: 950px;
            padding: 1.5rem;
            max-height: 90vh;
            overflow-y: auto;
        }

        .flexion-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .tense-card {
            background: rgba(17, 24, 39, 0.8);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 0.85rem;
        }

        .tense-title {
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--accent-amber);
            text-transform: uppercase;
            margin-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-color);
        }

        .tense-item { font-family: var(--font-mono); font-size: 0.8rem; padding: 0.15rem 0; color: #cbd5e1; }
        .tense-item strong { color: #f43f5e; }

        @media (max-width: 768px) {
            .navbar { flex-direction: column; align-items: stretch; gap: 0.75rem; }
            .split-screen-container { max-width: 100%; height: calc(100vh - 140px); }
        }
    """)


# -------------------------------------------------------------------------
# PURE PYTHON JAVASCRIPT LOGIC
# -------------------------------------------------------------------------

def get_app_scripts():
    """Returns FastHTML Script element with Speech Recognition + Speech Synthesis handlers."""
    return Script("""
        function playTTS(text, lang) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = lang || 'de-DE';
                utterance.rate = 0.85;
                window.speechSynthesis.speak(utterance);
                showToast('🔊 Pronúncia em ' + lang + ': ' + text);
            } else {
                showToast('⚠️ Síntese de voz não suportada.', 'error');
            }
        }

        function triggerSpeechRecognition(person, lang) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                showToast('⚠️ Seu navegador não suporta entrada por microfone. Digite a frase.', 'error');
                const promptText = prompt('Digite sua frase (' + lang + '):');
                if (promptText) {
                    processSpeechInput(person, promptText, lang);
                }
                return;
            }

            const recognition = new SpeechRecognition();
            recognition.lang = lang === 'de' ? 'de-DE' : (lang === 'pt' ? 'pt-BR' : 'en-US');
            recognition.interimResults = false;

            showToast('🎙️ Ouvindo (' + recognition.lang + ')... Fale agora!');

            recognition.onresult = function(event) {
                const text = event.results[0][0].transcript;
                showToast('Entendido: "' + text + '"');
                processSpeechInput(person, text, lang);
            };

            recognition.onerror = function(event) {
                console.error('Speech error:', event.error);
                showToast('Erro no microfone: ' + event.error, 'error');
            };

            recognition.start();
        }

        function processSpeechInput(person, text, lang) {
            const targetDiv = person === 'a' ? '#transcript-person-a' : '#transcript-person-b';
            htmx.ajax('POST', '/api/live-translate-speech', {
                target: targetDiv,
                swap: 'outerHTML',
                values: { person: person, text: text, lang: lang }
            });
        }

        function showToast(message, type = 'success') {
            let container = document.getElementById('toast-container');
            if (!container) {
                container = document.createElement('div');
                container.id = 'toast-container';
                container.className = 'toast-container';
                document.body.appendChild(container);
            }

            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.innerHTML = message;
            container.appendChild(toast);

            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(10px)';
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }

        function openModal(modalId) {
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        }

        function closeModal(modalId) {
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        }

        function switchAppTab(tabName) {
            const dictSec = document.getElementById('dictionary-section');
            const convSec = document.getElementById('conversation-section');
            const btnDict = document.getElementById('btn-tab-dict');
            const btnConv = document.getElementById('btn-tab-conv');

            if (tabName === 'conv') {
                if (dictSec) dictSec.style.display = 'none';
                if (convSec) convSec.style.display = 'flex';
                if (btnDict) btnDict.classList.remove('active');
                if (btnConv) btnConv.classList.add('active');
            } else {
                if (dictSec) dictSec.style.display = 'block';
                if (convSec) convSec.style.display = 'none';
                if (btnDict) btnDict.classList.add('active');
                if (btnConv) btnConv.classList.remove('active');
            }
        }
    """)


# -------------------------------------------------------------------------
# OFFLINE SVG ICONS
# -------------------------------------------------------------------------

def svg_icon(paths, width=18, height=18, class_name="", view_box="0 0 24 24"):
    return ft(
        "svg",
        *paths,
        width=str(width),
        height=str(height),
        viewBox=view_box,
        fill="none",
        stroke="currentColor",
        stroke_width="2",
        stroke_linecap="round",
        stroke_linejoin="round",
        cls=f"svg-icon {class_name}"
    )

def icon_mic(width=16, height=16):
    return svg_icon([
        ft("path", d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"),
        ft("path", d="M19 10v2a7 7 0 0 1-14 0v-2"),
        ft("line", x1="12", y1="19", x2="12", y2="22")
    ], width, height)

def icon_volume(width=16, height=16):
    return svg_icon([
        ft("polygon", points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"),
        ft("path", d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07")
    ], width, height)

def icon_table(width=16, height=16):
    return svg_icon([
        ft("rect", x="3", y="3", width="18", height="18", rx="2"),
        ft("line", x1="3", y1="9", x2="21", y2="9"),
        ft("line", x1="3", y1="15", x2="21", y2="15"),
        ft("line", x1="9", y1="3", x2="9", y2="21"),
        ft("line", x1="15", y1="3", x2="15", y2="21")
    ], width, height)

def icon_sparkles(width=16, height=16):
    return svg_icon([
        ft("path", d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3z")
    ], width, height)

def icon_search(width=18, height=18):
    return svg_icon([
        ft("circle", cx="11", cy="11", r="8"),
        ft("line", x1="21", y1="21", x2="16.65", y2="16.65")
    ], width, height)

def icon_users(width=18, height=18):
    return svg_icon([
        ft("path", d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"),
        ft("circle", cx="9", cy="7", r="4"),
        ft("path", d="M23 21v-2a4 4 0 0 0-3-3.87"),
        ft("path", d="M16 3.13a4 4 0 0 1 0 7.75")
    ], width, height)


# -------------------------------------------------------------------------
# LEO NAVBAR & MODE TAB SELECTOR
# -------------------------------------------------------------------------

def render_leo_navbar():
    """Renders main LEO header navigation bar with Mode Switch Tabs."""
    has_gemini = bool(get_gemini_api_key())
    gemini_text = "Gemini AI" if has_gemini else "Configurar Gemini"

    return Nav(
        A(
            Div("LEO", cls="brand-logo"),
            Div(
                Div("LEO Translator", cls="brand-title"),
                Div("Dicionário & Conversação Frente a Frente", cls="brand-subtitle")
            ),
            href="/",
            cls="brand"
        ),
        Div(
            Button(
                icon_search(16, 16),
                Span("Dicionário"),
                onclick="switchAppTab('dict')",
                id="btn-tab-dict",
                cls="mode-tab-btn active"
            ),
            Button(
                icon_users(16, 16),
                Span("Conversação 2 Pessoas"),
                onclick="switchAppTab('conv')",
                id="btn-tab-conv",
                cls="mode-tab-btn"
            ),
            Button(
                icon_sparkles(16, 16),
                Span(gemini_text),
                onclick="openModal('gemini-key-modal')",
                cls="btn btn-leo btn-sm"
            ),
            cls="nav-actions"
        ),
        cls="navbar"
    )


# -------------------------------------------------------------------------
# 📱 MOBILE SPLIT-SCREEN 2-PERSON FACE-TO-FACE CONVERSATION COMPONENT
# -------------------------------------------------------------------------

def render_conversation_split_screen():
    """
    Renders 2-Person Face-to-Face Live Conversation Split Screen UI for Mobile/Cellular.
    Top Half (Person A): Upside-down (rotate 180deg) for person sitting across the table!
    Bottom Half (Person B): Normal 0deg orientation!
    """
    return Div(
        # Top Half: Person A (Rotated 180deg for person across table)
        Div(
            Div(
                Span("👤 Pessoa A (Frente para Você)", cls="person-label", style="color: #a78bfa;"),
                Span("🇩🇪 Alemão / 🇬🇧 Inglês", style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;"),
                cls="person-header"
            ),
            Div(
                Div("Pronto para traduzir a voz da Pessoa A...", cls="speech-bubble"),
                id="transcript-person-a",
                cls="transcript-box"
            ),
            Button(
                icon_mic(20, 20),
                Span("Pessoa A: Falar / Pressionar"),
                onclick="triggerSpeechRecognition('a', 'de')",
                cls="talk-btn-large talk-btn-person-a"
            ),
            cls="person-a-screen"
        ),

        # Center Divider
        Div(
            icon_users(16, 16),
            Span("Modo Conversação Frente a Frente ~ 100% Offline"),
            cls="conversation-divider"
        ),

        # Bottom Half: Person B (Normal 0deg)
        Div(
            Div(
                Span("👤 Pessoa B (Você)", cls="person-label", style="color: var(--accent-emerald);"),
                Span("🇵🇹 Português", style="font-size: 0.75rem; color: var(--text-muted); font-weight: 700;"),
                cls="person-header"
            ),
            Div(
                Div("Pronto para traduzir a sua voz em Português...", cls="speech-bubble"),
                id="transcript-person-b",
                cls="transcript-box"
            ),
            Button(
                icon_mic(20, 20),
                Span("Pessoa B: Falar em Português"),
                onclick="triggerSpeechRecognition('b', 'pt')",
                cls="talk-btn-large talk-btn-person-b"
            ),
            cls="person-b-screen"
        ),
        id="conversation-section",
        cls="split-screen-container",
        style="display: none;"
    )


# -------------------------------------------------------------------------
# DICTIONARY SEARCH HERO & CATEGORIZED TABLES
# -------------------------------------------------------------------------

def render_search_hero():
    """Renders top search box."""
    return Div(
        H2("Procurar no Dicionário LEO", style="font-size: 1.5rem; font-weight: 800; color: var(--accent-amber);"),
        P("Consulte verbos com contextos (ex: rennen vs laufen vs fließen), síntese de voz Piper TTS e tabelas de flexão.", style="color: var(--text-secondary); font-size: 0.85rem;"),
        Form(
            Input(
                type="text",
                name="query",
                placeholder="Digite uma palavra em Alemão, Português ou Inglês (ex: correr, caminhar, Tagebuch)...",
                cls="search-input-large",
                hx_post="/api/search-leo",
                hx_trigger="keyup changed delay:250ms, search",
                hx_target="#leo-results-container"
            ),
            Button(
                icon_search(18, 18),
                Span("Pesquisar"),
                type="submit",
                cls="btn btn-leo"
            ),
            cls="search-box-large",
            hx_post="/api/search-leo",
            hx_target="#leo-results-container"
        ),
        cls="search-hero"
    )


def render_category_table(category_name, items):
    """Renders LEO-style categorized table with Piper TTS WAV audio player button."""
    if not items:
        return None

    rows = []
    for item in items:
        art_html = None
        if item.get("article_de"):
            art = item["article_de"]
            art_cls = f"article-tag art-{art}"
            art_html = Span(art, cls=art_cls)

        context_html = None
        if item.get("context_tag"):
            context_html = Span(f"[{item['context_tag']}]", cls="context-pill")

        word_de_clean = item.get("word_de", "").replace("'", "\\'")

        actions = [
            Button(
                icon_volume(14, 14),
                Span("Ouvir"),
                onclick=f"playTTS('{word_de_clean}', 'de-DE')",
                cls="btn btn-secondary btn-sm"
            ),
            Button(
                icon_mic(14, 14),
                Span("Piper Neural (WAV)"),
                hx_post="/api/piper-tts",
                hx_vals=f'{{"text": "{word_de_clean}", "lang": "de"}}',
                hx_target=f"#piper-audio-target-{item['id']}",
                cls="btn btn-emerald btn-sm"
            ),
            Button(
                icon_sparkles(14, 14),
                Span("Gemini AI"),
                hx_post="/api/gemini-explain",
                hx_vals=f'{{"word": "{word_de_clean}"}}',
                hx_target=f"#gemini-explain-target-{item['id']}",
                cls="btn btn-leo btn-sm"
            )
        ]

        if category_name == "Verbos" and item.get("conjugation"):
            actions.insert(
                2,
                Button(
                    icon_table(14, 14),
                    Span("Flexionstabelle"),
                    hx_post="/api/flexion",
                    hx_vals=f'{{"verb": "{word_de_clean}"}}',
                    hx_target="#flexion-modal-container",
                    cls="btn btn-secondary btn-sm"
                )
            )

        rows.append(
            Tr(
                Td(
                    Div(
                        art_html,
                        Span(item.get("word_de", ""), cls="term-de"),
                        context_html,
                        Span(f"| {item['forms_de']}" if item.get("forms_de") else "", cls="forms-de"),
                        Span(f" ({item['plural_de']})" if item.get("plural_de") else "", cls="forms-de")
                    ),
                    Div(*actions, cls="row-actions"),
                    Div(id=f"piper-audio-target-{item['id']}", style="margin-top: 0.5rem;"),
                    Div(id=f"gemini-explain-target-{item['id']}", style="margin-top: 0.5rem;"),
                    cls="col-left"
                ),
                Td(
                    Div(item.get("word_pt", ""), style="color: var(--text-primary); font-weight: 600;"),
                    Div(f"EN: {item['word_en']}", style="color: var(--text-secondary); font-size: 0.85rem; font-style: italic;") if item.get("word_en") else None,
                    Div(item.get("details_pt", ""), style="color: var(--text-muted); font-size: 0.8rem; margin-top: 0.2rem;") if item.get("details_pt") else None,
                    cls="col-right"
                )
            )
        )

    return Div(
        Div(category_name, cls="leo-cat-header"),
        Table(
            Tbody(*rows),
            cls="leo-table"
        ),
        cls="leo-cat-block"
    )


def render_all_category_tables(categories_dict):
    """Renders all category blocks (Verbos, Expressões, Substantivos, Exemplos)."""
    blocks = []
    for cat in ["Verbos", "Expressões", "Substantivos", "Exemplos"]:
        if cat in categories_dict and categories_dict[cat]:
            blocks.append(render_category_table(cat, categories_dict[cat]))

    if not blocks:
        return Div(
            H3("Nenhum resultado encontrado no LEO.", style="color: var(--text-muted); text-align: center; padding: 3rem;"),
            P("Tente pesquisar por outro termo em Alemão, Português ou Inglês.", style="color: var(--text-secondary); text-align: center;")
        )

    return Div(*blocks)


def render_flexionstabelle_modal(verb_item):
    """Renders LEO German Verb Conjugation Modal (Flexionstabelle)."""
    if not verb_item or not verb_item.get("conjugation"):
        return Div()

    conj = verb_item["conjugation"]
    verb_name = verb_item["word_de"]

    def format_tense_list(items):
        res = []
        for line in items:
            parts = line.split(" ")
            pronoun = parts[0]
            verb_part = " ".join(parts[1:])
            res.append(Div(Span(f"{pronoun} "), ft("strong", verb_part), cls="tense-item"))
        return res

    return Div(
        Div(
            Div(
                H3(f"LEO: Flexionstabelle für: {verb_name}", style="color: var(--accent-amber); font-weight: 800;"),
                Button("X", onclick="closeModal('flexion-modal')", cls="btn btn-secondary btn-sm"),
                style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem;"
            ),
            P(f"Formas Principais: {verb_item.get('forms_de', '')}", style="font-family: var(--font-mono); font-size: 0.85rem; color: var(--accent-cyan); margin-bottom: 1rem;"),
            Div(
                Div(Div("Präsens", cls="tense-title"), *format_tense_list(conj["praesens"]), cls="tense-card"),
                Div(Div("Perfekt", cls="tense-title"), *format_tense_list(conj["perfekt"]), cls="tense-card"),
                Div(Div("Präteritum", cls="tense-title"), *format_tense_list(conj["praeteritum"]), cls="tense-card"),
                Div(Div("Plusquamperfekt", cls="tense-title"), *format_tense_list(conj["plusquamperfekt"]), cls="tense-card"),
                Div(Div("Futur I", cls="tense-title"), *format_tense_list(conj["futur_1"]), cls="tense-card"),
                cls="flexion-grid"
            ),
            cls="flexion-box"
        ),
        id="flexion-modal",
        cls="modal-overlay active"
    )


def render_gemini_key_modal():
    """Renders modal to configure GEMINI_API_KEY in .env."""
    current_key = get_gemini_api_key()
    masked_key = (current_key[:6] + "..." + current_key[-4:]) if len(current_key) > 10 else current_key

    return Div(
        Div(
            Div(
                H3("Configurar Gemini API Key (.env)", style="color: var(--accent-amber); font-weight: 800;"),
                Button("X", onclick="closeModal('gemini-key-modal')", cls="btn btn-secondary btn-sm"),
                style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;"
            ),
            Form(
                P("Cole sua chave da API do Google Gemini abaixo para ativar explicações gramaticais com IA no dicionário LEO.", style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 1rem;"),
                Div(
                    Label("GEMINI_API_KEY", style="font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 0.4rem; display: block;"),
                    Input(
                        type="password",
                        name="gemini_key",
                        placeholder="AIzaSy...",
                        value=current_key,
                        required=True,
                        style="width: 100%; padding: 0.7rem 1rem; background: rgba(9, 13, 22, 0.9); border: 1px solid var(--border-color); border-radius: var(--radius-md); color: white;"
                    ),
                    style="margin-bottom: 1.25rem;"
                ),
                P(f"Chave atual salva no .env: {masked_key if current_key else 'Nenhuma chave configurada ainda.'}", style="font-size: 0.75rem; color: var(--accent-cyan); font-style: italic; margin-bottom: 1rem;"),
                Div(
                    Button("Cancelar", type="button", onclick="closeModal('gemini-key-modal')", cls="btn btn-secondary"),
                    Button("Salvar no .env", type="submit", cls="btn btn-leo"),
                    style="display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem;"
                ),
                action="/api/save-gemini-key",
                method="POST"
            ),
            cls="modal-box"
        ),
        id="gemini-key-modal",
        cls="modal-overlay"
    )
