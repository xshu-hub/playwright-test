"""
PIMPage - OrangeHRM PIM（人员信息管理）页面对象
封装员工列表、搜索、添加、编辑、删除等核心功能
"""

import contextlib

import allure
from playwright.sync_api import Page

from config.settings import settings
from pages.base_page import BasePage


class PIMPage(BasePage):
    """OrangeHRM PIM 页面对象"""

    # 页面名称
    page_name = "PIMPage"

    # 页面标题和导航
    PAGE_TITLE = ".oxd-topbar-header-breadcrumb"
    TOPBAR_MENU = ".oxd-topbar-body-nav"

    # 顶部导航菜单
    TAB_EMPLOYEE_LIST = ".oxd-topbar-body-nav a:has-text('Employee List')"
    TAB_ADD_EMPLOYEE = ".oxd-topbar-body-nav a:has-text('Add Employee')"
    TAB_REPORTS = ".oxd-topbar-body-nav a:has-text('Reports')"

    # 搜索过滤区域
    FILTER_FORM = ".oxd-table-filter"
    INPUT_EMPLOYEE_NAME = ".oxd-table-filter input[placeholder='Type for hints...']"
    INPUT_EMPLOYEE_ID = ".oxd-table-filter .oxd-input:not([placeholder])"
    DROPDOWN_EMPLOYMENT_STATUS = ".oxd-table-filter .oxd-select-text"
    SEARCH_BUTTON = "button[type='submit']"
    RESET_BUTTON = "button[type='reset']"

    # 自动完成下拉
    AUTOCOMPLETE_DROPDOWN = ".oxd-autocomplete-dropdown"
    AUTOCOMPLETE_OPTION = ".oxd-autocomplete-option"

    # 员工列表表格
    TABLE = ".oxd-table"
    TABLE_HEADER = ".oxd-table-header"
    TABLE_BODY = ".oxd-table-body"
    TABLE_ROW = ".oxd-table-card"
    TABLE_CELL = ".oxd-table-cell"
    CHECKBOX_ALL = ".oxd-table-header .oxd-checkbox-input"
    CHECKBOX_ROW = ".oxd-table-card .oxd-checkbox-input"

    # 表格操作按钮
    DELETE_SELECTED_BUTTON = ".orangehrm-horizontal-padding button.oxd-button--label-danger"
    ADD_BUTTON = ".orangehrm-header-container button"

    # 行内操作按钮
    ROW_EDIT_BUTTON = ".oxd-table-cell-actions .oxd-icon-button:has(.bi-pencil-fill)"
    ROW_DELETE_BUTTON = ".oxd-table-cell-actions .oxd-icon-button:has(.bi-trash)"

    # 删除确认对话框 - 使用多种选择器方案
    DELETE_DIALOG = ".oxd-dialog-sheet"
    DELETE_DIALOG_FOOTER = ".oxd-dialog-sheet .oxd-button"
    CONFIRM_DELETE_BUTTON = ".oxd-dialog-sheet button.oxd-button--label-danger"
    CANCEL_DELETE_BUTTON = ".oxd-dialog-sheet button.oxd-button--text"

    # Toast 消息
    TOAST_MESSAGE = ".oxd-toast"
    TOAST_SUCCESS = ".oxd-toast--success"
    TOAST_ERROR = ".oxd-toast--error"

    # 记录数信息
    RECORDS_COUNT = ".orangehrm-horizontal-padding span"

    # 分页
    PAGINATION = ".oxd-table-pager"
    PAGINATION_NEXT = ".oxd-pagination-page-item--next"
    PAGINATION_PREV = ".oxd-pagination-page-item--previous"

    # 加载指示器
    LOADER = ".oxd-loading-spinner"

    # 无记录提示
    NO_RECORDS = ".oxd-table-body .oxd-text--span"

    def __init__(self, page: Page):
        """
        初始化 PIM 页面

        Args:
            page: Playwright 页面实例
        """
        super().__init__(page)
        self.url = f"{settings.BASE_URL}/web/index.php/pim/viewEmployeeList"

    @allure.step("打开 PIM 员工列表页面")
    def open(self) -> "PIMPage":
        """
        打开 PIM 员工列表页面

        Returns:
            self，支持链式调用
        """
        self.navigate(self.url)
        self.wait_for_page_load()
        return self

    def wait_for_page_load(self) -> "PIMPage":
        """
        等待页面加载完成

        Returns:
            self，支持链式调用
        """
        # 等待加载器消失
        self.is_hidden(self.LOADER, timeout=10000)
        # 等待表格可见
        self.wait_for_visible(self.TABLE, timeout=10000)
        return self

    def wait_for_table_update(self) -> "PIMPage":
        """
        等待表格更新完成

        Returns:
            self，支持链式调用
        """
        # 等待可能的加载指示器
        self.page.wait_for_timeout(500)
        self.is_hidden(self.LOADER, timeout=10000)
        return self

    def is_on_pim_page(self) -> bool:
        """
        检查是否在 PIM 页面

        Returns:
            是否在 PIM 页面
        """
        return "pim" in self.get_current_url().lower()

    # ==================== 导航方法 ====================

    @allure.step("点击添加员工标签")
    def click_add_employee_tab(self) -> "PIMPage":
        """
        点击添加员工标签页

        Returns:
            self，支持链式调用
        """
        self.click(self.TAB_ADD_EMPLOYEE)
        self.page.wait_for_timeout(1000)
        return self

    @allure.step("点击员工列表标签")
    def click_employee_list_tab(self) -> "PIMPage":
        """
        点击员工列表标签页

        Returns:
            self，支持链式调用
        """
        self.click(self.TAB_EMPLOYEE_LIST)
        self.wait_for_page_load()
        return self

    @allure.step("点击添加按钮")
    def click_add_button(self) -> "PIMPage":
        """
        点击添加员工按钮

        Returns:
            self，支持链式调用
        """
        self.click(self.ADD_BUTTON)
        self.page.wait_for_timeout(1000)
        return self

    # ==================== 搜索方法 ====================

    @allure.step("输入员工姓名搜索: {name}")
    def search_by_employee_name(self, name: str) -> "PIMPage":
        """
        按员工姓名搜索

        Args:
            name: 员工姓名

        Returns:
            self，支持链式调用
        """
        # 查找员工姓名输入框（第一个输入框）
        name_input = self.page.locator(".oxd-table-filter .oxd-grid-item:first-child input")
        name_input.fill(name)

        # 等待自动完成选项出现并选择
        self.page.wait_for_timeout(1000)
        if self.is_visible(self.AUTOCOMPLETE_DROPDOWN, timeout=3000):
            # 选择第一个匹配项
            first_option = self.page.locator(self.AUTOCOMPLETE_OPTION).first
            if first_option.is_visible():
                first_option.click()

        return self

    @allure.step("输入员工 ID 搜索: {employee_id}")
    def search_by_employee_id(self, employee_id: str) -> "PIMPage":
        """
        按员工 ID 搜索

        Args:
            employee_id: 员工 ID

        Returns:
            self，支持链式调用
        """
        # 员工 ID 输入框是第二个
        id_input = self.page.locator(".oxd-table-filter .oxd-grid-item:nth-child(2) input")
        id_input.fill(employee_id)
        return self

    @allure.step("点击搜索按钮")
    def click_search(self) -> "PIMPage":
        """
        点击搜索按钮

        Returns:
            self，支持链式调用
        """
        self.click(self.SEARCH_BUTTON)
        self.wait_for_table_update()
        return self

    @allure.step("点击重置按钮")
    def click_reset(self) -> "PIMPage":
        """
        点击重置按钮

        Returns:
            self，支持链式调用
        """
        self.click(self.RESET_BUTTON)
        self.wait_for_table_update()
        return self

    # ==================== 表格操作方法 ====================

    def get_employee_count(self) -> int:
        """
        获取员工记录数

        Returns:
            员工数量
        """
        count_text = self.get_text(self.RECORDS_COUNT)
        # 解析 "(X) Records Found" 格式
        if "Records Found" in count_text:
            import re

            match = re.search(r"\((\d+)\)", count_text)
            if match:
                return int(match.group(1))
        return 0

    def get_table_rows(self) -> list:
        """
        获取表格行元素

        Returns:
            行元素列表
        """
        return self.page.locator(self.TABLE_ROW).all()

    def get_employee_data_from_row(self, row_index: int = 0) -> dict:
        """
        从指定行获取员工数据

        Args:
            row_index: 行索引

        Returns:
            包含员工信息的字典
        """
        row = self.page.locator(self.TABLE_ROW).nth(row_index)
        cells = row.locator(self.TABLE_CELL).all()

        # 表格列顺序: checkbox, id, first+middle, last, job_title, employment_status, sub_unit, supervisor, actions
        if len(cells) >= 7:
            return {
                "id": cells[1].text_content().strip(),
                "first_middle_name": cells[2].text_content().strip(),
                "last_name": cells[3].text_content().strip(),
                "job_title": cells[4].text_content().strip(),
                "employment_status": cells[5].text_content().strip(),
                "sub_unit": cells[6].text_content().strip(),
            }
        return {}

    def is_employee_in_list(self, employee_name: str) -> bool:
        """
        检查员工是否在列表中

        Args:
            employee_name: 员工姓名（可以是部分匹配）

        Returns:
            是否存在
        """
        rows = self.get_table_rows()
        for row in rows:
            row_text = row.text_content()
            if employee_name.lower() in row_text.lower():
                return True
        return False

    def has_no_records(self) -> bool:
        """
        检查是否显示无记录

        Returns:
            是否无记录
        """
        # 等待页面稳定
        self.page.wait_for_timeout(500)

        # 方法1: 检查表格行数是否为0
        rows = self.page.locator(self.TABLE_ROW).all()
        if len(rows) == 0:
            return True

        # 方法2: 检查 "No Records Found" 文本
        # 使用更精确的选择器
        no_records_selectors = [
            ".oxd-table-body span:has-text('No Records Found')",
            ".oxd-table-body .oxd-text--span:has-text('No Records')",
            "text=No Records Found",
        ]

        for selector in no_records_selectors:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0 and locator.first.is_visible():
                    return True
            except Exception:
                continue

        # 方法3: 检查记录数
        with contextlib.suppress(Exception):
            count = self.get_employee_count()
            if count == 0:
                return True

        return False

    # ==================== 编辑和删除操作 ====================

    @allure.step("点击第 {row_index} 行的编辑按钮")
    def click_edit_on_row(self, row_index: int = 0) -> "PIMPage":
        """
        点击指定行的编辑按钮

        Args:
            row_index: 行索引

        Returns:
            self，支持链式调用
        """
        row = self.page.locator(self.TABLE_ROW).nth(row_index)
        edit_button = row.locator(".bi-pencil-fill").first
        edit_button.click()
        self.page.wait_for_timeout(1000)
        return self

    @allure.step("点击第 {row_index} 行的删除按钮")
    def click_delete_on_row(self, row_index: int = 0) -> "PIMPage":
        """
        点击指定行的删除按钮

        Args:
            row_index: 行索引

        Returns:
            self，支持链式调用
        """
        row = self.page.locator(self.TABLE_ROW).nth(row_index)
        delete_button = row.locator(".bi-trash").first
        delete_button.wait_for(state="visible", timeout=5000)
        delete_button.click()
        # 等待删除确认对话框出现
        self.page.wait_for_timeout(500)
        return self

    @allure.step("确认删除")
    def confirm_delete(self) -> "PIMPage":
        """
        在删除确认对话框中点击确认

        Returns:
            self，支持链式调用
        """
        # 等待对话框出现
        dialog_selectors = [
            ".oxd-dialog-sheet",
            ".orangehrm-dialog-popup",
            "div[role='dialog']",
        ]

        dialog_visible = False
        for selector in dialog_selectors:
            try:
                dialog = self.page.locator(selector)
                dialog.wait_for(state="visible", timeout=5000)
                dialog_visible = True
                break
            except Exception:
                continue

        if not dialog_visible:
            # 如果对话框没出现，可能已经点击了，等待一下
            self.page.wait_for_timeout(1000)

        # 尝试不同的选择器找到确认删除按钮
        confirm_selectors = [
            ".oxd-dialog-sheet button.oxd-button--label-danger",
            ".orangehrm-modal-footer button.oxd-button--label-danger",
            "button.oxd-button--label-danger:has-text('Yes, Delete')",
            "button:has-text('Yes, Delete')",
            ".oxd-dialog-sheet button:last-child",  # 通常确认按钮在右边
        ]

        clicked = False
        for selector in confirm_selectors:
            try:
                confirm_btn = self.page.locator(selector).first
                if confirm_btn.is_visible():
                    confirm_btn.click()
                    clicked = True
                    break
            except Exception:
                continue

        if not clicked:
            # 最后尝试：直接点击对话框中的危险按钮
            with contextlib.suppress(Exception):
                self.page.locator("button.oxd-button--label-danger").first.click()

        # 等待删除操作完成
        self.page.wait_for_timeout(1500)

        # 等待对话框消失
        for selector in dialog_selectors:
            try:
                self.page.locator(selector).wait_for(state="hidden", timeout=5000)
                break
            except Exception:
                continue

        # 等待可能的 Toast 消息
        with contextlib.suppress(Exception):
            self.is_visible(self.TOAST_MESSAGE, timeout=3000)

        self.wait_for_table_update()
        return self

    @allure.step("取消删除")
    def cancel_delete(self) -> "PIMPage":
        """
        在删除确认对话框中点击取消

        Returns:
            self，支持链式调用
        """
        # 等待对话框出现
        self.page.wait_for_timeout(1000)

        # 尝试不同的选择器找到取消按钮
        cancel_selectors = [
            ".oxd-dialog-sheet button.oxd-button--text",
            ".orangehrm-modal-footer button.oxd-button--text",
            "button.oxd-button--text:has-text('No, Cancel')",
            "button:has-text('No, Cancel')",
        ]

        for selector in cancel_selectors:
            cancel_btn = self.page.locator(selector).first
            if cancel_btn.is_visible():
                cancel_btn.click()
                self.page.wait_for_timeout(500)
                return self

        # 如果都找不到，尝试最后一个选择器
        self.page.locator(cancel_selectors[-1]).first.click()
        self.page.wait_for_timeout(500)
        return self

    @allure.step("选择第 {row_index} 行的复选框")
    def select_row(self, row_index: int = 0) -> "PIMPage":
        """
        选择指定行的复选框

        Args:
            row_index: 行索引

        Returns:
            self，支持链式调用
        """
        row = self.page.locator(self.TABLE_ROW).nth(row_index)
        checkbox = row.locator(self.CHECKBOX_ROW)
        checkbox.click()
        return self

    @allure.step("选择所有行")
    def select_all_rows(self) -> "PIMPage":
        """
        选择所有行

        Returns:
            self，支持链式调用
        """
        self.click(self.CHECKBOX_ALL)
        return self

    @allure.step("删除选中的员工")
    def delete_selected(self) -> "PIMPage":
        """
        删除选中的员工

        Returns:
            self，支持链式调用
        """
        self.click(self.DELETE_SELECTED_BUTTON)
        return self

    # ==================== Toast 消息 ====================

    def get_toast_message(self) -> str:
        """
        获取 Toast 消息内容

        Returns:
            消息文本
        """
        if self.is_visible(self.TOAST_MESSAGE, timeout=5000):
            return self.get_text(self.TOAST_MESSAGE)
        return ""

    def is_success_toast_displayed(self) -> bool:
        """
        检查是否显示成功 Toast

        Returns:
            是否显示
        """
        return self.is_visible(self.TOAST_SUCCESS, timeout=5000)

    def wait_for_toast_disappear(self) -> "PIMPage":
        """
        等待 Toast 消息消失

        Returns:
            self，支持链式调用
        """
        self.is_hidden(self.TOAST_MESSAGE, timeout=10000)
        return self

    # ==================== 搜索并操作特定员工 ====================

    @allure.step("搜索并编辑员工: {employee_name}")
    def search_and_edit_employee(self, employee_name: str) -> "PIMPage":
        """
        搜索并编辑指定员工

        Args:
            employee_name: 员工姓名

        Returns:
            self，支持链式调用
        """
        self.search_by_employee_name(employee_name)
        self.click_search()
        self.click_edit_on_row(0)
        return self

    @allure.step("搜索并删除员工: {employee_name}")
    def search_and_delete_employee(self, employee_name: str) -> "PIMPage":
        """
        搜索并删除指定员工

        Args:
            employee_name: 员工姓名

        Returns:
            self，支持链式调用
        """
        self.search_by_employee_name(employee_name)
        self.click_search()
        if not self.has_no_records():
            self.click_delete_on_row(0)
            self.confirm_delete()
        return self
