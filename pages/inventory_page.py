"""
InventoryPage - 商品列表页面对象
封装 saucedemo.com 商品列表页面的元素和操作
"""
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from config.settings import settings


class InventoryPage(BasePage):
    """商品列表页面对象"""
    
    # 页面名称
    page_name = "InventoryPage"
    
    # 页面元素定位器
    INVENTORY_CONTAINER = "#inventory_container"
    INVENTORY_ITEM = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    INVENTORY_ITEM_DESC = ".inventory_item_desc"
    ADD_TO_CART_BUTTON = "[data-test^='add-to-cart']"
    REMOVE_BUTTON = "[data-test^='remove']"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    BURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"
    CLOSE_MENU = "#react-burger-cross-btn"
    
    # 排序选项
    SORT_AZ = "az"
    SORT_ZA = "za"
    SORT_LOW_HIGH = "lohi"
    SORT_HIGH_LOW = "hilo"
    
    def __init__(self, page: Page):
        """
        初始化商品列表页面
        
        Args:
            page: Playwright 页面实例
        """
        super().__init__(page)
        self.url = f"{settings.BASE_URL}/inventory.html"
    
    @allure.step("打开商品列表页面")
    def open(self) -> "InventoryPage":
        """
        打开商品列表页面
        
        Returns:
            self，支持链式调用
        """
        self.navigate(self.url)
        return self
    
    def is_on_inventory_page(self) -> bool:
        """
        检查是否在商品列表页面
        
        Returns:
            是否在商品列表页面
        """
        return self.is_visible(self.INVENTORY_CONTAINER, timeout=5000)
    
    def get_product_count(self) -> int:
        """
        获取商品数量
        
        Returns:
            商品数量
        """
        return self.get_element_count(self.INVENTORY_ITEM)
    
    def get_all_product_names(self) -> list[str]:
        """
        获取所有商品名称
        
        Returns:
            商品名称列表
        """
        return self.get_all_texts(self.INVENTORY_ITEM_NAME)
    
    def get_all_product_prices(self) -> list[str]:
        """
        获取所有商品价格
        
        Returns:
            商品价格列表
        """
        return self.get_all_texts(self.INVENTORY_ITEM_PRICE)
    
    @allure.step("添加第 {index} 个商品到购物车")
    def add_product_to_cart_by_index(self, index: int = 0) -> "InventoryPage":
        """
        按索引添加商品到购物车
        
        Args:
            index: 商品索引（从 0 开始）
            
        Returns:
            self，支持链式调用
            
        Raises:
            IndexError: 索引超出范围
            ValueError: 索引为负数
        """
        from utils.logger import logger
        
        if index < 0:
            logger.error(f"[{self.page_name}] 无效索引: {index}，索引不能为负数")
            raise ValueError(f"索引不能为负数: {index}")
        
        add_buttons = self.page.locator(self.ADD_TO_CART_BUTTON)
        count = add_buttons.count()
        
        if index >= count:
            logger.error(f"[{self.page_name}] 索引 {index} 超出范围，当前共 {count} 个可添加商品")
            raise IndexError(f"索引 {index} 超出范围，当前共 {count} 个可添加商品")
        
        add_buttons.nth(index).click()
        logger.info(f"[{self.page_name}] 已添加第 {index} 个商品到购物车")
        return self
    
    @allure.step("添加商品到购物车: {product_name}")
    def add_product_to_cart_by_name(self, product_name: str) -> "InventoryPage":
        """
        按商品名称添加到购物车
        
        Args:
            product_name: 商品名称
            
        Returns:
            self，支持链式调用
        """
        # 构建商品对应的添加按钮定位器
        # saucedemo 的按钮 data-test 格式: add-to-cart-{product-name-with-dashes}
        button_id = product_name.lower().replace(" ", "-")
        button_locator = f"[data-test='add-to-cart-{button_id}']"
        self.click(button_locator)
        return self
    
    @allure.step("从购物车移除商品: {product_name}")
    def remove_product_from_cart_by_name(self, product_name: str) -> "InventoryPage":
        """
        按商品名称从购物车移除
        
        Args:
            product_name: 商品名称
            
        Returns:
            self，支持链式调用
        """
        button_id = product_name.lower().replace(" ", "-")
        button_locator = f"[data-test='remove-{button_id}']"
        self.click(button_locator)
        return self
    
    def get_cart_count(self) -> int:
        """
        获取购物车中的商品数量
        
        Returns:
            购物车商品数量
        """
        if self.is_visible(self.SHOPPING_CART_BADGE, timeout=2000):
            badge_text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(badge_text) if badge_text else 0
        return 0
    
    @allure.step("点击购物车图标")
    def click_cart(self) -> "InventoryPage":
        """
        点击购物车图标
        
        Returns:
            self，支持链式调用
        """
        self.click(self.SHOPPING_CART_LINK)
        return self
    
    @allure.step("排序商品: {sort_option}")
    def sort_products(self, sort_option: str) -> "InventoryPage":
        """
        排序商品
        
        Args:
            sort_option: 排序选项（az, za, lohi, hilo）
            
        Returns:
            self，支持链式调用
        """
        self.select_option(self.SORT_DROPDOWN, sort_option)
        return self
    
    @allure.step("打开菜单")
    def open_menu(self) -> "InventoryPage":
        """
        打开侧边菜单
        
        Returns:
            self，支持链式调用
        """
        self.click(self.BURGER_MENU)
        self.wait_for_visible(self.LOGOUT_LINK)
        return self
    
    @allure.step("关闭菜单")
    def close_menu(self) -> "InventoryPage":
        """
        关闭侧边菜单
        
        Returns:
            self，支持链式调用
        """
        self.click(self.CLOSE_MENU)
        return self
    
    @allure.step("退出登录")
    def logout(self) -> "InventoryPage":
        """
        退出登录
        
        Returns:
            self，支持链式调用
        """
        self.open_menu()
        self.click(self.LOGOUT_LINK)
        return self
