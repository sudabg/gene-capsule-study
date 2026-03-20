# API 文档 - Gene-Capsule 经验抽取器

**版本**: v3.0  
**最后更新**: 2026-03-20

---

## 📦 模块概览

```
src/extraction/
├── extractor_v3.py    # 核心实现
└── __init__.py
```

### 核心类

| 类 | 用途 | 主要方法 |
|----|------|---------|
| `TrajectoryParser` | 轨迹解析 | `parse()`, `clean()`, `normalize()` |
| `PatternExtractor` | 模式抽取 | `extract_frequent_patterns()`, `cluster_similar_patterns()` |
| `Generalizer` | 泛化器 | `generalize_pattern()` |
| `CapsuleBuilder` | Capsule 构建 | `build()` |
| `ExperienceExtractor` | 主抽取器 | `extract()`, `save_capsules()` |

### 数据类

| 类 | 用途 |
|----|------|
| `TrajectoryStep` | 轨迹步骤 |
| `Trajectory` | 执行轨迹 |
| `GeneCapsule` | 经验胶囊 |

---

## 🔧 TrajectoryParser

### 类定义

```python
class TrajectoryParser:
    """轨迹解析器"""
    
    def __init__(self)
    def parse(self, raw_data: Dict) -> Trajectory
    def clean(self, trajectory: Trajectory) -> Trajectory
    def normalize(self, trajectory: Trajectory) -> Trajectory
```

### 方法详解

#### `parse(raw_data: Dict) -> Trajectory`

解析原始轨迹数据

**参数**:
- `raw_data` (Dict): 原始轨迹数据
  ```python
  {
      "trajectory_id": "traj_001",
      "task_description": "获取天气并分析",
      "steps": [...],
      "success": True,
      "total_time": 5.0
  }
  ```

**返回**:
- `Trajectory`: 解析后的轨迹对象

**示例**:
```python
parser = TrajectoryParser()
trajectory = parser.parse(raw_data)
```

#### `clean(trajectory: Trajectory) -> Trajectory`

清洗轨迹，移除无效步骤

**参数**:
- `trajectory` (Trajectory): 轨迹对象

**返回**:
- `Trajectory`: 清洗后的轨迹

**清洗规则**:
- 移除输出为空且失败的步骤

**示例**:
```python
cleaned = parser.clean(trajectory)
```

#### `normalize(trajectory: Trajectory) -> Trajectory`

标准化轨迹，统一动作类型

**参数**:
- `trajectory` (Trajectory): 轨迹对象

**返回**:
- `Trajectory`: 标准化后的轨迹

**标准化映射**:
```python
{
    "call_api": "CALL_API",
    "call_tool": "CALL_TOOL",
    "execute_code": "EXECUTE_CODE",
    "search_web": "SEARCH_WEB",
    "read_file": "READ_FILE",
    "write_file": "WRITE_FILE",
    "analyze": "ANALYZE",
    "reason": "REASON",
    "communicate": "COMMUNICATE",
}
```

**示例**:
```python
normalized = parser.normalize(trajectory)
```

---

## 🔍 PatternExtractor

### 类定义

```python
class PatternExtractor:
    """模式抽取器"""
    
    def __init__(self, min_frequency: int = 2, min_length: int = 2)
    
    def extract_frequent_patterns(
        trajectories: List[Trajectory], 
        pattern_length: int = 3
    ) -> Dict[Tuple[str, ...], int]
    
    def extract_success_patterns(
        trajectories: List[Trajectory]
    ) -> Dict[Tuple[str, ...], Dict[str, int]]
    
    def cluster_similar_patterns(
        patterns: Dict[Tuple[str, ...], int],
        similarity_threshold: float = 0.7
    ) -> List[List[Tuple[str, ...]]]
```

### 方法详解

#### `extract_frequent_patterns(...)`

提取频繁子序列模式

**参数**:
- `trajectories` (List[Trajectory]): 轨迹列表
- `pattern_length` (int): 模式长度，默认 3

**返回**:
- `Dict[Tuple[str, ...], int]`: 模式及其频率

**示例**:
```python
extractor = PatternExtractor(min_frequency=2)
patterns = extractor.extract_frequent_patterns(trajectories, pattern_length=3)

# 输出：{("CALL_API", "ANALYZE", "RETURN"): 5, ...}
```

#### `extract_success_patterns(trajectories: List[Trajectory])`

提取成功/失败模式统计

**参数**:
- `trajectories` (List[Trajectory]): 轨迹列表

**返回**:
- `Dict[Tuple[str, ...], Dict[str, int]]`: 模式 -> {success: count, failure: count}

**示例**:
```python
pattern_stats = extractor.extract_success_patterns(trajectories)

# 输出：{("CALL_API", "ANALYZE"): {"success": 10, "failure": 2}, ...}
```

#### `cluster_similar_patterns(...)`

聚类相似模式

**参数**:
- `patterns` (Dict): 模式字典
- `similarity_threshold` (float): 相似度阈值，默认 0.7

**返回**:
- `List[List[Tuple[str, ...]]]`: 模式簇列表

**示例**:
```python
clusters = extractor.cluster_similar_patterns(patterns, similarity_threshold=0.7)
```

---

## 🎯 Generalizer

### 类定义

```python
class Generalizer:
    """泛化器"""
    
    def __init__(self)
    
    def generalize_pattern(
        pattern_cluster: List[Tuple[str, ...]]
    ) -> Dict[str, Any]
```

### 方法详解

#### `generalize_pattern(pattern_cluster: List[Tuple[str, ...]]) -> Dict[str, Any]`

泛化模式簇

**参数**:
- `pattern_cluster` (List[Tuple[str, ...]]): 相似模式簇

**返回**:
- `Dict[str, Any]`: 泛化后的模式
  ```python
  {
      "pattern": ["CALL_API", "ANALYZE"],
      "variables": {"var_0": {"position": 2, "values": ["RETURN", "OUTPUT"]}},
      "abstraction_level": "parameterized"
  }
  ```

**抽象层次**:
- `concrete`: 无变量
- `parameterized`: 1-2 个变量
- `template`: 3+ 个变量

**示例**:
```python
generalizer = Generalizer()
generalized = generalizer.generalize_pattern(pattern_cluster)
```

---

## 🏗️ CapsuleBuilder

### 类定义

```python
class CapsuleBuilder:
    """Capsule 构建器"""
    
    def __init__(self)
    
    def build(
        generalized_pattern: Dict[str, Any],
        trajectories: List[Trajectory],
        pattern_stats: Optional[Dict] = None
    ) -> GeneCapsule
```

### 方法详解

#### `build(...) -> GeneCapsule`

构建 Gene/Capsule

**参数**:
- `generalized_pattern` (Dict): 泛化模式
- `trajectories` (List[Trajectory]): 源轨迹列表
- `pattern_stats` (Optional[Dict]): 模式统计信息

**返回**:
- `GeneCapsule`: 经验胶囊对象

**示例**:
```python
builder = CapsuleBuilder()
capsule = builder.build(generalized_pattern, trajectories, pattern_stats)
```

---

## 🎓 ExperienceExtractor

### 类定义

```python
class ExperienceExtractor:
    """经验抽取器 - 主类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None)
    
    def extract(
        raw_trajectories: List[Dict],
        pattern_length: int = 3
    ) -> List[GeneCapsule]
    
    def extract_from_file(file_path: str) -> List[GeneCapsule]
    
    def save_capsules(
        capsules: List[GeneCapsule], 
        output_path: str
    )
```

### 方法详解

#### `extract(raw_trajectories: List[Dict], pattern_length: int = 3) -> List[GeneCapsule]`

从原始轨迹抽取经验

**参数**:
- `raw_trajectories` (List[Dict]): 原始轨迹数据列表
- `pattern_length` (int): 模式长度，默认 3

**返回**:
- `List[GeneCapsule]`: 经验胶囊列表

**流程**:
1. 解析轨迹
2. 清洗和标准化
3. 提取频繁模式
4. 提取成功/失败模式
5. 聚类模式
6. 泛化模式
7. 构建 Capsule

**示例**:
```python
extractor = ExperienceExtractor()
capsules = extractor.extract(trajectories, pattern_length=3)
```

#### `extract_from_file(file_path: str) -> List[GeneCapsule]`

从文件加载轨迹并抽取经验

**参数**:
- `file_path` (str): JSON 文件路径

**返回**:
- `List[GeneCapsule]`: 经验胶囊列表

**示例**:
```python
capsules = extractor.extract_from_file("data/trajectories.json")
```

#### `save_capsules(capsules: List[GeneCapsule], output_path: str)`

保存 Capsule 到文件

**参数**:
- `capsules` (List[GeneCapsule]): Capsule 列表
- `output_path` (str): 输出文件路径

**输出格式**:
```json
{
    "capsules": [...],
    "count": 10,
    "generated_at": "2026-03-20T12:00:00"
}
```

**示例**:
```python
extractor.save_capsules(capsules, "output/capsules.json")
```

---

## 📊 GeneCapsule

### 类定义

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
    
    def to_dict(self) -> Dict
    def to_json(self, indent: int = 2) -> str
```

### 方法详解

#### `to_dict() -> Dict`

转换为字典

**返回**:
- `Dict`: 字典表示

**示例**:
```python
capsule_dict = capsule.to_dict()
```

#### `to_json(indent: int = 2) -> str`

转换为 JSON 字符串

**参数**:
- `indent` (int): 缩进空格数，默认 2

**返回**:
- `str`: JSON 字符串

**示例**:
```python
capsule_json = capsule.to_json(indent=2)
print(capsule_json)
```

---

## 🧪 测试 API

### 运行测试

```bash
# 运行所有测试
python3 -m unittest tests.test_extractor -v

# 运行特定测试类
python3 -m unittest tests.test_extractor.TestTrajectoryParser -v

# 运行特定测试方法
python3 -m unittest tests.test_extractor.TestTrajectoryParser.test_parse -v
```

### 测试覆盖率

| 模块 | 测试数 | 通过率 |
|------|--------|--------|
| `TrajectoryParser` | 3 | 100% |
| `PatternExtractor` | 3 | 100% |
| `Generalizer` | 3 | 100% |
| `CapsuleBuilder` | 3 | 100% |
| `ExperienceExtractor` | 2 | 100% |
| `GeneCapsule` | 2 | 100% |
| **总计** | **16** | **100%** |

---

## 📚 相关文档

- [使用教程](USAGE.md) - 快速入门
- [算法设计](algorithm-design-deep.md) - 算法原理
- [文献调研](../paper/literature-survey-deep.md) - 研究背景

---

*最后更新：2026-03-20*
