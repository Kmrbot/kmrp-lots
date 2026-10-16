import json
from pathlib import Path

from nonebot.log import logger

from utils.config import ensure_plugin_config_from_template

__TEMPLATE_PATH = Path(__file__).with_name("lots_data_template.json")

emoji_key_data = {}


def load_lots_data():
    path = ensure_plugin_config_from_template(
        "kmrp-lots",
        "lots_data.json",
        __TEMPLATE_PATH,
    )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_lots_pre(pre_name: str) -> str | None:
    lots_data = load_lots_data()
    # 这里为了可以热更 就遍历了 反正也没多少
    for pre_info in lots_data.get("pre", []):
        for name in pre_info["names"]:
            if name == pre_name:
                return pre_info["text"]
    return None


def get_lots_text_info(lots_key: int):
    lots_data = load_lots_data()
    if len(lots_data.get("lots_info", [])) == 0:
        logger.error(f"get_lots_text fail ! lots_info size invalid !")
        return "抽签错误"
    lots_id = lots_key % len(lots_data.get("lots_info", []))
    data = lots_data["lots_info"][lots_id]
    return {
        "value": data["lots_value"],
        "name": data["lots_name"],
        "title": data["lots_title"],
        "meaning": data["lots_meaning"],
    }
