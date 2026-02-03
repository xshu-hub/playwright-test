"""
LoginPage - OrangeHRM 登录页面对象

[示例代码] 此文件是针对 OrangeHRM Demo 系统的示例实现。

如果你要测试自己的系统，请参考此文件创建你自己的登录页面对象：
1. 复制此文件并重命名（如 your_login_page.py）
2. 修改页面元素定位器为你的系统实际的选择器
3. 调整登录方法以匹配你的系统登录流程

OrangeHRM Demo: https://opensource-demo.orangehrmlive.com
"""

import allure
from playwright.sync_api import Page

from config.settings import settings
from pages.base_page import BasePage


class LoginPage(BasePage):
    """OrangeHRM 登录页面对象"""

    # 页面名称
    page_name = "LoginPage"

    # 页面元素定位器
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".oxd-alert-content-text"
    ERROR_ICON = ".oxd-input-field-error-message"
    LOGO = ".orangehrm-login-logo"
    FORGOT_PASSWORD_LINK = ".orangehrm-login-forgot-header"
    LOGIN_TITLE = ".orangehrm-login-title"

    # 登录后的元素（用于验证登录成功）
    DASHBOARD_HEADER = ".oxd-topbar-header-title"
    USER_DROPDOWN = ".oxd-userdropdown"

    def __init__(self, page: Page):
        """
        初始化登录页面

        Args:
            page: Playwright 页面实例
        """
        super().__init__(page)
        self.url = f"{settings.BASE_URL}/web/index.php/auth/login"

    @allure.step("打开登录页面")
    def open(self) -> "LoginPage":
        """
        打开登录页面

        Returns:
            self，支持链式调用
        """
        self.navigate(self.url)
        self.wait_for_visible(self.LOGIN_BUTTON)
        return self

    @allure.step("输入用户名: {username}")
    def enter_username(self, username: str) -> "LoginPage":
        """
        输入用户名

        Args:
            username: 用户名

        Returns:
            self，支持链式调用
        """
        self.fill(self.USERNAME_INPUT, username)
        return self

    @allure.step("输入密码")
    def enter_password(self, password: str) -> "LoginPage":
        """
        输入密码

        Args:
            password: 密码

        Returns:
            self，支持链式调用
        """
        self.fill(self.PASSWORD_INPUT, password)
        return self

    @allure.step("点击登录按钮")
    def click_login(self) -> "LoginPage":
        """
        点击登录按钮

        Returns:
            self，支持链式调用
        """
        self.click(self.LOGIN_BUTTON)
        return self

    @allure.step("使用账号 {username} 登录")
    def login(self, username: str, password: str) -> "LoginPage":
        """
        执行登录操作

        Args:
            username: 用户名
            password: 密码

        Returns:
            self，支持链式调用
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    @allure.step("使用管理员账号登录")
    def login_as_admin(self) -> "LoginPage":
        """
        使用管理员账号登录

        Returns:
            self，支持链式调用
        """
        return self.login(settings.ADMIN_USER, settings.ADMIN_PASSWORD)

    def get_error_message(self) -> str:
        """
        获取错误消息

        Returns:
            错误消息文本
        """
        # 首先检查 alert 类型的错误消息
        if self.is_visible(self.ERROR_MESSAGE, timeout=3000):
            return self.get_text(self.ERROR_MESSAGE)
        # 然后检查输入框下的错误消息
        if self.is_visible(self.ERROR_ICON, timeout=1000):
            return self.get_text(self.ERROR_ICON)
        return ""

    def get_field_error(self, field_name: str = "username") -> str:
        """
        获取特定字段的错误消息

        Args:
            field_name: 字段名称 ('username' 或 'password')

        Returns:
            错误消息文本
        """
        # OrangeHRM 的字段错误在输入框旁边
        error_selector = (
            f".oxd-input-group:has(input[name='{field_name}']) .oxd-input-field-error-message"
        )
        if self.is_visible(error_selector, timeout=2000):
            return self.get_text(error_selector)
        return ""

    def is_error_displayed(self) -> bool:
        """
        检查是否显示错误消息

        Returns:
            是否显示错误消息
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000) or self.is_visible(
            self.ERROR_ICON, timeout=1000
        )

    def is_login_page(self) -> bool:
        """
        检查当前是否在登录页面

        Returns:
            是否在登录页面
        """
        return self.is_visible(self.LOGIN_BUTTON, timeout=3000)

    def is_logged_in(self) -> bool:
        """
        检查是否登录成功（通过检测仪表盘元素）

        Returns:
            是否登录成功
        """
        return self.is_visible(self.USER_DROPDOWN, timeout=10000)

    def wait_for_login_complete(self) -> "LoginPage":
        """
        等待登录完成

        Returns:
            self，支持链式调用
        """
        self.wait_for_visible(self.USER_DROPDOWN, timeout=15000)
        return self
