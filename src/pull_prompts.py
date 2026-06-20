"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

client = Client()

def pull_prompts_from_langsmith():
    print_section_header("Pulling prompts from LangSmith Prompt Hub...")
    return client.pull_prompt("leonanluppi/bug_to_user_story_v1")

def main():
    check_env_vars(["LANGSMITH_ENDPOINT", "LANGSMITH_API_KEY", "LANGSMITH_PROJECT"])
    prompt = pull_prompts_from_langsmith()
    root_dir = Path(__file__).resolve().parent.parent
    prompts_dir = str(root_dir / "prompts" / "bug_to_user_story_v1.yml")
    saved = save_yaml(prompt, prompts_dir)
    if saved:
        print_section_header("Prompt pulled and saved successfully!")
    else:
        print_section_header("Failed to save the prompt.")

if __name__ == "__main__":
    sys.exit(main())
