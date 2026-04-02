# ClawDev

<p align="center">
  Multi-agent software development framework based on OpenClaw ACP
</p>

[中文](./README_CN.md) | English

## Overview

ClawDev is a multi-agent collaborative development framework that combines OpenClaw ACP (Agent Client Protocol) with structured development workflows. Multiple AI agents (CEO, CPO, CTO, Programmer, Code Reviewer, Software Test Engineer, etc.) collaborate through specialized phases (demand analysis, coding, testing, documentation) to complete software development tasks.

## Acknowledgment

ClawDev is inspired by [ChatDev](https://github.com/OpenBMB/ChatDev), a virtual software company operated by intelligent agents developed by the [OpenBMB](https://www.openbmb.cn/) team:

> **ChatDev: Communicative Agents for Software Development**
>
> Paper: https://arxiv.org/abs/2307.07924

## Project Structure

```
ClawDev/
├── src/
│   ├── main.py                    # Entry point
│   ├── openclaw_acp/              # OpenClaw ACP client
│   │   ├── agent.py               # Agent connector
│   │   └── utils.py
│   └── clawdev/                   # Core framework
│       ├── adapter/               # Agent communication adapter
│       │   └── agent_adapter.py
│       ├── chain/                 # ChatChain orchestrator
│       │   └── chain.py
│       ├── env/                   # Environment state management
│       │   └── env.py
│       ├── phases/                # Development phases
│       │   ├── base.py           # Phase base class
│       │   ├── simple_phase.py    # Single dialog phase
│       │   └── composed_phase.py # Multi-phase composition
│       └── utils.py
├── configs/
│   └── default/
│       ├── ChatChainConfig.json   # Workflow configuration
│       ├── PhaseConfig.json       # Phase configuration
│       └── {Role}/              # Role configurations
│           ├── IDENTITY.md
│           ├── SOUL.md
│           ├── USER.md
│           ├── AGENTS.md
│           └── TOOLS.md
├── scripts/
│   └── deploy.sh                  # Deployment script
├── Dockerfile.sandbox             # Sandbox image
└── tests/                        # Tests
```

## Quick Start

### Requirements

- Python 3.10+
- Docker
- [uv](https://github.com/astral-sh/uv)
- OpenClaw (`openclaw` to configure vendor)
- clawhub (`npm i -g clawhub`)

### Deployment

```bash
# 1. Clone
git clone https://github.com/HDAnzz/ClawDev.git
cd ClawDev

# 2. Deploy (auto-configures everything)
./scripts/deploy.sh

# 3. Run
uv run src/main.py "Develop a calculator application"
```

## Development Workflow

```
DemandAnalysis → LanguageChoose → CodingDesign → CodingInit → CodingImprove → CodeReview → TestRun → CodingDoc
```

| Phase | Roles | Description |
|-------|-------|-------------|
| DemandAnalysis | CEO ↔ CPO | Analyze requirements, determine product modality |
| LanguageChoose | CEO ↔ CTO | Select programming language |
| CodingDesign | CTO | Design architecture, write framework code |
| CodingInit | CTO ↔ Programmer | Create repository, add collaborators |
| CodingImprove | CTO ↔ Programmer | Implement features, improve code |
| CodingTest | CTO ↔ Programmer | Write tests |
| CodeReview | CTO ↔ Reviewer | Code review |
| TestRun | Tester ↔ Programmer | Run tests, fix bugs |
| CodingDoc | CTO ↔ Programmer | Write documentation |

## License

Apache License 2.0
