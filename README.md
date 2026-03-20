# Gene-Capsule 经验抽取器

**版本**: v4.0 (简化版)  
**原则**: 越简单越好

---

## 🚀 快速开始

### 1. 安装

```bash
pip install -r requirements.txt
```

### 2. 使用

```python
from src.extractor import ExperienceExtractor

# 创建抽取器（零配置）
extractor = ExperienceExtractor()

# 抽取经验
capsules = extractor.extract(trajectories)

# 搜索经验
results = extractor.search("api analysis", capsules=capsules)

# 保存/加载
extractor.save(capsules, "output.json")
capsules = extractor.load("output.json")
```

---

## 📊 核心功能

| 功能 | 说明 |
|------|------|
| **extract()** | 从轨迹抽取经验 |
| **search()** | 关键词搜索 + 质量排序 |
| **save()** | 保存到 JSON 文件 |
| **load()** | 从 JSON 加载 |

---

## 📁 项目结构

```
gene-capsule-study/
├── src/
│   └── extractor.py          # ~180 行，核心实现
├── tests/
│   └── test_extractor.py     # 5 个集成测试
├── docs/
│   ├── SIMPLIFICATION_PLAN.md # 简化计划
│   └── ...
└── README.md
```

---

## 🧪 测试

```bash
python3 -m unittest tests.test_extractor -v
```

**测试覆盖**: 5 个集成测试，100% 通过

---

## 📐 设计原则

### 简单性标准
> 在其他条件相同的情况下，越简单越好。

**简化成果**:
- 代码：1578 行 → ~180 行 (**-89%**)
- 类：18 个 → 2 个 (**-89%**)
- 配置：15+ 项 → 0 项 (**-100%**)

### 核心 API

```python
# 零配置，开箱即用
extractor = ExperienceExtractor()
```

### 简化对比

| 版本 | 代码 | 类 | 配置 |
|------|------|-----|------|
| v3.0 | 1578 行 | 18 个 | 15+ 项 |
| v4.0 | ~180 行 | 2 个 | 0 项 |
| **减少** | **-89%** | **-89%** | **-100%** |

---

## 📚 文档

- [简化计划](docs/SIMPLIFICATION_PLAN.md) - 重构详情
- [使用教程](docs/USAGE.md) - 旧版（待更新）
- [API 文档](docs/API.md) - 旧版（待更新）

---

## 🎯 使用场景

### 场景 1: 从 Agent 轨迹抽取经验

```python
trajectories = [...]  # Agent 执行轨迹
capsules = extractor.extract(trajectories)
```

### 场景 2: 搜索可复用经验

```python
results = extractor.search("API 调用", capsules=capsules)
```

### 场景 3: 持久化经验库

```python
extractor.save(capsules, "experience.json")
```

---

## 📈 性能指标

| 指标 | 值 |
|------|-----|
| 代码行数 | ~180 |
| 测试数量 | 5 |
| 测试通过率 | 100% |
| 配置项 | 0 |

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

## 📄 许可证

MIT License

---

*最后更新：2026-03-21*
