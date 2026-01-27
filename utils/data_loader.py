"""
测试数据加载工具模块
从 test_data.json 加载测试数据，支持数据驱动测试
"""
import json
from pathlib import Path
from typing import Optional
from functools import lru_cache


class TestDataLoader:
    """测试数据加载器"""
    
    _data: Optional[dict] = None
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
        
        with open(cls._data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @classmethod
    def get_user(cls, user_type: str) -> dict:
        """
        获取用户信息
        
        Args:
            user_type: 用户类型，如 'standard_user', 'locked_out_user' 等
            
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
    def get_checkout_info(cls, info_type: str = "valid") -> dict:
        """
        获取结账信息
        
        Args:
            info_type: 信息类型，'valid' 或 'empty'
            
        Returns:
            包含 first_name, last_name, postal_code 的字典
            
        Raises:
            KeyError: 信息类型不存在
        """
        data = cls._load_data()
        if info_type not in data["checkout_info"]:
            raise KeyError(f"结账信息类型不存在: {info_type}")
        return data["checkout_info"][info_type]
    
    @classmethod
    def get_products(cls) -> list[dict]:
        """
        获取所有产品信息
        
        Returns:
            产品信息列表，每个产品包含 name 和 price
        """
        data = cls._load_data()
        return data["products"]
    
    @classmethod
    def get_product_by_index(cls, index: int) -> dict:
        """
        按索引获取产品信息
        
        Args:
            index: 产品索引
            
        Returns:
            产品信息字典
            
        Raises:
            IndexError: 索引超出范围
        """
        products = cls.get_products()
        if index >= len(products):
            raise IndexError(f"产品索引超出范围: {index}，共 {len(products)} 个产品")
        return products[index]
    
    @classmethod
    def get_error_message(cls, error_type: str) -> str:
        """
        获取错误消息
        
        Args:
            error_type: 错误类型，如 'locked_user', 'empty_username' 等
            
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
    def get_login_failure_test_cases(cls) -> list[tuple]:
        """
        获取登录失败测试用例数据（用于参数化测试）
        
        Returns:
            测试用例列表，每个元素为 (username, password, error_key, description)
        """
        data = cls._load_data()
        users = data["users"]
        
        test_cases = [
            # 被锁定用户
            (
                users["locked_out_user"]["username"],
                users["locked_out_user"]["password"],
                "locked_user",
                "被锁定用户登录"
            ),
            # 空用户名
            (
                "",
                users["standard_user"]["password"],
                "empty_username",
                "空用户名登录"
            ),
            # 空密码
            (
                users["standard_user"]["username"],
                "",
                "empty_password",
                "空密码登录"
            ),
            # 错误凭证
            (
                "invalid_user",
                "wrong_password",
                "invalid_credentials",
                "错误凭证登录"
            ),
        ]
        return test_cases


# 创建全局实例便于导入
test_data = TestDataLoader()
