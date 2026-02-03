pipeline {
    agent any

    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chromium', 'firefox', 'webkit', 'all'],
            description: '选择要运行测试的浏览器'
        )
        booleanParam(
            name: 'RUN_SMOKE_ONLY',
            defaultValue: false,
            description: '勾选后只运行冒烟测试（带 @pytest.mark.smoke 标记的用例）'
        )
    }

    environment {
        // 测试目标网站地址
        BASE_URL = 'https://opensource-demo.orangehrmlive.com'
        // 无头模式运行（不显示浏览器界面）
        HEADLESS = 'true'
        // 超时时间（毫秒）
        TIMEOUT = '30000'
        // Allure 报告数据目录
        ALLURE_RESULTS = 'reports/allure-results'
        // 解决 Windows 中文乱码问题
        PYTHONIOENCODING = 'utf-8'
    }

    options {
        // 构建超时时间：30分钟
        timeout(time: 30, unit: 'MINUTES')
        // 保留最近 20 次构建记录
        buildDiscarder(logRotator(numToKeepStr: '20'))
        // 禁止同一任务并发执行
        disableConcurrentBuilds()
        // 在日志中显示时间戳
        timestamps()
    }

    stages {
        stage('检出代码') {
            steps {
                echo '=== 从代码仓库检出代码 ==='
                checkout scm
            }
        }

        stage('环境准备') {
            steps {
                echo '=== 环境信息 ==='
                echo "浏览器: ${params.BROWSER}"
                echo "工作目录: ${env.WORKSPACE}"
                
                // 显示 Python 版本，便于排查问题
                bat 'python --version'
                bat 'pip --version'
                
                // 清理旧的报告目录
                bat '''
                    @echo off
                    if exist reports\\allure-results rmdir /s /q reports\\allure-results
                    if exist reports\\allure-report rmdir /s /q reports\\allure-report
                    if exist test-results rmdir /s /q test-results
                    if not exist reports mkdir reports
                    echo 报告目录已清理
                '''
            }
        }

        stage('安装依赖') {
            steps {
                echo '=== 安装项目依赖 ==='
                bat 'python -m pip install --upgrade pip -q'
                bat 'pip install -r requirements.txt'
                echo '依赖安装完成'
            }
        }

        stage('安装浏览器') {
            steps {
                echo '=== 安装 Playwright 浏览器 ==='
                script {
                    def browsers = params.BROWSER == 'all' ? 'chromium firefox webkit' : params.BROWSER
                    echo "将要安装的浏览器: ${browsers}"
                    bat "playwright install ${browsers}"
                }
                echo '浏览器安装完成'
            }
        }

        stage('运行测试') {
            steps {
                echo '=== 运行 Playwright 测试 ==='
                script {
                    def browsers = params.BROWSER == 'all' ? ['chromium', 'firefox', 'webkit'] : [params.BROWSER]
                    def testMarker = params.RUN_SMOKE_ONLY ? '-m smoke' : ''
                    
                    for (browser in browsers) {
                        echo ">>> 正在运行 ${browser} 浏览器测试 <<<"
                        
                        // returnStatus: true 表示即使测试失败也不中断流水线
                        def testResult = bat(
                            script: "pytest ${testMarker} --browser-type=${browser} --alluredir=${ALLURE_RESULTS} -v --tb=short --junitxml=reports/junit-${browser}.xml",
                            returnStatus: true
                        )
                        
                        if (testResult != 0) {
                            // 标记构建为不稳定状态（黄色），而不是失败（红色）
                            unstable("${browser} 浏览器测试存在失败用例")
                        } else {
                            echo "${browser} 浏览器测试全部通过"
                        }
                    }
                }
            }
        }

        stage('生成报告') {
            steps {
                echo '=== 生成测试报告 ==='
                
                // 发布 JUnit 测试报告（Jenkins 内置支持）
                junit(
                    testResults: 'reports/junit-*.xml',
                    allowEmptyResults: true
                )
                
                // 生成 Allure 报告（需要安装 Allure Jenkins Plugin）
                allure(
                    results: [[path: "${ALLURE_RESULTS}"]],
                    reportBuildPolicy: 'ALWAYS'
                )
                
                echo '报告生成完成，可在构建页面查看'
            }
        }
    }

    post {
        always {
            echo '=== 归档构建产物 ==='
            
            // 归档报告文件，可在构建页面下载
            archiveArtifacts(
                artifacts: 'reports/**/*',
                allowEmptyArchive: true
            )
            
            // 归档测试失败时的截图
            archiveArtifacts(
                artifacts: 'test-results/**/*',
                allowEmptyArchive: true
            )
        }
        
        success {
            echo '=========================================='
            echo '  构建成功！所有测试通过。'
            echo '=========================================='
        }
        
        failure {
            echo '=========================================='
            echo '  构建失败！请检查错误日志。'
            echo '=========================================='
        }
        
        unstable {
            echo '=========================================='
            echo '  构建完成，但存在失败的测试用例。'
            echo '  请查看 Allure 报告了解详情。'
            echo '=========================================='
        }
    }
}
