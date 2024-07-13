from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from termcolor import cprint


class DublicateMixin(BaseModel):
    enable_duplicate_requests: bool = Field(default=True)
    count_duplicate_request: int = Field(default=5)


class MoexSettings(DublicateMixin, BaseModel):
    base_url: str
    timeout: float


class Settings(BaseSettings):
    moex_settings: MoexSettings
    request_interval: int
    log_level: str

    model_config = SettingsConfigDict(env_file=[".env", "example.env"], env_file_encoding="utf-8", env_nested_delimiter="__")


SETTINGS = Settings()  # type: ignore
cprint(f"Settings file loaded:\n{SETTINGS.model_dump_json(indent=1)}", color="blue")
