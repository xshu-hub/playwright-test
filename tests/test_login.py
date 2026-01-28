"""
登录功能测试用例
测试 OrangeHRM 的登录功能
"""

import allure
import pytest

from config.settings import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from utils.data_loader import TestDataLoader


@allure.feature("登录功能")
class TestLogin:
    """登录功能测试类"""

    @allure.story("正常登录")
    @allure.title("使用管理员账号登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_with_admin(self, login_page: LoginPage):
        """
        测试使用管理员账号登录

        步骤:
        1. 打开登录页面
        2. 输入管理员凭证
        3. 点击登录按钮
        4. 验证登录成功（跳转到仪表盘）
        """
        with allure.step("打开登录页面"):
            login_page.open()

        with allure.step("使用管理员账号登录"):
            login_page.login(settings.ADMIN_USER, settings.ADMIN_PASSWORD)

        with allure.step("验证登录成功"):
            assert login_page.is_logged_in(), "登录失败，未跳转到仪表盘"
            assert "dashboard" in login_page.get_current_url().lower()

    @allure.story("登录失败")
    @allure.title("使用错误凭证登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_login_with_invalid_credentials(self, login_page: LoginPage):
        """
        测试使用错误凭证登录

        步骤:
        1. 打开登录页面
        2. 输入错误的用户名和密码
        3. 验证显示错误消息
        """
        with allure.step("打开登录页面"):
            login_page.open()

        with allure.step("使用错误凭证登录"):
            login_page.login("invalid_user", "wrong_password")

        with allure.step("验证显示错误消息"):
            assert login_page.is_error_displayed(), "未显示错误消息"
            error_message = login_page.get_error_message()
            assert "invalid" in error_message.lower(), f"错误消息不正确: {error_message}"

    @allure.story("登录失败")
    @allure.title("空用户名登录验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_login_with_empty_username(self, login_page: LoginPage):
        """
        测试空用户名登录

        步骤:
        1. 打开登录页面
        2. 只输入密码，不输入用户名
        3. 点击登录
        4. 验证显示必填字段错误
        """
        with allure.step("打开登录页面"):
            login_page.open()

        with allure.step("只输入密码"):
            login_page.enter_password(settings.ADMIN_PASSWORD)
            login_page.click_login()

        with allure.step("验证显示必填字段错误"):
            error = login_page.get_field_error("username")
            assert error, "未显示用户名必填错误"
            assert "required" in error.lower(), f"错误消息不正确: {error}"

    @allure.story("登录失败")
    @allure.title("空密码登录验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_login_with_empty_password(self, login_page: LoginPage):
        """
        测试空密码登录

        步骤:
        1. 打开登录页面
        2. 只输入用户名，不输入密码
        3. 点击登录
        4. 验证显示必填字段错误
        """
        with allure.step("打开登录页面"):
            login_page.open()

        with allure.step("只输入用户名"):
            login_page.enter_username(settings.ADMIN_USER)
            login_page.click_login()

        with allure.step("验证显示必填字段错误"):
            error = login_page.get_field_error("password")
            assert error, "未显示密码必填错误"
            assert "required" in error.lower(), f"错误消息不正确: {error}"

    @allure.story("登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.parametrize(
        "username, password, error_key, description",
        TestDataLoader.get_login_failure_test_cases(),
        ids=lambda x: x if isinstance(x, str) and len(x) < 20 else None,
    )
    def test_login_failure_scenarios(
        self, login_page: LoginPage, username: str, password: str, error_key: str, description: str
    ):
        """
        数据驱动测试：登录失败场景

        使用 test_data.json 中的数据进行参数化测试，
        覆盖多种登录失败情况。
        """
        allure.dynamic.title(f"登录失败测试：{description}")

        with allure.step("打开登录页面"):
            login_page.open()

        with allure.step(f"尝试登录 - {description}"):
            if username:
                login_page.enter_username(username)
            if password:
                login_page.enter_password(password)
            login_page.click_login()

        with allure.step("验证显示错误"):
            # 可能是字段错误或登录错误
            has_error = login_page.is_error_displayed()
            has_field_error = bool(login_page.get_field_error("username")) or bool(
                login_page.get_field_error("password")
            )
            assert has_error or has_field_error, "未显示任何错误消息"


@allure.feature("登录功能")
@allure.story("退出登录")
class TestLogout:
    """退出登录测试类"""

    @allure.title("正常退出登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_logout(self, logged_in_dashboard: DashboardPage):
        """
        测试退出登录功能

        步骤:
        1. 以已登录状态进入仪表盘
        2. 点击用户菜单
        3. 点击退出登录
        4. 验证返回登录页面
        """
        dashboard = logged_in_dashboard

        with allure.step("验证已登录状态"):
            assert dashboard.is_on_dashboard() or "dashboard" in dashboard.get_current_url().lower()

        with allure.step("执行退出登录"):
            dashboard.logout()

        with allure.step("验证返回登录页面"):
            login_page = LoginPage(dashboard.page)
            assert login_page.is_login_page(), "未返回登录页面"
