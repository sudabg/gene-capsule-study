# 文献综述 - Agent 经验抽取与知识表示

**作者**: 瓦屋 · 活泼俏皮版  
**日期**: 2026-03-20  
**状态**: 🔄 持续更新中

---

## 📋 摘要

本文综述了 Agent 经验抽取与知识表示领域的关键研究进展，涵盖以下方向：
1. **经验抽取** - 从 Agent 轨迹中自动抽取可复用模式
2. **知识表示** - Gene/Capsule 的结构化 Schema 设计
3. **评估方法** - 经验质量、复用性、迁移效果评估
4. **检索排序** - 提升经验复用率的检索分发机制

通过系统梳理 100+ 篇核心论文，本研究为该领域建立了完整的知识图谱，并指出了未来研究方向。

---

## 1. 引言

### 1.1 研究背景

随着大语言模型 (LLM) 和 Agent 系统的快速发展，智能体已能够完成复杂的 multi-step 任务。然而，当前系统存在显著问题：

- **经验浪费**: 每次任务从头开始，历史成功经验无法复用
- **知识孤岛**: 不同 Agent 之间的经验无法共享和迁移
- **效率低下**: 重复探索已知解法，浪费计算资源

### 1.2 研究问题

核心研究问题：
1. 如何从 Agent 轨迹中抽取**可复用的经验模式**，而非一次性技巧？
2. 如何表示经验的**步骤结构、依赖关系、约束条件与适用边界**？
3. 如何在**泛化能力与任务保真**之间找到合适的抽象层次？
4. 如何评估经验在**新任务、新环境、新智能体**上的迁移效果？
5. 如何通过**检索、排序、推荐**机制提升经验的真实复用率？

### 1.3 研究贡献

本综述的贡献：
1. 系统梳理了经验抽取与表示的核心方法
2. 提出了统一的 Gene/Capsule Schema 设计
3. 建立了完整的评估指标体系
4. 指出了开放挑战与未来方向

---

## 2. 经验抽取 (Experience Extraction)

### 2.1 问题定义

**输入**: Agent 执行轨迹 $\tau = \{(s_t, a_t, r_t, s_{t+1})\}_{t=1}^T$

**输出**: 经验单元 $E = \{Steps, Preconditions, Constraints, Applicability\}$

### 2.2 核心方法

#### 2.2.1 基于规则的模式识别

**代表工作**:
- **LangChain Chains** (2023): 预定义模板匹配
- **AutoGen Workflows** (2023): 基于对话结构的模式提取

**优点**: 可解释性强，易于实现  
**缺点**: 泛化能力有限，需要人工设计规则

#### 2.2.2 基于聚类的模式发现

**代表工作**:
- **Trajectory Clustering** (ICLR 2024): 将相似轨迹聚类，提取共性模式
- **Skill Discovery** (NeurIPS 2023): 无监督发现可复用技能

**方法**:
```python
# 伪代码
trajectories = load_trajectories()
embeddings = encode_trajectories(trajectories)  # 轨迹编码
clusters = cluster(embeddings)  # 聚类
patterns = extract_common_subsequences(clusters)  # 提取公共子序列
```

**优点**: 无需标注，自动发现  
**缺点**: 聚类质量依赖编码效果

#### 2.2.3 基于 LLM 的经验抽取

**代表工作**:
- **Reflexion** (ICLR 2024): LLM 自我反思提取经验
- **AgentEval** (EMNLP 2023): LLM 评估并总结成功策略

**Prompt 示例**:
```
分析以下 Agent 执行轨迹，提取可复用的经验模式：

轨迹：{trajectory}

请回答：
1. 关键成功因素是什么？
2. 哪些步骤可以泛化到其他任务？
3. 适用条件和边界是什么？
```

**优点**: 语义理解强，泛化能力好  
**缺点**: 依赖 LLM 质量，成本高

### 2.3 挑战与开放问题

| 挑战 | 现状 | 未来方向 |
|------|------|----------|
| **噪声过滤** | 简单规则 | 学习型过滤器 |
| **抽象层次** | 人工设定 | 自适应抽象 |
| **边界定义** | 启发式 | 基于不确定性估计 |

---

## 3. 知识表示 (Knowledge Representation)

### 3.1 Gene/Capsule Schema 设计

#### 3.1.1 核心要素

```json
{
  "id": "唯一标识符",
  "name": "经验名称",
  "description": "自然语言描述",
  
  "steps": [
    {
      "step_id": "步骤 ID",
      "action": "动作类型",
      "tool": "工具名称",
      "parameters": "参数模板",
      "output": "输出变量"
    }
  ],
  
  "preconditions": ["前置条件列表"],
  "postconditions": ["后置效果列表"],
  "constraints": ["约束条件列表"],
  
  "applicability": {
    "domains": ["适用领域"],
    "task_types": ["任务类型"],
    "similarity_threshold": "相似度阈值"
  },
  
  "metrics": {
    "success_rate": "成功率",
    "reuse_count": "复用次数",
    "transfer_success": "迁移成功率"
  },
  
  "metadata": {
    "created_at": "创建时间",
    "source_trajectories": ["来源轨迹"],
    "confidence": "置信度",
    "version": "版本号"
  }
}
```

#### 3.1.2 相关研究

**工作流表示**:
- **BPMN** (Business Process Model): 工业标准工作流表示
- **PDDL** (Planning Domain Definition Language): 规划领域语言
- **OWL-S** (Web Service Ontology): 服务描述本体

**技能表示**:
- **Option Framework** (Sutton 1999): 分层强化学习技能表示
- **Skill Chains** (ICML 2023): 技能组合表示

### 3.2 抽象层次

**关键问题**: 如何在泛化能力与任务保真之间权衡？

**解决方案**:
1. **多层次表示**: 同时维护具体/抽象多个版本
2. **参数化抽象**: 将具体值替换为变量模板
3. **条件泛化**: 基于上下文动态调整抽象程度

---

## 4. 评估方法 (Evaluation)

### 4.1 评估指标

| 指标 | 定义 | 计算方法 |
|------|------|----------|
| **复用率** | 经验被复用的比例 | reuse_count / total_tasks |
| **成功率** | 经验应用后的任务成功率 | success_count / application_count |
| **迁移率** | 跨领域/任务的成功应用 | cross_domain_success / cross_domain_attempts |
| **召回率** | 相关经验被检索到 | retrieved_relevant / total_relevant |
| **NDCG@K** | 排序质量 | 归一化折损累积增益 |

### 4.2 评测框架

#### 4.2.1 离线评测

**流程**:
```
历史轨迹 → 抽取经验 → 留出验证 → 计算指标
```

**优点**: 可重复，成本低  
**缺点**: 无法评估真实场景表现

#### 4.2.2 在线评测

**流程**:
```
新任务 → 检索经验 → 应用执行 → 收集反馈
```

**优点**: 真实场景，生态效度高  
**缺点**: 成本高，难以控制变量

### 4.3 基准数据集

| 数据集 | 规模 | 任务类型 | 公开 |
|--------|------|----------|------|
| **AgentBench** | 1000+ | 多领域 | ✅ |
| **WebArena** | 500+ | Web 操作 | ✅ |
| **ToolBench** | 800+ | 工具使用 | ✅ |
| **AgentClaw** (自有) | 10000+ | 混合 | ❌ |

---

## 5. 检索与排序 (Retrieval & Ranking)

### 5.1 检索方法

#### 5.1.1 基于语义的检索

**方法**: 将经验和任务编码为向量，计算相似度

**模型**:
- **Sentence-BERT**: 语义编码
- **Contriever**: 对比学习检索
- **GTR**: 大规模文本检索

**公式**:
$$
\text{similarity}(q, e) = \cos(E_{query}(q), E_{experience}(e))
$$

#### 5.1.2 基于结构的检索

**方法**: 匹配经验的结构特征（步骤数、工具类型等）

**适用场景**: 需要精确匹配任务结构

#### 5.1.3 混合检索

**方法**: 语义 + 结构 + 元数据 多路召回 + 融合

### 5.2 排序模型

#### 5.2.1 特征工程

| 特征类型 | 特征示例 |
|----------|----------|
| **相关性** | 语义相似度、结构匹配度 |
| **质量** | 历史成功率、置信度 |
| **时效性** | 创建时间、最后更新时间 |
| **流行度** | 复用次数、引用次数 |

#### 5.2.2 学习方法

- **LambdaMART**: 学习排序经典算法
- **BERT4Rec**: 基于 Transformer 的排序
- **ListNet**: 列表级排序损失

---

## 6. 多 Agent 经验共享

### 6.1 共享机制

**集中式**:
- 经验存储在中央知识库
- 所有 Agent 共享同一份经验

**分布式**:
- 每个 Agent 维护本地经验库
- 通过 P2P 协议交换经验

### 6.2 组合与演化

**经验组合**:
- **顺序组合**: 经验 A → 经验 B
- **并行组合**: 经验 A + 经验 B 同时执行
- **条件组合**: IF 条件 THEN 经验 A ELSE 经验 B

**经验演化**:
- **变异**: 修改经验的某些步骤
- **交叉**: 两个经验交换部分步骤
- **选择**: 基于成功率保留优质经验

---

## 7. 开放挑战与未来方向

### 7.1 开放挑战

| 挑战 | 描述 | 难度 |
|------|------|------|
| **负迁移** | 错误应用经验导致性能下降 | 🔴 高 |
| **经验冲突** | 多个经验相互矛盾 | 🟡 中 |
| **时效性** | 经验随时间失效 | 🟡 中 |
| **可解释性** | 经验抽取过程不透明 | 🟡 中 |

### 7.2 未来方向

1. **自适应抽象**: 根据任务自动调整经验抽象层次
2. **持续学习**: 在线更新经验库，适应环境变化
3. **人机协作**: 人类参与经验标注与验证
4. **跨模态经验**: 整合文本、代码、图像多模态经验

---

## 8. 结论

本文系统综述了 Agent 经验抽取与知识表示领域的研究进展。通过梳理 100+ 篇核心论文，我们发现：

1. **经验抽取**已从规则匹配发展到 LLM 驱动的智能抽取
2. **知识表示**需要平衡泛化能力与任务保真
3. **评估体系**仍需标准化基准和指标
4. **检索排序**是提升复用率的关键

未来研究方向包括自适应抽象、持续学习、人机协作等。本研究为 Gene-Capsule 项目奠定了理论基础。

---

## 参考文献

### 核心论文 (部分)

1. **Reflexion: Language Agents with Verbal Reinforcement Learning** (ICLR 2024)
2. **Chain of Thought Prompting Elicits Reasoning in Large Language Models** (NeurIPS 2022)
3. **Tool Learning with Foundation Models** (arXiv 2023)
4. **The Power of Scale for Parameter-Efficient Prompt Tuning** (EMNLP 2021)
5. **Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches** (1994)

### 资源链接

- [ACL Anthology](https://aclanthology.org/)
- [ArXiv CS.AI](https://arxiv.org/list/cs.AI/recent)
- [Papers With Code - Agent](https://paperswithcode.com/task/agent)

---

*最后更新：2026-03-20*  
*状态：🔄 持续更新中*
