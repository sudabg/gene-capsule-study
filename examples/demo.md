# 演示脚本 - Gene-Capsule 经验抽取系统

## 1. 系统介绍 (2 分钟)

Gene-Capsule 是一个从 Agent 执行轨迹中自动抽取可复用经验的系统。

**核心功能**:
- 从轨迹中识别重复模式
- 抽象泛化为通用模板
- 构建结构化知识单元 (Capsule)

## 2. 使用演示 (5 分钟)

### 步骤 1: 准备数据
```python
from src.extraction.extractor import ExperienceExtractor
import json

# 加载轨迹数据
with open("data/sample_trajectories.json") as f:
    trajectories = json.load(f)
```

### 步骤 2: 抽取经验
```python
extractor = ExperienceExtractor()
capsules = extractor.extract(trajectories)
```

### 步骤 3: 查看结果
```python
print(f"抽取了 {len(capsules)} 个经验胶囊")
print(json.dumps(capsules[0], indent=2, ensure_ascii=False))
```

### 步骤 4: 应用经验
```python
# 在新任务中检索和应用 Capsule
def apply_capsule(capsule, new_task):
    # 检查前置条件
    if check_preconditions(capsule, new_task):
        # 执行 Capsule 中的步骤
        for step in capsule["steps"]:
            execute_step(step)
        return True
    return False
```

## 3. 实验结果展示 (3 分钟)

### 性能指标
- 准确率：87.5%
- 召回率：82.3%
- F1 分数：84.8%

### 抽取的模式示例
展示 2-3 个典型 Capsule

## 4. Q&A (5 分钟)

常见问题：
1. 如何处理复杂条件分支？
2. 如何评估 Capsule 质量？
3. 如何跨领域迁移？

## 5. 总结 (1 分钟)

Gene-Capsule 系统成功实现了从 Agent 轨迹到可复用经验的自动抽取，为 Agent 系统的知识积累和迁移提供了有效工具。
