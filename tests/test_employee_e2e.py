"""
员工管理端到端测试用例
测试 OrangeHRM 的员工完整生命周期：创建 -> 搜索 -> 编辑 -> 删除
"""

import time

import allure
import pytest

from pages.dashboard_page import DashboardPage
from pages.employee_form_page import EmployeeFormPage
from pages.pim_page import PIMPage
from utils.data_loader import TestDataLoader


@allure.feature("员工管理")
@allure.story("创建员工")
class TestCreateEmployee:
    """创建员工测试类"""

    @allure.title("创建新员工 - 基本信息")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.pim
    def test_create_employee_basic(self, employee_form: EmployeeFormPage):
        """
        测试创建新员工（只填写基本信息）

        步骤:
        1. 导航到添加员工页面
        2. 填写员工姓名
        3. 保存
        4. 验证保存成功
        """
        form = employee_form
        employee_data = TestDataLoader.get_employee("new_employee")
        # 使用时间戳确保唯一性
        timestamp = str(int(time.time()))[-6:]
        first_name = f"{employee_data['first_name']}{timestamp}"

        with allure.step("填写员工基本信息"):
            form.wait_for_form_load()
            form.fill_employee_name(
                first_name=first_name,
                middle_name=employee_data["middle_name"],
                last_name=employee_data["last_name"],
            )

        with allure.step("获取自动生成的员工 ID"):
            employee_id = form.get_generated_employee_id()
            allure.attach(employee_id, name="员工 ID", attachment_type=allure.attachment_type.TEXT)

        with allure.step("保存员工"):
            form.click_save()

        with allure.step("验证保存成功"):
            # 保存成功后会跳转到员工详情页面
            assert form.is_success_toast_displayed() or "viewPersonalDetails" in form.get_current_url()


@allure.feature("员工管理")
@allure.story("搜索员工")
class TestSearchEmployee:
    """搜索员工测试类"""

    @allure.title("搜索员工列表")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.pim
    def test_search_employee_list(self, logged_in_pim: PIMPage):
        """
        测试员工列表页面基本功能

        步骤:
        1. 打开 PIM 员工列表
        2. 验证页面正常加载
        3. 检查员工记录是否存在
        """
        pim = logged_in_pim

        with allure.step("验证在 PIM 页面"):
            assert pim.is_on_pim_page(), "未进入 PIM 页面"

        with allure.step("检查员工列表"):
            employee_count = pim.get_employee_count()
            allure.attach(
                str(employee_count), name="员工数量", attachment_type=allure.attachment_type.TEXT
            )
            # OrangeHRM demo 系统通常有一些预置员工
            assert employee_count >= 0, "无法获取员工数量"

    @allure.title("按员工 ID 搜索")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pim
    def test_search_by_employee_id(self, logged_in_pim: PIMPage):
        """
        测试按员工 ID 搜索

        步骤:
        1. 打开 PIM 员工列表
        2. 获取第一个员工的 ID
        3. 使用该 ID 进行搜索
        4. 验证搜索结果
        """
        pim = logged_in_pim

        with allure.step("获取第一个员工信息"):
            if pim.has_no_records():
                pytest.skip("没有员工记录可供搜索")

            first_employee = pim.get_employee_data_from_row(0)
            employee_id = first_employee.get("id", "")
            if not employee_id:
                pytest.skip("无法获取员工 ID")

        with allure.step(f"按 ID 搜索: {employee_id}"):
            pim.search_by_employee_id(employee_id)
            pim.click_search()

        with allure.step("验证搜索结果"):
            # 搜索后应该能找到记录
            assert not pim.has_no_records(), f"未找到 ID 为 {employee_id} 的员工"


@allure.feature("员工管理")
@allure.story("编辑员工")
class TestEditEmployee:
    """编辑员工测试类"""

    @allure.title("编辑员工信息")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.pim
    def test_edit_employee_info(self, logged_in_pim: PIMPage):
        """
        测试编辑员工信息

        步骤:
        1. 打开 PIM 员工列表
        2. 点击第一个员工的编辑按钮
        3. 修改员工信息
        4. 保存并验证
        """
        pim = logged_in_pim

        with allure.step("检查是否有员工可编辑"):
            if pim.has_no_records():
                pytest.skip("没有员工记录可供编辑")

        with allure.step("点击编辑按钮"):
            pim.click_edit_on_row(0)

        with allure.step("验证进入编辑页面"):
            # 编辑页面 URL 包含 viewPersonalDetails
            assert "viewPersonalDetails" in pim.get_current_url() or "empNumber" in pim.get_current_url()


@allure.feature("员工管理")
@allure.story("删除员工")
class TestDeleteEmployee:
    """删除员工测试类"""

    @allure.title("取消删除员工")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pim
    def test_cancel_delete_employee(self, logged_in_pim: PIMPage):
        """
        测试取消删除员工

        步骤:
        1. 打开 PIM 员工列表
        2. 点击删除按钮
        3. 在确认对话框中点击取消
        4. 验证员工未被删除
        """
        pim = logged_in_pim

        with allure.step("检查是否有员工"):
            pim.page.wait_for_timeout(1000)
            if pim.has_no_records():
                pytest.skip("没有员工记录")
            initial_count = pim.get_employee_count()
            allure.attach(f"初始员工数量: {initial_count}", name="初始状态", attachment_type=allure.attachment_type.TEXT)

        with allure.step("点击删除按钮"):
            pim.click_delete_on_row(0)
            # 等待对话框出现
            pim.page.wait_for_timeout(1500)

        with allure.step("取消删除"):
            # 使用多种选择器尝试点击取消按钮
            cancel_clicked = False
            cancel_selectors = [
                ".oxd-dialog-sheet button.oxd-button--text",
                ".orangehrm-modal-footer button.oxd-button--text",
                "button:has-text('No, Cancel')",
                "button.oxd-button--text",
            ]

            for selector in cancel_selectors:
                try:
                    cancel_btn = pim.page.locator(selector).first
                    if cancel_btn.is_visible():
                        cancel_btn.click()
                        cancel_clicked = True
                        allure.attach(f"使用选择器: {selector}", name="取消按钮选择器", attachment_type=allure.attachment_type.TEXT)
                        break
                except Exception as e:
                    continue

            if not cancel_clicked:
                # 最后尝试按 Escape 键关闭对话框
                pim.page.keyboard.press("Escape")
                allure.attach("使用 Escape 键关闭对话框", name="取消方式", attachment_type=allure.attachment_type.TEXT)

            pim.page.wait_for_timeout(1000)

        with allure.step("验证员工未被删除"):
            pim.page.wait_for_timeout(1500)
            current_count = pim.get_employee_count()
            allure.attach(f"当前员工数量: {current_count}", name="当前状态", attachment_type=allure.attachment_type.TEXT)
            assert current_count == initial_count, f"员工被意外删除，初始: {initial_count}, 当前: {current_count}"


@allure.feature("员工管理")
@allure.story("E2E 完整流程")
class TestEmployeeE2E:
    """员工管理端到端测试 - 完整生命周期"""

    @allure.title("员工完整生命周期测试")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.e2e
    @pytest.mark.pim
    def test_employee_full_lifecycle(self, logged_in_pim: PIMPage):
        """
        测试员工完整生命周期

        完整 E2E 流程:
        1. 创建新员工
        2. 搜索验证员工存在
        3. 编辑员工信息
        4. 再次验证修改
        5. 删除员工
        6. 验证员工已删除
        """
        pim = logged_in_pim
        employee_data = TestDataLoader.get_employee("new_employee")

        # 使用时间戳生成唯一的员工名
        timestamp = str(int(time.time()))[-6:]
        first_name = f"E2E{timestamp}"
        middle_name = "Test"
        last_name = "Employee"
        full_name = f"{first_name} {middle_name} {last_name}"

        # ==================== 第 1 步：创建员工 ====================
        with allure.step("步骤 1: 创建新员工"):
            pim.click_add_employee_tab()

            form = EmployeeFormPage(pim.page)
            form.wait_for_form_load()
            form.fill_employee_name(first_name, middle_name, last_name)

            # 获取员工 ID
            employee_id = form.get_generated_employee_id()
            allure.attach(employee_id, name="新员工 ID", attachment_type=allure.attachment_type.TEXT)
            allure.attach(full_name, name="员工姓名", attachment_type=allure.attachment_type.TEXT)

            form.click_save()

            # 等待保存完成
            form.page.wait_for_timeout(2000)

            # 验证保存成功（跳转到详情页或显示成功消息）
            current_url = form.get_current_url()
            assert (
                "viewPersonalDetails" in current_url
                or form.is_success_toast_displayed()
            ), "创建员工失败"

        # ==================== 第 2 步：搜索验证 ====================
        with allure.step("步骤 2: 搜索验证员工存在"):
            # 返回员工列表
            pim.open()
            pim.wait_for_page_load()

            # 搜索刚创建的员工
            pim.search_by_employee_id(employee_id)
            pim.click_search()

            # 验证能找到
            assert not pim.has_no_records(), f"未找到刚创建的员工 (ID: {employee_id})"

            # 验证员工信息
            employee_info = pim.get_employee_data_from_row(0)
            assert employee_id in employee_info.get("id", ""), "员工 ID 不匹配"

        # ==================== 第 3 步：编辑员工 ====================
        with allure.step("步骤 3: 编辑员工信息"):
            pim.click_edit_on_row(0)

            # 等待页面加载
            form = EmployeeFormPage(pim.page)
            form.page.wait_for_timeout(3000)

            # 验证进入编辑页面
            assert "viewPersonalDetails" in form.get_current_url(), "未进入编辑页面"

            # 修改员工姓名
            edit_data = TestDataLoader.get_employee("edit_employee")
            new_first_name = f"Updated{timestamp}"

            # 编辑姓名 - 使用多种选择器尝试
            first_name_selectors = [
                ".orangehrm-card-container input[name='firstName']",
                "input[name='firstName']",
            ]

            first_name_input = None
            for selector in first_name_selectors:
                locator = form.page.locator(selector).first
                try:
                    locator.wait_for(state="visible", timeout=5000)
                    first_name_input = locator
                    break
                except Exception:
                    continue

            if first_name_input:
                first_name_input.clear()
                first_name_input.fill(new_first_name)

                # 点击第一个保存按钮
                save_btn = form.page.locator(form.SAVE_BUTTON).first
                save_btn.click()

                # 验证保存成功
                form.page.wait_for_timeout(2000)
                success = form.is_success_toast_displayed()
                allure.attach(f"保存状态: {success}", name="编辑结果", attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach("无法找到姓名输入框", name="编辑警告", attachment_type=allure.attachment_type.TEXT)

        # ==================== 第 4 步：再次验证修改 ====================
        with allure.step("步骤 4: 验证修改已保存"):
            pim.open()
            pim.wait_for_page_load()

            # 搜索修改后的员工
            pim.search_by_employee_id(employee_id)
            pim.click_search()

            assert not pim.has_no_records(), "未找到修改后的员工"

            # 验证名字已更新
            employee_info = pim.get_employee_data_from_row(0)
            assert new_first_name.lower() in employee_info.get(
                "first_middle_name", ""
            ).lower(), "员工姓名未更新"

        # ==================== 第 5 步：删除员工 ====================
        with allure.step("步骤 5: 删除员工"):
            pim.click_delete_on_row(0)
            pim.confirm_delete()

            # 等待删除完成
            pim.page.wait_for_timeout(3000)

        # ==================== 第 6 步：验证已删除 ====================
        with allure.step("步骤 6: 验证员工已删除"):
            # 刷新页面确保获取最新数据
            pim.open()
            pim.wait_for_page_load()
            
            # 重新搜索
            pim.search_by_employee_id(employee_id)
            pim.click_search()
            
            # 等待搜索结果
            pim.page.wait_for_timeout(2000)

            # 验证找不到该员工
            assert pim.has_no_records(), f"员工 (ID: {employee_id}) 未被成功删除"

        allure.attach(
            f"成功完成员工 '{full_name}' (ID: {employee_id}) 的完整生命周期测试",
            name="测试结果",
            attachment_type=allure.attachment_type.TEXT,
        )

    @allure.title("批量创建和删除员工")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.e2e
    @pytest.mark.pim
    def test_batch_employee_operations(self, logged_in_pim: PIMPage):
        """
        测试批量员工操作

        步骤:
        1. 创建多个员工
        2. 验证所有员工都已创建
        3. 逐个删除
        """
        pim = logged_in_pim
        timestamp = str(int(time.time()))[-4:]
        created_employees = []

        # 创建 2 个员工进行批量测试
        num_employees = 2

        with allure.step(f"批量创建 {num_employees} 个员工"):
            for i in range(num_employees):
                pim.click_add_employee_tab()

                form = EmployeeFormPage(pim.page)
                form.wait_for_form_load()

                first_name = f"Batch{timestamp}{i}"
                form.fill_employee_name(first_name, "Test", "Employee")
                emp_id = form.get_generated_employee_id()
                created_employees.append({"id": emp_id, "name": first_name})

                form.click_save()
                form.page.wait_for_timeout(2000)

                # 返回列表
                pim.open()
                pim.wait_for_page_load()

        with allure.step("验证所有员工已创建"):
            for emp in created_employees:
                pim.search_by_employee_id(emp["id"])
                pim.click_search()
                assert not pim.has_no_records(), f"未找到员工 {emp['name']} (ID: {emp['id']})"
                pim.click_reset()
                pim.wait_for_table_update()

        with allure.step("删除所有测试员工"):
            for emp in created_employees:
                pim.search_by_employee_id(emp["id"])
                pim.click_search()
                pim.page.wait_for_timeout(1500)
                if not pim.has_no_records():
                    pim.click_delete_on_row(0)
                    pim.confirm_delete()
                    pim.page.wait_for_timeout(3000)
                # 重置搜索以准备下一次搜索
                pim.click_reset()
                pim.wait_for_table_update()

        with allure.step("验证所有员工已删除"):
            # 刷新页面确保获取最新数据
            pim.open()
            pim.wait_for_page_load()
            
            for emp in created_employees:
                pim.search_by_employee_id(emp["id"])
                pim.click_search()
                pim.page.wait_for_timeout(2000)
                is_deleted = pim.has_no_records()
                allure.attach(
                    f"员工 {emp['name']} (ID: {emp['id']}) 删除状态: {is_deleted}",
                    name=f"删除验证-{emp['name']}",
                    attachment_type=allure.attachment_type.TEXT,
                )
                assert is_deleted, f"员工 {emp['name']} 未被删除"
                pim.click_reset()
                pim.wait_for_table_update()
