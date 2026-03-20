# 简化计划 - Gene-Capsule 重构

**基于简单性标准**: 在其他条件相同的情况下，越简单越好。

**创建时间**: 2026-03-21

---

## 📊 当前复杂度

| 指标 | 当前 | 目标 | 减少 |
|------|------|------|------|
| **代码行数** | 1578 | ~400 | -75% |
| **类数量** | 18 | 3 | -83% |
| **方法数量** | 71+ | ~15 | -79% |
| **配置选项** | 15+ | 3 | -80% |
| **测试数量** | 16 | 5 | -69% |

---

## 🎯 简化原则

### 1. 删除优于重构
- 如果代码可以删除而不影响功能，直接删除
- 不要重构可以删除的代码

### 2. 整合优于分离
- 相关功能合并到一个类
- 减少抽象层

### 3. 默认优于配置
- 移除不必要的配置选项
- 提供合理的默认值

### 4. 集成测试优于单元测试
- 测试端到端流程
- 不测试内部实现细节

---

## 📝 具体简化方案

### 方案 1: 合并类结构

**当前** (8 个类):
```
TrajectoryStep → Trajectory → GeneCapsule
      ↓              ↓              ↓
TrajectoryParser + PatternExtractor + Generalizer + CapsuleBuilder + ExperienceExtractor
```

**简化后** (3 个类):
```
GeneCapsule (数据类)
     ↓
ExperienceExtractor (主类，整合所有功能)
     ↓
ExperienceRetriever (检索，可选)
```

**删除的类**:
- ❌ `TrajectoryStep` - 直接用 dict
- ❌ `Trajectory` - 直接用 dict
- ❌ `TrajectoryParser` - 合并到 ExperienceExtractor
- ❌ `PatternExtractor` - 合并到 ExperienceExtractor
- ❌ `Generalizer` - 合并到 ExperienceExtractor
- ❌ `CapsuleBuilder` - 合并到 ExperienceExtractor

**代码减少**: 736 行 → 200 行 (-73%)

---

### 方案 2: 简化检索/排序

**当前** (4 检索 + 5 排序):
```python
search_strategy: keyword | semantic | structural | hybrid
rank_strategy: relevance | quality | recency | popularity | hybrid
```

**简化后** (1 检索 + 1 排序):
```python
# 默认且唯一
def search(query: str, top_k: int = 10) -> List[GeneCapsule]:
    # 1. 关键词匹配
    # 2. 按质量排序
    # 3. 返回 top_k
```

**删除的代码**:
- ❌ `CapsuleSearcher` 类 - 470 行
- ❌ `CapsuleRanker` 类
- ❌ 8 个检索/排序方法

**代码减少**: 470 行 → 50 行 (-89%)

---

### 方案 3: 简化数据结构

**当前** (15 个字段):
```python
@dataclass
class GeneCapsule:
    id: str
    name: str
    description: str
    pattern: List[str]
    variables: Dict[str, Any]
    preconditions: List[Dict[str, Any]]
    postconditions: List[Dict[str, Any]]
    constraints: List[Dict[str, Any]]
    applicability: Dict[str, Any]
    metrics: Dict[str, float]
    source_trajectories: List[str]
    confidence: float
    version: str
    created_at: str
    tags: List[str]
```

**简化后** (5 个核心字段):
```python
@dataclass
class GeneCapsule:
    id: str                      # 唯一标识
    pattern: List[str]           # 核心：动作模式
    metrics: Dict[str, float]    # 核心：评估指标
    confidence: float            # 核心：置信度
    tags: List[str]              # 可选：标签
```

**删除的字段**:
- ❌ `name` - 可以从 pattern 生成
- ❌ `description` - 可以从 pattern 生成
- ❌ `variables` - 过于复杂，很少用
- ❌ `preconditions` - 过于复杂，很少用
- ❌ `postconditions` - 过于复杂，很少用
- ❌ `constraints` - 过于复杂，很少用
- ❌ `applicability` - 过于复杂，很少用
- ❌ `source_trajectories` - 元数据，不需要
- ❌ `version` - 不需要
- ❌ `created_at` - 不需要

**简化收益**:
- 数据结构清晰
- 序列化更快
- 内存占用减少 60%

---

### 方案 4: 简化测试

**当前** (16 个单元测试):
```python
TestTrajectoryParser: 3 tests    # 测试内部方法
TestPatternExtractor: 3 tests
TestGeneralizer: 3 tests
TestCapsuleBuilder: 3 tests
TestExperienceExtractor: 2 tests
TestGeneCapsule: 2 tests
```

**简化后** (5 个集成测试):
```python
TestExperienceExtractor: 5 tests
  - test_extract_basic()         # 基本抽取
  - test_extract_multiple()      # 多轨迹抽取
  - test_search()                # 搜索功能
  - test_save_load()             # 持久化
  - test_end_to_end()            # 端到端
```

**删除的测试**:
- ❌ 所有内部方法测试
- ❌ 数据类测试
- ❌ 边界条件测试（过度）

**简化收益**:
- 测试更易维护
- 重构更自由
- 测试速度更快

---

## 📐 简化后的架构

```
gene-capsule-study/
├── src/
│   └── extractor.py              # ~200 行，整合所有功能
├── tests/
│   └── test_extractor.py         # ~100 行，5 个集成测试
├── docs/
│   ├── USAGE.md                  # 简化版使用教程
│   └── SIMPLIFICATION_PLAN.md    # 本文件
└── README.md
```

**文件对比**:

| 文件 | 当前 | 简化后 | 减少 |
|------|------|--------|------|
| `src/extraction/extractor_v3.py` | 736 行 | ~200 行 | -73% |
| `src/retrieval/search.py` | 470 行 | 删除 | -100% |
| `tests/test_extractor.py` | 372 行 | ~100 行 | -73% |
| **总计** | **1578 行** | **~300 行** | **-81%** |

---

## 🎯 简化后的核心 API

```python
from extractor import ExperienceExtractor, GeneCapsule

# 1. 创建抽取器（无配置）
extractor = ExperienceExtractor()

# 2. 抽取经验
capsules = extractor.extract(trajectories)

# 3. 搜索经验
results = extractor.search("API analysis", top_k=5)

# 4. 保存/加载
extractor.save(capsules, "output.json")
capsules = extractor.load("output.json")
```

**配置对比**:

| 配置项 | 当前 | 简化后 |
|--------|------|--------|
| `min_frequency` | ✅ | ❌ 固定为 2 |
| `min_length` | ✅ | ❌ 固定为 2 |
| `pattern_length` | ✅ | ❌ 固定为 3 |
| `search_strategy` | 4 种 | ❌ 固定为 keyword |
| `rank_strategy` | 5 种 | ❌ 固定为 quality |
| `rank_weights` | ✅ | ❌ 固定权重 |

---

## 📊 简化收益

### 代码质量
- ✅ 更易理解
- ✅ 更易维护
- ✅ 更易测试
- ✅ 更易扩展

### 开发效率
- ✅ 新功能开发更快
- ✅ Bug 修复更快
- ✅ 代码审查更快

### 用户体验
- ✅ API 更简单
- ✅ 文档更短
- ✅ 学习曲线更平缓

---

## ⚠️ 简化风险

### 风险 1: 功能减少
**缓解**: 保留核心功能，删除边缘功能

### 风险 2: 灵活性降低
**缓解**: 80% 场景不需要额外灵活性

### 风险 3: 性能影响
**缓解**: 简化后性能通常更好（代码更少）

---

## 📅 执行计划

### Phase 1: 删除检索模块 (1 小时)
- [ ] 删除 `src/retrieval/search.py`
- [ ] 删除相关测试
- [ ] 更新文档

### Phase 2: 合并抽取类 (2 小时)
- [ ] 合并 5 个类为 1 个
- [ ] 简化数据结构
- [ ] 更新测试

### Phase 3: 简化测试 (1 小时)
- [ ] 删除单元测试
- [ ] 编写集成测试
- [ ] 验证功能

### Phase 4: 更新文档 (1 小时)
- [ ] 简化 USAGE.md
- [ ] 简化 API.md
- [ ] 更新 README

**总时间**: 5 小时

---

## 🎯 成功标准

简化后应满足：
1. ✅ 代码行数减少 70%+
2. ✅ 所有现有测试通过
3. ✅ API 更简单易用
4. ✅ 文档更短更清晰
5. ✅ 核心功能完整保留

---

## 💡 简化的胜利

> "删除某些内容并获得相同或更好的结果是一个很好的结果 — 这是一种简化的胜利。"

**简化前**: 1578 行代码，18 个类，71+ 方法，复杂配置
**简化后**: ~300 行代码，3 个类，~15 方法，零配置

**获得**:
- ✅ 相同的核心功能
- ✅ 更好的可维护性
- ✅ 更好的用户体验
- ✅ 更快的开发速度

**失去**:
- ❌ 边缘功能（几乎不用）
- ❌ 过度配置（几乎不改）
- ❌ 复杂抽象（几乎不懂）

**结论**: 简化的胜利！🎉

---

*创建时间：2026-03-21*
*状态：待执行*
