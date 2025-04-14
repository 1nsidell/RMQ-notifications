from pathlib import Path

from notifications.core.settings import settings
import pytest
from tests.fixtures.const import REQUIRED_TEMPLATES


@pytest.mark.parametrize("template_file", REQUIRED_TEMPLATES)
def test_template_existence(template_file: str) -> None:
    """
    Checks if template file exists in the TEMPLATE_DIR directory.
    """
    template_dir: Path = settings.paths.TEMPLATE_DIR
    template_path = template_dir / template_file

    assert (
        template_dir.exists()
    ), f"Директория шаблонов отсутствует по пути {template_dir}"
    assert (
        template_path.exists()
    ), f"Шаблон {template_file} отсутствует по пути {template_path}"
    assert (
        template_path.is_file()
    ), f"Путь {template_path} существует, но не является файлом"
