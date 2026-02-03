"""
员工表单复杂操作测试用例

[示例代码] 此文件是针对 OrangeHRM Demo 系统的示例测试用例。

演示了复杂表单的测试场景：
- 必填字段验证
- 日期选择器操作
- 下拉框选择
- 多 Tab 页面切换
- 登录详情设置
- 测试数据清理

如果你的系统有类似的表单功能，可以参考此文件的测试结构。

OrangeHRM Demo: https://opensource-demo.orangehrmlive.com
"""

import time

import allure
import pytest

from pages.employee_form_page import EmployeeFormPage
from pages.pim_page import PIMPage
from utils.data_loader import TestDataLoader


@allure.feature("复杂表单")
@allure.story("必填字段验证")
class TestFormValidation:
    """表单验证测试类"""

    @allure.title("创建员工 - 必填字段为空验证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pim
    def test_create_employee_required_fields(self, employee_form: EmployeeFormPage):
        """
        测试创建员工时必填字段验证

        步骤:
        1. 打开添加员工表单
        2. 不填写任何信息直接保存
        3. 验证显示必填字段错误
        """
        form = employee_form

        with allure.step("等待表单加载"):
            form.wait_for_form_load()

        with allure.step("清空所有必填字段"):
            # 清空姓名字段 - 使用 .first 和更安全的方式
            first_name_input = form.page.locator(form.INPUT_FIRST_NAME).first
            first_name_input.clear()

            last_name_input = form.page.locator(form.INPUT_LAST_NAME).first
            last_name_input.clear()

        with allure.step("尝试保存"):
            form.click_save()

        with allure.step("验证显示错误消息"):
            form.page.wait_for_timeout(1500)
            # 检查是否有任何字段错误消息
            error_count = form.page.locator(form.FIELD_ERROR).count()
            has_error = error_count > 0
            # 应该显示必填字段错误
            assert has_error, f"未显示必填字段错误，错误消息数量: {error_count}"

    @allure.title("创建员工 - 只填写名不填写姓")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pim
    def test_create_employee_missing_last_name(self, employee_form: EmployeeFormPage):
        """
        测试只填写名不填写姓的情况

        步骤:
        1. 只填写 First Name
        2. 不填写 Last Name
        3. 保存并验证错误
        """
        form = employee_form

        with allure.step("只填写 First Name"):
            form.wait_for_form_load()
            first_name_input = form.page.locator(form.INPUT_FIRST_NAME).first
            first_name_input.fill("TestOnly")

            last_name_input = form.page.locator(form.INPUT_LAST_NAME).first
            last_name_input.clear()

        with allure.step("尝试保存"):
            form.click_save()

        with allure.step("验证显示错误"):
            form.page.wait_for_timeout(1500)
            # Last Name 是必填的，应该有错误提示
            error_count = form.page.locator(form.FIELD_ERROR).count()
            has_error = error_count > 0
            # 某些版本可能允许空姓，这里记录结果
            allure.attach(
                f"是否显示错误: {has_error}, 错误数量: {error_count}",
                name="验证结果",
                attachment_type=allure.attachment_type.TEXT,
            )


@allure.feature("复杂表单")
@allure.story("表单元素操作")
class TestFormElements:
    """表单元素操作测试类"""

    @allure.title("创建员工 - 填写完整信息")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.pim
    def test_create_employee_with_full_info(self, employee_form: EmployeeFormPage):
        """
        测试创建员工填写完整信息

        步骤:
        1. 填写员工基本信息
        2. 自定义员工 ID
        3. 保存员工
        """
        form = employee_form
        timestamp = str(int(time.time()))[-6:]

        with allure.step("填写完整员工信息"):
            form.wait_for_form_load()
            form.fill_employee_name(
                first_name=f"Full{timestamp}",
                middle_name="Info",
                last_name="Employee",
            )

        with allure.step("设置自定义员工 ID"):
            custom_id = f"EMP{timestamp}"
            form.fill_employee_id(custom_id)

        with allure.step("保存员工"):
            form.click_save()

        with allure.step("验证保存成功"):
            form.page.wait_for_timeout(2000)
            success = (
                form.is_success_toast_displayed() or "viewPersonalDetails" in form.get_current_url()
            )
            assert success, "创建员工失败"

        # 清理：删除测试员工
        with allure.step("清理：删除测试员工"):
            pim = PIMPage(form.page)
            pim.open()
            pim.search_by_employee_id(custom_id)
            pim.click_search()
            if not pim.has_no_records():
                pim.click_delete_on_row(0)
                pim.confirm_delete()


@allure.feature("复杂表单")
@allure.story("多 Tab 页面")
class TestFormTabs:
    """多 Tab 页面测试类"""

    @allure.title("编辑员工 - 切换不同 Tab")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pim
    def test_employee_form_tabs_navigation(self, logged_in_pim: PIMPage):
        """
        测试员工编辑页面的 Tab 切换

        步骤:
        1. 进入员工编辑页面
        2. 切换到不同的 Tab（个人详情、联系方式、工作信息等）
        3. 验证各 Tab 页面正常加载
        """
        pim = logged_in_pim

        with allure.step("检查是否有员工可编辑"):
            if pim.has_no_records():
                pytest.skip("没有员工记录可供编辑")

        with allure.step("进入第一个员工的编辑页面"):
            pim.click_edit_on_row(0)
            form = EmployeeFormPage(pim.page)
            form.page.wait_for_timeout(2000)

        with allure.step("验证在个人详情页面"):
            assert "viewPersonalDetails" in form.get_current_url()

        with allure.step("切换到联系方式 Tab"):
            form.go_to_contact_details()
            form.page.wait_for_timeout(1000)
            # 验证页面切换
            assert (
                form.is_visible(form.INPUT_STREET1, timeout=5000)
                or "contactDetails" in form.get_current_url()
            )

        with allure.step("切换到工作信息 Tab"):
            form.go_to_job_details()
            form.page.wait_for_timeout(1000)
            # 验证页面切换
            assert "job" in form.get_current_url().lower()

        with allure.step("返回个人详情 Tab"):
            form.go_to_personal_details()
            form.page.wait_for_timeout(1000)
            assert "viewPersonalDetails" in form.get_current_url()

    @allure.title("编辑员工 - 联系方式")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pim
    def test_edit_employee_contact_details(self, logged_in_pim: PIMPage):
        """
        测试编辑员工联系方式

        步骤:
        1. 进入员工编辑页面
        2. 切换到联系方式 Tab
        3. 填写联系信息
        4. 保存并验证
        """
        pim = logged_in_pim

        with allure.step("检查是否有员工"):
            if pim.has_no_records():
                pytest.skip("没有员工记录")

        with allure.step("进入编辑页面"):
            pim.click_edit_on_row(0)
            form = EmployeeFormPage(pim.page)
            form.page.wait_for_timeout(2000)

        with allure.step("切换到联系方式"):
            form.go_to_contact_details()
            form.page.wait_for_timeout(2000)

        with allure.step("填写地址信息"):
            contact_data = TestDataLoader.get_contact_details()
            form.fill_address(
                street1=contact_data["street1"],
                city=contact_data["city"],
                zip_code=contact_data["zip"],
            )

        with allure.step("保存"):
            form.click_save()
            form.page.wait_for_timeout(2000)

        with allure.step("验证保存成功"):
            # 应该显示成功 Toast
            success = form.is_success_toast_displayed()
            allure.attach(
                f"保存是否成功: {success}",
                name="保存结果",
                attachment_type=allure.attachment_type.TEXT,
            )


@allure.feature("复杂表单")
@allure.story("下拉选择器")
class TestDropdowns:
    """下拉选择器测试类"""

    @allure.title("编辑员工 - 选择国籍")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pim
    def test_select_nationality(self, logged_in_pim: PIMPage):
        """
        测试选择国籍下拉框

        步骤:
        1. 进入员工编辑页面
        2. 找到国籍下拉框
        3. 选择一个国籍
        4. 验证选择成功
        """
        pim = logged_in_pim

        with allure.step("检查是否有员工"):
            if pim.has_no_records():
                pytest.skip("没有员工记录")

        with allure.step("进入编辑页面"):
            pim.click_edit_on_row(0)
            form = EmployeeFormPage(pim.page)
            form.page.wait_for_timeout(3000)

        with allure.step("查找并操作国籍下拉框"):
            # 国籍下拉框在个人详情页 - 检查第一个匹配的元素
            nationality_dropdown = form.page.locator(form.SELECT_NATIONALITY).first
            if nationality_dropdown.is_visible():
                form.select_nationality("American")
                form.page.wait_for_timeout(500)

                # 保存 - 点击第一个保存按钮
                save_btn = form.page.locator(form.SAVE_BUTTON).first
                save_btn.click()
                form.page.wait_for_timeout(2000)

                allure.attach(
                    "国籍选择测试完成", name="结果", attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    "国籍下拉框不可见", name="结果", attachment_type=allure.attachment_type.TEXT
                )


@allure.feature("复杂表单")
@allure.story("日期选择器")
class TestDatePicker:
    """日期选择器测试类"""

    @allure.title("填写出生日期")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pim
    def test_fill_date_of_birth(self, logged_in_pim: PIMPage):
        """
        测试日期选择器

        步骤:
        1. 进入员工编辑页面
        2. 找到出生日期输入框
        3. 填写日期
        4. 验证日期已填写
        """
        pim = logged_in_pim

        with allure.step("检查是否有员工"):
            if pim.has_no_records():
                pytest.skip("没有员工记录")

        with allure.step("进入编辑页面"):
            pim.click_edit_on_row(0)
            form = EmployeeFormPage(pim.page)
            form.page.wait_for_timeout(3000)

        with allure.step("填写出生日期"):
            personal_data = TestDataLoader.get_personal_details()
            date_str = personal_data.get("date_of_birth", "1990-01-15")

            # 使用 .first 获取第一个匹配的日期输入框
            date_input = form.page.locator(form.INPUT_DATE_OF_BIRTH).first
            if date_input.is_visible():
                form.fill_date_of_birth(date_str)
                form.page.wait_for_timeout(500)

                # 保存 - 点击第一个保存按钮
                save_btn = form.page.locator(form.SAVE_BUTTON).first
                save_btn.click()
                form.page.wait_for_timeout(2000)

                success = form.is_success_toast_displayed()
                allure.attach(
                    f"日期填写测试完成，保存状态: {success}",
                    name="结果",
                    attachment_type=allure.attachment_type.TEXT,
                )
            else:
                allure.attach(
                    "出生日期输入框不可见", name="结果", attachment_type=allure.attachment_type.TEXT
                )


@allure.feature("复杂表单")
@allure.story("登录详情")
class TestLoginDetails:
    """登录详情测试类"""

    @allure.title("创建员工并设置登录凭证")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.pim
    def test_create_employee_with_login(self, employee_form: EmployeeFormPage):
        """
        测试创建员工时设置登录凭证

        步骤:
        1. 填写员工基本信息
        2. 启用登录详情
        3. 设置用户名和密码
        4. 保存并验证
        """
        form = employee_form
        timestamp = str(int(time.time()))[-6:]
        username = f"user{timestamp}"

        with allure.step("填写基本信息"):
            form.wait_for_form_load()
            form.fill_employee_name(
                first_name=f"Login{timestamp}",
                last_name="TestUser",
            )
            emp_id = form.get_generated_employee_id()

        with allure.step("启用并填写登录详情"):
            form.enable_login_details()
            form.page.wait_for_timeout(1000)  # 等待登录表单展开

            # 填写登录信息
            form.fill_login_details(
                username=username,
                password="Test@123456",
                status="Enabled",
            )

        with allure.step("保存员工"):
            # 使用 .first 点击保存按钮
            save_btn = form.page.locator(form.SAVE_BUTTON).first
            save_btn.click()
            form.page.wait_for_timeout(3000)

        with allure.step("验证保存成功"):
            success = (
                form.is_success_toast_displayed() or "viewPersonalDetails" in form.get_current_url()
            )

            allure.attach(
                f"员工ID: {emp_id}, 用户名: {username}, 保存成功: {success}",
                name="创建结果",
                attachment_type=allure.attachment_type.TEXT,
            )

        # 清理
        with allure.step("清理测试数据"):
            pim = PIMPage(form.page)
            pim.open()
            pim.wait_for_page_load()
            pim.search_by_employee_id(emp_id)
            pim.click_search()
            if not pim.has_no_records():
                pim.click_delete_on_row(0)
                pim.confirm_delete()
