"""
Pytest fixtures 配置文件
提供浏览器、页面和页面对象的 fixtures
"""
import pytest
import allure
from typing import Generator
from playwright.sync_api import Page, Browser, BrowserContext, Playwright, sync_playwright

from config.settings import settings
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption(
        "--browser-type",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to run tests: chromium, firefox, or webkit"
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
def playwright_instance() -> Generator[Playwright, None, None]:
    """创建 Playwright 实例"""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(
    playwright_instance: Playwright, 
    browser_type_name: str,
    is_headed: bool,
    slow_mo: int
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
    
    browser = browser_type.launch(
        headless=headless,
        slow_mo=slow_mo_value
    )
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
    已登录状态的页面
    
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
    已登录状态的商品列表页面
    
    Args:
        logged_in_page: 已登录的页面实例
        
    Returns:
        商品列表页面对象
    """
    return InventoryPage(logged_in_page)


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
                    screenshot,
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
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
