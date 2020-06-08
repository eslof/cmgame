import json
from config_properties import CONFIG_JSON_PATH, ConfigAttr


Config: ConfigAttr
with open(CONFIG_JSON_PATH) as cfg_r:
    Config = ConfigAttr(**json.load(cfg_r))
