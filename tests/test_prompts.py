"""
Testes automatizados para validação de prompts.
"""
import re
import sys
from pathlib import Path

import pytest
import yaml

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.utils import validate_prompt_structure

PROMPTS_FILE = (
    Path(__file__).parent.parent
    / "prompts"
    / "bug_to_user_story_v2.yml"
)


def load_prompts(file_path: Path):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


PROMPTS = load_prompts(PROMPTS_FILE)


class TestPrompts:

    @pytest.mark.parametrize("name,prompt", PROMPTS.items())
    def test_prompt_has_system_prompt(self, name, prompt):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt
        assert prompt["system_prompt"].strip()

    @pytest.mark.parametrize("name,prompt", PROMPTS.items())
    def test_prompt_has_role_definition(self, name, prompt):
        """Verifica se o prompt define uma persona."""
        system_prompt = prompt["system_prompt"]

        assert (
            "você é" in system_prompt.lower()
            or "voce é" in system_prompt.lower()
        ), f"{name}: não define uma persona"

    @pytest.mark.parametrize("name,prompt", PROMPTS.items())
    def test_prompt_mentions_format(self, name, prompt):
        """Verifica se o prompt exige formato de saída."""
        system_prompt = prompt["system_prompt"].lower()

        keywords = [
            "formato obrigatório",
            "markdown",
            "user story",
            "como [tipo de usuário]",
        ]

        assert any(k in system_prompt for k in keywords), (
            f"{name}: não define claramente o formato de saída."
        )

    @pytest.mark.parametrize("name,prompt", PROMPTS.items())
    def test_prompt_has_few_shot_examples(self, name, prompt):
        """Verifica se o prompt contém exemplos Few-shot."""
        system_prompt = prompt["system_prompt"].lower()

        example_count = len(re.findall(r"exemplo", system_prompt))

        assert example_count >= 2, (
            f"{name}: poucos exemplos encontrados ({example_count})."
        )

    @pytest.mark.parametrize("name,prompt", PROMPTS.items())
    def test_prompt_no_todos(self, name, prompt):
        """Garante que não existem TODOs esquecidos."""
        system_prompt = prompt["system_prompt"]

        assert "[todo]" not in system_prompt.lower()

    @pytest.mark.parametrize("name,prompt", PROMPTS.items())
    def test_minimum_techniques(self, name, prompt):
        """
        Verifica (através dos metadados do yaml)
        se pelo menos 2 técnicas foram listadas.
        """

        techniques = (
            prompt.get("metadata", {})
            .get("techniques", [])
        )

        assert isinstance(techniques, list)
        assert len(techniques) >= 2, (
            f"{name}: metadata.techniques deve possuir pelo menos 2 técnicas."
        )

    @pytest.mark.parametrize("name,prompt", PROMPTS.items())
    def test_prompt_structure(self, name, prompt):
        """Valida a estrutura geral do prompt."""
        valid, error = validate_prompt_structure(prompt)
        assert valid, f"{name}: Estrutura inválida. Erros: {error}"