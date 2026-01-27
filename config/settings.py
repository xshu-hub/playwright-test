"""
项目配置模块
支持通过环境变量覆盖默认配置
"""

import os

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


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


# 创建全局配置实例
settings = Settings()
