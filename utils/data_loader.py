"""
测试数据加载工具模块
从 test_data.json 加载测试数据，支持数据驱动测试
针对 OrangeHRM 人力资源管理系统
"""

import json
from functools import lru_cache
from pathlib import Path


class TestDataLoader:
    """测试数据加载器"""

    _data: dict | None = None
    _data_file: Path = Path(__file__).parent.parent / "data" / "test_data.json"

    @classmethod
    @lru_cache(maxsize=1)
    def _load_data(cls) -> dict:
        """
        加载测试数据文件（带缓存）

        Returns:
            测试数据字典
        """
        if not cls._data_file.exists():
            raise FileNotFoundError(f"测试数据文件不存在: {cls._data_file}")

        with open(cls._data_file, encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def get_user(cls, user_type: str = "admin") -> dict:
        """
        获取用户信息

        Args:
            user_type: 用户类型，默认为 'admin'

        Returns:
            包含 username, password, description 的字典

        Raises:
            KeyError: 用户类型不存在
        """
        data = cls._load_data()
        if user_type not in data["users"]:
            raise KeyError(f"用户类型不存在: {user_type}")
        return data["users"][user_type]

    @classmethod
    def get_all_users(cls) -> dict:
        """
        获取所有用户信息

        Returns:
            用户信息字典
        """
        data = cls._load_data()
        return data["users"]

    @classmethod
    def get_employee(cls, employee_type: str = "new_employee") -> dict:
        """
        获取员工信息

        Args:
            employee_type: 员工类型，如 'new_employee', 'edit_employee' 等

        Returns:
            员工信息字典

        Raises:
            KeyError: 员工类型不存在
        """
        data = cls._load_data()
        if employee_type not in data["employees"]:
            raise KeyError(f"员工类型不存在: {employee_type}")
        return data["employees"][employee_type]

    @classmethod
    def get_personal_details(cls, detail_type: str = "valid") -> dict:
        """
        获取个人详情信息

        Args:
            detail_type: 详情类型

        Returns:
            个人详情字典
        """
        data = cls._load_data()
        if detail_type not in data["personal_details"]:
            raise KeyError(f"个人详情类型不存在: {detail_type}")
        return data["personal_details"][detail_type]

    @classmethod
    def get_contact_details(cls, detail_type: str = "valid") -> dict:
        """
        获取联系方式信息

        Args:
            detail_type: 详情类型

        Returns:
            联系方式字典
        """
        data = cls._load_data()
        if detail_type not in data["contact_details"]:
            raise KeyError(f"联系方式类型不存在: {detail_type}")
        return data["contact_details"][detail_type]

    @classmethod
    def get_job_details(cls, detail_type: str = "valid") -> dict:
        """
        获取工作信息

        Args:
            detail_type: 详情类型

        Returns:
            工作信息字典
        """
        data = cls._load_data()
        if detail_type not in data["job_details"]:
            raise KeyError(f"工作信息类型不存在: {detail_type}")
        return data["job_details"][detail_type]

    @classmethod
    def get_error_message(cls, error_type: str) -> str:
        """
        获取错误消息

        Args:
            error_type: 错误类型

        Returns:
            错误消息字符串

        Raises:
            KeyError: 错误类型不存在
        """
        data = cls._load_data()
        if error_type not in data["error_messages"]:
            raise KeyError(f"错误消息类型不存在: {error_type}")
        return data["error_messages"][error_type]

    @classmethod
    def get_all_error_messages(cls) -> dict:
        """
        获取所有错误消息

        Returns:
            错误消息字典
        """
        data = cls._load_data()
        return data["error_messages"]

    @classmethod
    def get_menu_item(cls, menu_name: str) -> str:
        """
        获取菜单项名称

        Args:
            menu_name: 菜单键名

        Returns:
            菜单显示名称
        """
        data = cls._load_data()
        if menu_name not in data["menu_items"]:
            raise KeyError(f"菜单项不存在: {menu_name}")
        return data["menu_items"][menu_name]

    @classmethod
    def get_login_failure_test_cases(cls) -> list[tuple]:
        """
        获取登录失败测试用例数据（用于参数化测试）

        Returns:
            测试用例列表，每个元素为 (username, password, error_key, description)
        """
        data = cls._load_data()
        admin = data["users"]["admin"]

        test_cases = [
            # 空用户名
            ("", admin["password"], "empty_username", "空用户名登录"),
            # 空密码
            (admin["username"], "", "empty_password", "空密码登录"),
            # 错误凭证
            ("invalid_user", "wrong_password", "invalid_credentials", "错误凭证登录"),
            # 错误密码
            (admin["username"], "wrong_password", "invalid_credentials", "错误密码登录"),
        ]
        return test_cases


# 创建全局实例便于导入
test_data = TestDataLoader()
