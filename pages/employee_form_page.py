"""
EmployeeFormPage - OrangeHRM 员工表单页面对象
封装添加/编辑员工表单的复杂操作，包括多个 Tab 页面
"""

import allure
from playwright.sync_api import Page

from config.settings import settings
from pages.base_page import BasePage


class EmployeeFormPage(BasePage):
    """OrangeHRM 员工表单页面对象"""

    # 页面名称
    page_name = "EmployeeFormPage"

    # ==================== 添加员工表单元素 ====================

    # 基本信息
    INPUT_FIRST_NAME = "input[name='firstName']"
    INPUT_MIDDLE_NAME = "input[name='middleName']"
    INPUT_LAST_NAME = "input[name='lastName']"
    INPUT_EMPLOYEE_ID = ".oxd-grid-item:has-text('Employee Id') input.oxd-input"

    # 登录详情（可选）- 使用更精确的选择器
    TOGGLE_LOGIN_DETAILS = ".oxd-switch-input"
    LOGIN_DETAILS_SECTION = ".orangehrm-employee-form"
    INPUT_USERNAME = ".orangehrm-employee-form .oxd-grid-item:has-text('Username') input.oxd-input"
    INPUT_PASSWORD = ".orangehrm-employee-form .oxd-grid-item:has-text('Password') input.oxd-input"
    INPUT_CONFIRM_PASSWORD = (
        ".orangehrm-employee-form .oxd-grid-item:has-text('Confirm Password') input.oxd-input"
    )
    RADIO_ENABLED = ".orangehrm-employee-form label:has-text('Enabled')"
    RADIO_DISABLED = ".orangehrm-employee-form label:has-text('Disabled')"

    # 头像上传
    PROFILE_IMAGE = ".orangehrm-edit-employee-image"
    INPUT_FILE = "input[type='file']"

    # 保存按钮
    SAVE_BUTTON = "button[type='submit']"
    CANCEL_BUTTON = "button[type='button']:has-text('Cancel')"

    # ==================== 编辑员工详情页面 Tab ====================

    TAB_PERSONAL_DETAILS = "a:has-text('Personal Details')"
    TAB_CONTACT_DETAILS = "a:has-text('Contact Details')"
    TAB_EMERGENCY_CONTACTS = "a:has-text('Emergency Contacts')"
    TAB_DEPENDENTS = "a:has-text('Dependents')"
    TAB_IMMIGRATION = "a:has-text('Immigration')"
    TAB_JOB = "a:has-text('Job')"
    TAB_SALARY = "a:has-text('Salary')"
    TAB_TAX_EXEMPTIONS = "a:has-text('Tax Exemptions')"
    TAB_REPORT_TO = "a:has-text('Report-to')"
    TAB_QUALIFICATIONS = "a:has-text('Qualifications')"
    TAB_MEMBERSHIPS = "a:has-text('Memberships')"

    # ==================== 个人详情表单元素 ====================

    # 个人详情 - 姓名区域（编辑页面使用更通用的选择器）
    PERSONAL_FIRST_NAME = ".orangehrm-card-container input[name='firstName']"
    PERSONAL_MIDDLE_NAME = ".orangehrm-card-container input[name='middleName']"
    PERSONAL_LAST_NAME = ".orangehrm-card-container input[name='lastName']"

    # 个人详情 - 其他字段（使用更精确的选择器）
    INPUT_NICKNAME = ".oxd-form-row .oxd-grid-item:has-text('Nickname') input.oxd-input"
    INPUT_OTHER_ID = ".oxd-form-row .oxd-grid-item:has-text('Other Id') input.oxd-input"
    INPUT_DRIVER_LICENSE = ".oxd-form-row .oxd-grid-item:has-text('License Number') input.oxd-input"
    INPUT_LICENSE_EXPIRY = (
        ".oxd-form-row .oxd-grid-item:has-text('License Expiry Date') input.oxd-input"
    )
    INPUT_SSN = ".oxd-form-row .oxd-grid-item:has-text('SSN Number') input.oxd-input"
    INPUT_SIN = ".oxd-form-row .oxd-grid-item:has-text('SIN Number') input.oxd-input"

    # 下拉选择器（使用更精确的选择器，定位到具体的表单区域）
    SELECT_NATIONALITY = (
        ".orangehrm-card-container .oxd-grid-item:has-text('Nationality') .oxd-select-text"
    )
    SELECT_MARITAL_STATUS = (
        ".orangehrm-card-container .oxd-grid-item:has-text('Marital Status') .oxd-select-text"
    )

    # 日期选择（使用更精确的选择器）
    INPUT_DATE_OF_BIRTH = (
        ".orangehrm-card-container .oxd-grid-item:has-text('Date of Birth') input.oxd-input"
    )

    # 性别单选按钮
    RADIO_MALE = "input[type='radio'][value='1']"
    RADIO_FEMALE = "input[type='radio'][value='2']"

    # ==================== 联系方式表单元素 ====================

    INPUT_STREET1 = ".oxd-grid-item:has-text('Street 1') input"
    INPUT_STREET2 = ".oxd-grid-item:has-text('Street 2') input"
    INPUT_CITY = ".oxd-grid-item:has-text('City') input"
    INPUT_STATE = ".oxd-grid-item:has-text('State/Province') input"
    INPUT_ZIP = ".oxd-grid-item:has-text('Zip/Postal Code') input"
    SELECT_COUNTRY = ".oxd-grid-item:has-text('Country') .oxd-select-text"
    INPUT_HOME_PHONE = ".oxd-grid-item:has-text('Home') input"
    INPUT_MOBILE = ".oxd-grid-item:has-text('Mobile') input"
    INPUT_WORK_PHONE = ".oxd-grid-item:has-text('Work') input"
    INPUT_WORK_EMAIL = ".oxd-grid-item:has-text('Work Email') input"
    INPUT_OTHER_EMAIL = ".oxd-grid-item:has-text('Other Email') input"

    # ==================== 工作信息表单元素 ====================

    INPUT_JOINED_DATE = ".oxd-grid-item:has-text('Joined Date') input"
    SELECT_JOB_TITLE = ".oxd-grid-item:has-text('Job Title') .oxd-select-text"
    SELECT_JOB_CATEGORY = ".oxd-grid-item:has-text('Job Category') .oxd-select-text"
    SELECT_SUB_UNIT = ".oxd-grid-item:has-text('Sub Unit') .oxd-select-text"
    SELECT_LOCATION = ".oxd-grid-item:has-text('Location') .oxd-select-text"
    SELECT_EMPLOYMENT_STATUS = ".oxd-grid-item:has-text('Employment Status') .oxd-select-text"

    # ==================== 通用元素 ====================

    # 下拉选项
    DROPDOWN_OPTIONS = ".oxd-select-dropdown .oxd-select-option"

    # 日期选择器
    DATE_PICKER = ".oxd-date-input-calendar"
    DATE_PICKER_MONTH = ".oxd-calendar-selector-month"
    DATE_PICKER_YEAR = ".oxd-calendar-selector-year"
    DATE_PICKER_DAY = ".oxd-calendar-date"

    # 表单区域
    FORM_SECTION = ".orangehrm-card-container"

    # Toast 消息
    TOAST_MESSAGE = ".oxd-toast"
    TOAST_SUCCESS = ".oxd-toast--success"

    # 加载指示器
    LOADER = ".oxd-loading-spinner"

    # 错误消息
    FIELD_ERROR = ".oxd-input-field-error-message"

    def __init__(self, page: Page):
        """
        初始化员工表单页面

        Args:
            page: Playwright 页面实例
        """
        super().__init__(page)

    def wait_for_form_load(self) -> "EmployeeFormPage":
        """
        等待表单加载完成

        Returns:
            self，支持链式调用
        """
        self.is_hidden(self.LOADER, timeout=10000)
        self.wait_for_visible(self.INPUT_FIRST_NAME, timeout=10000)
        return self

    # ==================== 添加员工 - 基本信息填写 ====================

    @allure.step("填写员工姓名: {first_name} {middle_name} {last_name}")
    def fill_employee_name(
        self, first_name: str, middle_name: str = "", last_name: str = ""
    ) -> "EmployeeFormPage":
        """
        填写员工姓名

        Args:
            first_name: 名
            middle_name: 中间名
            last_name: 姓

        Returns:
            self，支持链式调用
        """
        self.fill(self.INPUT_FIRST_NAME, first_name)
        if middle_name:
            self.fill(self.INPUT_MIDDLE_NAME, middle_name)
        if last_name:
            self.fill(self.INPUT_LAST_NAME, last_name)
        return self

    @allure.step("填写员工 ID: {employee_id}")
    def fill_employee_id(self, employee_id: str) -> "EmployeeFormPage":
        """
        填写员工 ID

        Args:
            employee_id: 员工 ID

        Returns:
            self，支持链式调用
        """
        # 清空并填写
        emp_id_input = self.page.locator(self.INPUT_EMPLOYEE_ID).first
        emp_id_input.clear()
        emp_id_input.fill(employee_id)
        return self

    def get_generated_employee_id(self) -> str:
        """
        获取系统生成的员工 ID

        Returns:
            员工 ID
        """
        emp_id_input = self.page.locator(self.INPUT_EMPLOYEE_ID).first
        return emp_id_input.input_value()

    @allure.step("启用登录详情")
    def enable_login_details(self) -> "EmployeeFormPage":
        """
        启用创建登录详情选项

        Returns:
            self，支持链式调用
        """
        toggle = self.page.locator(self.TOGGLE_LOGIN_DETAILS)
        if not toggle.is_checked():
            toggle.click()
        return self

    @allure.step("填写登录详情")
    def fill_login_details(
        self, username: str, password: str, status: str = "Enabled"
    ) -> "EmployeeFormPage":
        """
        填写登录详情

        Args:
            username: 用户名
            password: 密码
            status: 状态 ('Enabled' 或 'Disabled')

        Returns:
            self，支持链式调用
        """
        self.enable_login_details()
        self.page.wait_for_timeout(500)

        # 填写用户名和密码 - 使用 .first 确保只选择一个元素
        username_input = self.page.locator(self.INPUT_USERNAME).first
        username_input.fill(username)

        password_input = self.page.locator(self.INPUT_PASSWORD).first
        password_input.fill(password)

        confirm_input = self.page.locator(self.INPUT_CONFIRM_PASSWORD).first
        confirm_input.fill(password)

        # 选择状态 - 使用 label 文本定位
        if status == "Enabled":
            self.page.locator(self.RADIO_ENABLED).click()
        else:
            self.page.locator(self.RADIO_DISABLED).click()

        return self

    @allure.step("上传头像")
    def upload_profile_image(self, file_path: str) -> "EmployeeFormPage":
        """
        上传员工头像

        Args:
            file_path: 图片文件路径

        Returns:
            self，支持链式调用
        """
        self.page.locator(self.INPUT_FILE).set_input_files(file_path)
        return self

    @allure.step("点击保存按钮")
    def click_save(self) -> "EmployeeFormPage":
        """
        点击保存按钮

        Returns:
            self，支持链式调用
        """
        self.click(self.SAVE_BUTTON)
        return self

    @allure.step("点击取消按钮")
    def click_cancel(self) -> "EmployeeFormPage":
        """
        点击取消按钮

        Returns:
            self，支持链式调用
        """
        self.click(self.CANCEL_BUTTON)
        return self

    # ==================== Tab 导航 ====================

    @allure.step("切换到个人详情标签")
    def go_to_personal_details(self) -> "EmployeeFormPage":
        """
        切换到个人详情标签页

        Returns:
            self，支持链式调用
        """
        self.click(self.TAB_PERSONAL_DETAILS)
        self.page.wait_for_timeout(1000)
        return self

    @allure.step("切换到联系方式标签")
    def go_to_contact_details(self) -> "EmployeeFormPage":
        """
        切换到联系方式标签页

        Returns:
            self，支持链式调用
        """
        self.click(self.TAB_CONTACT_DETAILS)
        self.page.wait_for_timeout(1000)
        return self

    @allure.step("切换到工作信息标签")
    def go_to_job_details(self) -> "EmployeeFormPage":
        """
        切换到工作信息标签页

        Returns:
            self，支持链式调用
        """
        self.click(self.TAB_JOB)
        self.page.wait_for_timeout(1000)
        return self

    # ==================== 编辑员工 - 个人详情 ====================

    @allure.step("编辑员工姓名")
    def edit_employee_name(
        self, first_name: str = "", middle_name: str = "", last_name: str = ""
    ) -> "EmployeeFormPage":
        """
        编辑员工姓名（在编辑页面）

        Args:
            first_name: 名
            middle_name: 中间名
            last_name: 姓

        Returns:
            self，支持链式调用
        """
        # 等待编辑表单加载
        self.page.wait_for_timeout(1000)

        if first_name:
            # 使用 .first 避免 strict mode violation
            first_name_input = self.page.locator(self.PERSONAL_FIRST_NAME).first
            first_name_input.wait_for(state="visible", timeout=10000)
            first_name_input.clear()
            first_name_input.fill(first_name)
        if middle_name:
            middle_name_input = self.page.locator(self.PERSONAL_MIDDLE_NAME).first
            middle_name_input.clear()
            middle_name_input.fill(middle_name)
        if last_name:
            last_name_input = self.page.locator(self.PERSONAL_LAST_NAME).first
            last_name_input.clear()
            last_name_input.fill(last_name)
        return self

    @allure.step("填写昵称: {nickname}")
    def fill_nickname(self, nickname: str) -> "EmployeeFormPage":
        """
        填写昵称

        Args:
            nickname: 昵称

        Returns:
            self，支持链式调用
        """
        self.fill(self.INPUT_NICKNAME, nickname)
        return self

    @allure.step("填写驾照号码: {license_number}")
    def fill_driver_license(self, license_number: str, expiry_date: str = "") -> "EmployeeFormPage":
        """
        填写驾照信息

        Args:
            license_number: 驾照号码
            expiry_date: 过期日期 (YYYY-MM-DD 格式)

        Returns:
            self，支持链式调用
        """
        self.fill(self.INPUT_DRIVER_LICENSE, license_number)
        if expiry_date:
            self.fill_date(self.INPUT_LICENSE_EXPIRY, expiry_date)
        return self

    # ==================== 下拉选择器操作 ====================

    def select_dropdown_option(
        self, dropdown_selector: str, option_text: str
    ) -> "EmployeeFormPage":
        """
        选择下拉选项

        Args:
            dropdown_selector: 下拉框选择器
            option_text: 选项文本

        Returns:
            self，支持链式调用
        """
        # 点击下拉框 - 使用 .first 避免 strict mode violation
        dropdown = self.page.locator(dropdown_selector).first
        dropdown.click()
        self.page.wait_for_timeout(500)

        # 等待下拉菜单出现
        self.page.locator(".oxd-select-dropdown").wait_for(state="visible", timeout=5000)

        # 选择选项 - 使用更精确的选择器
        option = self.page.locator(
            f".oxd-select-dropdown .oxd-select-option span:text-is('{option_text}')"
        ).first
        if option.is_visible():
            option.click()
        else:
            # 尝试部分匹配
            option_partial = self.page.locator(
                f".oxd-select-option:has-text('{option_text}')"
            ).first
            option_partial.click()

        self.page.wait_for_timeout(300)
        return self

    @allure.step("选择国籍: {nationality}")
    def select_nationality(self, nationality: str) -> "EmployeeFormPage":
        """
        选择国籍

        Args:
            nationality: 国籍

        Returns:
            self，支持链式调用
        """
        return self.select_dropdown_option(self.SELECT_NATIONALITY, nationality)

    @allure.step("选择婚姻状况: {status}")
    def select_marital_status(self, status: str) -> "EmployeeFormPage":
        """
        选择婚姻状况

        Args:
            status: 婚姻状况

        Returns:
            self，支持链式调用
        """
        return self.select_dropdown_option(self.SELECT_MARITAL_STATUS, status)

    # ==================== 日期选择器操作 ====================

    def fill_date(self, date_input_selector: str, date_str: str) -> "EmployeeFormPage":
        """
        填写日期（直接输入）

        Args:
            date_input_selector: 日期输入框选择器
            date_str: 日期字符串 (YYYY-MM-DD 格式)

        Returns:
            self，支持链式调用
        """
        # 使用 .first 避免 strict mode violation
        date_input = self.page.locator(date_input_selector).first
        date_input.clear()
        date_input.fill(date_str)
        # 点击其他地方关闭日期选择器
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(300)
        return self

    @allure.step("填写出生日期: {date_str}")
    def fill_date_of_birth(self, date_str: str) -> "EmployeeFormPage":
        """
        填写出生日期

        Args:
            date_str: 日期字符串

        Returns:
            self，支持链式调用
        """
        return self.fill_date(self.INPUT_DATE_OF_BIRTH, date_str)

    # ==================== 性别选择 ====================

    @allure.step("选择性别: {gender}")
    def select_gender(self, gender: str) -> "EmployeeFormPage":
        """
        选择性别

        Args:
            gender: 性别 ('Male' 或 'Female')

        Returns:
            self，支持链式调用
        """
        if gender.lower() == "male":
            self.page.locator("label:has-text('Male')").click()
        else:
            self.page.locator("label:has-text('Female')").click()
        return self

    # ==================== 联系方式填写 ====================

    @allure.step("填写地址信息")
    def fill_address(
        self,
        street1: str = "",
        street2: str = "",
        city: str = "",
        state: str = "",
        zip_code: str = "",
        country: str = "",
    ) -> "EmployeeFormPage":
        """
        填写地址信息

        Returns:
            self，支持链式调用
        """
        if street1:
            self.fill(self.INPUT_STREET1, street1)
        if street2:
            self.fill(self.INPUT_STREET2, street2)
        if city:
            self.fill(self.INPUT_CITY, city)
        if state:
            self.fill(self.INPUT_STATE, state)
        if zip_code:
            self.fill(self.INPUT_ZIP, zip_code)
        if country:
            self.select_dropdown_option(self.SELECT_COUNTRY, country)
        return self

    @allure.step("填写电话信息")
    def fill_phone_numbers(
        self, home: str = "", mobile: str = "", work: str = ""
    ) -> "EmployeeFormPage":
        """
        填写电话号码

        Returns:
            self，支持链式调用
        """
        if home:
            self.fill(self.INPUT_HOME_PHONE, home)
        if mobile:
            self.fill(self.INPUT_MOBILE, mobile)
        if work:
            self.fill(self.INPUT_WORK_PHONE, work)
        return self

    @allure.step("填写邮箱信息")
    def fill_email(self, work_email: str = "", other_email: str = "") -> "EmployeeFormPage":
        """
        填写邮箱

        Returns:
            self，支持链式调用
        """
        if work_email:
            self.fill(self.INPUT_WORK_EMAIL, work_email)
        if other_email:
            self.fill(self.INPUT_OTHER_EMAIL, other_email)
        return self

    # ==================== 工作信息填写 ====================

    @allure.step("选择职位: {job_title}")
    def select_job_title(self, job_title: str) -> "EmployeeFormPage":
        """
        选择职位

        Args:
            job_title: 职位名称

        Returns:
            self，支持链式调用
        """
        return self.select_dropdown_option(self.SELECT_JOB_TITLE, job_title)

    @allure.step("选择雇佣状态: {status}")
    def select_employment_status(self, status: str) -> "EmployeeFormPage":
        """
        选择雇佣状态

        Args:
            status: 雇佣状态

        Returns:
            self，支持链式调用
        """
        return self.select_dropdown_option(self.SELECT_EMPLOYMENT_STATUS, status)

    @allure.step("填写入职日期: {date_str}")
    def fill_joined_date(self, date_str: str) -> "EmployeeFormPage":
        """
        填写入职日期

        Args:
            date_str: 日期字符串

        Returns:
            self，支持链式调用
        """
        return self.fill_date(self.INPUT_JOINED_DATE, date_str)

    # ==================== 验证方法 ====================

    def get_field_error_message(self) -> str:
        """
        获取字段错误消息

        Returns:
            错误消息
        """
        if self.is_visible(self.FIELD_ERROR, timeout=3000):
            return self.get_text(self.FIELD_ERROR)
        return ""

    def is_success_toast_displayed(self) -> bool:
        """
        检查是否显示成功 Toast

        Returns:
            是否显示
        """
        return self.is_visible(self.TOAST_SUCCESS, timeout=5000)

    def get_toast_message(self) -> str:
        """
        获取 Toast 消息

        Returns:
            消息文本
        """
        if self.is_visible(self.TOAST_MESSAGE, timeout=5000):
            return self.get_text(self.TOAST_MESSAGE)
        return ""

    def wait_for_save_complete(self) -> "EmployeeFormPage":
        """
        等待保存完成

        Returns:
            self，支持链式调用
        """
        self.is_visible(self.TOAST_SUCCESS, timeout=10000)
        self.is_hidden(self.TOAST_MESSAGE, timeout=10000)
        return self

    # ==================== 快捷方法：创建新员工 ====================

    @allure.step("创建新员工")
    def create_new_employee(
        self,
        first_name: str,
        middle_name: str = "",
        last_name: str = "",
        employee_id: str = "",
    ) -> str:
        """
        创建新员工的快捷方法

        Args:
            first_name: 名
            middle_name: 中间名
            last_name: 姓
            employee_id: 员工 ID（可选，不填则使用系统生成的）

        Returns:
            员工 ID
        """
        self.wait_for_form_load()
        self.fill_employee_name(first_name, middle_name, last_name)

        if employee_id:
            self.fill_employee_id(employee_id)

        # 获取员工 ID（可能是系统生成的）
        emp_id = self.get_generated_employee_id()

        self.click_save()
        self.wait_for_save_complete()

        return emp_id
