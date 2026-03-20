"""
经验抽取器实现

版本：v1.0
日期：2026-03-20
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class TrajectoryStep:
    """轨迹步骤"""
    step_id: int
    action: str
    tool: str
    parameters: Dict[str, Any]
    output: Any
    timestamp: str


@dataclass
class Trajectory:
    """执行轨迹"""
    trajectory_id: str
    steps: List[TrajectoryStep]
    success: bool
    total_time: float


class TrajectoryParser:
    """轨迹解析器"""
    
    def __init__(self):
        pass
    
    def parse(self, raw_data: Dict) -> Trajectory:
        """解析原始轨迹数据"""
        steps = [
            TrajectoryStep(
                step_id=s["step_id"],
                action=s["action"],
                tool=s["tool"],
                parameters=s["parameters"],
                output=s["output"],
                timestamp=s["timestamp"]
            )
            for s in raw_data.get("steps", [])
        ]
        
        return Trajectory(
            trajectory_id=raw_data["trajectory_id"],
            steps=steps,
            success=raw_data.get("success", True),
            total_time=raw_data.get("total_time", 0.0)
        )
    
    def clean(self, trajectory: Trajectory) -> Trajectory:
        """清洗轨迹 - 移除无效步骤"""
        # 移除输出为空的步骤
        valid_steps = [s for s in trajectory.steps if s.output is not None]
        trajectory.steps = valid_steps
        return trajectory
    
    def normalize(self, trajectory: Trajectory) -> Trajectory:
        """标准化 - 统一动作类型"""
        action_map = {
            "call_api": "CALL_API",
            "call_tool": "CALL_TOOL",
            "execute_code": "EXECUTE_CODE",
        }
        
        for step in trajectory.steps:
            step.action = action_map.get(step.action, step.action.upper())
        
        return trajectory


class PatternExtractor:
    """模式抽取器"""
    
    def __init__(self, min_frequency: int = 2):
        self.min_frequency = min_frequency
    
    def extract_subsequences(self, trajectories: List[Trajectory], length: int = 3) -> Dict:
        """提取公共子序列"""
        subseq_count = {}
        
        for traj in trajectories:
            steps = traj.steps
            for i in range(len(steps) - length + 1):
                subseq = tuple(s.action for s in steps[i:i+length])
                subseq_count[subseq] = subseq_count.get(subseq, 0) + 1
        
        # 过滤低频子序列
        patterns = {
            k: v for k, v in subseq_count.items() 
            if v >= self.min_frequency
        }
        
        return patterns
    
    def cluster_patterns(self, patterns: Dict, threshold: float = 0.7) -> List[List]:
        """聚类相似模式"""
        # 简单实现：基于编辑距离聚类
        clusters = []
        
        for pattern in patterns:
            found_cluster = False
            for cluster in clusters:
                if self._similarity(pattern, cluster[0]) >= threshold:
                    cluster.append(pattern)
                    found_cluster = True
                    break
            
            if not found_cluster:
                clusters.append([pattern])
        
        return clusters
    
    def _similarity(self, p1, p2) -> float:
        """计算模式相似度"""
        if len(p1) != len(p2):
            return 0.0
        
        matches = sum(1 for a, b in zip(p1, p2) if a == b)
        return matches / len(p1)


class Generalizer:
    """泛化器"""
    
    def __init__(self):
        self.variable_counter = 0
    
    def generalize(self, pattern_cluster: List) -> Dict:
        """泛化模式簇"""
        if not pattern_cluster:
            return {}
        
        # 找到共同前缀
        common_prefix = self._find_common_prefix(pattern_cluster)
        
        # 识别可变部分
        variables = self._identify_variables(pattern_cluster, common_prefix)
        
        return {
            "pattern": common_prefix,
            "variables": variables,
            "abstraction_level": self._determine_abstraction_level(variables)
        }
    
    def _find_common_prefix(self, patterns: List) -> List:
        """找到共同前缀"""
        if not patterns:
            return []
        
        common = list(patterns[0])
        for pattern in patterns[1:]:
            i = 0
            while i < len(common) and i < len(pattern) and common[i] == pattern[i]:
                i += 1
            common = common[:i]
        
        return common
    
    def _identify_variables(self, patterns: List, common: List) -> Dict:
        """识别变量"""
        variables = {}
        
        for i, step in enumerate(common):
            # 检查该位置是否有变化
            values_at_position = [p[i] if i < len(p) else None for p in patterns]
            unique_values = set(values_at_position)
            
            if len(unique_values) > 1:
                var_name = f"var_{self.variable_counter}"
                self.variable_counter += 1
                variables[var_name] = {
                    "position": i,
                    "values": list(unique_values),
                    "type": self._infer_type(unique_values)
                }
        
        return variables
    
    def _infer_type(self, values) -> str:
        """推断变量类型"""
        if all(isinstance(v, str) for v in values):
            return "string"
        elif all(isinstance(v, (int, float)) for v in values):
            return "number"
        else:
            return "any"
    
    def _determine_abstraction_level(self, variables: Dict) -> str:
        """确定抽象层次"""
        if not variables:
            return "concrete"
        elif len(variables) < 3:
            return "parameterized"
        else:
            return "template"


class CapsuleBuilder:
    """Capsule 构建器"""
    
    def __init__(self):
        pass
    
    def build(self, generalized_pattern: Dict, trajectories: List[Trajectory]) -> Dict:
        """构建 Gene/Capsule"""
        capsule = {
            "id": f"capsule_{hash(str(generalized_pattern)) % 10000:04d}",
            "name": f"Pattern-{generalized_pattern.get('abstraction_level', 'unknown')}",
            "description": self._generate_description(generalized_pattern),
            "steps": self._build_steps(generalized_pattern),
            "preconditions": self._extract_preconditions(trajectories),
            "postconditions": self._extract_postconditions(trajectories),
            "constraints": self._extract_constraints(trajectories),
            "applicability": self._determine_applicability(trajectories),
            "metrics": self._calculate_metrics(trajectories),
            "metadata": {
                "source_trajectories": [t.trajectory_id for t in trajectories],
                "confidence": self._calculate_confidence(trajectories),
                "version": "1.0"
            }
        }
        
        return capsule
    
    def _generate_description(self, pattern: Dict) -> str:
        """生成描述"""
        level = pattern.get("abstraction_level", "unknown")
        return f"自动抽取的{level}经验模式"
    
    def _build_steps(self, pattern: Dict) -> List[Dict]:
        """构建步骤"""
        steps = []
        for i, action in enumerate(pattern.get("pattern", [])):
            steps.append({
                "step_id": i + 1,
                "action": action,
                "tool": f"tool_{i}",
                "parameters": {},
                "output": f"output_{i}"
            })
        return steps
    
    def _extract_preconditions(self, trajectories: List[Trajectory]) -> List[Dict]:
        """提取前置条件"""
        return [
            {"type": "trajectory_success", "required": True},
            {"type": "min_steps", "value": 1}
        ]
    
    def _extract_postconditions(self, trajectories: List[Trajectory]) -> List[Dict]:
        """提取后置条件"""
        return [
            {"type": "output_generated", "required": True}
        ]
    
    def _extract_constraints(self, trajectories: List[Trajectory]) -> List[Dict]:
        """提取约束条件"""
        avg_time = sum(t.total_time for t in trajectories) / len(trajectories)
        return [
            {"type": "time_limit", "value": avg_time * 2, "unit": "seconds"}
        ]
    
    def _determine_applicability(self, trajectories: List[Trajectory]) -> Dict:
        """确定适用范围"""
        return {
            "domains": ["general"],
            "task_types": ["multi_step"],
            "similarity_threshold": 0.7
        }
    
    def _calculate_metrics(self, trajectories: List[Trajectory]) -> Dict:
        """计算指标"""
        success_count = sum(1 for t in trajectories if t.success)
        return {
            "success_rate": success_count / len(trajectories),
            "avg_execution_time": sum(t.total_time for t in trajectories) / len(trajectories),
            "reuse_count": len(trajectories),
            "transfer_success": 0.0  # 需要跨任务测试
        }
    
    def _calculate_confidence(self, trajectories: List[Trajectory]) -> float:
        """计算置信度"""
        if not trajectories:
            return 0.0
        
        success_rate = sum(1 for t in trajectories if t.success) / len(trajectories)
        consistency = 1.0 / (1.0 + len(trajectories) * 0.1)  # 简单实现
        
        return (success_rate + consistency) / 2


class ExperienceExtractor:
    """经验抽取器 - 主类"""
    
    def __init__(self):
        self.parser = TrajectoryParser()
        self.extractor = PatternExtractor()
        self.generalizer = Generalizer()
        self.builder = CapsuleBuilder()
    
    def extract(self, raw_trajectories: List[Dict]) -> List[Dict]:
        """从原始轨迹抽取经验"""
        # 1. 解析轨迹
        trajectories = [self.parser.parse(raw) for raw in raw_trajectories]
        
        # 2. 清洗和标准化
        trajectories = [self.parser.clean(t) for t in trajectories]
        trajectories = [self.parser.normalize(t) for t in trajectories]
        
        # 3. 提取子序列模式
        patterns = self.extractor.extract_subsequences(trajectories)
        
        # 4. 聚类模式
        clusters = self.extractor.cluster_patterns(patterns)
        
        # 5. 泛化模式
        generalized = [self.generalizer.generalize(cluster) for cluster in clusters]
        
        # 6. 构建 Capsule
        capsules = [
            self.builder.build(g, trajectories) 
            for g in generalized if g
        ]
        
        return capsules


# 使用示例
if __name__ == "__main__":
    # 示例轨迹数据
    sample_trajectories = [
        {
            "trajectory_id": "traj_001",
            "steps": [
                {
                    "step_id": 1,
                    "action": "call_api",
                    "tool": "weather_api",
                    "parameters": {"location": "Beijing"},
                    "output": {"temp": 25},
                    "timestamp": "2026-03-20T10:00:00Z"
                },
                {
                    "step_id": 2,
                    "action": "analyze",
                    "tool": "data_processor",
                    "parameters": {"data": "{{output_1}}"},
                    "output": {"result": "sunny"},
                    "timestamp": "2026-03-20T10:00:05Z"
                }
            ],
            "success": True,
            "total_time": 5.0
        }
    ]
    
    # 抽取经验
    extractor = ExperienceExtractor()
    capsules = extractor.extract(sample_trajectories)
    
    # 输出结果
    print(json.dumps(capsules, indent=2, ensure_ascii=False))
