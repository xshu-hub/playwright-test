"""
LoginPage - 登录页面对象
封装 saucedemo.com 登录页面的元素和操作
"""

import allure
from playwright.sync_api import Page

from config.settings import settings
from pages.base_page import BasePage


class LoginPage(BasePage):
    """登录页面对象"""

    # 页面名称
    page_name = "LoginPage"

    # 页面元素定位器
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_BUTTON = ".error-button"
    LOGO = ".login_logo"

    def __init__(self, page: Page):
        """
        初始化登录页面

        Args:
            page: Playwright 页面实例
        """
        super().__init__(page)
        self.url = settings.BASE_URL

    @allure.step("打开登录页面")
    def open(self) -> "LoginPage":
        """
        打开登录页面

        Returns:
            self，支持链式调用
        """
        self.navigate(self.url)
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

    @allure.step("使用标准用户登录")
    def login_as_standard_user(self) -> "LoginPage":
        """
        使用标准用户登录

        Returns:
            self，支持链式调用
        """
        return self.login(settings.STANDARD_USER, settings.PASSWORD)

    def get_error_message(self) -> str:
        """
        获取错误消息

        Returns:
            错误消息文本
        """
        if self.is_visible(self.ERROR_MESSAGE, timeout=3000):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_error_displayed(self) -> bool:
        """
        检查是否显示错误消息

        Returns:
            是否显示错误消息
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=3000)

    @allure.step("关闭错误提示")
    def close_error(self) -> "LoginPage":
        """
        关闭错误提示

        Returns:
            self，支持链式调用
        """
        if self.is_visible(self.ERROR_BUTTON, timeout=2000):
            self.click(self.ERROR_BUTTON)
        return self

    def is_login_page(self) -> bool:
        """
        检查当前是否在登录页面

        Returns:
            是否在登录页面
        """
        return self.is_visible(self.LOGIN_BUTTON, timeout=3000)

    def is_logged_in(self) -> bool:
        """
        检查是否登录成功（通过 URL 判断）

        Returns:
            是否登录成功
        """
        return "inventory" in self.get_current_url()
