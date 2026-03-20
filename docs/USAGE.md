# 使用教程 - Gene-Capsule 经验抽取器

**版本**: v3.0  
**最后更新**: 2026-03-20

---

## 📦 快速开始

### 1. 安装依赖

```bash
cd gene-capsule-study
pip install -r requirements.txt
```

### 2. 基本使用

```python
from src.extraction.extractor_v3 import ExperienceExtractor

# 创建抽取器
extractor = ExperienceExtractor()

# 准备轨迹数据
trajectories = [
    {
        "trajectory_id": "traj_001",
        "task_description": "获取天气并分析",
        "steps": [
            {
                "step_id": 1,
                "action": "call_api",
                "tool": "weather_api",
                "parameters": {"location": "Beijing"},
                "output": {"temp": 25},
                "success": True
            },
            {
                "step_id": 2,
                "action": "analyze",
                "tool": "data_processor",
                "parameters": {"data": "{{output_1}}"},
                "output": {"result": "sunny"},
                "success": True
            }
        ],
        "success": True,
        "total_time": 5.0
    }
]

# 抽取经验
capsules = extractor.extract(trajectories)

# 查看结果
for capsule in capsules:
    print(capsule.to_json())
```

### 3. 保存到文件

```python
# 保存 Capsule
extractor.save_capsules(capsules, "output/capsules.json")

# 从文件加载
capsules = extractor.extract_from_file("output/capsules.json")
```

---

## 🔧 配置选项

### 自定义参数

```python
# 自定义配置
config = {
    "min_frequency": 2,      # 最小模式频率
    "min_length": 2,         # 最小模式长度
}

# 创建抽取器
extractor = ExperienceExtractor(config=config)

# 指定模式长度
capsules = extractor.extract(trajectories, pattern_length=3)
```

### 配置说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `min_frequency` | 2 | 模式最小出现频率 |
| `min_length` | 2 | 模式最小长度 |
| `pattern_length` | 3 | 抽取的模式长度 |

---

## 📊 输出格式

### GeneCapsule 结构

```json
{
  "id": "capsule_a1b2c3d4",
  "name": "Pattern-parameterized-3steps",
  "description": "自动抽取的 parameterized 经验模式，包含 3 个步骤",
  "pattern": ["CALL_API", "ANALYZE", "RETURN"],
  "variables": {
    "var_0": {
      "position": 2,
      "values": ["RETURN", "OUTPUT", "SAVE"],
      "type": "string"
    }
  },
  "preconditions": [
    {"type": "trajectory_success", "required": true},
    {"type": "tools_available", "tools": ["weather_api"], "required": true}
  ],
  "postconditions": [
    {"type": "output_generated", "required": true},
    {"type": "success_rate", "value": 1.0, "required": false}
  ],
  "constraints": [
    {"type": "time_limit", "value": 10.0, "unit": "seconds"},
    {"type": "max_steps", "value": 5}
  ],
  "applicability": {
    "domains": ["general"],
    "task_types": ["api_composition", "analysis"],
    "similarity_threshold": 0.7
  },
  "metrics": {
    "success_rate": 1.0,
    "avg_execution_time": 5.0,
    "reuse_count": 3,
    "transfer_success": 0.0
  },
  "source_trajectories": ["traj_001", "traj_002", "traj_003"],
  "confidence": 0.95,
  "version": "1.0",
  "created_at": "2026-03-20T12:00:00",
  "tags": ["auto-extracted", "parameterized", "medium-sequence"]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一标识符 |
| `name` | string | 模式名称 |
| `description` | string | 描述信息 |
| `pattern` | list[string] | 动作模式序列 |
| `variables` | dict | 可变量定义 |
| `preconditions` | list[dict] | 前置条件 |
| `postconditions` | list[dict] | 后置条件 |
| `constraints` | list[dict] | 约束条件 |
| `applicability` | dict | 适用范围 |
| `metrics` | dict | 评估指标 |
| `source_trajectories` | list[string] | 源轨迹 ID |
| `confidence` | float | 置信度 (0-1) |
| `version` | string | 版本号 |
| `created_at` | string | 创建时间 |
| `tags` | list[string] | 标签 |

---

## 🧪 运行测试

```bash
# 运行所有测试
python3 -m unittest tests.test_extractor -v

# 运行特定测试类
python3 -m unittest tests.test_extractor.TestTrajectoryParser -v

# 运行特定测试方法
python3 -m unittest tests.test_extractor.TestTrajectoryParser.test_parse -v
```

### 测试覆盖

| 模块 | 测试数 | 状态 |
|------|--------|------|
| TrajectoryParser | 3 | ✅ 通过 |
| PatternExtractor | 3 | ✅ 通过 |
| Generalizer | 3 | ✅ 通过 |
| CapsuleBuilder | 3 | ✅ 通过 |
| ExperienceExtractor | 2 | ✅ 通过 |
| GeneCapsule | 2 | ✅ 通过 |
| **总计** | **16** | **✅ 全部通过** |

---

## 📁 项目结构

```
gene-capsule-study/
├── src/
│   └── extraction/
│       ├── extractor_v3.py      # 核心实现
│       └── __init__.py
├── tests/
│   └── test_extractor.py        # 单元测试
├── docs/
│   ├── USAGE.md                 # 使用教程 (本文件)
│   ├── API.md                   # API 文档
│   └── algorithm-design-deep.md # 算法设计
├── paper/
│   ├── literature-survey-deep.md # 文献调研
│   └── literature-review-deep.md # 文献综述
├── experiments/                  # 实验结果
├── output/                       # 输出文件
├── requirements.txt              # 依赖
└── README.md                     # 项目说明
```

---

## 🔍 常见问题

### Q1: 为什么抽取不到 Capsule？

**可能原因**:
1. 轨迹数量太少 (< 3 条)
2. 模式频率阈值太高
3. 模式长度设置不合适

**解决方案**:
```python
# 降低频率阈值
config = {"min_frequency": 1}
extractor = ExperienceExtractor(config=config)

# 调整模式长度
capsules = extractor.extract(trajectories, pattern_length=2)
```

### Q2: 如何自定义动作类型？

**方法**: 修改 `TrajectoryParser` 的 `action_mapping`:

```python
parser = TrajectoryParser()
parser.action_mapping["custom_action"] = "CUSTOM_ACTION"
```

### Q3: 如何评估 Capsule 质量？

**指标**:
- `confidence`: 置信度 (0-1)，越高越好
- `success_rate`: 成功率 (0-1)，越高越好
- `reuse_count`: 复用次数，越高越好

**建议**: 选择 `confidence > 0.8` 且 `success_rate > 0.7` 的 Capsule

### Q4: 如何处理大规模数据？

**建议**:
1. 分批处理轨迹
2. 使用文件 I/O 而非内存
3. 考虑并行处理

```python
# 分批处理
batch_size = 100
for i in range(0, len(trajectories), batch_size):
    batch = trajectories[i:i+batch_size]
    capsules = extractor.extract(batch)
    extractor.save_capsules(capsules, f"output/capsules_{i}.json")
```

---

## 📚 相关文档

- [API 文档](API.md) - 详细 API 参考
- [算法设计](algorithm-design-deep.md) - 算法原理
- [文献调研](../paper/literature-survey-deep.md) - 研究背景

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/sudabg/gene-capsule-study.git
cd gene-capsule-study

# 安装依赖
pip install -r requirements.txt

# 运行测试
python3 -m unittest tests.test_extractor -v
```

### 代码规范

- 遵循 PEP 8 风格指南
- 添加完整的类型注解
- 编写单元测试
- 更新文档

---

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

*最后更新：2026-03-20*
