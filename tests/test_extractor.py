"""
经验抽取器单元测试

版本：v1.0
日期：2026-03-20
"""

import unittest
import json
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from extraction.extractor_v3 import (
    TrajectoryParser,
    PatternExtractor,
    Generalizer,
    CapsuleBuilder,
    ExperienceExtractor,
    TrajectoryStep,
    Trajectory,
    GeneCapsule
)


class TestTrajectoryParser(unittest.TestCase):
    """测试轨迹解析器"""
    
    def setUp(self):
        self.parser = TrajectoryParser()
        self.sample_raw = {
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
    
    def test_parse(self):
        """测试解析功能"""
        trajectory = self.parser.parse(self.sample_raw)
        
        self.assertEqual(trajectory.trajectory_id, "traj_001")
        self.assertEqual(len(trajectory.steps), 2)
        self.assertEqual(trajectory.success, True)
        self.assertEqual(trajectory.total_time, 5.0)
    
    def test_clean(self):
        """测试清洗功能"""
        trajectory = self.parser.parse(self.sample_raw)
        
        # 添加一个无效步骤
        trajectory.steps.append(
            TrajectoryStep(
                step_id=3,
                action="invalid",
                tool="",
                parameters={},
                output=None,
                success=False
            )
        )
        
        cleaned = self.parser.clean(trajectory)
        
        # 无效步骤应该被移除
        self.assertEqual(len(cleaned.steps), 2)
    
    def test_normalize(self):
        """测试标准化功能"""
        trajectory = self.parser.parse(self.sample_raw)
        
        normalized = self.parser.normalize(trajectory)
        
        # 动作应该被标准化为大写
        self.assertEqual(normalized.steps[0].action, "CALL_API")
        self.assertEqual(normalized.steps[1].action, "ANALYZE")


class TestPatternExtractor(unittest.TestCase):
    """测试模式抽取器"""
    
    def setUp(self):
        self.extractor = PatternExtractor(min_frequency=2)
        
        # 创建测试轨迹
        self.trajectories = [
            Trajectory(
                trajectory_id=f"traj_{i}",
                task_description="test",
                steps=[
                    TrajectoryStep(1, "CALL_API", "api1", {}, {"result": "ok"}, True),
                    TrajectoryStep(2, "ANALYZE", "processor", {}, {"result": "ok"}, True),
                    TrajectoryStep(3, "RETURN", "output", {}, {"result": "ok"}, True),
                ],
                success=True,
                total_time=5.0
            )
            for i in range(3)
        ]
    
    def test_extract_frequent_patterns(self):
        """测试频繁模式抽取"""
        patterns = self.extractor.extract_frequent_patterns(
            self.trajectories, 
            pattern_length=2
        )
        
        # 应该找到频繁模式
        self.assertGreater(len(patterns), 0)
        
        # 模式 ("CALL_API", "ANALYZE") 应该出现 3 次
        self.assertIn(("CALL_API", "ANALYZE"), patterns)
        self.assertEqual(patterns[("CALL_API", "ANALYZE")], 3)
    
    def test_extract_success_patterns(self):
        """测试成功/失败模式抽取"""
        pattern_stats = self.extractor.extract_success_patterns(self.trajectories)
        
        # 应该有统计信息
        self.assertGreater(len(pattern_stats), 0)
        
        # 所有轨迹都成功，所以 failure 应该是 0
        for pattern, stats in pattern_stats.items():
            self.assertEqual(stats["failure"], 0)
    
    def test_cluster_similar_patterns(self):
        """测试模式聚类"""
        patterns = {
            ("A", "B", "C"): 5,
            ("A", "B", "D"): 3,
            ("X", "Y", "Z"): 4,
        }
        
        clusters = self.extractor.cluster_similar_patterns(
            patterns, 
            similarity_threshold=0.7
        )
        
        # 至少应该有 1 个簇
        self.assertGreater(len(clusters), 0)


class TestGeneralizer(unittest.TestCase):
    """测试泛化器"""
    
    def setUp(self):
        self.generalizer = Generalizer()
    
    def test_generalize_pattern(self):
        """测试模式泛化"""
        pattern_cluster = [
            ("CALL_API", "ANALYZE", "RETURN"),
            ("CALL_API", "ANALYZE", "OUTPUT"),
            ("CALL_API", "ANALYZE", "SAVE"),
        ]
        
        result = self.generalizer.generalize_pattern(pattern_cluster)
        
        # 应该找到共同部分
        self.assertEqual(result["pattern"], ["CALL_API", "ANALYZE"])
        
        # 应该有变量
        self.assertIn("variables", result)
        
        # 抽象层次应该是 concrete/parameterized/template 之一
        self.assertIn(result["abstraction_level"], ["concrete", "parameterized", "template"])
    
    def test_find_common_subsequence(self):
        """测试共同子序列查找"""
        patterns = [
            ("A", "B", "C", "D"),
            ("A", "B", "X", "Y"),
            ("A", "B", "Z"),
        ]
        
        common = self.generalizer._find_common_subsequence(patterns)
        
        # 共同部分应该是 ["A", "B"]
        self.assertEqual(common, ["A", "B"])
    
    def test_infer_type(self):
        """测试类型推断"""
        # 字符串类型
        self.assertEqual(
            self.generalizer._infer_type({"hello", "world"}),
            "string"
        )
        
        # 数字类型
        self.assertEqual(
            self.generalizer._infer_type({1, 2, 3}),
            "number"
        )


class TestCapsuleBuilder(unittest.TestCase):
    """测试 Capsule 构建器"""
    
    def setUp(self):
        self.builder = CapsuleBuilder()
        
        self.generalized_pattern = {
            "pattern": ["CALL_API", "ANALYZE", "RETURN"],
            "variables": {"var_0": {"position": 2, "values": ["RETURN", "OUTPUT"]}},
            "abstraction_level": "parameterized"
        }
        
        self.trajectories = [
            Trajectory(
                trajectory_id="traj_001",
                task_description="test task",
                steps=[
                    TrajectoryStep(1, "CALL_API", "api", {}, {}, True),
                    TrajectoryStep(2, "ANALYZE", "processor", {}, {}, True),
                    TrajectoryStep(3, "RETURN", "output", {}, {}, True),
                ],
                success=True,
                total_time=5.0
            )
        ]
    
    def test_build(self):
        """测试 Capsule 构建"""
        capsule = self.builder.build(
            self.generalized_pattern,
            self.trajectories
        )
        
        # 验证基本属性
        self.assertIsNotNone(capsule.id)
        self.assertIn("Pattern", capsule.name)
        self.assertEqual(len(capsule.pattern), 3)
        self.assertGreater(capsule.confidence, 0)
        
        # 验证指标
        self.assertEqual(capsule.metrics["success_rate"], 1.0)
        self.assertEqual(capsule.metrics["reuse_count"], 1)
    
    def test_generate_description(self):
        """测试描述生成"""
        desc = self.builder._generate_description(self.generalized_pattern)
        
        # 描述应该包含抽象层次和步骤数
        self.assertIn("parameterized", desc)
        self.assertIn("3", desc)
    
    def test_calculate_confidence(self):
        """测试置信度计算"""
        confidence = self.builder._calculate_confidence(self.trajectories)
        
        # 置信度应该在 0-1 之间
        self.assertGreater(confidence, 0)
        self.assertLessEqual(confidence, 1)


class TestExperienceExtractor(unittest.TestCase):
    """测试经验抽取器主类"""
    
    def setUp(self):
        self.extractor = ExperienceExtractor()
        
        self.sample_trajectories = [
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
                        "output": {"articles": ["article1"]},
                        "success": True
                    },
                    {
                        "step_id": 2,
                        "action": "analyze",
                        "tool": "summarizer",
                        "parameters": {"text": "{{output_1}}"},
                        "output": {"summary": "tech news"},
                        "success": True
                    }
                ],
                "success": True,
                "total_time": 3.5
            }
        ]
    
    def test_extract(self):
        """测试完整抽取流程"""
        capsules = self.extractor.extract(self.sample_trajectories, pattern_length=2)
        
        # 由于样本较少，可能抽取不到 Capsule，这是正常的
        # 主要验证不报错
        self.assertIsInstance(capsules, list)
        
        # 如果有 Capsule，验证结构
        if len(capsules) > 0:
            capsule = capsules[0]
            self.assertIsInstance(capsule, GeneCapsule)
            self.assertIsNotNone(capsule.id)
            self.assertIsNotNone(capsule.pattern)
    
    def test_save_and_load(self):
        """测试保存和加载"""
        import tempfile
        import os
        
        capsules = self.extractor.extract(self.sample_trajectories)
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            self.extractor.save_capsules(capsules, temp_path)
            
            # 验证文件存在
            self.assertTrue(os.path.exists(temp_path))
            
            # 验证内容
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.assertIn("capsules", data)
            self.assertEqual(len(data["capsules"]), len(capsules))
            self.assertIn("generated_at", data)
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestGeneCapsule(unittest.TestCase):
    """测试 GeneCapsule 数据类"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        capsule = GeneCapsule(
            id="test_001",
            name="Test Pattern",
            description="A test pattern",
            pattern=["A", "B", "C"],
            variables={},
            preconditions=[],
            postconditions=[],
            constraints=[],
            applicability={},
            metrics={"success_rate": 0.9}
        )
        
        result = capsule.to_dict()
        
        # 验证所有字段都存在
        self.assertEqual(result["id"], "test_001")
        self.assertEqual(result["name"], "Test Pattern")
        self.assertEqual(result["pattern"], ["A", "B", "C"])
        self.assertIn("created_at", result)
    
    def test_to_json(self):
        """测试转换为 JSON"""
        capsule = GeneCapsule(
            id="test_002",
            name="Test Pattern 2",
            description="Another test",
            pattern=["X", "Y"],
            variables={},
            preconditions=[],
            postconditions=[],
            constraints=[],
            applicability={},
            metrics={}
        )
        
        json_str = capsule.to_json()
        
        # 验证是有效的 JSON
        data = json.loads(json_str)
        self.assertEqual(data["id"], "test_002")
        
        # 验证中文支持
        self.assertIn("Another test", json_str)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestTrajectoryParser))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternExtractor))
    suite.addTests(loader.loadTestsFromTestCase(TestGeneralizer))
    suite.addTests(loader.loadTestsFromTestCase(TestCapsuleBuilder))
    suite.addTests(loader.loadTestsFromTestCase(TestExperienceExtractor))
    suite.addTests(loader.loadTestsFromTestCase(TestGeneCapsule))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回结果
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
