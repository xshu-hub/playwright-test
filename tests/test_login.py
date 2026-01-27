"""
登录功能测试用例
测试 saucedemo.com 的登录功能
支持数据驱动测试
"""

import allure
import pytest

from config.settings import settings
from pages.login_page import LoginPage
from utils.data_loader import TestDataLoader


@allure.feature("登录功能")
class TestLogin:
    """登录功能测试类"""

    @allure.story("正常登录")
    @allure.title("使用标准用户登录成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_with_standard_user(self, login_page: LoginPage):
        """
        测试使用标准用户登录

        步骤:
        1. 打开登录页面
        2. 输入标准用户凭证
        3. 点击登录按钮
        4. 验证登录成功（跳转到商品页面）
        """
        with allure.step("打开登录页面"):
            login_page.open()

        with allure.step("使用标准用户登录"):
            login_page.login(settings.STANDARD_USER, settings.PASSWORD)

        with allure.step("验证登录成功"):
            assert login_page.is_logged_in(), "登录失败，未跳转到商品页面"
            assert "inventory" in login_page.get_current_url()

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
        expected_error = TestDataLoader.get_error_message(error_key)

        allure.dynamic.title(f"登录失败测试：{description}")

        with allure.step("打开登录页面"):
            login_page.open()

        with allure.step(f"使用凭证登录 - {description}"):
            if username:
                login_page.enter_username(username)
            if password:
                login_page.enter_password(password)
            login_page.click_login()

        with allure.step("验证显示正确的错误消息"):
            assert login_page.is_error_displayed(), "未显示错误消息"
            actual_error = login_page.get_error_message()
            assert (
                expected_error.lower() in actual_error.lower()
            ), f"错误消息不匹配\n期望包含: {expected_error}\n实际: {actual_error}"

    @allure.story("登录失败")
    @allure.title("使用被锁定用户登录失败")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    def test_login_with_locked_user(self, login_page: LoginPage):
        """
        测试使用被锁定用户登录（独立测试，验证完整错误消息）
        """
        expected_error = TestDataLoader.get_error_message("locked_user")

        with allure.step("打开登录页面"):
            login_page.open()

        with allure.step("使用被锁定用户登录"):
            login_page.login(settings.LOCKED_USER, settings.PASSWORD)

        with allure.step("验证显示完整错误消息"):
            assert login_page.is_error_displayed(), "未显示错误消息"
            error_message = login_page.get_error_message()
            assert (
                error_message == expected_error
            ), f"错误消息不完全匹配\n期望: {expected_error}\n实际: {error_message}"

    @allure.story("关闭错误提示")
    @allure.title("关闭登录错误提示")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.login
    def test_close_error_message(self, login_page: LoginPage):
        """
        测试关闭错误提示

        步骤:
        1. 打开登录页面
        2. 触发一个登录错误
        3. 关闭错误提示
        4. 验证错误提示已关闭
        """
        with allure.step("打开登录页面并触发错误"):
            login_page.open()
            login_page.click_login()  # 触发空用户名错误

        with allure.step("验证错误消息显示"):
            assert login_page.is_error_displayed(), "未显示错误消息"

        with allure.step("关闭错误提示"):
            login_page.close_error()

        with allure.step("验证错误提示已关闭"):
            assert not login_page.is_error_displayed(), "错误消息未关闭"


@allure.feature("登录功能")
@allure.story("多用户登录")
class TestMultiUserLogin:
    """多用户登录测试类 - 数据驱动测试"""

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.login
    @pytest.mark.parametrize(
        "user_type",
        ["standard_user", "problem_user", "performance_glitch_user"],
        ids=["标准用户", "问题用户", "性能用户"],
    )
    def test_valid_users_can_login(self, login_page: LoginPage, user_type: str):
        """
        数据驱动测试：验证有效用户可以登录
        """
        user_data = TestDataLoader.get_user(user_type)

        allure.dynamic.title(f"验证用户登录：{user_data['description']}")

        with allure.step("打开登录页面"):
            login_page.open()

        with allure.step(f"使用 {user_type} 登录"):
            login_page.login(user_data["username"], user_data["password"])

        with allure.step("验证登录成功"):
            assert login_page.is_logged_in(), f"{user_type} 登录失败"
