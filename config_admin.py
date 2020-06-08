import json
from typing import Any

from config_properties import CONFIG_JSON_PATH, ConfigAttr
from item_admin import ItemAdmin


def reset_defaults() -> None:
    with open(CONFIG_JSON_PATH, "w") as cfg_f:
        _defaultConfig = ConfigAttr()
        json.dump(_defaultConfig._asdict(), cfg_f)
        cfg_f.seek(0)


def update_key(cfg_key: str, cfg_value: Any) -> None:
    with open(CONFIG_JSON_PATH, "r+") as cfg_f:
        j_dict = json.load(cfg_f)
        assert cfg_key in j_dict and type(cfg_value) is type(j_dict[cfg_key])
        j_dict[cfg_key] = cfg_value
        cfg_f.seek(0)
        json.dump(j_dict, cfg_f)


reset_defaults()
update_key("ITEM_COUNT", ItemAdmin.table_count("item"))
update_key("BIODOME_COUNT", ItemAdmin.table_count("biodome"))
