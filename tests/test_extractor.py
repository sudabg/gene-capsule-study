"""
经验抽取器集成测试 - 简化版

版本：v4.0
日期：2026-03-21
"""

import unittest
import json
import tempfile
import os
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from extractor import ExperienceExtractor, GeneCapsule


class TestExperienceExtractor(unittest.TestCase):
    """集成测试 - 测试端到端功能"""
    
    def setUp(self):
        """准备测试数据"""
        self.extractor = ExperienceExtractor()
        self.trajectories = [
            {
                "trajectory_id": "traj_001",
                "steps": [
                    {"action": "call_api", "tool": "api1", "output": {}, "success": True},
                    {"action": "analyze", "tool": "processor", "output": {}, "success": True},
                    {"action": "return", "output": {}, "success": True}
                ],
                "success": True,
                "total_time": 5.0
            },
            {
                "trajectory_id": "traj_002",
                "steps": [
                    {"action": "call_api", "tool": "api2", "output": {}, "success": True},
                    {"action": "analyze", "tool": "processor", "output": {}, "success": True},
                    {"action": "return", "output": {}, "success": True}
                ],
                "success": True,
                "total_time": 3.5
            }
        ]
    
    def test_extract_basic(self):
        """测试基本抽取功能"""
        capsules = self.extractor.extract(self.trajectories)
        
        # 应该抽取到 Capsule
        self.assertGreater(len(capsules), 0)
        
        # 验证 Capsule 结构
        capsule = capsules[0]
        self.assertIsInstance(capsule, GeneCapsule)
        self.assertIsNotNone(capsule.id)
        self.assertIsNotNone(capsule.pattern)
        self.assertIn("metrics", capsule.to_dict())
        self.assertIn("confidence", capsule.to_dict())
    
    def test_extract_multiple(self):
        """测试多轨迹抽取"""
        # 添加更多轨迹
        for i in range(8):
            self.trajectories.append({
                "trajectory_id": f"traj_{i:03d}",
                "steps": [
                    {"action": "call_api", "output": {}, "success": True},
                    {"action": "analyze", "output": {}, "success": True},
                    {"action": "return", "output": {}, "success": True}
                ],
                "success": True,
                "total_time": 4.0
            })
        
        capsules = self.extractor.extract(self.trajectories)
        
        # 应该有多个 Capsule
        self.assertGreater(len(capsules), 0)
    
    def test_search(self):
        """测试搜索功能"""
        capsules = self.extractor.extract(self.trajectories)
        
        # 搜索
        results = self.extractor.search("api", capsules=capsules)
        
        # 应该有结果
        self.assertGreater(len(results), 0)
        
        # 验证返回类型
        self.assertIsInstance(results[0], GeneCapsule)
    
    def test_save_load(self):
        """测试保存/加载功能"""
        capsules = self.extractor.extract(self.trajectories)
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            # 保存
            self.extractor.save(capsules, temp_path)
            
            # 验证文件存在
            self.assertTrue(os.path.exists(temp_path))
            
            # 加载
            loaded = self.extractor.load(temp_path)
            
            # 验证加载成功
            self.assertEqual(len(loaded), len(capsules))
            
            # 验证内容
            with open(temp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.assertIn("capsules", data)
            self.assertIn("count", data)
            self.assertIn("generated_at", data)
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_end_to_end(self):
        """测试端到端流程"""
        # 1. 抽取
        capsules = self.extractor.extract(self.trajectories)
        self.assertGreater(len(capsules), 0)
        
        # 2. 搜索
        results = self.extractor.search("api", capsules=capsules)
        self.assertGreater(len(results), 0)
        
        # 3. 保存
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            self.extractor.save(capsules, temp_path)
            
            # 4. 加载
            loaded = self.extractor.load(temp_path)
            self.assertEqual(len(loaded), len(capsules))
            
            # 5. 验证数据完整性
            for original, loaded_capsule in zip(capsules, loaded):
                self.assertEqual(original.id, loaded_capsule.id)
                self.assertEqual(original.pattern, loaded_capsule.pattern)
                self.assertEqual(original.confidence, loaded_capsule.confidence)
        
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestExperienceExtractor)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
