"""
Pytest fixtures 配置文件
提供浏览器、页面和页面对象的 fixtures
支持 Session 复用以提高测试效率
支持多角色/多用户测试场景
"""

from collections.abc import Generator
from pathlib import Path
from typing import Callable

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config.settings import settings
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.logger import logger
from utils.session_manager import SessionManager


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
    # 注意: --headed 和 --slowmo 由 pytest-playwright 插件提供，无需重复定义


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
    # 命令行参数优先级高于配置文件
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

    # 命令行参数优先级高于配置文件
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

    # 检查文件是否为空或太小
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
    session_file = _get_session_file(settings.STANDARD_USER)

    # 如果启用 session 复用且 session 文件有效，直接使用
    if reuse_session and _is_session_valid(session_file):
        logger.info(f"复用已保存的 Session: {session_file}")
        yield session_file
        return

    # 如果需要保存 session 或复用 session（但文件不存在），则需要登录并保存
    if save_session or reuse_session:
        logger.info("执行登录以创建 Session...")

        # 创建临时上下文进行登录
        context_config = settings.get_context_config()
        context = browser.new_context(**context_config)
        page = context.new_page()

        try:
            # 执行登录
            login_page = LoginPage(page)
            login_page.open().login_as_standard_user()

            # 等待登录成功（URL 变化）
            page.wait_for_url("**/inventory.html", timeout=settings.TIMEOUT)

            # 保存 session 状态
            context.storage_state(path=str(session_file))
            logger.info(f"Session 已保存到: {session_file}")

            yield session_file
        finally:
            page.close()
            context.close()
    else:
        # 不使用 session 复用
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
        # 使用保存的 session 状态创建上下文
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
def inventory_page(page: Page) -> InventoryPage:
    """
    创建商品列表页面对象

    Args:
        page: 页面实例

    Returns:
        商品列表页面对象
    """
    return InventoryPage(page)


@pytest.fixture(scope="function")
def cart_page(page: Page) -> CartPage:
    """
    创建购物车页面对象

    Args:
        page: 页面实例

    Returns:
        购物车页面对象
    """
    return CartPage(page)


@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Generator[Page, None, None]:
    """
    已登录状态的页面（不使用 session 复用）

    Args:
        page: 页面实例

    Yields:
        已登录的页面实例
    """
    login_page = LoginPage(page)
    login_page.open().login_as_standard_user()
    yield page


@pytest.fixture(scope="function")
def logged_in_inventory_page(logged_in_page: Page) -> InventoryPage:
    """
    已登录状态的商品列表页面（不使用 session 复用）

    Args:
        logged_in_page: 已登录的页面实例

    Returns:
        商品列表页面对象
    """
    return InventoryPage(logged_in_page)


# ==================== 多角色/多用户支持 ====================


@pytest.fixture(scope="function")
def session_manager(
    browser: Browser, reuse_session: bool, save_session: bool
) -> Generator[SessionManager, None, None]:
    """
    Session 管理器 fixture

    用于多角色/多用户测试场景，如审批流程

    使用示例:
        ```python
        def test_approval_workflow(session_manager):
            # 用户提交申请
            user_page = session_manager.get_authenticated_page(
                "standard_user", start_url="https://example.com/submit"
            )
            user_page.click("#submit-btn")

            # 管理员审批
            admin_page = session_manager.get_authenticated_page(
                "admin_user", start_url="https://example.com/approve"
            )
            admin_page.click("#approve-btn")

            # 用户查看结果
            user_page.reload()
            assert user_page.locator("#status").text_content() == "已批准"
        ```

    Args:
        browser: 浏览器实例
        reuse_session: 是否复用 Session
        save_session: 是否保存 Session

    Yields:
        SessionManager 实例
    """
    manager = SessionManager(
        browser=browser,
        reuse_session=reuse_session,
        save_session=save_session,
    )
    yield manager
    manager.close_all()


@pytest.fixture(scope="function")
def user_page_factory(
    browser: Browser, reuse_session: bool, save_session: bool
) -> Generator[Callable[[str, str | None], Page], None, None]:
    """
    用户页面工厂 fixture

    提供一个工厂函数，用于动态创建不同用户的已认证页面

    使用示例:
        ```python
        def test_multi_user(user_page_factory):
            # 创建不同用户的页面
            user1_page = user_page_factory("user1", "password1")
            user2_page = user_page_factory("user2", "password2")

            # 在两个用户间进行交互测试
            user1_page.goto("https://example.com/send-message")
            user1_page.fill("#message", "Hello from user1")
            user1_page.click("#send")

            user2_page.goto("https://example.com/inbox")
            assert "Hello from user1" in user2_page.content()
        ```

    Yields:
        工厂函数，接收 (username, password) 返回 Page
    """
    manager = SessionManager(
        browser=browser,
        reuse_session=reuse_session,
        save_session=save_session,
    )

    def create_user_page(username: str, password: str | None = None) -> Page:
        return manager.get_page_for_user(username, password)

    yield create_user_page
    manager.close_all()


# ==================== 支持 Session 复用的已认证 Page Objects ====================


@pytest.fixture(scope="function")
def auth_inventory_page(auth_page: Page, auth_state: Path | None) -> InventoryPage:
    """
    已认证的商品列表页面（支持 session 复用）

    如果使用了 session 复用，直接访问商品列表页面
    否则先执行登录

    Args:
        auth_page: 已认证的页面实例
        auth_state: session 状态路径

    Returns:
        商品列表页面对象
    """
    if auth_state and _is_session_valid(auth_state):
        # 有有效的 session，直接访问商品列表页
        auth_page.goto(f"{settings.BASE_URL}/inventory.html")
    else:
        # 没有 session，需要先登录
        login_page = LoginPage(auth_page)
        login_page.open().login_as_standard_user()

    return InventoryPage(auth_page)


@pytest.fixture(scope="function")
def auth_cart_page(auth_page: Page, auth_state: Path | None) -> CartPage:
    """
    已认证的购物车页面（支持 session 复用）

    如果使用了 session 复用，直接访问购物车页面
    否则先执行登录

    Args:
        auth_page: 已认证的页面实例
        auth_state: session 状态路径

    Returns:
        购物车页面对象
    """
    if auth_state and _is_session_valid(auth_state):
        # 有有效的 session，直接访问购物车页
        auth_page.goto(f"{settings.BASE_URL}/cart.html")
    else:
        # 没有 session，需要先登录再跳转
        login_page = LoginPage(auth_page)
        login_page.open().login_as_standard_user()
        auth_page.goto(f"{settings.BASE_URL}/cart.html")

    return CartPage(auth_page)


# Hooks
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试报告钩子，用于在测试失败时自动截图
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 获取 page fixture
        page = item.funcargs.get("page")
        if page and settings.SCREENSHOT_ON_FAILURE:
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot, name="失败截图", attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass  # 忽略截图失败


def pytest_configure(config):
    """pytest 配置钩子"""
    # 添加自定义标记说明
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "login: 登录相关测试")
    config.addinivalue_line("markers", "cart: 购物车相关测试")
