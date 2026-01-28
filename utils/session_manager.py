"""
Session 管理器
支持多用户/多角色的 Session 管理，适用于审批流程等多角色测试场景
针对 OrangeHRM 人力资源管理系统
"""

import contextlib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from playwright.sync_api import Browser, BrowserContext, Page

from config.settings import settings
from utils.logger import logger


@dataclass
class UserCredentials:
    """用户凭证"""

    username: str
    password: str
    role: str = ""  # 可选的角色标识，如 "admin", "approver", "user"


class SessionManager:
    """
    Session 管理器

    支持多用户 Session 的保存、加载和管理，适用于：
    - 多角色测试场景（如审批流程）
    - 需要在不同用户间切换的测试
    - 并行运行多个用户的测试

    使用示例:
        ```python
        # 创建管理器
        session_manager = SessionManager(browser)

        # 获取用户的已认证页面
        admin_page = session_manager.get_authenticated_page("Admin", "admin123")

        # 多角色审批流程
        user_page.click("#submit-request")  # 用户提交申请
        admin_page.click("#approve-button")  # 管理员审批
        user_page.reload()  # 用户查看结果
        ```
    """

    def __init__(
        self,
        browser: Browser,
        reuse_session: bool = False,
        save_session: bool = False,
    ):
        """
        初始化 Session 管理器

        Args:
            browser: Playwright 浏览器实例
            reuse_session: 是否复用已保存的 Session
            save_session: 是否保存 Session
        """
        self.browser = browser
        self.reuse_session = reuse_session
        self.save_session = save_session

        # 缓存已创建的上下文和页面
        self._contexts: dict[str, BrowserContext] = {}
        self._pages: dict[str, Page] = {}

        # 自定义登录函数，默认为 None（使用内置登录逻辑）
        self._custom_login_func: Callable[[Page, str, str], None] | None = None

    def set_custom_login(self, login_func: Callable[[Page, str, str], None]) -> None:
        """
        设置自定义登录函数

        对于非默认项目，可以设置自定义登录逻辑

        Args:
            login_func: 登录函数，接收 (page, username, password) 参数
        """
        self._custom_login_func = login_func

    def _get_session_file(self, username: str) -> Path:
        """获取用户的 Session 文件路径"""
        return settings.get_session_file_path(username)

    def _is_session_valid(self, session_file: Path) -> bool:
        """检查 Session 文件是否有效"""
        if not session_file.exists():
            return False
        return not session_file.stat().st_size < 10

    def _perform_login(self, page: Page, username: str, password: str) -> None:
        """
        执行登录操作

        Args:
            page: 页面实例
            username: 用户名
            password: 密码
        """
        if self._custom_login_func:
            # 使用自定义登录函数
            self._custom_login_func(page, username, password)
        else:
            # 使用 OrangeHRM 登录逻辑
            from pages.login_page import LoginPage

            login_page = LoginPage(page)
            login_page.open().login(username, password)
            # 等待登录成功（跳转到仪表盘）
            page.wait_for_url("**/dashboard/**", timeout=settings.TIMEOUT)

    def get_context_for_user(
        self,
        username: str,
        password: str | None = None,
    ) -> BrowserContext:
        """
        获取指定用户的浏览器上下文

        如果启用了 Session 复用且存在有效的 Session，则从 Session 创建上下文
        否则创建新上下文并执行登录

        Args:
            username: 用户名
            password: 密码，如果为 None 则使用默认密码

        Returns:
            已认证的浏览器上下文
        """
        # 如果已有缓存的上下文，直接返回
        if username in self._contexts:
            return self._contexts[username]

        password = password or settings.ADMIN_PASSWORD
        session_file = self._get_session_file(username)
        context_config = settings.get_context_config()

        # 尝试复用 Session
        if self.reuse_session and self._is_session_valid(session_file):
            logger.info(f"复用用户 [{username}] 的 Session")
            context_config["storage_state"] = str(session_file)
            context = self.browser.new_context(**context_config)
        else:
            # 创建新上下文并登录
            context = self.browser.new_context(**context_config)
            page = context.new_page()

            try:
                logger.info(f"为用户 [{username}] 执行登录...")
                self._perform_login(page, username, password)

                # 保存 Session
                if self.save_session or self.reuse_session:
                    context.storage_state(path=str(session_file))
                    logger.info(f"用户 [{username}] 的 Session 已保存")
            finally:
                page.close()

        self._contexts[username] = context
        return context

    def get_page_for_user(
        self,
        username: str,
        password: str | None = None,
    ) -> Page:
        """
        获取指定用户的页面实例

        Args:
            username: 用户名
            password: 密码，如果为 None 则使用默认密码

        Returns:
            已认证的页面实例
        """
        # 如果已有缓存的页面，直接返回
        if username in self._pages:
            return self._pages[username]

        context = self.get_context_for_user(username, password)
        page = context.new_page()
        page.set_default_timeout(settings.TIMEOUT)

        self._pages[username] = page
        return page

    def get_authenticated_page(
        self,
        username: str,
        password: str | None = None,
        start_url: str | None = None,
    ) -> Page:
        """
        获取已认证的页面并导航到指定 URL

        Args:
            username: 用户名
            password: 密码
            start_url: 登录后要访问的 URL，如果为 None 则不导航

        Returns:
            已认证并导航到指定页面的页面实例
        """
        page = self.get_page_for_user(username, password)

        if start_url:
            page.goto(start_url)

        return page

    def switch_user(self, username: str, password: str | None = None) -> Page:
        """
        切换到指定用户（获取该用户的页面）

        这是 get_page_for_user 的别名，提供更直观的 API

        Args:
            username: 用户名
            password: 密码

        Returns:
            指定用户的页面实例
        """
        return self.get_page_for_user(username, password)

    def close_user_session(self, username: str) -> None:
        """
        关闭指定用户的 Session

        Args:
            username: 用户名
        """
        if username in self._pages:
            with contextlib.suppress(Exception):
                self._pages[username].close()
            del self._pages[username]

        if username in self._contexts:
            with contextlib.suppress(Exception):
                self._contexts[username].close()
            del self._contexts[username]

        logger.debug(f"已关闭用户 [{username}] 的 Session")

    def close_all(self) -> None:
        """关闭所有用户的 Session"""
        for username in list(self._pages.keys()):
            self.close_user_session(username)

    def __enter__(self) -> "SessionManager":
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """上下文管理器出口，自动清理资源"""
        self.close_all()


# ==================== 预定义用户凭证 ====================

# OrangeHRM 的预定义用户
PREDEFINED_USERS: dict[str, UserCredentials] = {
    "admin": UserCredentials(
        username=settings.ADMIN_USER,
        password=settings.ADMIN_PASSWORD,
        role="admin",
    ),
}


def get_user_credentials(user_key: str) -> UserCredentials:
    """
    获取预定义用户的凭证

    Args:
        user_key: 用户标识，如 "admin" 等

    Returns:
        用户凭证

    Raises:
        KeyError: 如果用户标识不存在
    """
    if user_key not in PREDEFINED_USERS:
        available = ", ".join(PREDEFINED_USERS.keys())
        raise KeyError(f"未找到用户 '{user_key}'，可用的用户: {available}")
    return PREDEFINED_USERS[user_key]
