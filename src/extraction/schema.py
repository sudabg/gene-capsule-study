"""
Gene/Capsule Schema 定义

版本：v1.0
日期：2026-03-20
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import json


class ActionType(str, Enum):
    """动作类型枚举"""
    CALL_API = "call_api"
    CALL_TOOL = "call_tool"
    EXECUTE_CODE = "execute_code"
    SEARCH_WEB = "search_web"
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    ANALYZE = "analyze"
    REASON = "reason"
    COMMUNICATE = "communicate"
    WAIT = "wait"
    CUSTOM = "custom"


class ConstraintType(str, Enum):
    """约束类型枚举"""
    RATE_LIMIT = "rate_limit"
    DATA_FRESHNESS = "data_freshness"
    RESOURCE_LIMIT = "resource_limit"
    TIME_LIMIT = "time_limit"
    DEPENDENCY = "dependency"
    CUSTOM = "custom"


@dataclass
class Step:
    """经验步骤"""
    step_id: int
    action: ActionType
    tool: str
    parameters: Dict[str, Any]
    output: str
    description: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "step_id": self.step_id,
            "action": self.action.value,
            "tool": self.tool,
            "parameters": self.parameters,
            "output": self.output,
            "description": self.description
        }


@dataclass
class Condition:
    """条件（前置/后置）"""
    type: str
    description: str
    required: bool = True
    check_method: str = "auto"
    
    def to_dict(self) -> Dict:
        return {
            "type": self.type,
            "description": self.description,
            "required": self.required,
            "check_method": self.check_method
        }


@dataclass
class Constraint:
    """约束条件"""
    type: ConstraintType
    description: str
    value: Any
    unit: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "type": self.type.value,
            "description": self.description,
            "value": self.value,
            "unit": self.unit
        }


@dataclass
class Applicability:
    """适用范围"""
    domains: List[str] = field(default_factory=list)
    task_types: List[str] = field(default_factory=list)
    similarity_threshold: float = 0.7
    excluded_domains: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "domains": self.domains,
            "task_types": self.task_types,
            "similarity_threshold": self.similarity_threshold,
            "excluded_domains": self.excluded_domains
        }


@dataclass
class Metrics:
    """经验指标"""
    success_rate: float = 0.0
    avg_execution_time: float = 0.0
    reuse_count: int = 0
    transfer_success: float = 0.0
    last_used: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "success_rate": self.success_rate,
            "avg_execution_time": self.avg_execution_time,
            "reuse_count": self.reuse_count,
            "transfer_success": self.transfer_success,
            "last_used": self.last_used
        }


@dataclass
class GeneCapsule:
    """
    Gene/Capsule - 经验知识单元
    
    核心数据结构，包含经验的所有信息
    """
    id: str
    name: str
    description: str
    steps: List[Step]
    preconditions: List[Condition] = field(default_factory=list)
    postconditions: List[Condition] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    applicability: Applicability = field(default_factory=Applicability)
    metrics: Metrics = field(default_factory=Metrics)
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    source_trajectories: List[str] = field(default_factory=list)
    confidence: float = 1.0
    version: str = "1.0"
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps],
            "preconditions": [p.to_dict() for p in self.preconditions],
            "postconditions": [p.to_dict() for p in self.postconditions],
            "constraints": [c.to_dict() for c in self.constraints],
            "applicability": self.applicability.to_dict(),
            "metrics": self.metrics.to_dict(),
            "metadata": {
                "created_at": self.created_at,
                "source_trajectories": self.source_trajectories,
                "confidence": self.confidence,
                "version": self.version,
                "tags": self.tags
            }
        }
    
    def to_json(self, indent: int = 2) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GeneCapsule':
        """从字典创建"""
        steps = [
            Step(
                step_id=s["step_id"],
                action=ActionType(s["action"]),
                tool=s["tool"],
                parameters=s["parameters"],
                output=s["output"],
                description=s.get("description", "")
            )
            for s in data.get("steps", [])
        ]
        
        preconditions = [
            Condition(
                type=p["type"],
                description=p["description"],
                required=p.get("required", True),
                check_method=p.get("check_method", "auto")
            )
            for p in data.get("preconditions", [])
        ]
        
        postconditions = [
            Condition(
                type=p["type"],
                description=p["description"],
                required=p.get("required", True),
                check_method=p.get("check_method", "auto")
            )
            for p in data.get("postconditions", [])
        ]
        
        constraints = [
            Constraint(
                type=ConstraintType(c["type"]),
                description=c["description"],
                value=c["value"],
                unit=c.get("unit", "")
            )
            for c in data.get("constraints", [])
        ]
        
        app_data = data.get("applicability", {})
        applicability = Applicability(
            domains=app_data.get("domains", []),
            task_types=app_data.get("task_types", []),
            similarity_threshold=app_data.get("similarity_threshold", 0.7),
            excluded_domains=app_data.get("excluded_domains", [])
        ]
        
        metrics_data = data.get("metrics", {})
        metrics = Metrics(
            success_rate=metrics_data.get("success_rate", 0.0),
            avg_execution_time=metrics_data.get("avg_execution_time", 0.0),
            reuse_count=metrics_data.get("reuse_count", 0),
            transfer_success=metrics_data.get("transfer_success", 0.0),
            last_used=metrics_data.get("last_used")
        )
        
        metadata = data.get("metadata", {})
        
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            steps=steps,
            preconditions=preconditions,
            postconditions=postconditions,
            constraints=constraints,
            applicability=applicability,
            metrics=metrics,
            created_at=metadata.get("created_at", datetime.now().isoformat()),
            source_trajectories=metadata.get("source_trajectories", []),
            confidence=metadata.get("confidence", 1.0),
            version=metadata.get("version", "1.0"),
            tags=metadata.get("tags", [])
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'GeneCapsule':
        """从 JSON 字符串创建"""
        data = json.loads(json_str)
        return cls.from_dict(data)


# 示例：创建一个 Gene/Capsule
def create_example_capsule() -> GeneCapsule:
    """创建示例经验单元"""
    return GeneCapsule(
        id="capsule_example_001",
        name="多步工具调用 - 数据获取与分析",
        description="通过连续调用多个 API 获取数据并进行分析的经验模式",
        steps=[
            Step(
                step_id=1,
                action=ActionType.CALL_API,
                tool="weather_api",
                parameters={"location": "{{input.location}}"},
                output="weather_data",
                description="获取天气数据"
            ),
            Step(
                step_id=2,
                action=ActionType.CALL_API,
                tool="news_api",
                parameters={"location": "{{input.location}}", "date": "{{today}}"},
                output="news_data",
                description="获取新闻数据"
            ),
            Step(
                step_id=3,
                action=ActionType.ANALYZE,
                tool="correlation_analysis",
                parameters={"inputs": ["weather_data", "news_data"]},
                output="analysis_result",
                description="分析天气与新闻的相关性"
            )
        ],
        preconditions=[
            Condition(type="api_available", description="天气 API 可用", required=True),
            Condition(type="api_available", description="新闻 API 可用", required=True),
            Condition(type="input_valid", description="位置参数有效", required=True)
        ],
        postconditions=[
            Condition(type="output_generated", description="生成分析报告", required=True)
        ],
        constraints=[
            Constraint(type=ConstraintType.RATE_LIMIT, description="API 调用限流", value=10, unit="calls/minute"),
            Constraint(type=ConstraintType.DATA_FRESHNESS, description="数据新鲜度", value=1, unit="hour")
        ],
        applicability=Applicability(
            domains=["weather", "news", "data_analysis"],
            task_types=["multi_step", "api_composition"],
            similarity_threshold=0.7
        ),
        metrics=Metrics(
            success_rate=0.95,
            avg_execution_time=2.3,
            reuse_count=47,
            transfer_success=0.89
        ),
        source_trajectories=["traj_001", "traj_023", "traj_045"],
        confidence=0.92,
        version="1.0",
        tags=["api", "multi-step", "analysis", "weather", "news"]
    )


if __name__ == "__main__":
    # 测试
    example = create_example_capsule()
    print(example.to_json())
