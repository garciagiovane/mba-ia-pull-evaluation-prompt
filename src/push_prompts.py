"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    ...


def validate_prompt(prompt_data: dict | None) -> tuple[bool, list]:
    if prompt_data is None:
        return False, ["Prompt data is None"]
    
    return True, [] 
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    ...

def main():
    check_env_vars(["LANGSMITH_ENDPOINT", "LANGSMITH_API_KEY", "LANGSMITH_PROJECT", "USERNAME_LANGSMITH_HUB"])
    root_dir = Path(__file__).resolve().parent.parent
    prompts_dir = str(root_dir / "prompts" / "bug_to_user_story_v2.yml")
    print_section_header(f"Loading prompt from {prompts_dir}...")
    prompt= load_yaml(prompts_dir)
    validation_result = validate_prompt(prompt)
    valid, errors = validation_result

    if not valid:
        print_section_header("Prompt validation failed with errors:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print_section_header("Prompt validation successful. Proceeding to push...")
    prompt_name = "bug_to_user_story_v2"

    ChatPromptTemplate()

    success = push_prompt_to_langsmith(prompt_name, prompt)
    if success:
        print_section_header("Prompt pushed successfully to LangSmith Hub!")
    else:
        print_section_header("Failed to push the prompt to LangSmith Hub.")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
