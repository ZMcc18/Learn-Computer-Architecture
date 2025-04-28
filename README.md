# 计算机体系结构学习代码

这个项目包含了一系列用于学习计算机体系结构的代码示例，按照循序渐进的方式组织，帮助你从基础到高级逐步掌握计算机体系结构的核心概念。

## 项目结构

```
computetixi/
├── 01_基础组件/
│   ├── cpu_simulator/        # 简单CPU模拟器
│   ├── memory_hierarchy/     # 内存层次结构可视化
│   └── assembly_interpreter/ # 简单汇编解释器
├── 02_数据通路与控制/
│   ├── datapath_simulator/   # 数据通路模拟
│   ├── control_unit/         # 控制单元实现
│   └── instruction_cycle/    # 指令周期可视化
├── 03_高级处理器架构/
│   ├── pipeline_simulator/   # 流水线模拟器
│   ├── branch_prediction/    # 分支预测算法
│   └── multicore_scheduler/  # 多核调度模拟
├── 04_并行计算基础/
│   ├── simd_examples/        # SIMD编程示例
│   ├── multithreading/       # 多线程编程示例
│   └── performance_analysis/ # 性能分析工具
└── 05_GPU与CUDA编程/
    ├── cuda_basics/          # CUDA基础示例
    ├── image_processing/     # 图像处理示例
    └── deep_learning/        # 深度学习算子实现
```

## 环境要求

- Python 3.8+
- C/C++ 编译器 (GCC/G++ 9.0+ 或 MSVC 2019+)
- NVIDIA CUDA Toolkit 11.0+ (用于CUDA示例)
- 适用于CUDA的GPU (用于CUDA示例)

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

每个子目录都包含独立的示例，可以单独运行。详细的使用说明请参考各个子目录中的README文件。

### 示例：运行CPU模拟器

```bash
cd 01_基础组件/cpu_simulator
python cpu_simulator.py
```

## 学习路径

请参考 [计算机体系结构学习路径.md](计算机体系结构学习路径.md) 获取详细的学习计划和建议。

## 贡献

欢迎提交问题和改进建议！
