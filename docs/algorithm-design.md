# 算法设计文档

## 1. 轨迹预处理

### 输入格式
```json
{
  "trajectory_id": "traj_001",
  "steps": [
    {
      "step_id": 1,
      "action": "call_api",
      "tool": "weather_api",
      "parameters": {"location": "Beijing"},
      "output": {"temp": 25, "condition": "sunny"},
      "timestamp": "2026-03-20T10:00:00Z"
    }
  ]
}
```

### 预处理步骤
1. **清洗** - 移除无效步骤
2. **标准化** - 统一动作类型
3. **分段** - 识别子任务边界
4. **标注** - 标记关键决策点

## 2. 模式识别算法

### 算法流程
```
输入：预处理后的轨迹集合 T
输出：模式集合 P

1. 对每个轨迹 t ∈ T:
   a. 提取动作序列 A = [a1, a2, ..., an]
   b. 识别重复子序列 S
   c. 计算子序列频率 f(S)
   d. 如果 f(S) >= threshold，加入候选模式集

2. 对候选模式聚类:
   a. 计算模式相似度 sim(p1, p2)
   b. 使用 DBSCAN 聚类
   c. 每个簇生成一个通用模式

3. 输出模式集合 P
```

### 相似度计算
```python
def pattern_similarity(p1, p2):
    # 结构相似度 (40%)
    struct_sim = lcs_length(p1.steps, p2.steps) / max(len(p1), len(p2))
    
    # 语义相似度 (40%)
    semantic_sim = cosine_similarity(p1.embedding, p2.embedding)
    
    # 工具相似度 (20%)
    tool_sim = jaccard(p1.tools, p2.tools)
    
    return 0.4 * struct_sim + 0.4 * semantic_sim + 0.2 * tool_sim
```

## 3. 抽象泛化机制

### 泛化层次
1. **具体层** - 保留所有具体值
2. **参数层** - 具体值替换为变量
3. **模板层** - 抽象为通用模板
4. **元模式层** - 最高级抽象

### 泛化规则
```
规则 1: 常量 → 变量
  "location": "Beijing" → "location": "{{input.location}}"

规则 2: 具体工具 → 工具类型
  "weather_api" → "{{weather_api}}"

规则 3: 具体值 → 约束条件
  "temp": 25 → "temp": {"type": "number", "range": [0, 50]}
```

## 4. 边界条件定义

### 前置条件
```json
{
  "preconditions": [
    {"type": "api_available", "apis": ["weather_api"]},
    {"type": "input_valid", "fields": ["location"]},
    {"type": "rate_limit", "max_calls": 10, "window": "1min"}
  ]
}
```

### 后置条件
```json
{
  "postconditions": [
    {"type": "output_generated", "format": "json"},
    {"type": "quality_check", "min_confidence": 0.8}
  ]
}
```

### 约束条件
```json
{
  "constraints": [
    {"type": "time_limit", "max_duration": "30s"},
    {"type": "resource_limit", "max_memory": "512MB"},
    {"type": "dependency", "requires": ["internet_connection"]}
  ]
}
```

## 5. 评估指标

### 抽取质量
- **准确率**: 抽取的模式 vs 人工标注
- **召回率**: 真实模式被抽取的比例
- **F1 分数**: 准确率和召回率的调和平均

### 复用性
- **复用次数**: 模式被复用的次数
- **复用成功率**: 复用后任务成功的比例
- **迁移率**: 跨领域复用的比例

### 稳定性
- **时间稳定性**: 不同时间段的表现一致性
- **环境稳定性**: 不同环境下的表现一致性
