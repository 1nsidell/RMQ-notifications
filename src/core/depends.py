from typing import Annotated

from fastapi import Depends

from src.settings import Settings, get_settings

SettingsService = Annotated[Settings, Depends(get_settings)]
