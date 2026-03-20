"""
Agent Experience Extractor - 完整实现

版本：v3.0 (使用 agency-agents 技能工程部门)
日期：2026-03-20
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib


# ============== 数据结构 ==============

@dataclass
class TrajectoryStep:
    """轨迹步骤"""
    step_id: int
    action: str
    tool: str
    parameters: Dict[str, Any]
    output: Any
    success: bool
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "step_id": self.step_id,
            "action": self.action,
            "tool": self.tool,
            "parameters": self.parameters,
            "output": self.output,
            "success": self.success,
            "timestamp": self.timestamp
        }


@dataclass
class Trajectory:
    """执行轨迹"""
    trajectory_id: str
    task_description: str
    steps: List[TrajectoryStep]
    success: bool
    total_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def action_sequence(self) -> List[str]:
        """获取动作序列"""
        return [step.action for step in self.steps]
    
    def to_dict(self) -> Dict:
        return {
            "trajectory_id": self.trajectory_id,
            "task_description": self.task_description,
            "steps": [step.to_dict() for step in self.steps],
            "success": self.success,
            "total_time": self.total_time,
            "metadata": self.metadata
        }


@dataclass
class GeneCapsule:
    """
    Gene/Capsule - 经验知识单元
    
    核心数据结构，包含可复用的经验模式
    """
    id: str
    name: str
    description: str
    pattern: List[str]  # 动作模式序列
    variables: Dict[str, Any]  # 可变量
    preconditions: List[Dict[str, Any]]  # 前置条件
    postconditions: List[Dict[str, Any]]  # 后置条件
    constraints: List[Dict[str, Any]]  # 约束条件
    applicability: Dict[str, Any]  # 适用范围
    metrics: Dict[str, float]  # 评估指标
    source_trajectories: List[str] = field(default_factory=list)
    confidence: float = 1.0
    version: str = "1.0"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "pattern": self.pattern,
            "variables": self.variables,
            "preconditions": self.preconditions,
            "postconditions": self.postconditions,
            "constraints": self.constraints,
            "applicability": self.applicability,
            "metrics": self.metrics,
            "source_trajectories": self.source_trajectories,
            "confidence": self.confidence,
            "version": self.version,
            "created_at": self.created_at,
            "tags": self.tags
        }
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ============== 核心模块 ==============

class TrajectoryParser:
    """
    轨迹解析器
    
    负责解析、清洗、标准化原始轨迹数据
    """
    
    def __init__(self):
        self.action_mapping = {
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
    
    def parse(self, raw_data: Dict) -> Trajectory:
        """解析原始轨迹数据"""
        steps = [
            TrajectoryStep(
                step_id=s.get("step_id", i),
                action=s.get("action", "UNKNOWN"),
                tool=s.get("tool", ""),
                parameters=s.get("parameters", {}),
                output=s.get("output"),
                success=s.get("success", True),
                timestamp=s.get("timestamp", datetime.now().isoformat())
            )
            for i, s in enumerate(raw_data.get("steps", []))
        ]
        
        return Trajectory(
            trajectory_id=raw_data.get("trajectory_id", self._generate_id()),
            task_description=raw_data.get("task_description", ""),
            steps=steps,
            success=raw_data.get("success", True),
            total_time=raw_data.get("total_time", 0.0),
            metadata=raw_data.get("metadata", {})
        )
    
    def clean(self, trajectory: Trajectory) -> Trajectory:
        """清洗轨迹 - 移除无效步骤"""
        # 移除输出为空且失败的步骤
        valid_steps = [
            s for s in trajectory.steps 
            if s.output is not None or s.success
        ]
        trajectory.steps = valid_steps
        return trajectory
    
    def normalize(self, trajectory: Trajectory) -> Trajectory:
        """标准化 - 统一动作类型"""
        for step in trajectory.steps:
            step.action = self.action_mapping.get(
                step.action.lower(), 
                step.action.upper()
            )
        return trajectory
    
    def _generate_id(self) -> str:
        """生成唯一 ID"""
        return f"traj_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}"


class PatternExtractor:
    """
    模式抽取器
    
    从轨迹中提取可复用的动作模式
    """
    
    def __init__(self, min_frequency: int = 2, min_length: int = 2):
        self.min_frequency = min_frequency
        self.min_length = min_length
    
    def extract_frequent_patterns(
        self, 
        trajectories: List[Trajectory], 
        pattern_length: int = 3
    ) -> Dict[Tuple[str, ...], int]:
        """
        提取频繁子序列模式
        
        Args:
            trajectories: 轨迹列表
            pattern_length: 模式长度
        
        Returns:
            模式及其频率的字典
        """
        pattern_count = {}
        
        for traj in trajectories:
            actions = traj.action_sequence
            # 滑动窗口提取子序列
            for i in range(len(actions) - pattern_length + 1):
                pattern = tuple(actions[i:i + pattern_length])
                pattern_count[pattern] = pattern_count.get(pattern, 0) + 1
        
        # 过滤低频模式
        frequent_patterns = {
            p: c for p, c in pattern_count.items()
            if c >= self.min_frequency
        }
        
        return frequent_patterns
    
    def extract_success_patterns(
        self, 
        trajectories: List[Trajectory]
    ) -> Dict[Tuple[str, ...], Dict[str, int]]:
        """
        提取成功/失败模式
        
        Returns:
            模式 -> {success: count, failure: count}
        """
        pattern_stats = {}
        
        for traj in trajectories:
            actions = traj.action_sequence
            for i in range(len(actions) - 2):
                pattern = tuple(actions[i:i + 3])
                if pattern not in pattern_stats:
                    pattern_stats[pattern] = {"success": 0, "failure": 0}
                
                if traj.success:
                    pattern_stats[pattern]["success"] += 1
                else:
                    pattern_stats[pattern]["failure"] += 1
        
        return pattern_stats
    
    def cluster_similar_patterns(
        self, 
        patterns: Dict[Tuple[str, ...], int],
        similarity_threshold: float = 0.7
    ) -> List[List[Tuple[str, ...]]]:
        """
        聚类相似模式
        
        Args:
            patterns: 模式字典
            similarity_threshold: 相似度阈值
        
        Returns:
            模式簇列表
        """
        clusters = []
        
        for pattern in patterns:
            found_cluster = False
            for cluster in clusters:
                if self._pattern_similarity(pattern, cluster[0]) >= similarity_threshold:
                    cluster.append(pattern)
                    found_cluster = True
                    break
            
            if not found_cluster:
                clusters.append([pattern])
        
        return clusters
    
    def _pattern_similarity(
        self, 
        p1: Tuple[str, ...], 
        p2: Tuple[str, ...]
    ) -> float:
        """计算模式相似度"""
        if len(p1) != len(p2):
            return 0.0
        
        matches = sum(1 for a, b in zip(p1, p2) if a == b)
        return matches / len(p1)


class Generalizer:
    """
    泛化器
    
    将具体模式泛化为可复用的模板
    """
    
    def __init__(self):
        self.variable_counter = 0
    
    def generalize_pattern(
        self, 
        pattern_cluster: List[Tuple[str, ...]]
    ) -> Dict[str, Any]:
        """
        泛化模式簇
        
        Args:
            pattern_cluster: 相似模式簇
        
        Returns:
            泛化后的模式
        """
        if not pattern_cluster:
            return {"pattern": [], "variables": {}, "abstraction_level": "none"}
        
        # 找到共同部分
        common_pattern = self._find_common_subsequence(pattern_cluster)
        
        # 识别可变部分
        variables = self._identify_variables(pattern_cluster, common_pattern)
        
        # 确定抽象层次
        abstraction_level = self._determine_abstraction_level(variables)
        
        return {
            "pattern": common_pattern,
            "variables": variables,
            "abstraction_level": abstraction_level
        }
    
    def _find_common_subsequence(
        self, 
        patterns: List[Tuple[str, ...]]
    ) -> List[str]:
        """找到共同子序列"""
        if not patterns:
            return []
        
        common = list(patterns[0])
        for pattern in patterns[1:]:
            i = 0
            while i < len(common) and i < len(pattern) and common[i] == pattern[i]:
                i += 1
            common = common[:i]
        
        return common
    
    def _identify_variables(
        self, 
        patterns: List[Tuple[str, ...]], 
        common: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """识别变量"""
        variables = {}
        
        for i in range(len(common)):
            # 检查该位置是否有变化
            values_at_position = [
                p[i] if i < len(p) else None 
                for p in patterns
            ]
            unique_values = set(v for v in values_at_position if v is not None)
            
            if len(unique_values) > 1:
                var_name = f"var_{self.variable_counter}"
                self.variable_counter += 1
                variables[var_name] = {
                    "position": i,
                    "values": list(unique_values),
                    "type": self._infer_type(unique_values)
                }
        
        return variables
    
    def _infer_type(self, values: set) -> str:
        """推断变量类型"""
        if all(isinstance(v, str) for v in values):
            return "string"
        elif all(isinstance(v, (int, float)) for v in values):
            return "number"
        else:
            return "any"
    
    def _determine_abstraction_level(
        self, 
        variables: Dict[str, Dict[str, Any]]
    ) -> str:
        """确定抽象层次"""
        if not variables:
            return "concrete"
        elif len(variables) < 3:
            return "parameterized"
        else:
            return "template"


class CapsuleBuilder:
    """
    Capsule 构建器
    
    构建完整的 Gene/Capsule 经验单元
    """
    
    def __init__(self):
        pass
    
    def build(
        self,
        generalized_pattern: Dict[str, Any],
        trajectories: List[Trajectory],
        pattern_stats: Optional[Dict] = None
    ) -> GeneCapsule:
        """
        构建 Gene/Capsule
        
        Args:
            generalized_pattern: 泛化模式
            trajectories: 源轨迹列表
            pattern_stats: 模式统计信息
        
        Returns:
            GeneCapsule 对象
        """
        # 生成 ID
        pattern_str = str(generalized_pattern.get("pattern", []))
        capsule_id = f"capsule_{hashlib.md5(pattern_str.encode()).hexdigest()[:8]}"
        
        # 构建 Capsule
        capsule = GeneCapsule(
            id=capsule_id,
            name=f"Pattern-{generalized_pattern.get('abstraction_level', 'unknown')}-{len(generalized_pattern.get('pattern', []))}steps",
            description=self._generate_description(generalized_pattern),
            pattern=generalized_pattern.get("pattern", []),
            variables=generalized_pattern.get("variables", {}),
            preconditions=self._extract_preconditions(trajectories),
            postconditions=self._extract_postconditions(trajectories),
            constraints=self._extract_constraints(trajectories),
            applicability=self._determine_applicability(trajectories),
            metrics=self._calculate_metrics(trajectories, pattern_stats),
            source_trajectories=[t.trajectory_id for t in trajectories],
            confidence=self._calculate_confidence(trajectories),
            tags=self._generate_tags(generalized_pattern)
        )
        
        return capsule
    
    def _generate_description(self, pattern: Dict[str, Any]) -> str:
        """生成描述"""
        level = pattern.get("abstraction_level", "unknown")
        steps = len(pattern.get("pattern", []))
        return f"自动抽取的{level}经验模式，包含{steps}个步骤"
    
    def _extract_preconditions(self, trajectories: List[Trajectory]) -> List[Dict]:
        """提取前置条件"""
        preconditions = [
            {"type": "trajectory_success", "required": True},
            {"type": "min_steps", "value": 1, "required": True}
        ]
        
        # 检查是否有共同的工具需求
        all_tools = set()
        for traj in trajectories:
            for step in traj.steps:
                all_tools.add(step.tool)
        
        if all_tools:
            preconditions.append({
                "type": "tools_available",
                "tools": list(all_tools),
                "required": True
            })
        
        return preconditions
    
    def _extract_postconditions(self, trajectories: List[Trajectory]) -> List[Dict]:
        """提取后置条件"""
        success_rate = sum(1 for t in trajectories if t.success) / len(trajectories)
        
        return [
            {"type": "output_generated", "required": True},
            {"type": "success_rate", "value": success_rate, "required": False}
        ]
    
    def _extract_constraints(self, trajectories: List[Trajectory]) -> List[Dict]:
        """提取约束条件"""
        constraints = []
        
        # 时间约束
        avg_time = sum(t.total_time for t in trajectories) / len(trajectories)
        constraints.append({
            "type": "time_limit",
            "value": avg_time * 2,
            "unit": "seconds"
        })
        
        # 步骤数约束
        avg_steps = sum(len(t.steps) for t in trajectories) / len(trajectories)
        constraints.append({
            "type": "max_steps",
            "value": int(avg_steps * 1.5)
        })
        
        return constraints
    
    def _determine_applicability(self, trajectories: List[Trajectory]) -> Dict[str, Any]:
        """确定适用范围"""
        # 分析任务类型
        task_keywords = set()
        for traj in trajectories:
            desc = traj.task_description.lower()
            if "api" in desc:
                task_keywords.add("api_composition")
            if "search" in desc:
                task_keywords.add("search")
            if "analyze" in desc:
                task_keywords.add("analysis")
        
        return {
            "domains": ["general"],
            "task_types": list(task_keywords) if task_keywords else ["multi_step"],
            "similarity_threshold": 0.7
        }
    
    def _calculate_metrics(
        self, 
        trajectories: List[Trajectory],
        pattern_stats: Optional[Dict] = None
    ) -> Dict[str, float]:
        """计算指标"""
        success_count = sum(1 for t in trajectories if t.success)
        success_rate = success_count / len(trajectories)
        avg_time = sum(t.total_time for t in trajectories) / len(trajectories)
        
        metrics = {
            "success_rate": success_rate,
            "avg_execution_time": avg_time,
            "reuse_count": len(trajectories),
            "transfer_success": 0.0  # 需要跨任务测试
        }
        
        # 如果有模式统计，添加成功率
        if pattern_stats:
            metrics["pattern_success_ratio"] = pattern_stats.get("success", 0) / max(
                pattern_stats.get("success", 0) + pattern_stats.get("failure", 0),
                1
            )
        
        return metrics
    
    def _calculate_confidence(self, trajectories: List[Trajectory]) -> float:
        """计算置信度"""
        if not trajectories:
            return 0.0
        
        success_rate = sum(1 for t in trajectories if t.success) / len(trajectories)
        consistency = 1.0 / (1.0 + len(trajectories) * 0.1)
        
        return (success_rate + consistency) / 2
    
    def _generate_tags(self, pattern: Dict[str, Any]) -> List[str]:
        """生成标签"""
        tags = ["auto-extracted"]
        
        level = pattern.get("abstraction_level", "unknown")
        tags.append(level)
        
        steps = len(pattern.get("pattern", []))
        if steps > 5:
            tags.append("long-sequence")
        elif steps > 2:
            tags.append("medium-sequence")
        else:
            tags.append("short-sequence")
        
        return tags


class ExperienceExtractor:
    """
    经验抽取器 - 主类
    
    整合所有模块，提供完整的经验抽取流程
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.parser = TrajectoryParser()
        self.extractor = PatternExtractor(
            min_frequency=self.config.get("min_frequency", 2),
            min_length=self.config.get("min_length", 2)
        )
        self.generalizer = Generalizer()
        self.builder = CapsuleBuilder()
    
    def extract(
        self, 
        raw_trajectories: List[Dict],
        pattern_length: int = 3
    ) -> List[GeneCapsule]:
        """
        从原始轨迹抽取经验
        
        Args:
            raw_trajectories: 原始轨迹数据列表
            pattern_length: 模式长度
        
        Returns:
            GeneCapsule 列表
        """
        # 1. 解析轨迹
        trajectories = [self.parser.parse(raw) for raw in raw_trajectories]
        
        # 2. 清洗和标准化
        trajectories = [self.parser.clean(t) for t in trajectories]
        trajectories = [self.parser.normalize(t) for t in trajectories]
        
        # 3. 提取频繁模式
        patterns = self.extractor.extract_frequent_patterns(
            trajectories, 
            pattern_length=pattern_length
        )
        
        # 4. 提取成功/失败模式
        pattern_stats = self.extractor.extract_success_patterns(trajectories)
        
        # 5. 聚类模式
        clusters = self.extractor.cluster_similar_patterns(patterns)
        
        # 6. 泛化模式
        generalized = [
            self.generalizer.generalize_pattern(cluster) 
            for cluster in clusters if cluster
        ]
        
        # 7. 构建 Capsule
        capsules = [
            self.builder.build(g, trajectories, pattern_stats) 
            for g in generalized if g.get("pattern")
        ]
        
        return capsules
    
    def extract_from_file(self, file_path: str) -> List[GeneCapsule]:
        """从文件加载轨迹并抽取经验"""
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        trajectories = raw_data.get("trajectories", [])
        return self.extract(trajectories)
    
    def save_capsules(self, capsules: List[GeneCapsule], output_path: str):
        """保存 Capsule 到文件"""
        data = {
            "capsules": [c.to_dict() for c in capsules],
            "count": len(capsules),
            "generated_at": datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# ============== 使用示例 ==============

if __name__ == "__main__":
    # 示例轨迹数据
    sample_trajectories = [
        {
            "trajectory_id": "traj_001",
            "task_description": "获取天气并分析",
            "steps": [
                {
                    "step_id": 1,
                    "action": "call_api",
                    "tool": "weather_api",
                    "parameters": {"location": "Beijing"},
                    "output": {"temp": 25, "condition": "sunny"},
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
        },
        {
            "trajectory_id": "traj_002",
            "task_description": "获取新闻并总结",
            "steps": [
                {
                    "step_id": 1,
                    "action": "call_api",
                    "tool": "news_api",
                    "parameters": {"category": "tech"},
                    "output": {"articles": ["article1", "article2"]},
                    "success": True
                },
                {
                    "step_id": 2,
                    "action": "analyze",
                    "tool": "summarizer",
                    "parameters": {"text": "{{output_1}}"},
                    "output": {"summary": "tech news summary"},
                    "success": True
                }
            ],
            "success": True,
            "total_time": 3.5
        }
    ]
    
    # 抽取经验
    extractor = ExperienceExtractor()
    capsules = extractor.extract(sample_trajectories)
    
    # 输出结果
    print(f"抽取了 {len(capsules)} 个经验胶囊\n")
    
    for i, capsule in enumerate(capsules, 1):
        print(f"=== Capsule {i} ===")
        print(capsule.to_json())
        print()
    
    # 保存到文件
    extractor.save_capsules(capsules, "output/capsules.json")
    print(f"已保存到 output/capsules.json")
