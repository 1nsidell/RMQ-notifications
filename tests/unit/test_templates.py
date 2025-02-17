import pytest
from pathlib import Path
from src.settings import settings
from tests.conftest import REQUIRED_TEMPLATES


@pytest.mark.parametrize("template_file", REQUIRED_TEMPLATES)
def test_template_existence(template_file: str) -> None:
    """
    Проверяет, что файл шаблона существует в директории TEMPLATE_DIR.
    """
    template_dir: Path = settings.paths.TEMPLATE_DIR
    assert (
        template_dir.exists()
    ), f"Шаблон {template_file} отсутствует по пути {settings.paths.TEMPLATE_DIR}"
