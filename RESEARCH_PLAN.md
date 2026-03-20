# 🔬 Gene-Capsule Study 研究计划

**启动时间**: 2026-03-20 18:05  
**状态**: 🟢 运行中  
**研究员**: auto-researcher (长时间运行)

---

## 📋 任务目标

实现从 Agent 执行轨迹中自动抽取可复用经验模式的完整系统

---

## 🎯 研究方向

1. **经验抽取算法** - 从轨迹中识别可复用模式
2. **评估框架** - 质量/复用性/稳定性指标
3. **检索排序** - 提升经验复用率

---

## 📅 执行计划

### Phase 1: 文献调研 (2-3 小时) 🟡 进行中

- [ ] 搜索 ACL/EMNLP/ICLR/NeurIPS 相关论文
- [ ] 调研 Case-Based Reasoning 方法
- [ ] 调研 Program Synthesis 技术
- [ ] 调研 Agent Trajectory Analysis 方法
- [ ] 输出文献综述更新版

**输出**: `paper/literature-review-v2.md`

### Phase 2: 算法设计 (2-3 小时) ⚪ 未开始

- [ ] 设计轨迹预处理流程
- [ ] 设计模式识别算法
- [ ] 设计抽象泛化机制
- [ ] 设计边界条件定义
- [ ] 输出算法设计文档

**输出**: `docs/algorithm-design.md`

### Phase 3: 代码实现 (3-4 小时) ⚪ 未开始

- [ ] 实现 TrajectoryParser
- [ ] 实现 PatternExtractor
- [ ] 实现 Generalizer
- [ ] 实现 CapsuleBuilder
- [ ] 编写单元测试
- [ ] 输出可运行代码

**输出**: `src/extraction/` 完整实现

### Phase 4: 实验验证 (2-3 小时) ⚪ 未开始

- [ ] 准备测试数据集
- [ ] 运行抽取实验
- [ ] 计算评估指标
- [ ] 分析实验结果
- [ ] 输出实验报告

**输出**: `experiments/results/` + `docs/experiment-report.md`

### Phase 5: 文档完善 (1-2 小时) ⚪ 未开始

- [ ] 更新 README.md
- [ ] 编写 API 文档
- [ ] 撰写技术报告
- [ ] 准备演示材料
- [ ] 提交 GitHub 仓库

**输出**: 完整的 GitHub 仓库

---

## 📊 预期输出

| 类型 | 内容 | 位置 |
|------|------|------|
| **代码** | 完整可运行的经验抽取系统 | `src/extraction/` |
| **文档** | 文献综述 + 算法设计 + 实验报告 | `paper/` + `docs/` |
| **数据** | 测试数据集 + 实验结果 | `data/` + `experiments/` |
| **演示** | 端到端使用示例 | `examples/` |

---

## ⚙️ 配置

- **代理**: `http://127.0.0.1:12334`
- **仓库**: https://github.com/sudabg/gene-capsule-study
- **运行模式**: 长时间运行，直到完成所有阶段
- **进度更新**: 每完成一个阶段自动汇报

---

## 📬 状态检查

查看当前进度：
```bash
cd /home/admin/openclaw/workspace/gene-capsule-study
cat RESEARCH_PLAN.md
```

查看子代理状态：
```bash
openclaw subagents list
```

---

*最后更新：2026-03-20 18:05*  
*预计完成：2026-03-20 23:00 (约 5 小时)*
