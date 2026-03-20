# API 文档

## 模块：src.extraction.extractor

### 类：ExperienceExtractor

经验抽取器主类

#### 初始化
```python
extractor = ExperienceExtractor()
```

#### 方法：extract
从原始轨迹抽取经验胶囊

**参数**:
- `raw_trajectories: List[Dict]` - 原始轨迹数据列表

**返回**:
- `List[Dict]` - 经验胶囊列表

**示例**:
```python
capsules = extractor.extract(my_trajectories)
```

### 类：TrajectoryParser

轨迹解析器

#### 方法：parse
解析原始轨迹数据

**参数**:
- `raw_data: Dict` - 原始轨迹数据

**返回**:
- `Trajectory` - 解析后的轨迹对象

#### 方法：clean
清洗轨迹，移除无效步骤

**参数**:
- `trajectory: Trajectory` - 轨迹对象

**返回**:
- `Trajectory` - 清洗后的轨迹

#### 方法：normalize
标准化轨迹，统一动作类型

**参数**:
- `trajectory: Trajectory` - 轨迹对象

**返回**:
- `Trajectory` - 标准化后的轨迹

### 类：PatternExtractor

模式抽取器

#### 初始化
```python
extractor = PatternExtractor(min_frequency=2)
```

**参数**:
- `min_frequency: int` - 最小频率阈值

#### 方法：extract_subsequences
提取公共子序列

**参数**:
- `trajectories: List[Trajectory]` - 轨迹列表
- `length: int` - 子序列长度（默认 3）

**返回**:
- `Dict` - 子序列及其频率

#### 方法：cluster_patterns
聚类相似模式

**参数**:
- `patterns: Dict` - 模式字典
- `threshold: float` - 相似度阈值（默认 0.7）

**返回**:
- `List[List]` - 模式簇列表

### 类：Generalizer

泛化器

#### 方法：generalize
泛化模式簇

**参数**:
- `pattern_cluster: List` - 模式簇

**返回**:
- `Dict` - 泛化后的模式

### 类：CapsuleBuilder

Capsule 构建器

#### 方法：build
构建 Gene/Capsule

**参数**:
- `generalized_pattern: Dict` - 泛化模式
- `trajectories: List[Trajectory]` - 源轨迹列表

**返回**:
- `Dict` - Gene/Capsule 对象

## 数据结构

### Trajectory
```python
@dataclass
class Trajectory:
    trajectory_id: str
    steps: List[TrajectoryStep]
    success: bool
    total_time: float
```

### TrajectoryStep
```python
@dataclass
class TrajectoryStep:
    step_id: int
    action: str
    tool: str
    parameters: Dict[str, Any]
    output: Any
    timestamp: str
```

### GeneCapsule
```python
{
    "id": "capsule_0042",
    "name": "Pattern-parameterized",
    "description": "自动抽取的 parameterized 经验模式",
    "steps": [...],
    "preconditions": [...],
    "postconditions": [...],
    "constraints": [...],
    "applicability": {...},
    "metrics": {...},
    "metadata": {...}
}
```
