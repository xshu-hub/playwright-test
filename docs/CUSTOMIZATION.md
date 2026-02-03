# 自定义指南：为你的系统创建测试

本指南帮助你使用此框架为你自己的系统创建自动化测试。

## 目录

- [快速开始](#快速开始)
- [第一步：配置环境](#第一步配置环境)
- [第二步：创建页面对象](#第二步创建页面对象)
- [第三步：编写测试用例](#第三步编写测试用例)
- [第四步：配置 Fixtures](#第四步配置-fixtures)
- [第五步：管理测试数据](#第五步管理测试数据)
- [进阶：Session 复用](#进阶session-复用)
- [最佳实践](#最佳实践)

---

## 快速开始

### 你需要修改的文件

| 文件 | 必须修改 | 说明 |
|------|---------|------|
| `.env` | 是 | 配置你的系统 URL 和登录凭证 |
| `pages/your_*.py` | 是 | 创建你的页面对象 |
| `tests/test_your_*.py` | 是 | 创建你的测试用例 |
| `tests/conftest.py` | 可选 | 添加你的页面对象 fixtures |
| `data/test_data.json` | 可选 | 配置你的测试数据 |

### 可以直接复用的文件

| 文件 | 说明 |
|------|------|
| `pages/base_page.py` | 页面基类，封装了常用操作 |
| `utils/logger.py` | 日志工具 |
| `utils/data_loader.py` | 数据加载器 |
| `utils/session_manager.py` | Session 管理器 |
| `config/settings.py` | 配置模块（只需配置环境变量） |

---

## 第一步：配置环境

### 1.1 创建 .env 文件

```bash
cp .env.example .env
```

### 1.2 修改目标系统配置

编辑 `.env` 文件：

```bash
# 你的测试系统 URL
BASE_URL=https://your-system.example.com

# 测试账号
ADMIN_USER=your_admin_username
ADMIN_PASSWORD=your_admin_password

# Session 验证（用于 Session 复用功能）
SESSION_VALIDATION_PATH=/dashboard    # 登录后能访问的页面路径
LOGIN_URL_PATTERN=/login              # 登录页面 URL 特征
```

### 1.3 验证配置

```bash
# 运行一个简单的测试验证配置
python -c "from config.settings import settings; print(f'BASE_URL: {settings.BASE_URL}')"
```

---

## 第二步：创建页面对象

页面对象（Page Object）封装了页面的元素和操作，是测试代码复用的核心。

### 2.1 创建登录页面

```python
# pages/your_login_page.py
"""
YourLoginPage - 你的系统登录页面

根据你的系统修改元素定位器和登录流程。
"""

from pages.base_page import BasePage
from config.settings import settings


class YourLoginPage(BasePage):
    """你的系统登录页面对象"""

    # 页面名称（用于日志输出）
    page_name = "YourLoginPage"

    # ==================== 元素定位器 ====================
    # 根据你的系统实际情况修改这些选择器
    
    USERNAME_INPUT = "#username"           # 用户名输入框
    PASSWORD_INPUT = "#password"           # 密码输入框
    LOGIN_BUTTON = "button[type='submit']" # 登录按钮
    ERROR_MESSAGE = ".error-message"       # 错误消息
    
    # 登录成功后的元素（用于验证登录状态）
    USER_MENU = ".user-menu"               # 用户菜单

    def __init__(self, page):
        super().__init__(page)
        self.url = f"{settings.BASE_URL}/login"

    def open(self) -> "YourLoginPage":
        """打开登录页面"""
        self.navigate(self.url)
        self.wait_for_visible(self.LOGIN_BUTTON)
        return self

    def enter_username(self, username: str) -> "YourLoginPage":
        """输入用户名"""
        self.fill(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "YourLoginPage":
        """输入密码"""
        self.fill(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> "YourLoginPage":
        """点击登录按钮"""
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str) -> "YourLoginPage":
        """执行登录操作"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def login_as_admin(self) -> "YourLoginPage":
        """使用管理员账号登录"""
        return self.login(settings.ADMIN_USER, settings.ADMIN_PASSWORD)

    def is_logged_in(self) -> bool:
        """检查是否登录成功"""
        return self.is_visible(self.USER_MENU, timeout=10000)

    def get_error_message(self) -> str:
        """获取错误消息"""
        if self.is_visible(self.ERROR_MESSAGE, timeout=3000):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_login_page(self) -> bool:
        """检查是否在登录页面"""
        return self.is_visible(self.LOGIN_BUTTON, timeout=3000)
```

### 2.2 创建其他页面

使用相同的模式创建其他页面对象：

```python
# pages/your_dashboard_page.py
"""你的系统仪表盘页面"""

from pages.base_page import BasePage
from config.settings import settings


class YourDashboardPage(BasePage):
    """仪表盘页面对象"""

    page_name = "YourDashboardPage"

    # 元素定位器
    WELCOME_MESSAGE = ".welcome"
    SIDEBAR = ".sidebar"
    LOGOUT_BUTTON = "#logout"

    def __init__(self, page):
        super().__init__(page)
        self.url = f"{settings.BASE_URL}/dashboard"

    def open(self) -> "YourDashboardPage":
        """打开仪表盘页面"""
        self.navigate(self.url)
        return self

    def is_on_dashboard(self) -> bool:
        """检查是否在仪表盘页面"""
        return "dashboard" in self.get_current_url()

    def logout(self) -> "YourDashboardPage":
        """退出登录"""
        self.click(self.LOGOUT_BUTTON)
        return self
```

### 2.3 BasePage 提供的常用方法

`BasePage` 基类提供了丰富的页面操作方法：

| 方法 | 说明 |
|------|------|
| `navigate(url)` | 导航到指定 URL |
| `click(selector)` | 点击元素 |
| `fill(selector, text)` | 填写输入框 |
| `clear_and_fill(selector, text)` | 清空并填写 |
| `get_text(selector)` | 获取元素文本 |
| `get_input_value(selector)` | 获取输入框值 |
| `is_visible(selector, timeout)` | 检查元素是否可见 |
| `is_hidden(selector, timeout)` | 检查元素是否隐藏 |
| `wait_for_visible(selector, timeout)` | 等待元素可见 |
| `wait_for_hidden(selector, timeout)` | 等待元素消失 |
| `select_option(selector, value)` | 选择下拉选项 |
| `hover(selector)` | 鼠标悬停 |
| `get_element_count(selector)` | 获取匹配元素数量 |
| `get_all_texts(selector)` | 获取所有匹配元素的文本 |
| `take_screenshot(name)` | 截图 |
| `get_current_url()` | 获取当前 URL |
| `get_title()` | 获取页面标题 |
| `refresh()` | 刷新页面 |
| `go_back()` | 返回上一页 |
| `expect_visible(selector)` | 断言元素可见 |
| `expect_text(selector, text)` | 断言元素包含指定文本 |

---

## 第三步：编写测试用例

### 3.1 基本测试结构

```python
# tests/test_your_login.py
"""你的系统登录测试"""

import pytest
import allure
from pages.your_login_page import YourLoginPage


@allure.feature("登录功能")
class TestYourLogin:
    """登录功能测试类"""

    @allure.story("正常登录")
    @allure.title("使用管理员账号登录成功")
    @pytest.mark.smoke
    def test_login_success(self, page):
        """测试正常登录"""
        login_page = YourLoginPage(page)
        
        with allure.step("打开登录页面"):
            login_page.open()
        
        with allure.step("输入凭证并登录"):
            login_page.login_as_admin()
        
        with allure.step("验证登录成功"):
            assert login_page.is_logged_in(), "登录失败"

    @allure.story("登录失败")
    @allure.title("使用错误密码登录失败")
    def test_login_with_wrong_password(self, page):
        """测试错误密码登录"""
        login_page = YourLoginPage(page)
        
        login_page.open()
        login_page.login("admin", "wrong_password")
        
        assert not login_page.is_logged_in()
        error = login_page.get_error_message()
        assert error, "应显示错误消息"
```

### 3.2 使用数据驱动测试

```python
import pytest
from utils.data_loader import TestDataLoader

class TestDataDriven:
    
    @pytest.mark.parametrize(
        "username, password, expected_result",
        [
            ("admin", "admin123", True),
            ("admin", "wrong", False),
            ("", "admin123", False),
        ],
        ids=["正确凭证", "错误密码", "空用户名"]
    )
    def test_login_scenarios(self, page, username, password, expected_result):
        """数据驱动的登录测试"""
        login_page = YourLoginPage(page)
        login_page.open()
        login_page.login(username, password)
        
        assert login_page.is_logged_in() == expected_result
```

### 3.3 使用测试标记

```python
@pytest.mark.smoke      # 冒烟测试
@pytest.mark.regression # 回归测试
@pytest.mark.e2e        # 端到端测试
def test_example(self, page):
    pass
```

运行特定标记的测试：

```bash
pytest -m smoke           # 只运行冒烟测试
pytest -m "not e2e"       # 排除 E2E 测试
pytest -m "smoke and login"  # 组合标记
```

---

## 第四步：配置 Fixtures

### 4.1 添加页面对象 Fixtures

在 `tests/conftest.py` 中添加你的页面对象 fixtures：

```python
# tests/conftest.py

# 在文件末尾添加你的 fixtures

from pages.your_login_page import YourLoginPage
from pages.your_dashboard_page import YourDashboardPage


# ==============================================================================
# [你的系统] 页面对象 Fixtures
# ==============================================================================


@pytest.fixture(scope="function")
def your_login_page(page: Page) -> YourLoginPage:
    """创建你的登录页面对象"""
    return YourLoginPage(page)


@pytest.fixture(scope="function")
def your_dashboard_page(page: Page) -> YourDashboardPage:
    """创建你的仪表盘页面对象"""
    return YourDashboardPage(page)


@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Generator[Page, None, None]:
    """已登录状态的页面"""
    login_page = YourLoginPage(page)
    login_page.open().login_as_admin()
    
    # 等待登录完成 - 根据你的系统调整
    page.wait_for_url("**/dashboard/**", timeout=30000)
    
    yield page
```

### 4.2 在测试中使用 Fixtures

```python
class TestWithFixtures:
    
    def test_login(self, your_login_page):
        """使用 login_page fixture"""
        your_login_page.open()
        your_login_page.login_as_admin()
        assert your_login_page.is_logged_in()
    
    def test_dashboard(self, logged_in_page, your_dashboard_page):
        """使用已登录的页面"""
        # logged_in_page 已经完成登录
        your_dashboard_page.open()
        assert your_dashboard_page.is_on_dashboard()
```

---

## 第五步：管理测试数据

### 5.1 使用 JSON 数据文件

编辑 `data/test_data.json`：

```json
{
  "users": {
    "admin": {
      "username": "admin",
      "password": "admin123",
      "description": "管理员账号"
    },
    "user": {
      "username": "testuser",
      "password": "test123",
      "description": "普通用户"
    }
  },
  "error_messages": {
    "invalid_credentials": "用户名或密码错误",
    "required_field": "此字段必填"
  }
}
```

### 5.2 使用 TestDataLoader

```python
from utils.data_loader import TestDataLoader

# 获取用户信息
admin = TestDataLoader.get_user("admin")
print(admin["username"])  # "admin"

# 获取错误消息
error_msg = TestDataLoader.get_error_message("invalid_credentials")
```

### 5.3 自定义数据加载方法

如果你的数据结构不同，可以扩展 `TestDataLoader`：

```python
# utils/data_loader.py

class TestDataLoader:
    # ... 现有方法 ...
    
    @classmethod
    def get_your_custom_data(cls, key: str) -> dict:
        """获取自定义数据"""
        data = cls._load_data()
        return data.get("your_custom_section", {}).get(key, {})
```

---

## 进阶：Session 复用

Session 复用可以保存登录状态，避免每次测试都重新登录，显著加速测试执行。

### 配置 Session 复用

1. **修改 `auth_state` fixture**（在 `tests/conftest.py` 中）：

```python
@pytest.fixture(scope="session")
def auth_state(browser: Browser, reuse_session: bool, save_session: bool):
    # ...
    
    if save_session or reuse_session:
        # 修改此处的登录逻辑为你的系统
        login_page = YourLoginPage(page)  # 改为你的登录页面
        login_page.open().login_as_admin()
        
        # 修改等待条件为你的系统登录成功后的 URL
        page.wait_for_url("**/your-dashboard/**", timeout=settings.TIMEOUT)
        
        # ...
```

2. **配置 Session 验证**（在 `.env` 中）：

```bash
# 登录后能访问的页面（用于验证 Session 是否有效）
SESSION_VALIDATION_PATH=/dashboard

# 登录页面 URL 特征（被重定向到此则说明 Session 失效）
LOGIN_URL_PATTERN=/login
```

### 使用 Session 复用

```bash
# 首次运行：执行登录并保存 Session
pytest --save-session

# 后续运行：复用 Session，跳过登录
pytest --reuse-session

# 或通过环境变量
REUSE_SESSION=true pytest
```

---

## 最佳实践

### 1. 页面对象设计

- 每个页面一个类
- 元素定位器定义为类属性
- 操作方法返回 `self` 支持链式调用
- 验证方法返回布尔值或具体数据

### 2. 测试用例设计

- 测试方法名清晰表达测试目的
- 使用 `with allure.step()` 划分测试步骤
- 单个测试只验证一个功能点
- 测试之间相互独立，不依赖执行顺序

### 3. 元素定位器选择

优先级从高到低：
1. `data-testid` 属性（推荐）
2. `id` 属性
3. `name` 属性
4. CSS 选择器
5. XPath（尽量避免）

### 4. 等待策略

- 优先使用显式等待（`wait_for_visible`）
- 避免硬编码的 `time.sleep()`
- 设置合理的超时时间

### 5. 测试数据管理

- 测试数据与测试代码分离
- 敏感数据通过环境变量配置
- 测试完成后清理创建的数据

---

## 常见问题

### Q: 如何调试定位器？

```bash
# 有头模式 + 慢动作
pytest --headed --slowmo 1000 tests/test_your_login.py -v

# 使用 Playwright 调试器
PWDEBUG=1 pytest tests/test_your_login.py::TestYourLogin::test_login_success
```

### Q: 元素找不到怎么办？

1. 检查定位器是否正确
2. 检查元素是否在 iframe 中
3. 增加等待时间
4. 使用 `page.pause()` 暂停调试

### Q: 如何处理动态元素？

```python
# 等待元素出现
self.wait_for_visible(".dynamic-element", timeout=10000)

# 等待元素消失
self.wait_for_hidden(".loading-spinner", timeout=10000)

# 等待页面 URL 变化
self.page.wait_for_url("**/expected-path/**")
```

---

## 参考资料

- [Playwright Python 文档](https://playwright.dev/python/)
- [Pytest 文档](https://docs.pytest.org/)
- [Allure 报告文档](https://docs.qameta.io/allure/)
