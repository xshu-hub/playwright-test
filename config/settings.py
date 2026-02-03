"""
项目配置模块
支持通过环境变量覆盖默认配置

[框架核心] 此文件是框架的核心配置模块，可直接复用。

配置分为两类：
1. 框架通用配置：通常无需修改，适用于所有测试项目
2. 目标系统配置：需要根据你的测试系统进行修改

使用方法：
1. 复制 .env.example 为 .env
2. 修改 .env 中的目标系统配置
3. 框架会自动加载环境变量覆盖默认值
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

    # ==========================================================================
    # 目标系统配置（需要根据你的测试系统修改）
    # ==========================================================================

    # 测试目标网站 URL
    # 示例默认值为 OrangeHRM Demo，请修改为你的测试系统 URL
    BASE_URL: str = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")

    # 测试用户凭证
    # 请修改为你的测试系统的管理员账号
    ADMIN_USER: str = os.getenv("ADMIN_USER", "Admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")

    # Session 验证配置
    # SESSION_VALIDATION_PATH: 用于验证 session 有效性的路径（需要登录才能访问的页面）
    # LOGIN_URL_PATTERN: 登录页面的 URL 特征（用于检测是否被重定向到登录页）
    SESSION_VALIDATION_PATH: str = os.getenv("SESSION_VALIDATION_PATH", "/dashboard")
    LOGIN_URL_PATTERN: str = os.getenv("LOGIN_URL_PATTERN", "/login")

    # 用于测试的默认用户（向后兼容）
    DEFAULT_USER: str = ADMIN_USER
    DEFAULT_PASSWORD: str = ADMIN_PASSWORD

    # ==========================================================================
    # 框架通用配置（通常无需修改）
    # ==========================================================================

    # 超时设置（毫秒）
    # 默认 30 秒，适用于大多数场景
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30000"))

    # 无头模式
    # true: 后台运行，适用于 CI/CD
    # false: 显示浏览器窗口，适用于调试
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"

    # 慢动作模式（毫秒）
    # 用于调试时减慢操作速度，便于观察
    # 0 表示不延迟
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))

    # 浏览器视口大小
    VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "1080"))

    # 截图设置
    # 测试失败时自动截图，便于问题排查
    SCREENSHOT_ON_FAILURE: bool = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"

    # ==========================================================================
    # Session 复用配置
    # ==========================================================================

    # Session 文件存储目录
    SESSION_DIR: Path = PROJECT_ROOT / "data" / "sessions"

    # Session 文件名
    SESSION_FILE: str = os.getenv("SESSION_FILE", "auth_state.json")

    # 是否复用已保存的 Session
    # 启用后可跳过登录流程，显著加速测试
    # 可通过命令行参数 --reuse-session 覆盖
    REUSE_SESSION: bool = os.getenv("REUSE_SESSION", "false").lower() == "true"

    # ==========================================================================
    # 方法
    # ==========================================================================

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

    @classmethod
    def validate(cls) -> None:
        """
        验证配置有效性

        Raises:
            ValueError: 如果配置验证失败
        """
        errors = []

        if not cls.BASE_URL.startswith(("http://", "https://")):
            errors.append(f"BASE_URL 格式无效: {cls.BASE_URL}")

        if cls.TIMEOUT <= 0:
            errors.append(f"TIMEOUT 必须大于 0: {cls.TIMEOUT}")

        if cls.VIEWPORT_WIDTH <= 0 or cls.VIEWPORT_HEIGHT <= 0:
            errors.append(f"VIEWPORT 尺寸无效: {cls.VIEWPORT_WIDTH}x{cls.VIEWPORT_HEIGHT}")

        if cls.SLOW_MO < 0:
            errors.append(f"SLOW_MO 不能为负数: {cls.SLOW_MO}")

        if errors:
            raise ValueError("配置验证失败:\n" + "\n".join(f"  - {e}" for e in errors))


# 创建全局配置实例
settings = Settings()
