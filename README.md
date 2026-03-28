# Gene-Capsule Study

![GitHub Stars](https://img.shields.io/github/stars/sudabg/gene-capsule-study?style=social)
![License](https://img.shields.io/github/license/sudabg/gene-capsule-study)
![Python](https://img.shields.io/badge/python-3.10+-blue)

**Agent Experience Extraction & Knowledge Representation Research**

一个研究 AI Agent 经验如何被结构化抽取、表示和复用的开源项目。核心概念：**Gene**（可复用策略模板）+ **Capsule**（经验证的具体解决方案）。

---

## 🚀 快速开始

```bash
pip install -r requirements.txt
```

```python
from src.extractor import ExperienceExtractor

extractor = ExperienceExtractor()  # 零配置，开箱即用
capsules = extractor.extract(trajectories)
results = extractor.search("api timeout", capsules=capsules)
extractor.save(capsules, "output.json")
```

---

## 📊 核心功能

| 功能 | 说明 |
|------|------|
| **extract()** | 从 Agent 轨迹中抽取经验 Capsule |
| **search()** | 关键词搜索 + 质量排序 |
| **save()/load()** | 持久化经验库 (JSON) |

---

## 📁 项目结构

```
gene-capsule-study/
├── src/
│   ├── extractor.py              # 核心抽取器 (v4.0, ~180行)
│   └── extraction/
│       ├── extractor_v2.py       # v2 迭代
│       ├── extractor_v3.py       # v3 迭代
│       └── schema.py             # Gene/Capsule 数据结构定义
├── paper/
│   ├── literature-review.md      # 文献综述 v1
│   ├── literature-review-v2.md   # 文献综述 v2
│   ├── literature-review-deep.md # 深度文献综述
│   └── literature-survey-deep.md # 深度调研报告
├── experiments/
│   └── experiment-report.md      # 实验报告
├── docs/                         # 文档目录
├── tests/                        # 测试 (5 个集成测试, 100% 通过)
├── README.md
└── requirements.txt
```

---

## 🧪 测试

```bash
python3 -m unittest tests.test_extractor -v
```

---

## 📐 设计哲学

> "在其他条件相同的情况下，越简单越好。"

**v4.0 简化成果**:
- 代码: 1578 行 → ~180 行 (**-89%**)
- 类: 18 个 → 2 个 (**-89%**)
- 配置: 15+ 项 → 0 项 (**-100%**)

---

## 🔬 研究方向

1. **经验抽取**: 从 Agent 执行轨迹中自动识别可复用模式
2. **知识表示**: Gene (策略模板) + Capsule (验证方案) 双层结构
3. **质量评估**: 基于置信度和成功次数的自动评分
4. **检索分发**: 跨 Agent 的经验共享与复用机制

相关项目: [EvoMap](https://evomap.ai) — AI Agent 协作进化市场

---

## 📚 文献综述

本项目包含多版本文献综述，覆盖：
- Agent 经验抽取相关工作
- 知识图谱在 Agent 记忆中的应用
- RAG 在长期运行 Agent 中的扩展
- 对比学习在知识去重中的进展

详见 `paper/` 目录。

---

## 📄 许可证

MIT License

---

*最后更新: 2026-03-28*
