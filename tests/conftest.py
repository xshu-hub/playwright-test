"""
Pytest fixtures 配置文件
提供浏览器、页面和页面对象的 fixtures
针对 OrangeHRM 人力资源管理系统
"""

from collections.abc import Generator
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config.settings import settings
from pages.dashboard_page import DashboardPage
from pages.employee_form_page import EmployeeFormPage
from pages.login_page import LoginPage
from pages.pim_page import PIMPage
from utils.logger import logger


def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption(
        "--browser-type",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to run tests: chromium, firefox, or webkit",
    )
    parser.addoption(
        "--reuse-session",
        action="store_true",
        default=False,
        help="Reuse saved session state to skip login (speeds up tests)",
    )
    parser.addoption(
        "--save-session",
        action="store_true",
        default=False,
        help="Save session state after login for future reuse",
    )


@pytest.fixture(scope="session")
def browser_type_name(request) -> str:
    """获取浏览器类型名称"""
    return request.config.getoption("--browser-type")


@pytest.fixture(scope="session")
def is_headed(request) -> bool:
    """获取是否有头模式（由 pytest-playwright 提供）"""
    return request.config.getoption("--headed", default=False)


@pytest.fixture(scope="session")
def slow_mo(request) -> int:
    """获取慢动作延迟时间（由 pytest-playwright 提供）"""
    return request.config.getoption("--slowmo", default=0)


@pytest.fixture(scope="session")
def reuse_session(request) -> bool:
    """获取是否复用 Session"""
    cli_option = request.config.getoption("--reuse-session", default=False)
    return cli_option or settings.REUSE_SESSION


@pytest.fixture(scope="session")
def save_session(request) -> bool:
    """获取是否保存 Session"""
    return request.config.getoption("--save-session", default=False)


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """创建 Playwright 实例"""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(
    playwright_instance: Playwright, browser_type_name: str, is_headed: bool, slow_mo: int
) -> Generator[Browser, None, None]:
    """
    创建浏览器实例

    Args:
        playwright_instance: Playwright 实例
        browser_type_name: 浏览器类型名称
        is_headed: 是否有头模式
        slow_mo: 慢动作延迟时间

    Yields:
        浏览器实例
    """
    browser_type = getattr(playwright_instance, browser_type_name)

    headless = not is_headed and settings.HEADLESS
    slow_mo_value = slow_mo if slow_mo > 0 else settings.SLOW_MO

    browser = browser_type.launch(headless=headless, slow_mo=slow_mo_value)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    创建浏览器上下文

    Args:
        browser: 浏览器实例

    Yields:
        浏览器上下文
    """
    context_config = settings.get_context_config()
    context = browser.new_context(**context_config)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    创建页面实例

    Args:
        context: 浏览器上下文

    Yields:
        页面实例
    """
    page = context.new_page()
    page.set_default_timeout(settings.TIMEOUT)
    yield page
    page.close()


# ==================== Session 复用相关 Fixtures ====================


def _get_session_file(username: str | None = None) -> Path:
    """获取 session 文件路径"""
    return settings.get_session_file_path(username)


def _is_session_valid(session_file: Path) -> bool:
    """
    检查 session 文件是否存在且有效

    Args:
        session_file: session 文件路径

    Returns:
        session 是否有效
    """
    if not session_file.exists():
        return False

    if session_file.stat().st_size < 10:
        return False

    return True


@pytest.fixture(scope="session")
def auth_state(
    browser: Browser, reuse_session: bool, save_session: bool
) -> Generator[Path | None, None, None]:
    """
    管理认证状态的 session 级别 fixture

    此 fixture 负责：
    1. 检查是否存在可复用的 session
    2. 如果不存在或不复用，则执行登录并保存 session
    3. 返回 session 文件路径供其他 fixtures 使用

    Args:
        browser: 浏览器实例
        reuse_session: 是否复用已保存的 session
        save_session: 是否保存 session

    Yields:
        session 文件路径，如果不使用 session 复用则为 None
    """
    session_file = _get_session_file(settings.ADMIN_USER)

    if reuse_session and _is_session_valid(session_file):
        logger.info(f"复用已保存的 Session: {session_file}")
        yield session_file
        return

    if save_session or reuse_session:
        logger.info("执行登录以创建 Session...")

        context_config = settings.get_context_config()
        context = browser.new_context(**context_config)
        page = context.new_page()

        try:
            login_page = LoginPage(page)
            login_page.open().login_as_admin()

            # 等待登录成功
            page.wait_for_url("**/dashboard/**", timeout=settings.TIMEOUT)

            context.storage_state(path=str(session_file))
            logger.info(f"Session 已保存到: {session_file}")

            yield session_file
        finally:
            page.close()
            context.close()
    else:
        yield None


@pytest.fixture(scope="function")
def auth_context(
    browser: Browser, auth_state: Path | None
) -> Generator[BrowserContext, None, None]:
    """
    创建已认证的浏览器上下文

    如果有可用的 session 状态，则从该状态创建上下文（无需登录）
    否则创建普通上下文

    Args:
        browser: 浏览器实例
        auth_state: session 文件路径

    Yields:
        已认证的浏览器上下文
    """
    context_config = settings.get_context_config()

    if auth_state and _is_session_valid(auth_state):
        context_config["storage_state"] = str(auth_state)
        logger.debug("使用保存的 Session 状态创建上下文")

    context = browser.new_context(**context_config)
    yield context
    context.close()


@pytest.fixture(scope="function")
def auth_page(auth_context: BrowserContext) -> Generator[Page, None, None]:
    """
    创建已认证的页面实例

    此页面已经处于登录状态（如果使用了 session 复用）

    Args:
        auth_context: 已认证的浏览器上下文

    Yields:
        已认证的页面实例
    """
    page = auth_context.new_page()
    page.set_default_timeout(settings.TIMEOUT)
    yield page
    page.close()


# ==================== 页面对象 Fixtures ====================


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """
    创建登录页面对象

    Args:
        page: 页面实例

    Returns:
        登录页面对象
    """
    return LoginPage(page)


@pytest.fixture(scope="function")
def dashboard_page(page: Page) -> DashboardPage:
    """
    创建仪表盘页面对象

    Args:
        page: 页面实例

    Returns:
        仪表盘页面对象
    """
    return DashboardPage(page)


@pytest.fixture(scope="function")
def pim_page(page: Page) -> PIMPage:
    """
    创建 PIM 页面对象

    Args:
        page: 页面实例

    Returns:
        PIM 页面对象
    """
    return PIMPage(page)


@pytest.fixture(scope="function")
def employee_form_page(page: Page) -> EmployeeFormPage:
    """
    创建员工表单页面对象

    Args:
        page: 页面实例

    Returns:
        员工表单页面对象
    """
    return EmployeeFormPage(page)


# ==================== 已登录状态的页面 Fixtures ====================


@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Generator[Page, None, None]:
    """
    已登录状态的页面

    Args:
        page: 页面实例

    Yields:
        已登录的页面实例
    """
    login_page = LoginPage(page)
    login_page.open().login_as_admin()
    login_page.wait_for_login_complete()
    yield page


@pytest.fixture(scope="function")
def logged_in_dashboard(logged_in_page: Page) -> DashboardPage:
    """
    已登录状态的仪表盘页面

    Args:
        logged_in_page: 已登录的页面实例

    Returns:
        仪表盘页面对象
    """
    return DashboardPage(logged_in_page)


@pytest.fixture(scope="function")
def logged_in_pim(logged_in_page: Page) -> PIMPage:
    """
    已登录状态的 PIM 页面

    Args:
        logged_in_page: 已登录的页面实例

    Returns:
        PIM 页面对象
    """
    pim = PIMPage(logged_in_page)
    pim.open()
    return pim


@pytest.fixture(scope="function")
def employee_form(logged_in_page: Page) -> EmployeeFormPage:
    """
    已登录状态下的员工表单页面
    （导航到添加员工页面）

    Args:
        logged_in_page: 已登录的页面实例

    Returns:
        员工表单页面对象
    """
    pim = PIMPage(logged_in_page)
    pim.open()
    pim.click_add_employee_tab()
    return EmployeeFormPage(logged_in_page)


# ==================== Hooks ====================


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试报告钩子，用于在测试失败时自动截图
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
        if page and settings.SCREENSHOT_ON_FAILURE:
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot, name="失败截图", attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass


def pytest_configure(config):
    """pytest 配置钩子"""
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "login: 登录相关测试")
    config.addinivalue_line("markers", "pim: PIM 员工管理相关测试")
    config.addinivalue_line("markers", "e2e: 端到端测试")
