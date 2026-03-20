"""
Gene-Capsule 经验抽取器 - 简化版

版本：v4.0 (简化重构版)
日期：2026-03-21
原则：越简单越好
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib


@dataclass
class GeneCapsule:
    """经验胶囊 - 简化版（5 个核心字段）"""
    id: str
    pattern: List[str]
    metrics: Dict[str, float]
    confidence: float
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "pattern": self.pattern,
            "metrics": self.metrics,
            "confidence": self.confidence,
            "tags": self.tags
        }
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GeneCapsule':
        return cls(
            id=data.get("id", ""),
            pattern=data.get("pattern", []),
            metrics=data.get("metrics", {}),
            confidence=data.get("confidence", 0.0),
            tags=data.get("tags", [])
        )


class ExperienceExtractor:
    """
    经验抽取器 - 简化版
    
    整合所有功能：解析、抽取、泛化、构建、检索
    零配置，开箱即用
    """
    
    def __init__(self):
        # 固定参数，无需配置
        self.min_frequency = 2
        self.pattern_length = 3
    
    def extract(self, trajectories: List[Dict]) -> List[GeneCapsule]:
        """
        从轨迹抽取经验
        
        Args:
            trajectories: 轨迹列表
        
        Returns:
            GeneCapsule 列表
        """
        if not trajectories:
            return []
        
        # 1. 提取动作序列
        patterns = self._extract_patterns(trajectories)
        
        # 2. 构建 Capsule
        capsules = [
            self._build_capsule(pattern, count, trajectories)
            for pattern, count in patterns.items()
            if count >= self.min_frequency
        ]
        
        return capsules
    
    def _extract_patterns(self, trajectories: List[Dict]) -> Dict[tuple, int]:
        """提取频繁模式"""
        pattern_count = {}
        
        for traj in trajectories:
            steps = traj.get("steps", [])
            actions = [s.get("action", "").upper() for s in steps]
            
            # 滑动窗口提取子序列
            for i in range(len(actions) - self.pattern_length + 1):
                pattern = tuple(actions[i:i + self.pattern_length])
                pattern_count[pattern] = pattern_count.get(pattern, 0) + 1
        
        return pattern_count
    
    def _build_capsule(self, pattern: tuple, count: int, trajectories: List[Dict]) -> GeneCapsule:
        """构建 Capsule"""
        # 计算指标
        success_count = sum(1 for t in trajectories if t.get("success", True))
        success_rate = success_count / len(trajectories) if trajectories else 0.0
        
        avg_time = sum(t.get("total_time", 0) for t in trajectories) / len(trajectories) if trajectories else 0.0
        
        # 生成 ID
        pattern_str = "_".join(pattern)
        capsule_id = f"capsule_{hashlib.md5(pattern_str.encode()).hexdigest()[:8]}"
        
        # 生成标签
        tags = ["auto-extracted"]
        if len(pattern) > 5:
            tags.append("long-sequence")
        elif len(pattern) > 2:
            tags.append("medium-sequence")
        else:
            tags.append("short-sequence")
        
        return GeneCapsule(
            id=capsule_id,
            pattern=list(pattern),
            metrics={
                "success_rate": success_rate,
                "avg_execution_time": avg_time,
                "reuse_count": count
            },
            confidence=min(1.0, success_rate * 0.7 + (count / 10) * 0.3),
            tags=tags
        )
    
    def search(self, query: str, top_k: int = 10, capsules: List[GeneCapsule] = None) -> List[GeneCapsule]:
        """
        搜索 Capsule - 简单关键词匹配 + 质量排序
        
        Args:
            query: 查询字符串
            top_k: 返回数量
            capsules: Capsule 列表（可选，默认使用当前）
        
        Returns:
            搜索结果列表
        """
        if not capsules:
            return []
        
        query_lower = query.lower()
        results = []
        
        for capsule in capsules:
            score = 0.0
            
            # 标签匹配
            if any(query_lower in tag.lower() for tag in capsule.tags):
                score += 0.5
            
            # 模式匹配
            if any(query_lower in action.lower() for action in capsule.pattern):
                score += 0.3
            
            # 质量加分
            score += capsule.confidence * 0.2
            
            if score > 0:
                results.append((capsule, score))
        
        # 按分数排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        return [c for c, _ in results[:top_k]]
    
    def save(self, capsules: List[GeneCapsule], output_path: str):
        """保存到文件"""
        data = {
            "capsules": [c.to_dict() for c in capsules],
            "count": len(capsules),
            "generated_at": datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load(self, input_path: str) -> List[GeneCapsule]:
        """从文件加载"""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [GeneCapsule.from_dict(c) for c in data.get("capsules", [])]


# ============== 使用示例 ==============

if __name__ == "__main__":
    # 示例轨迹
    trajectories = [
        {
            "trajectory_id": "traj_001",
            "steps": [
                {"action": "call_api", "tool": "weather_api", "output": {"temp": 25}, "success": True},
                {"action": "analyze", "tool": "processor", "output": {"result": "sunny"}, "success": True},
                {"action": "return", "output": {"final": "sunny"}, "success": True}
            ],
            "success": True,
            "total_time": 5.0
        }
    ]
    
    # 使用
    extractor = ExperienceExtractor()
    capsules = extractor.extract(trajectories)
    
    print(f"抽取了 {len(capsules)} 个 Capsule")
    for c in capsules:
        print(c.to_json())
    
    # 搜索
    results = extractor.search("api", capsules=capsules)
    print(f"找到 {len(results)} 个结果")
    
    # 保存/加载
    extractor.save(capsules, "output.json")
    loaded = extractor.load("output.json")
    print(f"加载了 {len(loaded)} 个 Capsule")
