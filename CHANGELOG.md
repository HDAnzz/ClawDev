# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-04-02

### Fixed
- 修复 deploy_agent_configs.sh 中技能目录路径错误 - 现在正确从 source_dir/skills/ 读取 skills.json
- 恢复 main.py 中缺失的 load_dotenv 导入和调用
- 修复技能复制功能，正确将 ~/.openclaw/workspace/skills/ 中的技能复制到各智能体工作目录

### Added
- 添加 --verbose 命令行参数用于启用调试日志
- 添加文件日志功能，日志保存到 ./logs/YYYY-MM-DD.log
- 使用命名日志器避免影响第三方库
- 添加 logs 目录到 .gitignore

### Changed
- 更新所有源代码文件的版权年份从 2024 到 2026
