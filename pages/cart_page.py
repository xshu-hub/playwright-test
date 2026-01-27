"""
CartPage - 购物车页面对象
封装 saucedemo.com 购物车页面的元素和操作
"""
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage
from config.settings import settings


class CartPage(BasePage):
    """购物车页面对象"""
    
    # 页面名称
    page_name = "CartPage"
    
    # 页面元素定位器
    CART_CONTAINER = "#cart_contents_container"
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    CART_ITEM_QUANTITY = ".cart_quantity"
    REMOVE_BUTTON = "[data-test^='remove']"
    CONTINUE_SHOPPING_BUTTON = "[data-test='continue-shopping']"
    CHECKOUT_BUTTON = "[data-test='checkout']"
    
    # 结账页面元素
    FIRST_NAME_INPUT = "[data-test='firstName']"
    LAST_NAME_INPUT = "[data-test='lastName']"
    POSTAL_CODE_INPUT = "[data-test='postalCode']"
    CONTINUE_BUTTON = "[data-test='continue']"
    CANCEL_BUTTON = "[data-test='cancel']"
    FINISH_BUTTON = "[data-test='finish']"
    BACK_HOME_BUTTON = "[data-test='back-to-products']"
    
    # 结账完成页面
    CHECKOUT_COMPLETE = "#checkout_complete_container"
    COMPLETE_HEADER = ".complete-header"
    
    # 错误消息
    ERROR_MESSAGE = "[data-test='error']"
    
    def __init__(self, page: Page):
        """
        初始化购物车页面
        
        Args:
            page: Playwright 页面实例
        """
        super().__init__(page)
        self.url = f"{settings.BASE_URL}/cart.html"
    
    @allure.step("打开购物车页面")
    def open(self) -> "CartPage":
        """
        打开购物车页面
        
        Returns:
            self，支持链式调用
        """
        self.navigate(self.url)
        return self
    
    def is_on_cart_page(self) -> bool:
        """
        检查是否在购物车页面
        
        Returns:
            是否在购物车页面
        """
        return self.is_visible(self.CART_CONTAINER, timeout=5000)
    
    def get_cart_items_count(self) -> int:
        """
        获取购物车中的商品数量
        
        Returns:
            商品数量
        """
        return self.get_element_count(self.CART_ITEM)
    
    def get_cart_item_names(self) -> list[str]:
        """
        获取购物车中所有商品的名称
        
        Returns:
            商品名称列表
        """
        return self.get_all_texts(self.CART_ITEM_NAME)
    
    def get_cart_item_prices(self) -> list[str]:
        """
        获取购物车中所有商品的价格
        
        Returns:
            商品价格列表
        """
        return self.get_all_texts(self.CART_ITEM_PRICE)
    
    @allure.step("移除第 {index} 个商品")
    def remove_item_by_index(self, index: int = 0) -> "CartPage":
        """
        按索引移除商品
        
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
        
        remove_buttons = self.page.locator(self.REMOVE_BUTTON)
        count = remove_buttons.count()
        
        if index >= count:
            logger.error(f"[{self.page_name}] 索引 {index} 超出范围，当前购物车共 {count} 个商品")
            raise IndexError(f"索引 {index} 超出范围，当前购物车共 {count} 个商品")
        
        remove_buttons.nth(index).click()
        logger.info(f"[{self.page_name}] 已移除第 {index} 个商品")
        return self
    
    @allure.step("移除商品: {product_name}")
    def remove_item_by_name(self, product_name: str) -> "CartPage":
        """
        按商品名称移除
        
        Args:
            product_name: 商品名称
            
        Returns:
            self，支持链式调用
        """
        button_id = product_name.lower().replace(" ", "-")
        button_locator = f"[data-test='remove-{button_id}']"
        self.click(button_locator)
        return self
    
    @allure.step("继续购物")
    def continue_shopping(self) -> "CartPage":
        """
        点击继续购物按钮
        
        Returns:
            self，支持链式调用
        """
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        return self
    
    @allure.step("点击结账")
    def checkout(self) -> "CartPage":
        """
        点击结账按钮
        
        Returns:
            self，支持链式调用
        """
        self.click(self.CHECKOUT_BUTTON)
        return self
    
    @allure.step("填写收货信息")
    def fill_checkout_info(
        self, 
        first_name: str, 
        last_name: str, 
        postal_code: str
    ) -> "CartPage":
        """
        填写结账信息
        
        Args:
            first_name: 名
            last_name: 姓
            postal_code: 邮编
            
        Returns:
            self，支持链式调用
        """
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)
        return self
    
    @allure.step("继续结账")
    def continue_checkout(self) -> "CartPage":
        """
        点击继续按钮（填写信息后）
        
        Returns:
            self，支持链式调用
        """
        self.click(self.CONTINUE_BUTTON)
        return self
    
    @allure.step("完成订单")
    def finish_checkout(self) -> "CartPage":
        """
        点击完成按钮
        
        Returns:
            self，支持链式调用
        """
        self.click(self.FINISH_BUTTON)
        return self
    
    @allure.step("返回首页")
    def back_to_home(self) -> "CartPage":
        """
        点击返回首页按钮
        
        Returns:
            self，支持链式调用
        """
        self.click(self.BACK_HOME_BUTTON)
        return self
    
    def is_checkout_complete(self) -> bool:
        """
        检查是否完成结账
        
        Returns:
            是否完成结账
        """
        return self.is_visible(self.CHECKOUT_COMPLETE, timeout=5000)
    
    def get_complete_header(self) -> str:
        """
        获取结账完成的标题文本
        
        Returns:
            标题文本
        """
        return self.get_text(self.COMPLETE_HEADER)
    
    def get_error_message(self) -> str:
        """
        获取错误消息
        
        Returns:
            错误消息文本
        """
        if self.is_visible(self.ERROR_MESSAGE, timeout=3000):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def is_cart_empty(self) -> bool:
        """
        检查购物车是否为空
        
        Returns:
            购物车是否为空
        """
        return self.get_cart_items_count() == 0
