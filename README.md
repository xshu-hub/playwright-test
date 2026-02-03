# Playwright Web 自动化测试框架

基于 **Playwright + Pytest + Allure + Page Object** 模式的通用 Web 自动化测试框架。

本项目提供了一套完整的测试框架骨架，并以 **OrangeHRM** 人力资源管理系统作为示例，展示如何构建端到端的自动化测试。

## 特性

- **Page Object 模式**：清晰的页面对象封装，提高代码复用性和可维护性
- **多浏览器支持**：支持 Chromium、Firefox、WebKit 三大浏览器
- **Session 复用**：保存登录状态，跳过重复登录，显著加速测试执行
- **数据驱动测试**：支持 JSON 数据文件驱动的参数化测试
- **Allure 报告**：美观详细的测试报告，支持截图和步骤记录
- **失败自动重试**：测试失败自动重试机制，提高测试稳定性
- **并行执行**：支持多进程并行执行测试，加快执行速度
- **CI/CD 集成**：内置 Jenkins 配置，支持自动化测试流水线
- **日志记录**：完善的日志系统，支持控制台和文件双输出
- **环境配置**：支持通过环境变量灵活配置测试环境

## 框架结构

本框架分为 **核心组件**（可直接复用）和 **示例代码**（参考实现）两部分：

```
playwright-test/
├── config/                     # [框架核心] 配置模块
│   └── settings.py             # 项目配置类
├── pages/                      # Page Object 页面对象
│   ├── base_page.py            # [框架核心] 页面基类 - 可直接复用
│   ├── login_page.py           # [示例] OrangeHRM 登录页面
│   ├── dashboard_page.py       # [示例] OrangeHRM 仪表盘页面
│   ├── pim_page.py             # [示例] OrangeHRM PIM 员工管理页面
│   └── employee_form_page.py   # [示例] OrangeHRM 员工表单页面
├── tests/                      # 测试用例
│   ├── conftest.py             # [框架核心 + 示例] Pytest fixtures
│   ├── test_login.py           # [示例] 登录功能测试
│   ├── test_employee_form.py   # [示例] 员工表单测试
│   └── test_employee_e2e.py    # [示例] 员工管理端到端测试
├── utils/                      # [框架核心] 工具模块 - 可直接复用
│   ├── data_loader.py          # 测试数据加载器
│   ├── logger.py               # 日志工具
│   └── session_manager.py      # 多用户 Session 管理
├── data/                       # 测试数据
│   ├── test_data.json          # [示例] OrangeHRM 测试数据
│   └── sessions/               # Session 状态文件目录（自动生成）
├── docs/                       # 项目文档
│   ├── DEVELOPMENT.md          # 开发文档
│   └── CUSTOMIZATION.md        # 自定义指南
├── jenkins/                    # Jenkins CI/CD 配置
│   └── README.md               # Jenkins 配置指南
├── reports/                    # 测试报告输出目录
├── logs/                       # 日志文件目录（自动生成）
├── .env.example                # 环境变量示例
├── pytest.ini                  # Pytest 配置
├── Jenkinsfile                 # Jenkins 流水线配置
└── requirements.txt            # Python 依赖
```

### 框架核心组件（可直接复用）

| 组件 | 路径 | 说明 |
|------|------|------|
| 页面基类 | `pages/base_page.py` | 封装 Playwright 常用操作，所有页面对象继承此类 |
| 配置模块 | `config/settings.py` | 环境变量驱动的配置管理 |
| 日志工具 | `utils/logger.py` | 控制台 + 文件双输出日志 |
| 数据加载器 | `utils/data_loader.py` | JSON 测试数据加载 |
| Session 管理 | `utils/session_manager.py` | 多用户登录状态管理 |
| 基础 Fixtures | `tests/conftest.py` | 浏览器、页面、Session 复用等 |

### 示例代码（OrangeHRM）

示例代码展示了如何针对 [OrangeHRM Demo](https://opensource-demo.orangehrmlive.com) 构建测试：

| 组件 | 路径 | 说明 |
|------|------|------|
| 登录页面 | `pages/login_page.py` | OrangeHRM 登录页面对象 |
| 仪表盘页面 | `pages/dashboard_page.py` | OrangeHRM 仪表盘页面对象 |
| PIM 页面 | `pages/pim_page.py` | OrangeHRM 员工管理页面对象 |
| 登录测试 | `tests/test_login.py` | 登录功能测试用例 |
| 员工测试 | `tests/test_employee_*.py` | 员工管理测试用例 |
| 测试数据 | `data/test_data.json` | OrangeHRM 测试数据 |

## 文档

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目说明（本文件） |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | 详细开发文档 |
| [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md) | 自定义指南：如何为你的系统创建测试 |
| [jenkins/README.md](jenkins/README.md) | Jenkins 配置指南 |

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

### 2. 运行示例测试（OrangeHRM）

框架内置了针对 OrangeHRM Demo 的示例测试，可直接运行：

```bash
# 运行所有测试（无头模式）
pytest

# 有头模式运行（可视化）
pytest --headed

# 运行冒烟测试
pytest -m smoke

# 运行登录测试
pytest -m login
```

### 3. 配置你的测试环境

如果要测试自己的系统，复制并修改环境变量配置：

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，修改以下配置：
# - BASE_URL：你的测试系统 URL
# - ADMIN_USER / ADMIN_PASSWORD：测试账号
# - SESSION_VALIDATION_PATH：登录后的页面路径
# - LOGIN_URL_PATTERN：登录页面 URL 特征
```

详细的自定义指南请参考 [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md)。

## 运行测试

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
pytest -m regression     # 回归测试
pytest -m login          # 登录测试
pytest -m pim            # PIM 员工管理测试
pytest -m "smoke and login"  # 组合标记

# 并行运行测试（pytest-xdist）
pytest -n auto           # 按 CPU 核心数自动开进程（推荐）
pytest -n 4              # 指定 4 个 worker

# 跳过失败重试
pytest --reruns 0

# Session 复用（加速需要登录的测试）
pytest --save-session      # 首次运行：保存登录状态
pytest --reuse-session     # 后续运行：复用已保存的登录状态

# 运行单个测试文件
pytest tests/test_login.py

# 运行单个测试方法
pytest tests/test_login.py::TestLogin::test_login_with_admin
```

### 并行运行

项目已安装 **pytest-xdist**，可直接并行执行用例以缩短总耗时：

```bash
# 自动按 CPU 核心数开 worker（推荐）
pytest -n auto

# 指定 worker 数量
pytest -n 4
```

**注意：** 并行时每个 worker 是独立进程、各自起浏览器；与 `--reuse-session` / `--save-session` 同时用时，多进程可能同时读写同一 session 文件，建议并行时不启用 session 复用。

### 查看 Allure 报告

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

#### 框架通用配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `TIMEOUT` | 默认超时时间（毫秒） | 30000 |
| `HEADLESS` | 是否无头模式 | true |
| `SLOW_MO` | 慢动作延迟（毫秒） | 0 |
| `VIEWPORT_WIDTH` | 浏览器视口宽度 | 1920 |
| `VIEWPORT_HEIGHT` | 浏览器视口高度 | 1080 |
| `SCREENSHOT_ON_FAILURE` | 失败时自动截图 | true |
| `LOG_LEVEL` | 控制台日志级别 | INFO |
| `FILE_LOG_LEVEL` | 文件日志级别 | DEBUG |

#### 目标系统配置（需根据你的系统修改）

| 变量名 | 说明 | 示例默认值（OrangeHRM） |
|--------|------|--------|
| `BASE_URL` | 测试目标网站 URL | https://opensource-demo.orangehrmlive.com |
| `ADMIN_USER` | 管理员用户名 | Admin |
| `ADMIN_PASSWORD` | 管理员密码 | admin123 |
| `SESSION_VALIDATION_PATH` | Session 验证路径 | /dashboard |
| `LOGIN_URL_PATTERN` | 登录页面 URL 特征 | /login |
| `REUSE_SESSION` | 是否复用已保存的 Session | false |
| `SESSION_FILE` | Session 文件名 | auth_state.json |

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
| `@pytest.mark.pim` | PIM 员工管理测试 | `pytest -m pim` |
| `@pytest.mark.e2e` | 端到端测试 | `pytest -m e2e` |

## 为你的系统创建测试

详细指南请参考 [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md)，以下是快速概览：

### 1. 创建页面对象

```python
# pages/your_login_page.py
from pages.base_page import BasePage
from config.settings import settings

class YourLoginPage(BasePage):
    """你的系统登录页面"""
    
    page_name = "YourLoginPage"
    
    # 定义页面元素定位器
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    
    def __init__(self, page):
        super().__init__(page)
        self.url = f"{settings.BASE_URL}/login"
    
    def open(self):
        self.navigate(self.url)
        return self
    
    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self
```

### 2. 编写测试用例

```python
# tests/test_your_login.py
import pytest
from pages.your_login_page import YourLoginPage

class TestYourLogin:
    
    @pytest.mark.smoke
    def test_login_success(self, page):
        login_page = YourLoginPage(page)
        login_page.open()
        login_page.login("your_user", "your_password")
        
        assert "dashboard" in page.url
```

### 3. 配置环境变量

```bash
# .env
BASE_URL=https://your-system.example.com
ADMIN_USER=your_admin
ADMIN_PASSWORD=your_password
SESSION_VALIDATION_PATH=/dashboard
LOGIN_URL_PATTERN=/login
```

## 可用的 Fixtures

### 框架核心 Fixtures

| Fixture | Scope | 说明 |
|---------|-------|------|
| `playwright_instance` | session | Playwright 实例 |
| `browser` | session | 浏览器实例 |
| `context` | function | 浏览器上下文 |
| `page` | function | Playwright 页面实例 |
| `auth_state` | session | Session 状态文件路径 |
| `auth_context` | function | 已认证的浏览器上下文（支持 Session 复用） |
| `auth_page` | function | 已认证的页面实例（支持 Session 复用） |

### OrangeHRM 示例 Fixtures

| Fixture | Scope | 说明 |
|---------|-------|------|
| `login_page` | function | 登录页面对象 |
| `dashboard_page` | function | 仪表盘页面对象 |
| `pim_page` | function | PIM 页面对象 |
| `employee_form_page` | function | 员工表单页面对象 |
| `logged_in_page` | function | 已登录的页面实例 |
| `logged_in_dashboard` | function | 已登录的仪表盘页面 |
| `logged_in_pim` | function | 已登录的 PIM 页面 |

## CI/CD

项目内置 Jenkins 流水线配置（`Jenkinsfile`），支持：

- **参数化构建**：支持选择浏览器、冒烟测试
- **自动化测试**：Playwright 测试执行
- **Allure 报告**：自动生成 Allure 测试报告
- **JUnit 报告**：Jenkins 内置测试结果展示
- **构建产物归档**：自动归档测试报告和失败截图

### Jenkins 配置

详细的 Jenkins 配置说明请参考 [jenkins/README.md](jenkins/README.md)。

### 构建参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| BROWSER | 选择测试浏览器 | chromium |
| RUN_SMOKE_ONLY | 只运行冒烟测试 | false |

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
PWDEBUG=1 pytest tests/test_login.py::TestLogin::test_login_with_admin
```

### 4. 如何只安装特定浏览器

```bash
# 只安装 Chromium
playwright install chromium

# 安装浏览器及系统依赖
playwright install --with-deps chromium
```

### 5. 如何为新系统创建测试

请参考 [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md) 自定义指南。

## 许可证

MIT License
