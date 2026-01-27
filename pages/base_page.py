"""
BasePage - Page Object 模式基类
封装 Playwright 常用操作，提供统一的页面交互接口
支持字符串选择器和 Playwright 原生 Locator 对象
集成日志记录功能
"""

import allure
from playwright.sync_api import Locator, Page, TimeoutError as PlaywrightTimeoutError, expect

from config.settings import settings
from utils.logger import logger

# 定义选择器类型：支持字符串选择器或 Locator 对象
SelectorType = str | Locator


class BasePage:
    """页面对象基类"""

    # 页面名称，子类可覆盖
    page_name: str = "BasePage"

    def __init__(self, page: Page):
        """
        初始化页面对象

        Args:
            page: Playwright 页面实例
        """
        self.page = page
        self.timeout = settings.TIMEOUT
        logger.debug(f"[{self.page_name}] 页面对象已初始化")

    @staticmethod
    def _get_selector_desc(selector: SelectorType) -> str:
        """
        获取选择器的描述信息，用于日志记录

        Args:
            selector: 选择器

        Returns:
            选择器描述字符串
        """
        if isinstance(selector, str):
            return selector
        # Locator 对象，尝试获取其字符串表示
        try:
            return str(selector)
        except (TypeError, AttributeError, ValueError):
            return "<Locator>"

    def _get_locator(self, selector: SelectorType) -> Locator:
        """
        统一处理选择器，支持字符串和 Locator 对象

        Args:
            selector: 字符串选择器或 Locator 对象

        Returns:
            Locator 对象
        """
        if isinstance(selector, Locator):
            return selector
        return self.page.locator(selector)

    @allure.step("导航到: {url}")
    def navigate(self, url: str | None = None) -> None:
        """
        导航到指定 URL

        Args:
            url: 目标 URL，默认使用配置中的 BASE_URL
        """
        target_url = url or settings.BASE_URL
        logger.info(f"[{self.page_name}] 导航到: {target_url}")
        try:
            self.page.goto(target_url, wait_until="domcontentloaded")
            logger.debug(f"[{self.page_name}] 页面加载完成: {target_url}")
        except PlaywrightTimeoutError as e:
            logger.error(f"[{self.page_name}] 导航超时: {target_url}")
            raise e
        except Exception as e:
            logger.error(f"[{self.page_name}] 导航失败: {target_url}, 错误: {e}")
            raise e

    @allure.step("点击元素")
    def click(self, selector: SelectorType) -> None:
        """
        点击元素

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 点击元素: {selector_desc}")
        try:
            self._get_locator(selector).click()
            logger.info(f"[{self.page_name}] 点击成功: {selector_desc}")
        except PlaywrightTimeoutError as e:
            logger.error(f"[{self.page_name}] 点击超时，元素未找到: {selector_desc}")
            raise e
        except Exception as e:
            logger.error(f"[{self.page_name}] 点击失败: {selector_desc}, 错误: {e}")
            raise e

    @allure.step("输入文本")
    def fill(self, selector: SelectorType, text: str) -> None:
        """
        在输入框中填入文本

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
            text: 要输入的文本
        """
        selector_desc = self._get_selector_desc(selector)
        # 敏感信息脱敏处理
        masked_text = text if len(text) <= 3 else text[:2] + "*" * (len(text) - 2)
        logger.debug(f"[{self.page_name}] 输入文本: {selector_desc} -> '{masked_text}'")
        try:
            self._get_locator(selector).fill(text)
            logger.info(f"[{self.page_name}] 输入成功: {selector_desc}")
        except PlaywrightTimeoutError as e:
            logger.error(f"[{self.page_name}] 输入超时，元素未找到: {selector_desc}")
            raise e
        except Exception as e:
            logger.error(f"[{self.page_name}] 输入失败: {selector_desc}, 错误: {e}")
            raise e

    @allure.step("清空并输入")
    def clear_and_fill(self, selector: SelectorType, text: str) -> None:
        """
        清空输入框并填入新文本

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
            text: 要输入的文本
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 清空并输入: {selector_desc}")
        try:
            element = self._get_locator(selector)
            element.clear()
            element.fill(text)
            logger.info(f"[{self.page_name}] 清空并输入成功: {selector_desc}")
        except Exception as e:
            logger.error(f"[{self.page_name}] 清空并输入失败: {selector_desc}, 错误: {e}")
            raise e

    def get_text(self, selector: SelectorType) -> str:
        """
        获取元素文本内容

        Args:
            selector: 元素选择器（字符串或 Locator 对象）

        Returns:
            元素的文本内容
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 获取文本: {selector_desc}")
        try:
            text = self._get_locator(selector).text_content() or ""
            logger.debug(
                f"[{self.page_name}] 获取文本成功: '{text[:50]}{'...' if len(text) > 50 else ''}'"
            )
            return text
        except Exception as e:
            logger.error(f"[{self.page_name}] 获取文本失败: {selector_desc}, 错误: {e}")
            raise e

    def get_input_value(self, selector: SelectorType) -> str:
        """
        获取输入框的值

        Args:
            selector: 元素选择器（字符串或 Locator 对象）

        Returns:
            输入框的值
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 获取输入框值: {selector_desc}")
        try:
            value = self._get_locator(selector).input_value()
            logger.debug(f"[{self.page_name}] 获取输入框值成功")
            return value
        except Exception as e:
            logger.error(f"[{self.page_name}] 获取输入框值失败: {selector_desc}, 错误: {e}")
            raise e

    def is_visible(self, selector: SelectorType, timeout: int | None = None) -> bool:
        """
        检查元素是否可见

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
            timeout: 等待超时时间（毫秒）

        Returns:
            元素是否可见
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 检查元素可见性: {selector_desc}")
        try:
            self._get_locator(selector).wait_for(state="visible", timeout=timeout or self.timeout)
            logger.debug(f"[{self.page_name}] 元素可见: {selector_desc}")
            return True
        except PlaywrightTimeoutError:
            logger.debug(f"[{self.page_name}] 元素不可见: {selector_desc}")
            return False
        except Exception as e:
            logger.warning(f"[{self.page_name}] 检查可见性异常: {selector_desc}, 错误: {e}")
            return False

    def is_hidden(self, selector: SelectorType, timeout: int | None = None) -> bool:
        """
        检查元素是否隐藏

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
            timeout: 等待超时时间（毫秒）

        Returns:
            元素是否隐藏
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 检查元素是否隐藏: {selector_desc}")
        try:
            self._get_locator(selector).wait_for(state="hidden", timeout=timeout or self.timeout)
            logger.debug(f"[{self.page_name}] 元素已隐藏: {selector_desc}")
            return True
        except PlaywrightTimeoutError:
            logger.debug(f"[{self.page_name}] 元素仍可见: {selector_desc}")
            return False
        except Exception as e:
            logger.warning(f"[{self.page_name}] 检查隐藏状态异常: {selector_desc}, 错误: {e}")
            return False

    @allure.step("等待元素可见")
    def wait_for_visible(self, selector: SelectorType, timeout: int | None = None) -> Locator:
        """
        等待元素可见

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
            timeout: 等待超时时间（毫秒）

        Returns:
            定位到的元素
        """
        selector_desc = self._get_selector_desc(selector)
        wait_timeout = timeout or self.timeout
        logger.debug(f"[{self.page_name}] 等待元素可见: {selector_desc}, 超时: {wait_timeout}ms")
        try:
            element = self._get_locator(selector)
            element.wait_for(state="visible", timeout=wait_timeout)
            logger.info(f"[{self.page_name}] 元素已可见: {selector_desc}")
            return element
        except PlaywrightTimeoutError as e:
            logger.error(f"[{self.page_name}] 等待元素可见超时: {selector_desc}")
            raise e
        except Exception as e:
            logger.error(f"[{self.page_name}] 等待元素可见失败: {selector_desc}, 错误: {e}")
            raise e

    @allure.step("等待元素消失")
    def wait_for_hidden(self, selector: SelectorType, timeout: int | None = None) -> None:
        """
        等待元素消失

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
            timeout: 等待超时时间（毫秒）
        """
        selector_desc = self._get_selector_desc(selector)
        wait_timeout = timeout or self.timeout
        logger.debug(f"[{self.page_name}] 等待元素消失: {selector_desc}, 超时: {wait_timeout}ms")
        try:
            self._get_locator(selector).wait_for(state="hidden", timeout=wait_timeout)
            logger.info(f"[{self.page_name}] 元素已消失: {selector_desc}")
        except PlaywrightTimeoutError as e:
            logger.error(f"[{self.page_name}] 等待元素消失超时: {selector_desc}")
            raise e
        except Exception as e:
            logger.error(f"[{self.page_name}] 等待元素消失失败: {selector_desc}, 错误: {e}")
            raise e

    @allure.step("选择下拉选项")
    def select_option(self, selector: SelectorType, value: str) -> None:
        """
        选择下拉框选项

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
            value: 选项值
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 选择下拉选项: {selector_desc} -> '{value}'")
        try:
            self._get_locator(selector).select_option(value)
            logger.info(f"[{self.page_name}] 选择成功: {selector_desc} -> '{value}'")
        except Exception as e:
            logger.error(f"[{self.page_name}] 选择失败: {selector_desc}, 错误: {e}")
            raise e

    @allure.step("悬停元素")
    def hover(self, selector: SelectorType) -> None:
        """
        鼠标悬停在元素上

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 悬停元素: {selector_desc}")
        try:
            self._get_locator(selector).hover()
            logger.info(f"[{self.page_name}] 悬停成功: {selector_desc}")
        except Exception as e:
            logger.error(f"[{self.page_name}] 悬停失败: {selector_desc}, 错误: {e}")
            raise e

    def get_element_count(self, selector: SelectorType) -> int:
        """
        获取匹配元素的数量

        Args:
            selector: 元素选择器（字符串或 Locator 对象）

        Returns:
            匹配元素的数量
        """
        selector_desc = self._get_selector_desc(selector)
        count = self._get_locator(selector).count()
        logger.debug(f"[{self.page_name}] 元素数量: {selector_desc} -> {count}")
        return count

    def get_all_texts(self, selector: SelectorType) -> list[str]:
        """
        获取所有匹配元素的文本内容

        Args:
            selector: 元素选择器（字符串或 Locator 对象）

        Returns:
            文本内容列表
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 获取所有文本: {selector_desc}")
        texts = self._get_locator(selector).all_text_contents()
        logger.debug(f"[{self.page_name}] 获取到 {len(texts)} 个文本内容")
        return texts

    @allure.step("截图")
    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """
        截取当前页面截图

        Args:
            name: 截图名称

        Returns:
            截图的字节数据
        """
        logger.info(f"[{self.page_name}] 截取页面截图: {name}")
        try:
            screenshot = self.page.screenshot(full_page=True)
            allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
            logger.debug(f"[{self.page_name}] 截图完成: {name}")
            return screenshot
        except Exception as e:
            logger.error(f"[{self.page_name}] 截图失败: {e}")
            raise e

    def get_current_url(self) -> str:
        """
        获取当前页面 URL

        Returns:
            当前页面 URL
        """
        url = self.page.url
        logger.debug(f"[{self.page_name}] 当前 URL: {url}")
        return url

    def get_title(self) -> str:
        """
        获取页面标题

        Returns:
            页面标题
        """
        title = self.page.title()
        logger.debug(f"[{self.page_name}] 页面标题: {title}")
        return title

    @allure.step("刷新页面")
    def refresh(self) -> None:
        """刷新当前页面"""
        logger.info(f"[{self.page_name}] 刷新页面")
        self.page.reload()
        logger.debug(f"[{self.page_name}] 页面刷新完成")

    @allure.step("返回上一页")
    def go_back(self) -> None:
        """返回上一页"""
        logger.info(f"[{self.page_name}] 返回上一页")
        self.page.go_back()
        logger.debug(f"[{self.page_name}] 已返回上一页")

    @allure.step("前进到下一页")
    def go_forward(self) -> None:
        """前进到下一页"""
        logger.info(f"[{self.page_name}] 前进到下一页")
        self.page.go_forward()
        logger.debug(f"[{self.page_name}] 已前进到下一页")

    def expect_visible(self, selector: SelectorType) -> None:
        """
        断言元素可见

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 断言元素可见: {selector_desc}")
        try:
            expect(self._get_locator(selector)).to_be_visible()
            logger.info(f"[{self.page_name}] 断言通过 - 元素可见: {selector_desc}")
        except AssertionError as e:
            logger.error(f"[{self.page_name}] 断言失败 - 元素不可见: {selector_desc}")
            raise e

    def expect_text(self, selector: SelectorType, text: str) -> None:
        """
        断言元素包含指定文本

        Args:
            selector: 元素选择器（字符串或 Locator 对象）
            text: 期望的文本
        """
        selector_desc = self._get_selector_desc(selector)
        logger.debug(f"[{self.page_name}] 断言文本: {selector_desc} -> '{text}'")
        try:
            expect(self._get_locator(selector)).to_have_text(text)
            logger.info(f"[{self.page_name}] 断言通过 - 文本匹配: {selector_desc}")
        except AssertionError as e:
            logger.error(
                f"[{self.page_name}] 断言失败 - 文本不匹配: {selector_desc}, 期望: '{text}'"
            )
            raise e

    def expect_url_contains(self, url_part: str) -> None:
        """
        断言 URL 包含指定字符串

        Args:
            url_part: URL 中应包含的字符串
        """
        logger.debug(f"[{self.page_name}] 断言 URL 包含: '{url_part}'")
        try:
            expect(self.page).to_have_url(f"*{url_part}*")
            logger.info(f"[{self.page_name}] 断言通过 - URL 包含: '{url_part}'")
        except AssertionError as e:
            logger.error(
                f"[{self.page_name}] 断言失败 - URL 不包含: '{url_part}', 当前 URL: {self.page.url}"
            )
            raise e
