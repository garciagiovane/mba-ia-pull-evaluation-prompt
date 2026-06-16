"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

client = Client()

def pull_prompts_from_langsmith():
    return client.pull_prompt("bug_to_user_story_v1")


def main():
    check_env_vars(["LANGSMITH_ENDPOINT", "LANGSMITH_API_KEY", "LANGSMITH_PROJECT"])
    prompt = pull_prompts_from_langsmith()
    print(prompt)


if __name__ == "__main__":
    sys.exit(main())
