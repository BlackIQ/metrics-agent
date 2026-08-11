# Libs
import tomllib  # Toml
from pathlib import Path  # Path
from typing import Any  # Typing
from pydantic import Field  # Pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict  # Settings

# Check if app is installed
INSTALLED = Path("/etc/openhubble-agent/.env").exists()

# Now we need to define variables based on INSTALLED
if INSTALLED:
    ROOT_DIR = Path("/opt/openhubble-agent")  # Application
    ENV_FILE = Path("/etc/openhubble-agent/.env")  # Settings
    DATA_DIR = "/var/lib/openhubble-agent"  # Database
    LOG_DIR = Path("/var/log/openhubble-agent")  # Log
else:
    ROOT_DIR = Path(__file__).resolve().parent.parent  # Application
    ENV_FILE = Path(".env")  # Settings
    DATA_DIR = str(ROOT_DIR)  # Database
    LOG_DIR = ROOT_DIR / "logs"  # Log

# Ensure directories exist
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "openhubble-agent.log"


# Load toml file
def load_pyproject_meta() -> dict[str, Any]:
    pyproject = ROOT_DIR / "pyproject.toml"

    if pyproject.exists():
        with pyproject.open("rb") as f:
            return tomllib.load(f).get("project", {})

    return {}


# Our toml file
_pyproject = load_pyproject_meta()


# Class Settings
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE if ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_mode: str = ""
    allowed_ips: str = ""
    bind_ip: str = "0.0.0.0"
    port: int = 9703
    hostname: str = ""
    api_key: str = ""

    database_dir: str = DATA_DIR
    database_name: str = "agent.db"

    project_name: str = Field(default_factory=lambda: _pyproject.get("name", ""))
    project_version: str = Field(default_factory=lambda: _pyproject.get("version", ""))
    project_description: str = Field(
        default_factory=lambda: _pyproject.get("description", "")
    )
    project_authors: list[str] = Field(
        default_factory=lambda: _pyproject.get("authors", [])
    )

    @property
    def database_url(self) -> str:
        return f"sqlite:///{Path(self.database_dir) / self.database_name}"


# Run settings
settings = Settings()
