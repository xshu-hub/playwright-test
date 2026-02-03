# Windows 本地 Jenkins 配置指南

本文档详细说明如何在 Windows 本地搭建 Jenkins 并配置 Playwright 自动化测试流水线。

---

## 目录

1. [安装 Jenkins](#1-安装-jenkins)
2. [首次访问 Jenkins](#2-首次访问-jenkins)
3. [安装必要插件](#3-安装必要插件)
4. [安装 Python 环境](#4-安装-python-环境)
5. [安装 Git](#5-安装-git)
6. [配置 Allure 报告工具](#6-配置-allure-报告工具)
7. [创建流水线任务](#7-创建流水线任务)
8. [运行测试](#8-运行测试)
9. [查看测试报告](#9-查看测试报告)
10. [常见问题解答](#10-常见问题解答)

---

## 1. 安装 Jenkins

### 1.1 下载 Jenkins

1. 打开浏览器，访问 Jenkins 官网：https://www.jenkins.io/download/
2. 在页面中找到 **Windows** 选项
3. 点击下载 **LTS（长期支持版）** 的 `.msi` 安装包

### 1.2 安装 Jenkins

1. 双击下载的 `.msi` 文件启动安装程序
2. 点击 **Next** 继续
3. 选择安装目录（建议使用默认路径 `C:\Program Files\Jenkins`）
4. **服务登录凭据**页面：
   - 选择 **Run service as local or domain user**
   - 输入当前 Windows 用户名和密码
   - 这样 Jenkins 就能使用你安装的 Python 和 Git
5. 端口设置：默认 **8080**，如果被占用可以改成其他端口（如 8081）
6. 选择 Java 路径（安装程序会自动检测）
7. 点击 **Install** 开始安装
8. 安装完成后点击 **Finish**

### 1.3 验证 Jenkins 服务

1. 按 `Win + R`，输入 `services.msc`，回车
2. 在服务列表中找到 **Jenkins**
3. 确认状态为 **正在运行**
4. 如果没有运行，右键点击选择 **启动**

---

## 2. 首次访问 Jenkins

### 2.1 打开 Jenkins 页面

1. 打开浏览器，访问 http://localhost:8080
2. 如果你改了端口，访问 http://localhost:你的端口号

### 2.2 解锁 Jenkins

首次访问会看到 **Unlock Jenkins** 页面：

1. 页面会显示一个文件路径，类似：
   ```
   C:\Program Files\Jenkins\secrets\initialAdminPassword
   ```
2. 打开文件资源管理器，导航到这个路径
3. 用记事本打开 `initialAdminPassword` 文件
4. 复制里面的密码（一串字母数字）
5. 粘贴到网页的密码框中
6. 点击 **Continue**

### 2.3 安装推荐插件

1. 在 **Customize Jenkins** 页面，点击 **Install suggested plugins**
2. 等待插件安装完成（可能需要几分钟）

### 2.4 创建管理员账户

1. 填写用户名、密码、确认密码、全名、邮箱
2. 点击 **Save and Continue**
3. 确认 Jenkins URL（默认即可）
4. 点击 **Save and Finish**
5. 点击 **Start using Jenkins**

---

## 3. 安装必要插件

### 3.1 进入插件管理

1. 在 Jenkins 首页，点击左侧 **Manage Jenkins**（系统管理）
2. 点击 **Plugins**（插件管理）
3. 点击 **Available plugins**（可用插件）标签

### 3.2 搜索并安装插件

在搜索框中依次搜索以下插件，勾选后点击 **Install**：

| 插件名称 | 搜索关键词 | 用途 |
|---------|-----------|------|
| Allure Jenkins Plugin | `allure` | 生成 Allure 测试报告 |
| Timestamper | `timestamper` | 在日志中显示时间戳 |

> 注意：Pipeline、Git、JUnit 插件在初始化时已经安装，无需重复安装。

### 3.3 等待安装完成

1. 勾选 **Restart Jenkins when installation is complete**
2. 等待 Jenkins 自动重启
3. 重启后重新登录

---

## 4. 安装 Python 环境

### 4.1 下载 Python

1. 访问 Python 官网：https://www.python.org/downloads/
2. 点击 **Download Python 3.11.x**（或更高版本）

### 4.2 安装 Python

1. 双击下载的安装程序
2. **重要**：勾选底部的 **Add python.exe to PATH**
3. 点击 **Install Now**
4. 等待安装完成，点击 **Close**

### 4.3 验证安装

打开命令提示符（按 `Win + R`，输入 `cmd`，回车），执行：

```cmd
python --version
```

应该显示类似 `Python 3.11.x` 的版本号。

```cmd
pip --version
```

应该显示 pip 的版本信息。

### 4.4 重启 Jenkins 服务

安装 Python 后，需要重启 Jenkins 服务才能识别：

1. 按 `Win + R`，输入 `services.msc`，回车
2. 找到 **Jenkins** 服务
3. 右键点击，选择 **重新启动**

---

## 5. 安装 Git

### 5.1 下载 Git

1. 访问 Git 官网：https://git-scm.com/download/win
2. 页面会自动开始下载，如果没有，点击 **Click here to download manually**

### 5.2 安装 Git

1. 双击下载的安装程序
2. 一路点击 **Next** 使用默认配置即可
3. 最后点击 **Install**，完成后点击 **Finish**

### 5.3 验证安装

打开新的命令提示符窗口，执行：

```cmd
git --version
```

应该显示类似 `git version 2.x.x` 的版本号。

---

## 6. 配置 Allure 报告工具

### 6.1 进入工具配置

1. 在 Jenkins 首页，点击 **Manage Jenkins**
2. 点击 **Tools**（工具）

### 6.2 添加 Allure 配置

1. 向下滚动，找到 **Allure Commandline** 部分
2. 点击 **Add Allure Commandline**
3. 填写配置：
   - **Name**：输入 `allure`（这个名字会在流水线中使用）
   - **Install automatically**：勾选此选项
4. 点击 **Add Installer**，选择 **Install from Maven Central**
5. 在 **Version** 下拉框中选择最新版本（如 `2.32.0`）
6. 点击页面底部的 **Save** 保存

---

## 7. 创建流水线任务

### 7.1 新建任务

1. 在 Jenkins 首页，点击左侧 **New Item**（新建任务）
2. 在 **Enter an item name** 输入任务名称，例如：`playwright-tests`
3. 选择 **Pipeline**（流水线）
4. 点击 **OK**

### 7.2 配置流水线

#### 方式一：从代码仓库加载（推荐）

如果你的代码在 Git 仓库中：

1. 向下滚动到 **Pipeline** 部分
2. **Definition** 选择 **Pipeline script from SCM**
3. **SCM** 选择 **Git**
4. **Repository URL** 填写你的仓库地址，例如：
   - GitHub：`https://github.com/你的用户名/playwright-test.git`
   - GitLab：`https://gitlab.com/你的用户名/playwright-test.git`
   - 本地仓库：`file:///D:/project/playwright-test`（注意是三个斜杠）
5. **Credentials**：如果是私有仓库，点击 **Add** 添加凭据
6. **Branch Specifier**：填写 `*/main` 或 `*/master`（根据你的分支名）
7. **Script Path**：填写 `Jenkinsfile`
8. 点击 **Save**

#### 方式二：直接粘贴脚本

如果暂时不想配置 Git：

1. 向下滚动到 **Pipeline** 部分
2. **Definition** 保持 **Pipeline script**
3. 将项目根目录下 `Jenkinsfile` 的内容复制粘贴到脚本框中
4. 点击 **Save**

---

## 8. 运行测试

### 8.1 首次运行

1. 在任务页面，点击左侧 **Build with Parameters**
2. 选择参数：
   - **BROWSER**：选择要测试的浏览器（首次建议选 `chromium`）
   - **RUN_SMOKE_ONLY**：是否只运行冒烟测试
3. 点击 **Build** 开始构建

> 注意：首次运行会比较慢，因为需要下载 Playwright 浏览器（约 200MB）。

### 8.2 查看构建进度

1. 点击左下角 **Build History** 中的构建编号（如 `#1`）
2. 点击 **Console Output** 查看实时日志
3. 等待构建完成

### 8.3 构建状态说明

| 状态 | 颜色 | 含义 |
|-----|------|------|
| SUCCESS | 蓝色 | 所有测试通过 |
| UNSTABLE | 黄色 | 构建完成但有测试失败 |
| FAILURE | 红色 | 构建过程出错 |
| ABORTED | 灰色 | 构建被手动取消 |

---

## 9. 查看测试报告

### 9.1 Allure 报告

构建完成后：

1. 在构建页面，点击左侧 **Allure Report**
2. 可以看到：
   - **Overview**：测试概览，通过/失败数量
   - **Suites**：按测试套件分组查看
   - **Graphs**：测试趋势图表
   - **Timeline**：测试执行时间线

### 9.2 JUnit 报告

1. 在构建页面，点击 **Test Result**
2. 查看测试用例列表和失败详情

### 9.3 下载报告文件

1. 在构建页面，点击 **Artifacts**（构建产物）
2. 可以下载 `reports/` 目录下的所有报告文件

---

## 10. 常见问题解答

### Q1: 找不到 python 命令

**错误信息**：`'python' is not recognized as an internal or external command`

**解决方法**：

1. 确认 Python 已安装：打开命令提示符，输入 `python --version`
2. 如果未安装，参考第 4 节安装 Python
3. 如果已安装但 Jenkins 找不到：
   - 按 `Win + R`，输入 `sysdm.cpl`，回车
   - 点击 **高级** 标签 → **环境变量**
   - 在 **系统变量** 中找到 **Path**，双击编辑
   - 确认包含 Python 路径，例如：
     - `C:\Users\你的用户名\AppData\Local\Programs\Python\Python311\`
     - `C:\Users\你的用户名\AppData\Local\Programs\Python\Python311\Scripts\`
   - 点击确定保存
   - **重启 Jenkins 服务**

### Q2: Playwright 浏览器安装失败

**错误信息**：`browserType.launch: Executable doesn't exist`

**解决方法**：

手动安装浏览器：

```cmd
# 以管理员身份运行命令提示符
pip install playwright
playwright install chromium
playwright install firefox
playwright install webkit
```

### Q3: Allure Report 按钮没有出现

**可能原因**：Allure 插件未正确配置

**解决方法**：

1. 确认已安装 **Allure Jenkins Plugin**
2. 确认已在 **Manage Jenkins** → **Tools** 中配置 Allure
3. 确认 Jenkinsfile 中的 `allure()` 步骤没有被跳过
4. 查看 Console Output 中是否有 Allure 相关错误

### Q4: 控制台输出中文乱码

**解决方法**：

已在 Jenkinsfile 中添加 `PYTHONIOENCODING = 'utf-8'`，如果仍有乱码：

1. **Manage Jenkins** → **System**
2. 找到 **Global properties**
3. 勾选 **Environment variables**
4. 点击 **Add**
5. Name: `JAVA_TOOL_OPTIONS`，Value: `-Dfile.encoding=UTF-8`
6. 保存并重新构建

### Q5: Git 仓库拉取失败

**错误信息**：`Failed to connect to repository`

**解决方法**：

1. 检查仓库地址是否正确
2. 如果是私有仓库，需要添加凭据：
   - 在任务配置页面，点击 **Credentials** 旁边的 **Add**
   - 选择 **Jenkins**
   - **Kind** 选择 **Username with password**
   - 填写 Git 用户名和密码/Token
   - 点击 **Add**
   - 在 **Credentials** 下拉框中选择刚添加的凭据

### Q6: 构建超时

**错误信息**：`Aborted by timeout`

**解决方法**：

测试用例较多时可能超过默认的 30 分钟，修改 Jenkinsfile：

```groovy
options {
    timeout(time: 60, unit: 'MINUTES')  // 改为 60 分钟
}
```

### Q7: 磁盘空间不足

Jenkins 会保留构建历史和产物，占用磁盘空间。

**解决方法**：

1. 在任务配置中，找到 **Discard old builds**
2. 勾选并设置保留天数或保留构建数量
3. 或者手动清理：
   - 在构建历史中，点击要删除的构建
   - 点击 **Delete build**

---

## 附录：项目目录结构

```
playwright-test/
├── Jenkinsfile              # Jenkins 流水线配置文件
├── jenkins/
│   └── README.md            # 本文档
├── requirements.txt         # Python 依赖包列表
├── pytest.ini               # Pytest 配置文件
├── tests/                   # 测试用例目录
│   ├── conftest.py          # Pytest 配置和 fixtures
│   ├── test_login.py        # 登录测试
│   ├── test_employee_form.py
│   └── test_employee_e2e.py
├── pages/                   # Page Object 模式页面类
│   ├── base_page.py
│   ├── login_page.py
│   └── ...
├── config/                  # 配置文件
│   └── settings.py
├── utils/                   # 工具类
│   ├── data_loader.py
│   └── logger.py
├── data/                    # 测试数据
│   └── test_data.json
└── reports/                 # 测试报告（运行时生成）
    ├── allure-results/      # Allure 原始数据
    └── junit-*.xml          # JUnit 报告文件
```

---

## 附录：流水线参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| BROWSER | 选择 | chromium | 选择测试浏览器：chromium/firefox/webkit/all |
| RUN_SMOKE_ONLY | 布尔 | false | 只运行标记为 @pytest.mark.smoke 的测试用例 |

---

## 附录：定时构建配置

在任务配置中，找到 **Build Triggers**，勾选 **Build periodically**，输入 Cron 表达式：

```
# 每天早上 9 点运行
H 9 * * *

# 每 2 小时运行一次
H */2 * * *

# 工作日（周一到周五）早上 9 点运行
H 9 * * 1-5

# 每天凌晨 2 点运行
H 2 * * *
```

> 提示：使用 `H` 而不是具体数字，可以让 Jenkins 自动分散负载。

---

## 参考链接

- [Jenkins 官方文档](https://www.jenkins.io/doc/)
- [Jenkins Pipeline 语法](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Allure Jenkins Plugin](https://plugins.jenkins.io/allure-jenkins-plugin/)
- [Playwright Python 文档](https://playwright.dev/python/docs/intro)
- [Pytest 文档](https://docs.pytest.org/)
