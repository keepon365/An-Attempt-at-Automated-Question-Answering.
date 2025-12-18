import json
import os
import logging

class Config:
    def __init__(self):
        self.config_path = os.path.join("config", "settings.json")
        self.config_data = self._load_config()
        self._validate_config()

    def _load_config(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"配置文件未找到：{self.config_path}")
            raise FileNotFoundError(f"请确保配置文件存在：{self.config_path}")
        except json.JSONDecodeError:
            logging.error(f"配置文件格式错误：{self.config_path}")
            raise ValueError(f"配置文件格式无效，请检查JSON语法")

    def _validate_config(self):
        required_keys = [
            "ai_api_key", "ai_api_url", "browser_type",
            "wisdom_tree_username", "wisdom_tree_password"
        ]
        missing_keys = [key for key in required_keys if key not in self.config_data]
        if missing_keys:
            logging.error(f"配置文件缺少必要字段：{', '.join(missing_keys)}")
            raise ValueError(f"配置文件缺少必要字段：{', '.join(missing_keys)}")

    # 获取配置值（支持默认值）
    def get(self, key, default=None):
        return self.config_data.get(key, default)

    # 快捷获取常用配置
    @property
    def ai_api_key(self):
        return self.get("ai_api_key")

    @property
    def ai_api_url(self):
        return self.get("ai_api_url")

    @property
    def browser_type(self):
        return self.get("browser_type", "chrome").lower()

    @property
    def username(self):
        return self.get("wisdom_tree_username")

    @property
    def password(self):
        return self.get("wisdom_tree_password")

    @property
    def target_proficiency(self):
        return int(self.get("target_proficiency", 80))

    @property
    def max_retries(self):
        return int(self.get("max_retries", 3))