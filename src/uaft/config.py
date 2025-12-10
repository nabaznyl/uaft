import os
import json
from typing import Dict, Any
from uaft.utils import load_json_config, Colors


def load_config() -> Dict[str, Any]:
    """Load and merge uaft.json from global and local locations"""
    config = {}

    # 1. Load global config first (base)
    global_config_path = os.path.expanduser("~/.config/uaft/uaft.json")
    if os.path.exists(global_config_path):
        global_data = load_json_config(global_config_path)
        if global_data:
            config.update(global_data)

    # 2. Load local config (override)
    local_config_path = os.path.join(os.getcwd(), "uaft.json")
    if os.path.exists(local_config_path):
        local_data = load_json_config(local_config_path)
        if local_data:
            config.update(local_data)

    # Fallback check for legacy yaml
    if not config and os.path.exists("uaft.yaml"):
        print(
            f"{Colors.YELLOW}Warning: uaft.yaml found but YAML support is deprecated. Please migrate to uaft.json.{Colors.ENDC}"
        )

    return config
