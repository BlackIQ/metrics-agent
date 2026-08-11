# Toml Ib
import tomllib

# Path Lib
from pathlib import Path

# Pydantic Settings
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Check if app is installed
INSTALLED = Path("/etc/openhubble-agent/.env").exists()

# Define variables based on INSTALLED
if INSTALLED:
    ROOT_DIR = Path("/opt/openhubble-agent")
    ENV_FILE = "/etc/openhubble-agent/.env"
    DATA_DIR = "/var/lib/openhubble-agent"
else:
    ROOT_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE = ".env"
    DATA_DIR = str(ROOT_DIR)


# Settings Class
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE)

    # App
    app_mode: str = ""

    # Server
    allowed_ips: str = ""

    # Agent
    bind_ip: str = "0.0.0.0"
    port: int = 9703

    # Host
    hostname: str = ""

    # API
    api_key: str = ""

    # Database
    database_dir: str = DATA_DIR
    database_name: str = "agent.db"

    # Data from pyproject.toml
    project_name: str = ""
    project_version: str = ""
    project_description: str = ""
    project_authors: list[str] = Field(default_factory=list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pyproject = ROOT_DIR / "pyproject.toml"

        if pyproject.exists():
            with pyproject.open("rb") as f:
                data = tomllib.load(f)

            metadata = data.get("project", {})

            self.project_name = metadata.get("name", "")
            self.project_version = metadata.get("version", "")
            self.project_description = metadata.get("description", "")
            self.project_authors = metadata.get("authors", [])

    @property
    def database_url(self) -> str:
        return f"sqlite:///{Path(self.database_dir) / self.database_name}"


# Run settings
settings = Settings()
