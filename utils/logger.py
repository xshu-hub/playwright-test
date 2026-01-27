"""
日志工具模块
提供统一的日志记录功能
支持日志轮转和环境变量配置
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

# 日志级别映射
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class Logger:
    """日志记录器（单例模式）"""

    _instance: Optional["Logger"] = None
    _logger: logging.Logger | None = None

    # 默认配置
    DEFAULT_LOG_LEVEL = "INFO"
    DEFAULT_FILE_LOG_LEVEL = "DEBUG"
    DEFAULT_MAX_BYTES = 5 * 1024 * 1024  # 5MB
    DEFAULT_BACKUP_COUNT = 5

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _get_log_level(self, env_var: str, default: str) -> int:
        """
        从环境变量获取日志级别

        Args:
            env_var: 环境变量名
            default: 默认级别

        Returns:
            日志级别整数值
        """
        level_str = os.getenv(env_var, default).upper()
        return LOG_LEVELS.get(level_str, LOG_LEVELS[default])

    def _initialize_logger(self) -> None:
        """初始化日志记录器"""
        self._logger = logging.getLogger("playwright-test")
        self._logger.setLevel(logging.DEBUG)

        # 防止重复添加处理器
        if self._logger.handlers:
            return

        # 控制台处理器
        self._setup_console_handler()

        # 文件处理器（带轮转）
        self._setup_file_handler()

    def _setup_console_handler(self) -> None:
        """设置控制台日志处理器"""
        console_level = self._get_log_level("LOG_LEVEL", self.DEFAULT_LOG_LEVEL)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_level)
        console_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_format)
        self._logger.addHandler(console_handler)

    def _setup_file_handler(self) -> None:
        """设置文件日志处理器（带轮转）"""
        file_level = self._get_log_level("FILE_LOG_LEVEL", self.DEFAULT_FILE_LOG_LEVEL)
        max_bytes = int(os.getenv("LOG_MAX_BYTES", str(self.DEFAULT_MAX_BYTES)))
        backup_count = int(os.getenv("LOG_BACKUP_COUNT", str(self.DEFAULT_BACKUP_COUNT)))

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # 使用日期作为日志文件名
        log_file = log_dir / f"test_{datetime.now().strftime('%Y%m%d')}.log"

        # 使用 RotatingFileHandler 实现日志轮转
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setLevel(file_level)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_format)
        self._logger.addHandler(file_handler)

    def set_level(self, level: str) -> None:
        """
        动态设置日志级别

        Args:
            level: 日志级别字符串（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        """
        level_int = LOG_LEVELS.get(level.upper(), logging.INFO)
        for handler in self._logger.handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(
                handler, RotatingFileHandler
            ):
                handler.setLevel(level_int)

    def debug(self, message: str) -> None:
        """记录 DEBUG 级别日志"""
        self._logger.debug(message)

    def info(self, message: str) -> None:
        """记录 INFO 级别日志"""
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """记录 WARNING 级别日志"""
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """记录 ERROR 级别日志"""
        self._logger.error(message)

    def critical(self, message: str) -> None:
        """记录 CRITICAL 级别日志"""
        self._logger.critical(message)

    def exception(self, message: str) -> None:
        """记录异常日志（包含堆栈信息）"""
        self._logger.exception(message)


# 创建全局日志实例
logger = Logger()
