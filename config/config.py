import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
LOCAL_ENV_FILE = ROOT_DIR / ".env"
DEFAULT_LICENSE_PATH = ROOT_DIR / "license.lic"

class ConfigManager:
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        # 1. Load from local .env if exists
        if LOCAL_ENV_FILE.exists():
            with open(LOCAL_ENV_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        os.environ[key.strip()] = val.strip().strip('"').strip("'")

        # 2. Setup internal platform fallbacks
        self.config["LICENSE_PATH"] = os.environ.get("HUNTER_LICENSE_PATH", str(DEFAULT_LICENSE_PATH))
        self.config["OUTPUT_DIR"] = os.environ.get("HUNTER_OUTPUT_DIR", str(ROOT_DIR / "reports"))

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve config value prioritizing environment variables."""
        return os.environ.get(key, self.config.get(key, default))

    def set(self, key: str, value: Any):
        """Set dynamic runtime configuration configuration."""
        self.config[key] = value

config = ConfigManager()
