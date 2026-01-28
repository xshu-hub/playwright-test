"""
DashboardPage - OrangeHRM 仪表盘页面对象
封装 OrangeHRM 仪表盘页面的元素和操作，包括侧边栏导航
"""

import allure
from playwright.sync_api import Page

from config.settings import settings
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """OrangeHRM 仪表盘页面对象"""

    # 页面名称
    page_name = "DashboardPage"

    # 顶部栏元素
    HEADER_TITLE = ".oxd-topbar-header-title"
    USER_DROPDOWN = ".oxd-userdropdown"
    USER_DROPDOWN_MENU = ".oxd-dropdown-menu"
    LOGOUT_LINK = "a:has-text('Logout')"
    PROFILE_LINK = "a:has-text('About')"

    # 侧边栏导航
    SIDEBAR = ".oxd-sidepanel"
    SIDEBAR_TOGGLE = ".oxd-sidepanel-header"
    SEARCH_INPUT = ".oxd-main-menu-search input"

    # 侧边栏菜单项
    MENU_ADMIN = "a.oxd-main-menu-item:has-text('Admin')"
    MENU_PIM = "a.oxd-main-menu-item:has-text('PIM')"
    MENU_LEAVE = "a.oxd-main-menu-item:has-text('Leave')"
    MENU_TIME = "a.oxd-main-menu-item:has-text('Time')"
    MENU_RECRUITMENT = "a.oxd-main-menu-item:has-text('Recruitment')"
    MENU_MY_INFO = "a.oxd-main-menu-item:has-text('My Info')"
    MENU_PERFORMANCE = "a.oxd-main-menu-item:has-text('Performance')"
    MENU_DASHBOARD = "a.oxd-main-menu-item:has-text('Dashboard')"
    MENU_DIRECTORY = "a.oxd-main-menu-item:has-text('Directory')"
    MENU_MAINTENANCE = "a.oxd-main-menu-item:has-text('Maintenance')"
    MENU_CLAIM = "a.oxd-main-menu-item:has-text('Claim')"
    MENU_BUZZ = "a.oxd-main-menu-item:has-text('Buzz')"

    # 仪表盘内容区域
    DASHBOARD_GRID = ".orangehrm-dashboard-grid"
    QUICK_LAUNCH = ".orangehrm-quick-launch"
    QUICK_LAUNCH_CARD = ".orangehrm-quick-launch-card"

    # 加载指示器
    LOADER = ".oxd-loading-spinner"

    def __init__(self, page: Page):
        """
        初始化仪表盘页面

        Args:
            page: Playwright 页面实例
        """
        super().__init__(page)
        self.url = f"{settings.BASE_URL}/web/index.php/dashboard/index"

    @allure.step("打开仪表盘页面")
    def open(self) -> "DashboardPage":
        """
        打开仪表盘页面

        Returns:
            self，支持链式调用
        """
        self.navigate(self.url)
        self.wait_for_page_load()
        return self

    def wait_for_page_load(self) -> "DashboardPage":
        """
        等待页面加载完成

        Returns:
            self，支持链式调用
        """
        # 等待加载器消失
        self.is_hidden(self.LOADER, timeout=10000)
        # 等待侧边栏可见
        self.wait_for_visible(self.SIDEBAR)
        return self

    def is_on_dashboard(self) -> bool:
        """
        检查是否在仪表盘页面

        Returns:
            是否在仪表盘页面
        """
        return self.is_visible(self.DASHBOARD_GRID, timeout=5000) or "dashboard" in self.get_current_url()

    # ==================== 导航方法 ====================

    @allure.step("点击用户下拉菜单")
    def click_user_dropdown(self) -> "DashboardPage":
        """
        点击用户下拉菜单

        Returns:
            self，支持链式调用
        """
        self.click(self.USER_DROPDOWN)
        self.wait_for_visible(self.USER_DROPDOWN_MENU)
        return self

    @allure.step("退出登录")
    def logout(self) -> "DashboardPage":
        """
        退出登录

        Returns:
            self，支持链式调用
        """
        self.click_user_dropdown()
        self.click(self.LOGOUT_LINK)
        return self

    @allure.step("导航到 Admin 模块")
    def go_to_admin(self) -> "DashboardPage":
        """
        导航到 Admin 模块

        Returns:
            self，支持链式调用
        """
        self.click(self.MENU_ADMIN)
        self.wait_for_page_load()
        return self

    @allure.step("导航到 PIM 模块")
    def go_to_pim(self) -> "DashboardPage":
        """
        导航到 PIM（人员信息管理）模块

        Returns:
            self，支持链式调用
        """
        self.click(self.MENU_PIM)
        self.wait_for_page_load()
        return self

    @allure.step("导航到 Leave 模块")
    def go_to_leave(self) -> "DashboardPage":
        """
        导航到 Leave（假期）模块

        Returns:
            self，支持链式调用
        """
        self.click(self.MENU_LEAVE)
        self.wait_for_page_load()
        return self

    @allure.step("导航到 Time 模块")
    def go_to_time(self) -> "DashboardPage":
        """
        导航到 Time（考勤）模块

        Returns:
            self，支持链式调用
        """
        self.click(self.MENU_TIME)
        self.wait_for_page_load()
        return self

    @allure.step("导航到 Recruitment 模块")
    def go_to_recruitment(self) -> "DashboardPage":
        """
        导航到 Recruitment（招聘）模块

        Returns:
            self，支持链式调用
        """
        self.click(self.MENU_RECRUITMENT)
        self.wait_for_page_load()
        return self

    @allure.step("导航到 My Info")
    def go_to_my_info(self) -> "DashboardPage":
        """
        导航到 My Info（我的信息）

        Returns:
            self，支持链式调用
        """
        self.click(self.MENU_MY_INFO)
        self.wait_for_page_load()
        return self

    @allure.step("导航到 Dashboard")
    def go_to_dashboard(self) -> "DashboardPage":
        """
        导航到 Dashboard（仪表盘）

        Returns:
            self，支持链式调用
        """
        self.click(self.MENU_DASHBOARD)
        self.wait_for_page_load()
        return self

    @allure.step("导航到 Directory")
    def go_to_directory(self) -> "DashboardPage":
        """
        导航到 Directory（通讯录）

        Returns:
            self，支持链式调用
        """
        self.click(self.MENU_DIRECTORY)
        self.wait_for_page_load()
        return self

    @allure.step("在菜单中搜索: {keyword}")
    def search_menu(self, keyword: str) -> "DashboardPage":
        """
        在侧边栏中搜索菜单

        Args:
            keyword: 搜索关键词

        Returns:
            self，支持链式调用
        """
        self.fill(self.SEARCH_INPUT, keyword)
        return self

    def get_visible_menu_items(self) -> list[str]:
        """
        获取当前可见的菜单项

        Returns:
            菜单项文本列表
        """
        return self.get_all_texts(".oxd-main-menu-item span")

    # ==================== 快速启动区域 ====================

    def get_quick_launch_cards(self) -> list[str]:
        """
        获取快速启动卡片标题

        Returns:
            卡片标题列表
        """
        return self.get_all_texts(f"{self.QUICK_LAUNCH_CARD} p")

    @allure.step("点击快速启动卡片: {card_name}")
    def click_quick_launch(self, card_name: str) -> "DashboardPage":
        """
        点击快速启动卡片

        Args:
            card_name: 卡片名称

        Returns:
            self，支持链式调用
        """
        card_selector = f"{self.QUICK_LAUNCH_CARD}:has-text('{card_name}')"
        self.click(card_selector)
        self.wait_for_page_load()
        return self
