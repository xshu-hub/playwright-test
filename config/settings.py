"""
项目配置模块
支持通过环境变量覆盖默认配置
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


class Settings:
    """项目配置类"""

    # 基础 URL
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")

    # 超时设置（毫秒）
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30000"))

    # 无头模式
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"

    # 慢动作模式（毫秒），用于调试
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))

    # 浏览器视口大小
    VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "1080"))

    # 截图设置
    SCREENSHOT_ON_FAILURE: bool = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"

    # Session 复用设置
    SESSION_DIR: Path = PROJECT_ROOT / "data" / "sessions"
    SESSION_FILE: str = os.getenv("SESSION_FILE", "auth_state.json")
    REUSE_SESSION: bool = os.getenv("REUSE_SESSION", "false").lower() == "true"

    # 测试用户凭证 - 从环境变量读取
    STANDARD_USER: str = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER: str = os.getenv("LOCKED_USER", "locked_out_user")
    PROBLEM_USER: str = os.getenv("PROBLEM_USER", "problem_user")
    PERFORMANCE_USER: str = os.getenv("PERFORMANCE_USER", "performance_glitch_user")
    ERROR_USER: str = os.getenv("ERROR_USER", "error_user")
    VISUAL_USER: str = os.getenv("VISUAL_USER", "visual_user")
    PASSWORD: str = os.getenv("TEST_PASSWORD", "secret_sauce")

    @classmethod
    def get_browser_config(cls) -> dict:
        """获取浏览器启动配置"""
        return {
            "headless": cls.HEADLESS,
            "slow_mo": cls.SLOW_MO,
        }

    @classmethod
    def get_context_config(cls) -> dict:
        """获取浏览器上下文配置"""
        return {
            "viewport": {
                "width": cls.VIEWPORT_WIDTH,
                "height": cls.VIEWPORT_HEIGHT,
            },
            "ignore_https_errors": True,
        }

    @classmethod
    def get_session_file_path(cls, username: str | None = None) -> Path:
        """
        获取 Session 文件路径

        Args:
            username: 用户名，用于区分不同用户的 session。
                     如果为 None，则使用默认的 SESSION_FILE

        Returns:
            Session 文件完整路径
        """
        # 确保 session 目录存在
        cls.SESSION_DIR.mkdir(parents=True, exist_ok=True)

        if username:
            return cls.SESSION_DIR / f"{username}_session.json"
        return cls.SESSION_DIR / cls.SESSION_FILE


# 创建全局配置实例
settings = Settings()
