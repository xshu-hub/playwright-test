"""
Page Objects 模块
提供 OrangeHRM 系统各页面的页面对象
"""

from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.employee_form_page import EmployeeFormPage
from pages.login_page import LoginPage
from pages.pim_page import PIMPage

__all__ = [
    "BasePage",
    "LoginPage",
    "DashboardPage",
    "PIMPage",
    "EmployeeFormPage",
]
