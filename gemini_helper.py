"""
Gemini AI Language Assistant Helper Module
Loads GEMINI_API_KEY from .env and provides strict Duden-level linguistic explanations.
Enforces 3-step verification AND Multi-Context Synonym Disambiguation (e.g., rennen vs laufen vs fließen).
"""

import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv(override=True)

def get_gemini_api_key():
    """Retrieves GEMINI_API_KEY from environment or .env file."""
    load_dotenv(override=True)
    return os.environ.get("GEMINI_API_KEY", "").strip()

def save_gemini_api_key(key: str):
    """Saves GEMINI_API_KEY into .env file."""
    env_path = ".env"
    key_clean = key.strip()
    
    # Read existing content
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
    updated = False
    new_lines = []
    for line in lines:
        if line.startswith("GEMINI_API_KEY="):
            new_lines.append(f'GEMINI_API_KEY="{key_clean}"\n')
            updated = True
        else:
            new_lines.append(line)
            
    if not updated:
        new_lines.append(f'GEMINI_API_KEY="{key_clean}"\n')
        
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
        
    os.environ["GEMINI_API_KEY"] = key_clean
    return True, "Chave da API do Gemini salva com sucesso no arquivo .env!"


def explain_word_with_gemini(word: str, target_lang: str = "pt") -> dict:
    """
    Queries Gemini AI using the Duden Linguist + Multi-Context Synonym Disambiguation Prompt.
    Never gives a 1:1 direct translation if multiple contextual options exist (e.g. rennen vs laufen).
    """
    api_key = get_gemini_api_key()
    
    # Fallback response if no API key is set
    if not api_key:
        return {
            "success": False,
            "has_key": False,
            "word": word,
            "explanation": f"""
📌 **Análise Gramatical & Contextos (Duden) de '{word}'**:
- **Termo**: `{word}`
- **Análise Contextual**: Ativada.
- **Dica**: Adicione sua **GEMINI_API_KEY** no botão 'Configurar Gemini AI' para obter o desmembramento completo de sinônimos por contexto (ex: *rennen* [alta velocidade] vs *laufen* [jogging/a pé] vs *fließen* [líquidos]).
"""
        }

    try:
        super_prompt = f"""
Aja como um professor de alemão nativo, linguista especialista e programador (nível Duden). 
As traduções NUNCA podem ser 1:1 simples. Muitas palavras em português (como 'correr', 'andar', 'falar', 'olhar') possuem MÚLTIPLOS equivalentes em alemão dependendo do contexto.

Para o termo: "{word}", siga OBRIGATORIAMENTE este padrão de resposta:

1. **Verificação Morfológica Duden**: Se for um substantivo no plural (ex: Überprüfungen), identifique como Nomen, informe o singular (die Überprüfung) e o artigo (der/die/das).
2. **Desmembramento de Sinônimos por Contexto**: Nunca me dê apenas 1 opção se houver verbos ou palavras diferentes para contextos diferentes. Explicite a diferença semântica entre eles (ex: *rennen* = alta velocidade, *laufen* = esportes/ir a pé, *fließen* = líquidos).
3. **Validação de Particípio & Auxiliar**: Se for verbo, informe a forma do Infinitivo, o Partizip II correto (valide inseparáveis como 'überprüft' e não 'geüberprüft') e o verbo auxiliar (haben/sein).
4. **Frases de Exemplo por Contexto**: Dê 1 frase de exemplo para cada contexto variante em Alemão com tradução para Português.

Formate a resposta em Markdown claro e legível.
"""

        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=super_prompt,
            )
            text_output = response.text
        except Exception:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=api_key)
            model = genai_legacy.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(super_prompt)
            text_output = response.text

        return {
            "success": True,
            "has_key": True,
            "word": word,
            "explanation": text_output
        }
    except Exception as e:
        return {
            "success": False,
            "has_key": True,
            "word": word,
            "error": str(e),
            "explanation": f"❌ Erro ao conectar à API do Gemini: {str(e)}"
        }
