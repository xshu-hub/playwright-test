# Playwright Web 自动化测试框架

基于 **Playwright + Pytest + Allure + Page Object** 模式的 Web 自动化测试框架。

## 特性

- **Page Object 模式**：清晰的页面对象封装，提高代码复用性和可维护性
- **多浏览器支持**：支持 Chromium、Firefox、WebKit 三大浏览器
- **数据驱动测试**：支持 JSON 数据文件驱动的参数化测试
- **Allure 报告**：美观详细的测试报告，支持截图和步骤记录
- **失败自动重试**：测试失败自动重试机制，提高测试稳定性
- **并行执行**：支持多进程并行执行测试，加快执行速度
- **CI/CD 集成**：内置 GitHub Actions 配置，支持自动化测试流水线
- **日志记录**：完善的日志系统，支持控制台和文件双输出
- **环境配置**：支持通过环境变量灵活配置测试环境

## 项目结构

```
playwright-test/
├── .github/workflows/     # GitHub Actions CI/CD 配置
│   └── test.yml           # 测试工作流配置
├── config/                # 配置模块
│   └── settings.py        # 项目配置类
├── pages/                 # Page Object 页面对象
│   ├── base_page.py       # 页面基类
│   ├── login_page.py      # 登录页面
│   ├── inventory_page.py  # 商品列表页面
│   └── cart_page.py       # 购物车页面
├── tests/                 # 测试用例
│   ├── conftest.py        # Pytest fixtures 配置
│   ├── test_login.py      # 登录功能测试
│   └── test_cart.py       # 购物车功能测试
├── utils/                 # 工具模块
│   ├── data_loader.py     # 测试数据加载器
│   └── logger.py          # 日志工具
├── data/                  # 测试数据
│   └── test_data.json     # 测试数据文件
├── reports/               # 测试报告输出目录
├── logs/                  # 日志文件目录（自动生成）
├── .env.example           # 环境变量示例
├── pytest.ini             # Pytest 配置
├── ruff.toml              # Ruff 代码检查配置
└── requirements.txt       # Python 依赖
```

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install
```

### 2. 配置环境变量（可选）

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件配置你的测试环境
```

### 3. 运行测试

```bash
# 运行所有测试（无头模式）
pytest

# 运行指定浏览器测试
pytest --browser-type chromium
pytest --browser-type firefox
pytest --browser-type webkit

# 有头模式运行（可视化）
pytest --headed

# 慢动作模式（便于调试，单位毫秒）
pytest --headed --slowmo 500

# 运行带标记的测试
pytest -m smoke          # 冒烟测试
pytest -m login          # 登录测试
pytest -m cart           # 购物车测试
pytest -m "smoke and login"  # 组合标记

# 并行运行测试（需要 pytest-xdist）
pytest -n auto           # 自动检测 CPU 核心数
pytest -n 4              # 指定 4 个进程

# 跳过失败重试
pytest --reruns 0

# 运行单个测试文件
pytest tests/test_login.py

# 运行单个测试类或方法
pytest tests/test_login.py::TestLogin::test_login_with_standard_user
```

### 4. 查看 Allure 报告

```bash
# 生成并打开报告（需要安装 Allure 命令行工具）
allure serve reports/allure-results

# 或生成静态报告
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## 配置说明

### 环境变量

支持通过 `.env` 文件或系统环境变量进行配置：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `BASE_URL` | 测试目标网站 URL | https://www.saucedemo.com |
| `TIMEOUT` | 默认超时时间（毫秒） | 30000 |
| `HEADLESS` | 是否无头模式 | true |
| `SLOW_MO` | 慢动作延迟（毫秒） | 0 |
| `VIEWPORT_WIDTH` | 浏览器视口宽度 | 1920 |
| `VIEWPORT_HEIGHT` | 浏览器视口高度 | 1080 |
| `SCREENSHOT_ON_FAILURE` | 失败时自动截图 | true |
| `LOG_LEVEL` | 控制台日志级别 | INFO |
| `FILE_LOG_LEVEL` | 文件日志级别 | DEBUG |

### 测试用户

项目预配置了 saucedemo.com 的测试用户：

| 用户类型 | 环境变量 | 说明 |
|----------|----------|------|
| 标准用户 | `STANDARD_USER` | 可正常登录和操作 |
| 锁定用户 | `LOCKED_USER` | 被锁定，无法登录 |
| 问题用户 | `PROBLEM_USER` | 部分功能异常 |
| 性能用户 | `PERFORMANCE_USER` | 响应较慢 |
| 错误用户 | `ERROR_USER` | 会触发错误 |
| 视觉用户 | `VISUAL_USER` | 界面有差异 |

### pytest.ini 配置

| 配置项 | 说明 |
|--------|------|
| `testpaths` | 测试文件目录：`tests` |
| `--reruns=2` | 失败自动重试 2 次 |
| `--reruns-delay=1` | 重试间隔 1 秒 |
| `--timeout=120` | 单个测试超时 120 秒 |
| `--alluredir` | Allure 结果输出目录 |

### 测试标记

| 标记 | 说明 | 使用方式 |
|------|------|----------|
| `@pytest.mark.smoke` | 冒烟测试 | `pytest -m smoke` |
| `@pytest.mark.regression` | 回归测试 | `pytest -m regression` |
| `@pytest.mark.login` | 登录相关测试 | `pytest -m login` |
| `@pytest.mark.cart` | 购物车相关测试 | `pytest -m cart` |

## 编写测试用例

### Page Object 示例

```python
from pages.login_page import LoginPage

def test_login(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    assert login_page.is_logged_in()
```

### 使用 Fixture

```python
import pytest
from pages.login_page import LoginPage

class TestLogin:
    def test_login_success(self, login_page: LoginPage):
        """使用 login_page fixture"""
        login_page.open()
        login_page.login_as_standard_user()
        assert login_page.is_logged_in()
    
    def test_with_logged_in_page(self, logged_in_page):
        """使用已登录的页面 fixture"""
        assert "inventory" in logged_in_page.url
```

### 使用 Allure 装饰器

```python
import allure

@allure.feature("登录功能")
@allure.story("正常登录")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:
    
    @allure.title("使用标准用户登录成功")
    def test_valid_login(self, login_page):
        with allure.step("打开登录页面"):
            login_page.open()
        
        with allure.step("输入凭证并登录"):
            login_page.login_as_standard_user()
        
        with allure.step("验证登录成功"):
            assert login_page.is_logged_in()
```

### 数据驱动测试

```python
import pytest
from utils.data_loader import TestDataLoader

@pytest.mark.parametrize(
    "user_type",
    ["standard_user", "problem_user"],
    ids=["标准用户", "问题用户"]
)
def test_users_can_login(self, login_page, user_type: str):
    user_data = TestDataLoader.get_user(user_type)
    login_page.open()
    login_page.login(user_data["username"], user_data["password"])
    assert login_page.is_logged_in()
```

## 代码质量

项目使用 Ruff 进行代码质量检查和格式化：

```bash
# 代码检查
ruff check .

# 自动修复
ruff check --fix .

# 代码格式化
ruff format .

# 检查格式（不修改）
ruff format --check .
```

## CI/CD

项目内置 GitHub Actions 配置（`.github/workflows/test.yml`），支持：

- **自动触发**：Push/PR 自动触发测试
- **代码质量检查**：Ruff 代码检查和格式验证
- **多版本测试**：Python 3.10/3.11/3.12 矩阵测试
- **多浏览器测试**：Chromium/Firefox/WebKit 矩阵测试
- **PR 冒烟测试**：PR 时只运行冒烟测试，快速反馈
- **Allure 报告**：自动生成并发布到 GitHub Pages
- **失败截图**：测试失败时自动上传截图

### 手动触发测试

在 GitHub Actions 页面可以手动触发测试，支持选择：
- 浏览器类型：chromium / firefox / webkit / all
- Python 版本：3.10 / 3.11 / 3.12

## 可用的 Fixtures

| Fixture | Scope | 说明 |
|---------|-------|------|
| `page` | function | Playwright 页面实例 |
| `context` | function | 浏览器上下文 |
| `browser` | session | 浏览器实例 |
| `login_page` | function | 登录页面对象 |
| `inventory_page` | function | 商品列表页面对象 |
| `cart_page` | function | 购物车页面对象 |
| `logged_in_page` | function | 已登录的页面实例 |
| `logged_in_inventory_page` | function | 已登录的商品列表页面 |

## 常见问题

### 1. 运行测试报错 "unrecognized arguments: --reruns"

需要安装所有依赖：

```bash
pip install -r requirements.txt
```

### 2. 浏览器启动失败

确保已安装 Playwright 浏览器：

```bash
playwright install
```

### 3. 如何调试测试

```bash
# 有头模式 + 慢动作
pytest --headed --slowmo 1000 tests/test_login.py -v

# 使用 PWDEBUG 调试模式
PWDEBUG=1 pytest tests/test_login.py::TestLogin::test_login_with_standard_user
```

### 4. 如何只安装特定浏览器

```bash
# 只安装 Chromium
playwright install chromium

# 安装浏览器及系统依赖
playwright install --with-deps chromium
```

## 许可证

MIT License
