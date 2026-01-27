"""
购物车功能测试用例
测试 saucedemo.com 的购物车功能
支持数据驱动测试
"""
import pytest
import allure
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.data_loader import TestDataLoader


@allure.feature("购物车功能")
class TestCart:
    """购物车功能测试类"""
    
    @allure.story("添加商品")
    @allure.title("添加单个商品到购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_single_item_to_cart(self, logged_in_inventory_page: InventoryPage):
        """
        测试添加单个商品到购物车
        
        步骤:
        1. 登录后进入商品列表页面
        2. 添加第一个商品到购物车
        3. 验证购物车数量变为 1
        """
        inventory_page = logged_in_inventory_page
        
        with allure.step("验证在商品列表页面"):
            assert inventory_page.is_on_inventory_page(), "未进入商品列表页面"
        
        with allure.step("获取初始购物车数量"):
            initial_count = inventory_page.get_cart_count()
            assert initial_count == 0, "购物车初始不为空"
        
        with allure.step("添加第一个商品到购物车"):
            inventory_page.add_product_to_cart_by_index(0)
        
        with allure.step("验证购物车数量增加"):
            new_count = inventory_page.get_cart_count()
            assert new_count == 1, f"购物车数量应为 1，实际为 {new_count}"
    
    @allure.story("添加商品")
    @allure.title("添加多个商品到购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.cart
    def test_add_multiple_items_to_cart(self, logged_in_inventory_page: InventoryPage):
        """
        测试添加多个商品到购物车
        
        步骤:
        1. 登录后进入商品列表页面
        2. 添加多个商品到购物车
        3. 验证购物车数量正确
        """
        inventory_page = logged_in_inventory_page
        products = TestDataLoader.get_products()
        
        with allure.step(f"添加 3 个商品到购物车"):
            for i in range(min(3, len(products))):
                inventory_page.add_product_to_cart_by_index(i)
        
        with allure.step("验证购物车数量"):
            cart_count = inventory_page.get_cart_count()
            assert cart_count == 3, f"购物车数量应为 3，实际为 {cart_count}"
    
    @allure.story("添加商品")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    @pytest.mark.parametrize(
        "product_index",
        [0, 1, 2],
        ids=["第一个商品", "第二个商品", "第三个商品"]
    )
    def test_add_specific_product_to_cart(
        self,
        logged_in_inventory_page: InventoryPage,
        cart_page: CartPage,
        product_index: int
    ):
        """
        数据驱动测试：添加指定商品到购物车并验证
        """
        inventory_page = logged_in_inventory_page
        product_data = TestDataLoader.get_product_by_index(product_index)
        product_name = product_data["name"]
        
        allure.dynamic.title(f"添加商品到购物车：{product_name}")
        
        with allure.step(f"添加商品 {product_name} 到购物车"):
            inventory_page.add_product_to_cart_by_name(product_name)
        
        with allure.step("进入购物车页面"):
            inventory_page.click_cart()
        
        with allure.step("验证商品在购物车中"):
            cart_items = cart_page.get_cart_item_names()
            assert product_name in cart_items, f"商品 {product_name} 未在购物车中"
    
    @allure.story("移除商品")
    @allure.title("从商品列表页移除购物车商品")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.cart
    def test_remove_item_from_inventory_page(self, logged_in_inventory_page: InventoryPage):
        """
        测试从商品列表页移除购物车中的商品
        """
        inventory_page = logged_in_inventory_page
        product_data = TestDataLoader.get_product_by_index(0)
        product_name = product_data["name"]
        
        with allure.step(f"添加商品 {product_name} 到购物车"):
            inventory_page.add_product_to_cart_by_name(product_name)
        
        with allure.step("验证商品已添加"):
            assert inventory_page.get_cart_count() == 1
        
        with allure.step("移除商品"):
            inventory_page.remove_product_from_cart_by_name(product_name)
        
        with allure.step("验证购物车为空"):
            assert inventory_page.get_cart_count() == 0, "购物车应该为空"
    
    @allure.story("移除商品")
    @allure.title("从购物车页面移除商品")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.cart
    def test_remove_item_from_cart_page(
        self, 
        logged_in_inventory_page: InventoryPage,
        cart_page: CartPage
    ):
        """
        测试从购物车页面移除商品
        """
        inventory_page = logged_in_inventory_page
        
        with allure.step("添加商品到购物车"):
            inventory_page.add_product_to_cart_by_index(0)
            inventory_page.add_product_to_cart_by_index(1)
        
        with allure.step("进入购物车页面"):
            inventory_page.click_cart()
            assert cart_page.is_on_cart_page(), "未进入购物车页面"
        
        with allure.step("验证购物车有 2 个商品"):
            assert cart_page.get_cart_items_count() == 2
        
        with allure.step("移除第一个商品"):
            cart_page.remove_item_by_index(0)
        
        with allure.step("验证购物车剩余 1 个商品"):
            assert cart_page.get_cart_items_count() == 1
    
    @allure.story("购物车查看")
    @allure.title("查看购物车中的商品")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_view_cart_items(
        self, 
        logged_in_inventory_page: InventoryPage,
        cart_page: CartPage
    ):
        """
        测试查看购物车中的商品详情
        """
        inventory_page = logged_in_inventory_page
        product_data = TestDataLoader.get_product_by_index(0)
        product_name = product_data["name"]
        
        with allure.step(f"添加商品 {product_name} 到购物车"):
            inventory_page.add_product_to_cart_by_name(product_name)
        
        with allure.step("进入购物车页面"):
            inventory_page.click_cart()
        
        with allure.step("验证商品在购物车中"):
            cart_items = cart_page.get_cart_item_names()
            assert product_name in cart_items, f"商品 {product_name} 未在购物车中"
    
    @allure.story("继续购物")
    @allure.title("从购物车返回继续购物")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_continue_shopping(
        self, 
        logged_in_inventory_page: InventoryPage,
        cart_page: CartPage
    ):
        """
        测试从购物车返回继续购物
        """
        inventory_page = logged_in_inventory_page
        
        with allure.step("进入购物车页面"):
            inventory_page.click_cart()
            assert cart_page.is_on_cart_page()
        
        with allure.step("点击继续购物"):
            cart_page.continue_shopping()
        
        with allure.step("验证返回商品列表页面"):
            assert inventory_page.is_on_inventory_page(), "未返回商品列表页面"


@allure.feature("购物车功能")
@allure.story("结账流程")
class TestCheckout:
    """结账流程测试类 - 数据驱动测试"""
    
    @allure.title("完整结账流程")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_checkout_flow(
        self, 
        logged_in_inventory_page: InventoryPage,
        cart_page: CartPage
    ):
        """
        测试完整的结账流程（使用测试数据）
        """
        inventory_page = logged_in_inventory_page
        checkout_info = TestDataLoader.get_checkout_info("valid")
        
        with allure.step("添加商品到购物车"):
            inventory_page.add_product_to_cart_by_index(0)
        
        with allure.step("进入购物车并点击结账"):
            inventory_page.click_cart()
            cart_page.checkout()
        
        with allure.step("填写收货信息"):
            cart_page.fill_checkout_info(
                first_name=checkout_info["first_name"],
                last_name=checkout_info["last_name"],
                postal_code=checkout_info["postal_code"]
            )
            cart_page.continue_checkout()
        
        with allure.step("完成订单"):
            cart_page.finish_checkout()
        
        with allure.step("验证订单完成"):
            assert cart_page.is_checkout_complete(), "订单未完成"
            complete_header = cart_page.get_complete_header()
            assert "thank you" in complete_header.lower(), f"完成消息不正确: {complete_header}"
    
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    @pytest.mark.parametrize(
        "missing_field, error_key",
        [
            ("first_name", "empty_first_name"),
            ("last_name", "empty_last_name"),
            ("postal_code", "empty_postal_code"),
        ],
        ids=["缺少姓名", "缺少姓氏", "缺少邮编"]
    )
    def test_checkout_validation(
        self,
        logged_in_inventory_page: InventoryPage,
        cart_page: CartPage,
        missing_field: str,
        error_key: str
    ):
        """
        数据驱动测试：结账时必填字段验证
        """
        inventory_page = logged_in_inventory_page
        checkout_info = TestDataLoader.get_checkout_info("valid").copy()
        expected_error = TestDataLoader.get_error_message(error_key)
        
        # 清空指定字段
        checkout_info[missing_field] = ""
        
        allure.dynamic.title(f"结账验证：{missing_field} 为空")
        
        with allure.step("添加商品并进入结账"):
            inventory_page.add_product_to_cart_by_index(0)
            inventory_page.click_cart()
            cart_page.checkout()
        
        with allure.step(f"填写信息（{missing_field} 为空）"):
            cart_page.fill_checkout_info(
                first_name=checkout_info["first_name"],
                last_name=checkout_info["last_name"],
                postal_code=checkout_info["postal_code"]
            )
            cart_page.continue_checkout()
        
        with allure.step("验证显示正确的错误消息"):
            actual_error = cart_page.get_error_message()
            assert actual_error, "未显示错误消息"
            assert expected_error.lower() in actual_error.lower(), (
                f"错误消息不匹配\n期望包含: {expected_error}\n实际: {actual_error}"
            )
    
    @allure.title("结账时必填信息验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.cart
    def test_checkout_all_fields_empty(
        self, 
        logged_in_inventory_page: InventoryPage,
        cart_page: CartPage
    ):
        """
        测试所有必填信息为空时的验证
        """
        inventory_page = logged_in_inventory_page
        expected_error = TestDataLoader.get_error_message("empty_first_name")
        
        with allure.step("添加商品并进入结账"):
            inventory_page.add_product_to_cart_by_index(0)
            inventory_page.click_cart()
            cart_page.checkout()
        
        with allure.step("不填写信息直接继续"):
            cart_page.continue_checkout()
        
        with allure.step("验证显示首个必填字段错误"):
            error_message = cart_page.get_error_message()
            assert error_message, "未显示错误消息"
            assert expected_error.lower() in error_message.lower(), (
                f"错误消息不匹配\n期望: {expected_error}\n实际: {error_message}"
            )
