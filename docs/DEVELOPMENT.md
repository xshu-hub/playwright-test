# Playwright 自动化测试框架 - 开发文档

本文档详细介绍项目的架构设计、核心模块、开发规范和最佳实践，帮助开发者快速上手并编写高质量的自动化测试。

---

## 目录

1. [项目概述](#1-项目概述)
2. [环境搭建](#2-环境搭建)
3. [项目结构](#3-项目结构)
4. [核心模块详解](#4-核心模块详解)
5. [Page Object 模式](#5-page-object-模式)
6. [Fixtures 系统](#6-fixtures-系统)
7. [测试数据管理](#7-测试数据管理)
8. [配置管理](#8-配置管理)
9. [日志系统](#9-日志系统)
10. [编写测试用例](#10-编写测试用例)
11. [运行测试](#11-运行测试)
12. [测试报告](#12-测试报告)
13. [CI/CD 集成](#13-cicd-集成)
14. [最佳实践](#14-最佳实践)
15. [常见问题](#15-常见问题)

---

## 1. 项目概述

### 1.1 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 编程语言 |
| Playwright | 1.49+ | 浏览器自动化 |
| Pytest | 8.3+ | 测试框架 |
| Allure | 2.13+ | 测试报告 |

### 1.2 框架特性

- **Page Object 模式**：清晰的页面对象封装，提高代码复用性
- **多浏览器支持**：Chromium、Firefox、WebKit
- **Session 复用**：保存登录状态，加速测试执行
- **数据驱动测试**：JSON 数据文件驱动的参数化测试
- **Allure 报告**：美观详细的测试报告
- **失败自动重试**：提高测试稳定性
- **并行执行**：多进程并行执行测试
- **日志系统**：控制台和文件双输出

### 1.3 设计原则

1. **分层架构**：测试用例 → Page Object → Playwright API
2. **单一职责**：每个类/方法只做一件事
3. **DRY 原则**：通过封装减少重复代码
4. **可配置性**：通过环境变量灵活配置
5. **可维护性**：清晰的命名和完善的注释

---

## 2. 环境搭建

### 2.1 前置条件

- Python 3.10 或更高版本
- pip 包管理器
- Git（可选，用于版本控制）

### 2.2 安装步骤

#### 步骤 1：克隆/下载项目

```bash
git clone <repository-url>
cd playwright-test
```

#### 步骤 2：创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### 步骤 3：安装依赖

```bash
pip install -r requirements.txt
```

#### 步骤 4：安装 Playwright 浏览器

```bash
# 安装所有浏览器
playwright install

# 或只安装特定浏览器
playwright install chromium
```

#### 步骤 5：配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，配置测试系统信息
```

### 2.3 验证安装

```bash
# 运行冒烟测试验证环境
pytest -m smoke -v
```

---

## 3. 项目结构

```
playwright-test/
├── config/                     # 配置模块
│   ├── __init__.py
│   └── settings.py             # 项目配置类
│
├── pages/                      # Page Object 页面对象
│   ├── __init__.py
│   ├── base_page.py            # 页面基类（核心）
│   ├── login_page.py           # 登录页面
│   ├── dashboard_page.py       # 仪表盘页面
│   ├── pim_page.py             # PIM 员工管理页面
│   └── employee_form_page.py   # 员工表单页面
│
├── tests/                      # 测试用例
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures 配置（核心）
│   ├── test_login.py           # 登录功能测试
│   ├── test_employee_form.py   # 员工表单测试
│   └── test_employee_e2e.py    # 端到端测试
│
├── utils/                      # 工具模块
│   ├── __init__.py
│   ├── data_loader.py          # 测试数据加载器
│   ├── logger.py               # 日志工具
│   └── session_manager.py      # 多用户 Session 管理
│
├── data/                       # 测试数据
│   ├── test_data.json          # 测试数据文件
│   └── sessions/               # Session 状态文件（自动生成）
│
├── reports/                    # 测试报告（自动生成）
│   ├── allure-results/         # Allure 原始数据
│   └── allure-report/          # Allure HTML 报告
│
├── logs/                       # 日志文件（自动生成）
│
├── docs/                       # 文档
│   └── DEVELOPMENT.md          # 开发文档（本文件）
│
├── jenkins/                    # Jenkins 配置
│   └── README.md               # Jenkins 配置指南
│
├── .env.example                # 环境变量示例
├── pytest.ini                  # Pytest 配置
├── requirements.txt            # Python 依赖
├── Jenkinsfile                 # Jenkins 流水线配置
└── README.md                   # 项目说明
```

---

## 4. 核心模块详解

### 4.1 模块依赖关系

```
┌─────────────────────────────────────────────────────────┐
│                      测试用例层                          │
│              tests/test_*.py                            │
└───────────────────────┬─────────────────────────────────┘
                        │ 使用
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    Page Object 层                        │
│              pages/*_page.py                            │
│         ┌─────────────────────────────┐                 │
│         │      BasePage              │                  │
│         │  (封装 Playwright 操作)     │                  │
│         └──────────┬──────────────────┘                 │
│                    │ 继承                               │
│    ┌───────────────┼───────────────┐                   │
│    ▼               ▼               ▼                    │
│ LoginPage    DashboardPage    PIMPage ...               │
└───────────────────────┬─────────────────────────────────┘
                        │ 调用
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    基础设施层                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Settings │  │ Logger   │  │DataLoader│              │
│  │ (配置)   │  │ (日志)   │  │ (数据)   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└───────────────────────┬─────────────────────────────────┘
                        │ 依赖
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    Playwright API                        │
└─────────────────────────────────────────────────────────┘
```

### 4.2 数据流

```
环境变量 (.env)
      │
      ▼
配置类 (Settings)
      │
      ├──────────────────────────┐
      ▼                          ▼
Fixtures (conftest.py)      Page Objects
      │                          │
      └──────────┬───────────────┘
                 ▼
         测试用例 (test_*.py)
                 │
                 ▼
         Allure 报告
```

---

## 5. Page Object 模式

### 5.1 设计理念

Page Object 模式将页面的元素定位和操作封装在独立的类中，实现：

- **UI 与测试逻辑分离**：页面变化只需修改 Page Object
- **代码复用**：多个测试可共享同一个 Page Object
- **可读性**：测试代码更接近自然语言

### 5.2 BasePage 基类

`pages/base_page.py` 是所有页面对象的基类，封装了常用操作：

```python
class BasePage:
    """页面对象基类"""
    
    page_name: str = "BasePage"  # 页面名称，用于日志
    
    def __init__(self, page: Page):
        self.page = page
        self.timeout = settings.TIMEOUT
```

#### 核心方法一览

| 方法 | 功能 | 示例 |
|------|------|------|
| `navigate(url)` | 导航到 URL | `self.navigate("/login")` |
| `click(selector)` | 点击元素 | `self.click("#btn")` |
| `fill(selector, text)` | 输入文本 | `self.fill("#name", "test")` |
| `get_text(selector)` | 获取文本 | `self.get_text(".title")` |
| `is_visible(selector)` | 检查可见性 | `self.is_visible(".modal")` |
| `wait_for_visible(selector)` | 等待元素可见 | `self.wait_for_visible(".list")` |
| `wait_for_hidden(selector)` | 等待元素消失 | `self.wait_for_hidden(".loading")` |
| `take_screenshot(name)` | 截图 | `self.take_screenshot("error")` |
| `expect_visible(selector)` | 断言可见 | `self.expect_visible(".success")` |
| `expect_text(selector, text)` | 断言文本 | `self.expect_text(".msg", "OK")` |

#### 选择器支持

BasePage 支持两种选择器类型：

```python
# 字符串选择器
self.click("#submit-btn")
self.fill("input[name='username']", "admin")

# Locator 对象（推荐用于复杂定位）
username_input = self.page.get_by_label("用户名")
self.fill(username_input, "admin")
```

### 5.3 创建新的 Page Object

#### 步骤 1：创建页面类文件

```python
# pages/my_page.py
"""
MyPage - 我的页面对象
"""

from playwright.sync_api import Page
import allure

from pages.base_page import BasePage
from config.settings import settings


class MyPage(BasePage):
    """我的页面对象"""
    
    # 页面名称（用于日志）
    page_name = "MyPage"
    
    # 页面元素定位器（使用常量便于维护）
    TITLE = ".page-title"
    SUBMIT_BUTTON = "button[type='submit']"
    NAME_INPUT = "input[name='name']"
    SUCCESS_MESSAGE = ".alert-success"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{settings.BASE_URL}/my-page"
    
    @allure.step("打开我的页面")
    def open(self) -> "MyPage":
        """打开页面"""
        self.navigate(self.url)
        self.wait_for_visible(self.TITLE)
        return self
    
    @allure.step("填写表单")
    def fill_form(self, name: str) -> "MyPage":
        """填写表单"""
        self.fill(self.NAME_INPUT, name)
        return self
    
    @allure.step("提交表单")
    def submit(self) -> "MyPage":
        """提交表单"""
        self.click(self.SUBMIT_BUTTON)
        return self
    
    def is_success(self) -> bool:
        """检查是否成功"""
        return self.is_visible(self.SUCCESS_MESSAGE, timeout=5000)
```

#### 步骤 2：在 conftest.py 中添加 fixture

```python
# tests/conftest.py
from pages.my_page import MyPage

@pytest.fixture(scope="function")
def my_page(page: Page) -> MyPage:
    """创建我的页面对象"""
    return MyPage(page)
```

#### 步骤 3：在测试中使用

```python
# tests/test_my_feature.py
def test_my_feature(my_page: MyPage):
    my_page.open()
    my_page.fill_form("测试数据")
    my_page.submit()
    assert my_page.is_success()
```

### 5.4 Page Object 设计原则

1. **方法返回 self**：支持链式调用

```python
login_page.open().enter_username("admin").enter_password("123").click_login()
```

2. **使用 @allure.step 装饰器**：自动记录步骤到报告

```python
@allure.step("输入用户名: {username}")
def enter_username(self, username: str) -> "LoginPage":
    self.fill(self.USERNAME_INPUT, username)
    return self
```

3. **元素定位器使用常量**：便于维护

```python
class LoginPage(BasePage):
    # 推荐：使用常量
    USERNAME_INPUT = "input[name='username']"
    
    # 不推荐：硬编码在方法中
    def enter_username(self, username):
        self.fill("input[name='username']", username)  # 不好维护
```

4. **封装业务操作**：而不是简单的元素操作

```python
# 推荐：封装业务操作
def login(self, username: str, password: str):
    self.enter_username(username)
    self.enter_password(password)
    self.click_login()

# 不推荐：测试中直接操作元素
def test_login(page):
    page.fill("#username", "admin")
    page.fill("#password", "123")
    page.click("#login")
```

---

## 6. Fixtures 系统

### 6.1 Fixtures 概述

Pytest Fixtures 是测试的基础设施，提供：

- 浏览器和页面实例
- Page Object 实例
- 测试数据
- 前置/后置操作

### 6.2 核心 Fixtures

#### 浏览器相关

```python
# session 级别：整个测试会话共享一个浏览器实例
@pytest.fixture(scope="session")
def browser(playwright_instance, browser_type_name, is_headed, slow_mo):
    """创建浏览器实例"""
    browser_type = getattr(playwright_instance, browser_type_name)
    browser = browser_type.launch(headless=not is_headed, slow_mo=slow_mo)
    yield browser
    browser.close()

# function 级别：每个测试函数独立的上下文
@pytest.fixture(scope="function")
def context(browser: Browser):
    """创建浏览器上下文"""
    context = browser.new_context(**settings.get_context_config())
    yield context
    context.close()

# function 级别：每个测试函数独立的页面
@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """创建页面实例"""
    page = context.new_page()
    page.set_default_timeout(settings.TIMEOUT)
    yield page
    page.close()
```

#### Page Object Fixtures

```python
@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """登录页面对象"""
    return LoginPage(page)

@pytest.fixture(scope="function")
def logged_in_page(page: Page) -> Page:
    """已登录状态的页面"""
    login_page = LoginPage(page)
    login_page.open().login_as_admin()
    login_page.wait_for_login_complete()
    yield page
```

### 6.3 Fixture 作用域

| 作用域 | 说明 | 使用场景 |
|--------|------|----------|
| `function` | 每个测试函数执行一次 | 页面、上下文（默认） |
| `class` | 每个测试类执行一次 | 共享测试数据 |
| `module` | 每个模块执行一次 | 模块级资源 |
| `session` | 整个会话执行一次 | 浏览器实例 |

### 6.4 自定义命令行参数

```python
# conftest.py
def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption(
        "--browser-type",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="选择浏览器类型",
    )
    parser.addoption(
        "--reuse-session",
        action="store_true",
        default=False,
        help="复用已保存的登录状态",
    )

# 获取参数值
@pytest.fixture(scope="session")
def browser_type_name(request) -> str:
    return request.config.getoption("--browser-type")
```

### 6.5 Fixtures 一览表

| Fixture | 作用域 | 说明 |
|---------|--------|------|
| `page` | function | Playwright 页面实例 |
| `context` | function | 浏览器上下文 |
| `browser` | session | 浏览器实例 |
| `login_page` | function | 登录页面对象 |
| `dashboard_page` | function | 仪表盘页面对象 |
| `pim_page` | function | PIM 页面对象 |
| `logged_in_page` | function | 已登录的页面 |
| `logged_in_dashboard` | function | 已登录的仪表盘页面 |
| `auth_state` | session | Session 状态文件路径 |
| `auth_context` | function | 已认证的浏览器上下文 |
| `auth_page` | function | 已认证的页面实例 |

---

## 7. 测试数据管理

### 7.1 数据文件结构

测试数据存放在 `data/test_data.json`：

```json
{
  "users": {
    "admin": {
      "username": "Admin",
      "password": "admin123",
      "description": "系统管理员"
    }
  },
  "employees": {
    "new_employee": {
      "first_name": "Test",
      "last_name": "Employee"
    }
  },
  "error_messages": {
    "required_field": "Required",
    "invalid_credentials": "Invalid credentials"
  }
}
```

### 7.2 TestDataLoader 使用

```python
from utils.data_loader import TestDataLoader

# 获取用户信息
user = TestDataLoader.get_user("admin")
print(user["username"])  # "Admin"

# 获取员工信息
employee = TestDataLoader.get_employee("new_employee")

# 获取错误消息
error = TestDataLoader.get_error_message("required_field")

# 获取所有用户
all_users = TestDataLoader.get_all_users()
```

### 7.3 数据驱动测试

```python
import pytest
from utils.data_loader import TestDataLoader

@pytest.mark.parametrize(
    "username, password, error_key, description",
    TestDataLoader.get_login_failure_test_cases(),
    ids=lambda x: x if isinstance(x, str) and len(x) < 20 else None,
)
def test_login_failure(login_page, username, password, error_key, description):
    """数据驱动的登录失败测试"""
    login_page.open()
    login_page.login(username, password)
    assert login_page.is_error_displayed()
```

### 7.4 添加新的测试数据

#### 步骤 1：在 test_data.json 中添加数据

```json
{
  "my_feature": {
    "valid_data": {
      "name": "Test",
      "value": 100
    },
    "invalid_data": {
      "name": "",
      "value": -1
    }
  }
}
```

#### 步骤 2：在 TestDataLoader 中添加方法

```python
# utils/data_loader.py
@classmethod
def get_my_feature_data(cls, data_type: str = "valid_data") -> dict:
    """获取我的功能测试数据"""
    data = cls._load_data()
    return data["my_feature"][data_type]
```

#### 步骤 3：在测试中使用

```python
def test_my_feature(my_page):
    data = TestDataLoader.get_my_feature_data("valid_data")
    my_page.fill_form(data["name"])
```

---

## 8. 配置管理

### 8.1 Settings 类

`config/settings.py` 集中管理所有配置：

```python
class Settings:
    """项目配置类"""
    
    # 基础 URL
    BASE_URL: str = os.getenv("BASE_URL", "https://default-url.com")
    
    # 超时设置（毫秒）
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30000"))
    
    # 无头模式
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    
    # 浏览器视口
    VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "1080"))
    
    # 测试用户
    ADMIN_USER: str = os.getenv("ADMIN_USER", "Admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
```

### 8.2 环境变量配置

创建 `.env` 文件（从 `.env.example` 复制）：

```bash
# 测试目标网站
BASE_URL=https://your-test-system.com

# 超时时间（毫秒）
TIMEOUT=30000

# 无头模式
HEADLESS=true

# 测试用户
ADMIN_USER=your_username
ADMIN_PASSWORD=your_password

# 日志级别
LOG_LEVEL=INFO
```

### 8.3 配置优先级

1. 环境变量（最高优先级）
2. `.env` 文件
3. 代码中的默认值

### 8.4 辅助方法

```python
# 获取浏览器启动配置
browser_config = Settings.get_browser_config()
# {'headless': True, 'slow_mo': 0}

# 获取上下文配置
context_config = Settings.get_context_config()
# {'viewport': {'width': 1920, 'height': 1080}, 'ignore_https_errors': True}

# 获取 Session 文件路径
session_file = Settings.get_session_file_path("admin")
# Path('data/sessions/admin_session.json')
```

---

## 9. 日志系统

### 9.1 日志配置

`utils/logger.py` 提供统一的日志功能：

- 控制台输出：彩色日志，便于调试
- 文件输出：详细日志，便于问题排查
- 日志轮转：自动清理旧日志文件

### 9.2 使用方法

```python
from utils.logger import logger

# 记录不同级别的日志
logger.debug("详细调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")

# 记录异常（包含堆栈）
try:
    risky_operation()
except Exception:
    logger.exception("操作失败")
```

### 9.3 日志级别配置

通过环境变量配置：

```bash
# 控制台日志级别
LOG_LEVEL=INFO

# 文件日志级别
FILE_LOG_LEVEL=DEBUG

# 日志文件大小限制（字节）
LOG_MAX_BYTES=5242880

# 日志文件备份数量
LOG_BACKUP_COUNT=5
```

### 9.4 日志输出格式

**控制台格式**：
```
2024-01-15 10:30:45 [INFO] 登录成功
```

**文件格式**：
```
2024-01-15 10:30:45 [INFO] [login_page.py:95] 登录成功
```

---

## 10. 编写测试用例

### 10.1 测试文件命名

- 测试文件：`test_<feature>.py`
- 测试类：`Test<Feature>`
- 测试方法：`test_<scenario>`

```python
# tests/test_login.py
class TestLogin:
    def test_login_success(self):
        pass
    
    def test_login_with_invalid_password(self):
        pass
```

### 10.2 测试用例模板

```python
"""
<功能>测试用例
测试 <系统> 的 <功能>
"""

import allure
import pytest

from pages.my_page import MyPage


@allure.feature("功能模块名称")
class TestMyFeature:
    """功能测试类"""

    @allure.story("用户故事")
    @allure.title("测试用例标题")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_scenario(self, my_page: MyPage):
        """
        测试场景描述
        
        前置条件:
        - 条件1
        - 条件2
        
        步骤:
        1. 步骤1
        2. 步骤2
        3. 步骤3
        
        预期结果:
        - 结果1
        - 结果2
        """
        with allure.step("步骤1"):
            my_page.open()
        
        with allure.step("步骤2"):
            my_page.do_something()
        
        with allure.step("验证结果"):
            assert my_page.is_success(), "操作应该成功"
```

### 10.3 Allure 装饰器

```python
import allure

# 功能模块
@allure.feature("登录功能")

# 用户故事
@allure.story("正常登录")

# 测试标题
@allure.title("使用管理员账号登录成功")

# 严重程度
@allure.severity(allure.severity_level.CRITICAL)  # BLOCKER, CRITICAL, NORMAL, MINOR, TRIVIAL

# 测试步骤
with allure.step("打开登录页面"):
    login_page.open()

# 动态标题
allure.dynamic.title(f"测试用户: {username}")

# 附加信息
allure.attach("附加内容", name="附件名", attachment_type=allure.attachment_type.TEXT)
```

### 10.4 测试标记

```python
# 冒烟测试
@pytest.mark.smoke

# 回归测试
@pytest.mark.regression

# 登录相关
@pytest.mark.login

# 端到端测试
@pytest.mark.e2e

# 组合标记
@pytest.mark.smoke
@pytest.mark.login
def test_login():
    pass
```

### 10.5 参数化测试

```python
@pytest.mark.parametrize(
    "username, password, expected",
    [
        ("admin", "admin123", True),
        ("user", "wrong", False),
        ("", "123", False),
    ],
    ids=["管理员登录", "错误密码", "空用户名"]
)
def test_login_scenarios(login_page, username, password, expected):
    login_page.open()
    login_page.login(username, password)
    assert login_page.is_logged_in() == expected
```

### 10.6 跳过测试

```python
# 无条件跳过
@pytest.mark.skip(reason="功能未实现")
def test_not_implemented():
    pass

# 条件跳过
@pytest.mark.skipif(
    settings.BASE_URL.startswith("https://prod"),
    reason="不在生产环境执行"
)
def test_dangerous_operation():
    pass

# 预期失败
@pytest.mark.xfail(reason="已知Bug #123")
def test_known_bug():
    pass
```

---

## 11. 运行测试

### 11.1 基本命令

```bash
# 运行所有测试
pytest

# 运行指定文件
pytest tests/test_login.py

# 运行指定类
pytest tests/test_login.py::TestLogin

# 运行指定方法
pytest tests/test_login.py::TestLogin::test_login_success

# 详细输出
pytest -v

# 显示 print 输出
pytest -s

# 组合
pytest -vs tests/test_login.py
```

### 11.2 浏览器选择

```bash
# Chromium（默认）
pytest --browser-type chromium

# Firefox
pytest --browser-type firefox

# WebKit
pytest --browser-type webkit
```

### 11.3 显示模式

```bash
# 无头模式（默认，后台运行）
pytest

# 有头模式（显示浏览器）
pytest --headed

# 慢动作模式（便于观察）
pytest --headed --slowmo 500
```

### 11.4 测试标记筛选

```bash
# 运行冒烟测试
pytest -m smoke

# 运行登录测试
pytest -m login

# 组合标记
pytest -m "smoke and login"
pytest -m "smoke or regression"
pytest -m "not slow"
```

### 11.5 并行执行

```bash
# 自动检测 CPU 核心数
pytest -n auto

# 指定并行数
pytest -n 4

# 并行 + 指定目录
pytest -n 4 tests/
```

### 11.6 失败处理

```bash
# 失败后停止
pytest -x

# 失败 N 次后停止
pytest --maxfail=3

# 只运行上次失败的测试
pytest --lf

# 先运行上次失败的测试
pytest --ff

# 禁用重试
pytest --reruns 0
```

### 11.7 Session 复用

```bash
# 首次运行：保存登录状态
pytest --save-session

# 后续运行：复用登录状态（加速测试）
pytest --reuse-session
```

---

## 12. 测试报告

### 12.1 Allure 报告

#### 生成报告

```bash
# 运行测试（自动生成 allure-results）
pytest --alluredir=reports/allure-results

# 查看报告（启动临时服务器）
allure serve reports/allure-results

# 生成静态报告
allure generate reports/allure-results -o reports/allure-report --clean

# 打开静态报告
allure open reports/allure-report
```

#### 报告内容

- **Overview**：测试概览，通过/失败统计
- **Suites**：按测试套件分组
- **Graphs**：趋势图表
- **Timeline**：执行时间线
- **Behaviors**：按 Feature/Story 分组
- **Packages**：按模块分组

### 12.2 JUnit 报告

```bash
# 生成 JUnit XML 报告
pytest --junitxml=reports/junit.xml
```

### 12.3 HTML 报告

```bash
# 安装插件
pip install pytest-html

# 生成报告
pytest --html=reports/report.html
```

---

## 13. CI/CD 集成

### 13.1 Jenkins 集成

项目提供 `Jenkinsfile` 配置文件，支持：

- 参数化构建（浏览器选择、冒烟测试）
- 自动化测试执行
- Allure 报告生成
- 构建产物归档

详细配置请参考 `jenkins/README.md`。

### 13.2 流水线阶段

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  检出代码   │ -> │  环境准备   │ -> │  安装依赖   │
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                                             v
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  生成报告   │ <- │  运行测试   │ <- │  安装浏览器  │
└─────────────┘    └─────────────┘    └─────────────┘
```

---

## 14. 最佳实践

### 15.1 测试设计

1. **独立性**：每个测试应该独立运行，不依赖其他测试的执行顺序
2. **原子性**：每个测试只验证一个功能点
3. **可重复性**：测试结果应该稳定，多次运行结果一致
4. **自清理**：测试产生的数据应该清理或隔离

### 15.2 元素定位

优先级（从高到低）：

1. `data-testid` 属性（最稳定）
2. `id` 属性
3. `name` 属性
4. 文本内容（使用 Playwright 的 `get_by_text`）
5. CSS 选择器
6. XPath（最后选择）

```python
# 推荐
self.page.locator("[data-testid='submit-btn']")
self.page.get_by_role("button", name="提交")
self.page.get_by_label("用户名")

# 避免
self.page.locator("//div[@class='form']/button[2]")  # 脆弱的 XPath
```

### 15.3 等待策略

```python
# 推荐：显式等待
self.wait_for_visible(".result")
self.page.wait_for_url("**/dashboard")
self.page.wait_for_load_state("networkidle")

# 避免：硬编码等待
import time
time.sleep(3)  # 不推荐
```

### 15.4 断言

```python
# 推荐：使用 Playwright expect
from playwright.sync_api import expect

expect(page.locator(".title")).to_be_visible()
expect(page.locator(".count")).to_have_text("10")
expect(page).to_have_url("**/dashboard")

# 或使用 pytest assert（提供更好的错误信息）
assert login_page.is_logged_in(), "登录应该成功"
```

### 15.5 错误处理

```python
# 在 Page Object 中处理异常
def click_optional_button(self) -> bool:
    """点击可选按钮，不存在则返回 False"""
    try:
        self.click(self.OPTIONAL_BUTTON)
        return True
    except PlaywrightTimeoutError:
        logger.info("可选按钮不存在，跳过")
        return False
```

---

## 15. 常见问题

### Q1: 测试运行很慢

**解决方案**：

1. 使用 Session 复用跳过重复登录
2. 使用并行执行 `pytest -n auto`
3. 只安装需要的浏览器 `playwright install chromium`

### Q2: 元素找不到

**排查步骤**：

1. 检查选择器是否正确
2. 添加等待 `wait_for_visible()`
3. 使用有头模式调试 `pytest --headed`
4. 使用 Playwright Inspector：`PWDEBUG=1 pytest ...`

### Q3: 测试不稳定

**解决方案**：

1. 增加显式等待
2. 使用更稳定的选择器
3. 启用失败重试 `--reruns=2`
4. 检查是否有竞态条件

### Q4: 如何调试

```bash
# 方法1：有头模式 + 慢动作
pytest --headed --slowmo 1000

# 方法2：Playwright Inspector
PWDEBUG=1 pytest tests/test_login.py::TestLogin::test_login_success

# 方法3：在代码中添加断点
page.pause()  # 会暂停执行并打开 Inspector
```

### Q5: 如何处理弹窗

```python
# 处理 alert
page.on("dialog", lambda dialog: dialog.accept())

# 处理确认框
page.on("dialog", lambda dialog: dialog.dismiss())

# 获取弹窗内容
def handle_dialog(dialog):
    print(dialog.message)
    dialog.accept()
page.on("dialog", handle_dialog)
```

### Q6: 如何处理新窗口/标签页

```python
# 等待新页面打开
with page.expect_popup() as popup_info:
    page.click("#open-new-window")
new_page = popup_info.value

# 在新页面操作
new_page.fill("#input", "text")
new_page.close()
```

### Q7: 如何上传文件

```python
# 方法1：直接设置文件
page.set_input_files("input[type='file']", "path/to/file.pdf")

# 方法2：处理文件选择对话框
with page.expect_file_chooser() as fc_info:
    page.click("#upload-btn")
file_chooser = fc_info.value
file_chooser.set_files("path/to/file.pdf")
```

---

## 附录：常用命令速查

```bash
# 环境
python -m venv venv                    # 创建虚拟环境
pip install -r requirements.txt        # 安装依赖
playwright install                     # 安装浏览器

# 运行测试
pytest                                 # 运行所有测试
pytest -m smoke                        # 运行冒烟测试
pytest -v --headed                     # 有头模式详细输出
pytest -n auto                         # 并行执行
pytest --reuse-session                 # 复用 Session

# 报告
allure serve reports/allure-results    # 查看 Allure 报告

# 调试
PWDEBUG=1 pytest tests/test_login.py   # Playwright Inspector
pytest --headed --slowmo 500           # 慢动作模式
```

---

*文档版本：1.0*
*最后更新：2024年*
