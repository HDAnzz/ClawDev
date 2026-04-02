# ClawDev

<p align="center">
  基于 OpenClaw ACP 的多智能体软件开发框架
</p>

[English](./README.md) | 中文

## 简介

ClawDev 是一个多智能体协作开发框架，结合 OpenClaw ACP（Agent Client Protocol）与结构化开发流程。多个 AI 角色（CEO、CPO、CTO、Programmer、Code Reviewer、Software Test Engineer 等）通过专业化阶段（需求分析、编码、测试、文档）协作完成软件开发任务。

## 致谢

ClawDev 受到 [ChatDev](https://github.com/OpenBMB/ChatDev) 的启发，ChatDev 是由 [OpenBMB](https://www.openbmb.cn/) 团队开发的虚拟软件公司智能体系统：

> **ChatDev: Communicative Agents for Software Development**
>
> 论文: https://arxiv.org/abs/2307.07924

## 目录结构

```
ClawDev/
├── src/
│   ├── main.py                    # 主入口
│   ├── openclaw_acp/              # OpenClaw ACP 客户端
│   │   ├── agent.py               # Agent 连接器
│   │   └── utils.py              # 工具函数
│   └── clawdev/                   # 核心框架
│       ├── adapter/               # 智能体通信适配器
│       │   └── agent_adapter.py
│       ├── chain/                 # ChatChain 编排器
│       │   └── chain.py
│       ├── env/                   # 环境状态管理
│       │   └── env.py
│       ├── phases/                # 开发阶段
│       │   ├── base.py            # 阶段基类
│       │   ├── simple_phase.py    # 单对话阶段
│       │   └── composed_phase.py  # 复合阶段
│       └── utils.py
├── configs/
│   └── default/
│       ├── ChatChainConfig.json   # 流程配置
│       ├── PhaseConfig.json       # 阶段配置
│       └── {Role}/               # 各角色配置
│           ├── IDENTITY.md
│           ├── SOUL.md
│           ├── USER.md
│           ├── AGENTS.md
│           └── TOOLS.md
├── scripts/
│   └── deploy.sh                  # 部署脚本
├── Dockerfile.sandbox             # 沙箱镜像
└── tests/                        # 测试
```

## 快速开始

### 环境要求

- Python 3.10+
- Docker
- [uv](https://github.com/astral-sh/uv)
- OpenClaw (`openclaw` 配置 vendor)
- clawhub (`npm i -g clawhub`)

### 部署

```bash
# 1. 克隆
git clone https://github.com/HDAnzz/ClawDev.git
cd ClawDev

# 2. 部署（自动完成所有配置）
./scripts/deploy.sh

# 3. 运行
uv run src/main.py "开发一个计算器应用"
```

## 开发流程

```
需求分析 → 技术选型 → 编码设计 → 仓库初始化 → 代码实现 → 代码审查 → 测试运行 → 文档编写
```

| 阶段 | 角色 | 说明 |
|------|------|------|
| DemandAnalysis | CEO ↔ CPO | 分析需求，确定产品形态 |
| LanguageChoose | CEO ↔ CTO | 选择编程语言 |
| CodingDesign | CTO | 设计架构，写框架代码 |
| CodingInit | CTO ↔ Programmer | 创建仓库，添加协作者 |
| CodingImprove | CTO ↔ Programmer | 实现功能，改进代码 |
| CodingTest | CTO ↔ Programmer | 编写测试 |
| CodeReview | CTO ↔ Reviewer | 代码审查 |
| TestRun | Tester ↔ Programmer | 运行测试，修复 bug |
| CodingDoc | CTO ↔ Programmer | 编写文档 |

## License

Apache License 2.0
