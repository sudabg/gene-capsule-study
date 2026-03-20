"""
经验检索模块

版本：v1.0
日期：2026-03-20
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
import json
import math
from datetime import datetime


@dataclass
class SearchResult:
    """搜索结果"""
    capsule_id: str
    capsule_name: str
    score: float
    rank: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "capsule_id": self.capsule_id,
            "capsule_name": self.capsule_name,
            "score": self.score,
            "rank": self.rank,
            "metadata": self.metadata
        }


class CapsuleSearcher:
    """
    Capsule 检索器
    
    支持多种检索策略：
    1. 关键词匹配
    2. 语义相似度
    3. 结构匹配
    4. 混合检索
    """
    
    def __init__(self, capsules: List[Dict[str, Any]]):
        """
        初始化检索器
        
        Args:
            capsules: Capsule 字典列表
        """
        self.capsules = capsules
        self.index = self._build_index()
    
    def _build_index(self) -> Dict[str, Any]:
        """构建检索索引"""
        index = {
            "by_id": {},
            "by_name": {},
            "by_pattern": {},
            "by_tag": {},
            "by_domain": {}
        }
        
        for capsule in self.capsules:
            capsule_id = capsule.get("id", "")
            
            # 按 ID 索引
            index["by_id"][capsule_id] = capsule
            
            # 按名称索引
            name = capsule.get("name", "").lower()
            index["by_name"][name] = capsule
            
            # 按模式索引
            pattern = tuple(capsule.get("pattern", []))
            if pattern not in index["by_pattern"]:
                index["by_pattern"][pattern] = []
            index["by_pattern"][pattern].append(capsule)
            
            # 按标签索引
            for tag in capsule.get("tags", []):
                if tag not in index["by_tag"]:
                    index["by_tag"][tag] = []
                index["by_tag"][tag].append(capsule)
            
            # 按领域索引
            domains = capsule.get("applicability", {}).get("domains", [])
            for domain in domains:
                if domain not in index["by_domain"]:
                    index["by_domain"][domain] = []
                index["by_domain"][domain].append(capsule)
        
        return index
    
    def search(
        self,
        query: str,
        strategy: str = "keyword",
        top_k: int = 10
    ) -> List[SearchResult]:
        """
        搜索 Capsule
        
        Args:
            query: 查询字符串
            strategy: 检索策略 (keyword/semantic/structural/hybrid)
            top_k: 返回结果数量
        
        Returns:
            List[SearchResult]: 搜索结果列表
        """
        if strategy == "keyword":
            results = self._keyword_search(query)
        elif strategy == "semantic":
            results = self._semantic_search(query)
        elif strategy == "structural":
            results = self._structural_search(query)
        elif strategy == "hybrid":
            results = self._hybrid_search(query)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        # 排序并截取 top_k
        results.sort(key=lambda x: x.score, reverse=True)
        
        # 添加排名
        for i, result in enumerate(results[:top_k]):
            result.rank = i + 1
        
        return results[:top_k]
    
    def _keyword_search(self, query: str) -> List[SearchResult]:
        """关键词检索"""
        results = []
        query_lower = query.lower()
        
        for capsule in self.capsules:
            score = 0.0
            
            # 名称匹配
            name = capsule.get("name", "").lower()
            if query_lower in name:
                score += 0.5
            
            # 描述匹配
            desc = capsule.get("description", "").lower()
            if query_lower in desc:
                score += 0.3
            
            # 标签匹配
            tags = capsule.get("tags", [])
            if query_lower in [t.lower() for t in tags]:
                score += 0.2
            
            if score > 0:
                results.append(SearchResult(
                    capsule_id=capsule.get("id", ""),
                    capsule_name=capsule.get("name", ""),
                    score=score,
                    rank=0,
                    metadata={"match_type": "keyword"}
                ))
        
        return results
    
    def _semantic_search(self, query: str) -> List[SearchResult]:
        """语义检索（简化版）"""
        # TODO: 实现基于向量嵌入的语义检索
        # 目前使用关键词检索作为占位
        return self._keyword_search(query)
    
    def _structural_search(self, query: str) -> List[SearchResult]:
        """结构检索 - 基于模式匹配"""
        results = []
        
        # 解析查询为模式
        try:
            query_pattern = tuple(query.split(","))
        except:
            return results
        
        # 查找匹配的模式
        if query_pattern in self.index["by_pattern"]:
            for capsule in self.index["by_pattern"][query_pattern]:
                results.append(SearchResult(
                    capsule_id=capsule.get("id", ""),
                    capsule_name=capsule.get("name", ""),
                    score=1.0,
                    rank=0,
                    metadata={"match_type": "structural"}
                ))
        
        return results
    
    def _hybrid_search(self, query: str) -> List[SearchResult]:
        """混合检索 - 结合多种策略"""
        # 关键词检索
        keyword_results = self._keyword_search(query)
        
        # 结构检索
        structural_results = self._structural_search(query)
        
        # 合并结果
        results_dict = {}
        for result in keyword_results + structural_results:
            if result.capsule_id not in results_dict:
                results_dict[result.capsule_id] = result
            else:
                # 分数相加
                results_dict[result.capsule_id].score += result.score
        
        return list(results_dict.values())
    
    def search_by_id(self, capsule_id: str) -> Optional[Dict[str, Any]]:
        """按 ID 搜索"""
        return self.index["by_id"].get(capsule_id)
    
    def search_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """按标签搜索"""
        return self.index["by_tag"].get(tag, [])
    
    def search_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """按领域搜索"""
        return self.index["by_domain"].get(domain, [])


class CapsuleRanker:
    """
    Capsule 排序器
    
    支持多种排序策略：
    1. 相关性排序
    2. 质量排序
    3. 时效性排序
    4. 混合排序
    """
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        初始化排序器
        
        Args:
            weights: 权重配置
        """
        self.weights = weights or {
            "relevance": 0.4,
            "quality": 0.3,
            "recency": 0.2,
            "popularity": 0.1
        }
    
    def rank(
        self,
        capsules: List[Dict[str, Any]],
        query: Optional[str] = None,
        strategy: str = "hybrid"
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        排序 Capsule
        
        Args:
            capsules: Capsule 列表
            query: 查询字符串（用于相关性计算）
            strategy: 排序策略 (relevance/quality/recency/popularity/hybrid)
        
        Returns:
            List[Tuple[Dict, float]]: (Capsule, 分数) 列表
        """
        if strategy == "relevance":
            return self._rank_by_relevance(capsules, query)
        elif strategy == "quality":
            return self._rank_by_quality(capsules)
        elif strategy == "recency":
            return self._rank_by_recency(capsules)
        elif strategy == "popularity":
            return self._rank_by_popularity(capsules)
        elif strategy == "hybrid":
            return self._rank_hybrid(capsules, query)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def _rank_by_relevance(
        self,
        capsules: List[Dict[str, Any]],
        query: Optional[str]
    ) -> List[Tuple[Dict[str, Any], float]]:
        """按相关性排序"""
        if not query:
            return [(c, 0.0) for c in capsules]
        
        results = []
        query_lower = query.lower()
        
        for capsule in capsules:
            score = 0.0
            
            # 名称匹配
            name = capsule.get("name", "").lower()
            if query_lower in name:
                score += 0.5
            
            # 描述匹配
            desc = capsule.get("description", "").lower()
            if query_lower in desc:
                score += 0.3
            
            # 标签匹配
            tags = capsule.get("tags", [])
            if query_lower in [t.lower() for t in tags]:
                score += 0.2
            
            results.append((capsule, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def _rank_by_quality(
        self,
        capsules: List[Dict[str, Any]]
    ) -> List[Tuple[Dict[str, Any], float]]:
        """按质量排序"""
        results = []
        
        for capsule in capsules:
            metrics = capsule.get("metrics", {})
            
            # 质量分数 = 成功率 * 0.5 + 置信度 * 0.5
            success_rate = metrics.get("success_rate", 0.0)
            confidence = capsule.get("confidence", 0.0)
            
            quality_score = success_rate * 0.5 + confidence * 0.5
            
            results.append((capsule, quality_score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def _rank_by_recency(
        self,
        capsules: List[Dict[str, Any]]
    ) -> List[Tuple[Dict[str, Any], float]]:
        """按时效性排序"""
        results = []
        now = datetime.now()
        
        for capsule in capsules:
            created_at = capsule.get("created_at", "")
            
            try:
                created_time = datetime.fromisoformat(created_at)
                days_old = (now - created_time).days
                # 越新分数越高，最大 1.0
                recency_score = max(0.0, 1.0 - days_old / 365.0)
            except:
                recency_score = 0.0
            
            results.append((capsule, recency_score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def _rank_by_popularity(
        self,
        capsules: List[Dict[str, Any]]
    ) -> List[Tuple[Dict[str, Any], float]]:
        """按流行度排序"""
        results = []
        
        for capsule in capsules:
            metrics = capsule.get("metrics", {})
            reuse_count = metrics.get("reuse_count", 0)
            
            # 流行度分数 = log(reuse_count + 1)
            popularity_score = math.log(reuse_count + 1) / 10.0  # 归一化到 0-1
            
            results.append((capsule, popularity_score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def _rank_hybrid(
        self,
        capsules: List[Dict[str, Any]],
        query: Optional[str]
    ) -> List[Tuple[Dict[str, Any], float]]:
        """混合排序"""
        # 获取各维度分数
        relevance_scores = dict(self._rank_by_relevance(capsules, query))
        quality_scores = dict(self._rank_by_quality(capsules))
        recency_scores = dict(self._rank_by_recency(capsules))
        popularity_scores = dict(self._rank_by_popularity(capsules))
        
        # 计算加权分数
        results = []
        for capsule in capsules:
            capsule_id = capsule.get("id", "")
            
            hybrid_score = (
                relevance_scores.get(capsule_id, 0.0) * self.weights["relevance"] +
                quality_scores.get(capsule_id, 0.0) * self.weights["quality"] +
                recency_scores.get(capsule_id, 0.0) * self.weights["recency"] +
                popularity_scores.get(capsule_id, 0.0) * self.weights["popularity"]
            )
            
            results.append((capsule, hybrid_score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results


class ExperienceRetriever:
    """
    经验检索器 - 主类
    
    整合搜索和排序功能
    """
    
    def __init__(
        self,
        capsules: List[Dict[str, Any]],
        ranker_weights: Optional[Dict[str, float]] = None
    ):
        """
        初始化检索器
        
        Args:
            capsules: Capsule 字典列表
            ranker_weights: 排序权重配置
        """
        self.searcher = CapsuleSearcher(capsules)
        self.ranker = CapsuleRanker(weights=ranker_weights)
        self.capsules = capsules
    
    def retrieve(
        self,
        query: str,
        top_k: int = 10,
        search_strategy: str = "hybrid",
        rank_strategy: str = "hybrid"
    ) -> List[SearchResult]:
        """
        检索经验
        
        Args:
            query: 查询字符串
            top_k: 返回结果数量
            search_strategy: 搜索策略
            rank_strategy: 排序策略
        
        Returns:
            List[SearchResult]: 搜索结果
        """
        # 搜索
        search_results = self.searcher.search(
            query=query,
            strategy=search_strategy,
            top_k=top_k * 2  # 多取一些用于排序
        )
        
        # 获取对应的 Capsule
        capsule_ids = [r.capsule_id for r in search_results]
        capsules = [
            c for c in self.capsules
            if c.get("id") in capsule_ids
        ]
        
        # 排序
        ranked = self.ranker.rank(
            capsules=capsules,
            query=query,
            strategy=rank_strategy
        )
        
        # 更新搜索结果的分数和排名
        final_results = []
        for i, (capsule, score) in enumerate(ranked[:top_k]):
            capsule_id = capsule.get("id")
            
            # 找到对应的搜索结果
            for result in search_results:
                if result.capsule_id == capsule_id:
                    result.score = score
                    result.rank = i + 1
                    result.metadata["capsule"] = capsule
                    final_results.append(result)
                    break
        
        return final_results
    
    def retrieve_by_id(self, capsule_id: str) -> Optional[Dict[str, Any]]:
        """按 ID 检索"""
        return self.searcher.search_by_id(capsule_id)
    
    def retrieve_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """按标签检索"""
        return self.searcher.search_by_tag(tag)
    
    def retrieve_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        """按领域检索"""
        return self.searcher.search_by_domain(domain)
    
    def load_capsules_from_file(self, file_path: str):
        """从文件加载 Capsule"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        capsules = data.get("capsules", [])
        self.capsules = capsules
        self.searcher = CapsuleSearcher(capsules)


# ============== 使用示例 ==============

if __name__ == "__main__":
    # 示例 Capsule
    sample_capsules = [
        {
            "id": "capsule_001",
            "name": "Pattern-parameterized-3steps",
            "description": "API 调用 + 分析 + 返回",
            "pattern": ["CALL_API", "ANALYZE", "RETURN"],
            "tags": ["api", "analysis"],
            "applicability": {"domains": ["general"]},
            "metrics": {"success_rate": 0.95, "reuse_count": 10},
            "confidence": 0.9,
            "created_at": "2026-03-20T10:00:00"
        },
        {
            "id": "capsule_002",
            "name": "Pattern-concrete-2steps",
            "description": "搜索 + 总结",
            "pattern": ["SEARCH_WEB", "ANALYZE"],
            "tags": ["search", "summary"],
            "applicability": {"domains": ["research"]},
            "metrics": {"success_rate": 0.85, "reuse_count": 5},
            "confidence": 0.8,
            "created_at": "2026-03-19T10:00:00"
        }
    ]
    
    # 创建检索器
    retriever = ExperienceRetriever(sample_capsules)
    
    # 搜索
    query = "API analysis"
    results = retriever.retrieve(query, top_k=5)
    
    print(f"搜索查询：{query}")
    print(f"找到 {len(results)} 个结果\n")
    
    for result in results:
        print(f"排名：{result.rank}")
        print(f"ID: {result.capsule_id}")
        print(f"名称：{result.capsule_name}")
        print(f"分数：{result.score:.3f}")
        print(f"元数据：{result.metadata}")
        print("-" * 50)
