# CUDA基础编程示例

这个项目包含了一系列CUDA基础编程示例，帮助你学习GPU并行计算的基本概念和编程技巧。

## 功能特点

- 从简单到复杂的CUDA编程示例
- 详细的代码注释和执行原理解释
- 性能对比和优化技巧
- 包含常见CUDA编程模式
- 支持多种GPU架构

## 文件说明

- `01_hello_cuda/`: 第一个CUDA程序
- `02_vector_addition/`: 向量加法
- `03_matrix_multiplication/`: 矩阵乘法
- `04_shared_memory/`: 共享内存使用
- `05_memory_coalescing/`: 内存合并访问
- `06_reduction/`: 并行归约
- `07_scan/`: 前缀和
- `08_streams/`: CUDA流和异步执行
- `utils/`: 辅助函数和工具

## 环境要求

- NVIDIA GPU（计算能力3.0或更高）
- CUDA Toolkit 10.0或更高版本
- 支持CUDA的C/C++编译器
- CMake 3.10+
- Python 3.6+（用于性能分析脚本）

## 编译和运行

```bash
mkdir build && cd build
cmake ..
make
```

运行示例：

```bash
# 运行Hello CUDA示例
./01_hello_cuda/hello_cuda

# 运行向量加法示例
./02_vector_addition/vector_add

# 运行矩阵乘法示例
./03_matrix_multiplication/matrix_mul
```

## CUDA编程基础

### CUDA编程模型

CUDA（Compute Unified Device Architecture）是NVIDIA开发的并行计算平台和编程模型，它允许开发者利用NVIDIA GPU的强大计算能力进行通用计算。

CUDA编程模型基于以下概念：

- **主机(Host)和设备(Device)**：主机是CPU及其内存，设备是GPU及其内存
- **内核(Kernel)**：在GPU上并行执行的函数
- **线程层次结构**：线程(Thread)、线程块(Block)和网格(Grid)
- **内存层次结构**：全局内存、共享内存、常量内存、纹理内存和寄存器

### 线程组织

CUDA使用三级层次结构组织线程：

- **线程(Thread)**：最基本的执行单元
- **线程块(Block)**：一组线程，可以协作通过共享内存和同步操作
- **网格(Grid)**：一组线程块，构成完整的内核执行

### 内存层次结构

CUDA设备具有多种类型的内存：

- **全局内存(Global Memory)**：所有线程都可访问，但延迟较高
- **共享内存(Shared Memory)**：同一线程块内的线程共享，延迟低
- **常量内存(Constant Memory)**：只读，有缓存
- **纹理内存(Texture Memory)**：针对2D空间局部性优化的只读内存
- **寄存器(Registers)**：每个线程私有，速度最快
- **本地内存(Local Memory)**：每个线程私有，但实际位于全局内存

## 示例内容

### 基础示例

- **Hello CUDA**：CUDA环境检测和简单内核
- **向量加法**：基本的并行向量操作
- **矩阵乘法**：朴素实现和优化版本

### 内存管理

- **内存分配与传输**：cudaMalloc, cudaMemcpy等
- **统一内存**：使用cudaMallocManaged简化内存管理
- **零拷贝内存**：使用cudaHostAlloc实现主机和设备内存共享

### 性能优化

- **共享内存使用**：减少全局内存访问
- **内存访问合并**：优化全局内存访问模式
- **避免分支发散**：减少线程束内的分支差异
- **占用率优化**：平衡寄存器使用和活跃线程数

### 高级特性

- **CUDA流**：实现任务并行和重叠执行
- **动态并行**：从GPU内核启动新的内核
- **原子操作**：安全地更新共享数据
- **线程同步**：使用屏障和内存栅栏

## 性能分析

项目包含性能分析工具和脚本：

- 执行时间测量
- 内存带宽计算
- 计算吞吐量分析
- 与CPU实现的性能对比

## 常见问题和解决方案

- **内存管理错误**：使用cuda-memcheck检测
- **内核启动失败**：检查设备属性和错误代码
- **性能低于预期**：使用nvprof或Nsight分析瓶颈
- **结果不正确**：调试策略和验证方法

## 学习路径

1. 从基础示例开始，了解CUDA编程模型
2. 学习内存管理和数据传输
3. 研究性能优化技巧和最佳实践
4. 尝试实现自己的CUDA算法
5. 使用性能分析工具评估和优化

## 参考资源

- [CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html)
- [CUDA C++ Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)
- [Programming Massively Parallel Processors](https://www.elsevier.com/books/programming-massively-parallel-processors/hwu/978-0-12-811986-0)
- [CUDA by Example](https://developer.nvidia.com/cuda-example)

## 贡献

欢迎提交问题和改进建议！如果你有新的CUDA示例或优化技巧，请提交PR。

## 许可证

MIT 