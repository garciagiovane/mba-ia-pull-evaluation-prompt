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
from langsmith import Client
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
    client = Client()

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    prompt_identifier = f"{username}/{prompt_name}"

    template = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_data["system_prompt"]),
            ("user", prompt_data["user_prompt"])
        ]
    )

    print_section_header(f"Pushing prompt '{prompt_identifier}' to LangSmith Hub...")
    link = client.push_prompt(prompt_identifier, object = template, is_public=True, description=prompt_data["description"], tags=prompt_data["tags"])
    return link is not None


def validate_prompt(prompt_data: dict | None) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    ...
    if prompt_data is None:
        return False, ["Prompt data is None"]
    
    required_fields = ["description", "system_prompt", "user_prompt", "version", "tags"]
    
    valid = True
    errors = []
    for field in required_fields:
        if field not in prompt_data:
            valid = False
            errors.append(f"Missing required field: {field}")
    
    return valid, errors

def main():
    check_env_vars(["LANGSMITH_ENDPOINT", "LANGSMITH_API_KEY", "LANGSMITH_PROJECT", "USERNAME_LANGSMITH_HUB"])
    root_dir = Path(__file__).resolve().parent.parent
    prompt_name = "bug_to_user_story_v2"
    prompt_file_name = prompt_name + ".yml"

    prompt_dir = str(root_dir / "prompts" / prompt_file_name)
    print_section_header(f"Loading prompt from {prompt_dir}...")
    prompt = load_yaml(prompt_dir)
    prompt = prompt if prompt is not None else {}
    v2 = prompt["bug_to_user_story_v2"]
    validation_result = validate_prompt(v2)
    valid, errors = validation_result

    if not valid:
        print_section_header("Prompt validation failed with errors:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)

    print_section_header("Prompt validation successful. Proceeding to push...")

    success = push_prompt_to_langsmith(prompt_name, v2)
    if success:
        print_section_header("Prompt pushed successfully to LangSmith Hub!")
    else:
        print_section_header("Failed to push the prompt to LangSmith Hub.")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
