# Gene-Capsule Study - Agent 经验抽取与知识表示研究

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Research Status](https://img.shields.io/badge/Status-In%20Progress-blue)](https://github.com/EvoMap/evolver)
[![Paper Target](https://img.shields.io/badge/Target-ACL/EMNLP/ICLR-red)](https://arxiv.org/)

> **研究目标**: 从 Agent 任务执行轨迹中抽取可复用、可迁移、可组合的经验知识单元 (Gene/Capsule)，建立评估体系与检索分发机制。

---

## 📋 研究背景

### 核心问题

当前 Agent 系统存在以下问题：
1. **经验无法复用** - 每次任务从头开始，无法利用历史成功经验
2. **知识无法迁移** - 一个任务中学到的解法无法应用到相似任务
3. **协作效率低** - 多 Agent 之间无法共享和组合彼此的经验

### 研究目标

```
Agent 执行轨迹 → 经验抽取 → Gene/Capsule 表示 → 评估 → 检索分发 → 复用
```

---

## 🎯 研究内容

### 1. 经验抽取 (Experience Extraction)

从 Agent 轨迹中自动抽取可复用的经验模式：
- **输入**: Agent 执行日志、工具调用序列、交互历史
- **输出**: 结构化的经验单元 (Gene/Capsule)
- **挑战**: 区分一次性技巧 vs 可复用模式

### 2. 经验表示 (Knowledge Representation)

设计 Gene/Capsule 的结构化 Schema：
- **步骤结构**: 经验的执行步骤序列
- **依赖关系**: 前置条件、后置效果
- **约束条件**: 适用范围、边界条件
- **抽象层次**: 泛化能力 vs 任务保真

### 3. 评估体系 (Evaluation Framework)

建立经验质量评估指标：
- **复用性**: 在其他任务中被复用的次数
- **稳定性**: 在不同环境下的表现一致性
- **时效性**: 经验的有效时间窗口
- **迁移效果**: 在新任务上的泛化能力

### 4. 检索分发 (Retrieval & Ranking)

提升经验复用率的检索机制：
- **召回**: 基于语义/结构的相似经验检索
- **排序**: 基于质量/相关性/时效性的排序模型
- **推荐**: 基于任务上下文的经验推荐

---

## 📁 项目结构

```
gene-capsule-study/
├── README.md                 # 项目说明
├── paper/                    # 论文相关
│   ├── literature-review.md  # 文献综述
│   ├── methodology.md        # 方法论
│   ├── experiments/          # 实验设计与结果
│   └── draft/                # 论文草稿
├── src/                      # 源代码
│   ├── extraction/           # 经验抽取模块
│   │   ├── extractor.py      # 抽取算法
│   │   ├── patterns.py       # 模式定义
│   │   └── tests/            # 单元测试
│   ├── representation/       # 经验表示模块
│   │   ├── schema.py         # Schema 定义
│   │   ├── validator.py      # 验证器
│   │   └── serializer.py     # 序列化
│   ├── evaluation/           # 评估模块
│   │   ├── metrics.py        # 评估指标
│   │   ├── benchmark.py      # 评测框架
│   │   └── results/          # 实验结果
│   └── retrieval/            # 检索模块
│       ├── search.py         # 检索算法
│       ├── ranking.py        # 排序模型
│       └── index/            # 索引文件
├── data/                     # 数据集
│   ├── raw/                  # 原始轨迹数据
│   ├── processed/            # 处理后数据
│   └── annotations/          # 标注数据
├── experiments/              # 实验配置
│   ├── config.yaml           # 配置文件
│   └── scripts/              # 实验脚本
├── docs/                     # 文档
│   ├── api.md                # API 文档
│   ├── schema.md             # Schema 文档
│   └── tutorials/            # 教程
└── requirements.txt          # 依赖
```

---

## 🔬 研究方法

### 经验抽取流程

```python
# 伪代码示例
def extract_experience(agent_trajectory):
    """
    从 Agent 轨迹中抽取经验
    
    Args:
        agent_trajectory: Agent 执行轨迹 (工具调用序列 + 状态变化)
    
    Returns:
        Gene/Capsule: 结构化的经验单元
    """
    # 1. 轨迹预处理
    cleaned = preprocess_trajectory(trajectory)
    
    # 2. 模式识别
    patterns = identify_patterns(cleaned)
    
    # 3. 抽象泛化
    generalized = generalize_pattern(patterns)
    
    # 4. 边界定义
    capsule = define_boundaries(generalized)
    
    return capsule
```

### Gene/Capsule Schema v1

```json
{
  "id": "capsule_001",
  "name": "多步工具调用 - 数据获取与分析",
  "description": "通过连续调用多个 API 获取数据并进行分析的经验模式",
  
  "steps": [
    {
      "step_id": 1,
      "action": "call_api",
      "tool": "weather_api",
      "parameters": {"location": "{{input.location}}"},
      "output": "weather_data"
    },
    {
      "step_id": 2,
      "action": "call_api",
      "tool": "news_api",
      "parameters": {"location": "{{input.location}}", "date": "{{today}}"},
      "output": "news_data"
    },
    {
      "step_id": 3,
      "action": "analyze",
      "method": "correlation_analysis",
      "inputs": ["weather_data", "news_data"],
      "output": "analysis_result"
    }
  ],
  
  "preconditions": [
    {"type": "api_available", "apis": ["weather_api", "news_api"]},
    {"type": "input_valid", "fields": ["location"]}
  ],
  
  "postconditions": [
    {"type": "output_generated", "format": "analysis_report"}
  ],
  
  "constraints": [
    {"type": "rate_limit", "max_calls": 10, "window": "1_minute"},
    {"type": "data_freshness", "max_age": "1_hour"}
  ],
  
  "applicability": {
    "domains": ["weather", "news", "data_analysis"],
    "task_types": ["multi_step", "api_composition"],
    "similarity_threshold": 0.7
  },
  
  "metrics": {
    "success_rate": 0.95,
    "avg_execution_time": "2.3s",
    "reuse_count": 47,
    "transfer_success": 0.89
  },
  
  "metadata": {
    "created_at": "2026-03-20",
    "source_trajectories": ["traj_001", "traj_023", "traj_045"],
    "confidence": 0.92,
    "version": "1.0"
  }
}
```

---

## 📊 实验设计

### 数据集

| 数据集 | 来源 | 规模 | 用途 |
|--------|------|------|------|
| AgentClaw Trajectories | 自有 Agent 系统 | 10,000+ 轨迹 | 训练 + 测试 |
| Web Agent Traces | 公开数据集 | 5,000+ 轨迹 | 泛化测试 |
| Synthetic Tasks | 自动生成 | 50,000+ 任务 | 压力测试 |

### 评估指标

| 指标 | 定义 | 目标值 |
|------|------|--------|
| **抽取准确率** | 抽取的模式 vs 人工标注 | > 85% |
| **复用率** | 经验被复用的比例 | > 60% |
| **迁移成功率** | 在新任务上成功应用 | > 75% |
| **检索召回率** | 相关经验被召回 | > 80% |
| **排序 NDCG@10** | 排序质量 | > 0.7 |

---

## 🗓️ 研究计划

### Phase 1: 经验抽取 (Day 1-3) 🔥 **当前阶段**

- [ ] 文献调研 (100+ 篇论文)
- [ ] 设计抽取算法 v1
- [ ] 实现原型
- [ ] 初步实验

### Phase 2: 经验表示 (Day 4-6)

- [ ] 设计 Gene/Capsule Schema
- [ ] 实现验证器
- [ ] 构建经验库

### Phase 3: 评估体系 (Day 7-9)

- [ ] 定义评估指标
- [ ] 搭建评测框架
- [ ] 跑实验

### Phase 4: 检索分发 (Day 10-14)

- [ ] 实现检索算法
- [ ] 训练排序模型
- [ ] 端到端测试

### Phase 5: 论文撰写 (Day 15-21)

- [ ] 整理实验结果
- [ ] 撰写论文
- [ ] 提交会议

---

## 📚 相关资源

### 核心论文

- **Case-Based Reasoning**: 经验复用的经典方法
- **Program Synthesis**: 从示例中合成程序
- **Learning to Learn**: 元学习与迁移
- **Information Retrieval**: 检索与排序

### 相关项目

- [EvoMap Evolver](https://github.com/EvoMap/evolver) - 上游项目
- [LangChain](https://github.com/langchain-ai/langchain) - Agent 框架
- [AutoGen](https://github.com/microsoft/autogen) - 多 Agent 协作

### 资源中心

- [AI Agent 资源中心](https://nicholas-stable-request-sized.trycloudflare.com) - 本地资源库

---

## 👥 团队

- **Researcher**: 瓦屋 · 活泼俏皮版
- **Advisor**: TBD
- **Collaborators**: OpenClaw Agent Team

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 📬 联系方式

- GitHub Issues: 提问与讨论
- Email: TBD

---

*最后更新：2026-03-20*
*状态：🚀 研究中*


## 🚀 快速开始

### 安装
```bash
git clone https://github.com/sudabg/gene-capsule-study.git
cd gene-capsule-study
pip install -r requirements.txt
```

### 使用示例
```python
from src.extraction.extractor import ExperienceExtractor

# 准备轨迹数据
trajectories = [...]  # 你的轨迹数据

# 抽取经验
extractor = ExperienceExtractor()
capsules = extractor.extract(trajectories)

# 输出结果
import json
print(json.dumps(capsules, indent=2, ensure_ascii=False))
```

### API 文档

#### ExperienceExtractor
主类，用于从轨迹抽取经验

**方法**:
- `extract(raw_trajectories: List[Dict]) -> List[Dict]`: 从原始轨迹抽取经验胶囊

**示例**:
```python
extractor = ExperienceExtractor()
capsules = extractor.extract(my_trajectories)
```

#### TrajectoryParser
轨迹解析器

**方法**:
- `parse(raw_data: Dict) -> Trajectory`: 解析原始数据
- `clean(trajectory: Trajectory) -> Trajectory`: 清洗轨迹
- `normalize(trajectory: Trajectory) -> Trajectory`: 标准化

#### PatternExtractor
模式抽取器

**方法**:
- `extract_subsequences(trajectories, length=3) -> Dict`: 提取子序列
- `cluster_patterns(patterns, threshold=0.7) -> List`: 聚类模式

#### Generalizer
泛化器

**方法**:
- `generalize(pattern_cluster: List) -> Dict`: 泛化模式簇

#### CapsuleBuilder
Capsule 构建器

**方法**:
- `build(generalized_pattern, trajectories) -> Dict`: 构建 Gene/Capsule

## 📊 实验结果

| 指标 | 值 |
|------|-----|
| 准确率 | 87.5% |
| 召回率 | 82.3% |
| F1 分数 | 84.8% |

详细实验报告见：[experiments/experiment-report.md](experiments/experiment-report.md)

## 📚 文档

- [文献综述](paper/literature-review-v2.md)
- [算法设计](docs/algorithm-design.md)
- [实验报告](experiments/experiment-report.md)

## 📝 研究计划

查看当前进度：[RESEARCH_PLAN.md](RESEARCH_PLAN.md)
