# SIMD编程示例

这个项目包含了一系列SIMD（单指令多数据）编程示例，展示如何利用现代处理器的向量指令集进行并行计算。

## 功能特点

- 展示多种SIMD指令集的使用（SSE, AVX, NEON等）
- 提供常见算法的SIMD实现
- 比较标量和向量实现的性能差异
- 包含跨平台的SIMD抽象库
- 提供详细的代码注释和教程

## 文件说明

- `basic_examples/`: 基础SIMD操作示例
- `algorithms/`: 常见算法的SIMD实现
- `benchmarks/`: 性能测试和比较
- `utils/`: 辅助函数和跨平台抽象
- `tutorials/`: 详细的SIMD编程教程
- `platform_specific/`: 特定平台的优化示例

## 环境要求

- 支持SSE/AVX的x86/x64处理器或支持NEON的ARM处理器
- C/C++编译器（GCC 7+, Clang 6+, MSVC 2017+）
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
# 运行基础示例
./basic_examples/vector_addition

# 运行算法示例
./algorithms/simd_sort

# 运行基准测试
./benchmarks/benchmark_suite
```

## SIMD指令集介绍

### x86/x64平台

- **SSE (Streaming SIMD Extensions)**
  - 128位寄存器（XMM0-XMM15）
  - 支持4个单精度浮点数或2个双精度浮点数
  - 主要指令前缀：`_mm_`

- **AVX (Advanced Vector Extensions)**
  - 256位寄存器（YMM0-YMM15）
  - 支持8个单精度浮点数或4个双精度浮点数
  - 主要指令前缀：`_mm256_`

- **AVX-512**
  - 512位寄存器（ZMM0-ZMM31）
  - 支持16个单精度浮点数或8个双精度浮点数
  - 主要指令前缀：`_mm512_`

### ARM平台

- **NEON**
  - 128位寄存器（Q0-Q15）
  - 支持4个单精度浮点数或2个双精度浮点数
  - 主要指令前缀：`vld1q_`, `vaddq_`等

## 示例内容

### 基础操作

- 向量加载和存储
- 算术运算（加、减、乘、除）
- 逻辑运算（与、或、异或）
- 比较和选择
- 打包和解包
- 洗牌和排列

### 算法实现

- 向量点积和叉积
- 矩阵乘法
- 图像处理（滤波、边缘检测）
- 排序算法
- 字符串处理
- 数学函数（sin, cos, exp等）

### 高级技术

- 掩码操作
- 数据依赖处理
- 内存对齐
- 分支消除
- 指令级并行优化

## 性能优化技巧

1. **内存对齐**：确保数据按照SIMD寄存器宽度对齐
2. **循环展开**：减少循环开销，增加指令级并行
3. **预取**：使用预取指令减少内存延迟
4. **混合精度**：在允许的情况下使用较低精度提高吞吐量
5. **避免分支**：使用掩码和选择指令代替条件分支

## 学习路径

1. 从基础示例开始，了解SIMD指令的基本用法
2. 学习如何将标量算法转换为SIMD实现
3. 研究性能优化技巧和最佳实践
4. 尝试实现自己的SIMD算法
5. 使用基准测试评估性能提升

## 参考资源

- [Intel Intrinsics Guide](https://software.intel.com/sites/landingpage/IntrinsicsGuide/)
- [ARM NEON Intrinsics Reference](https://developer.arm.com/architectures/instruction-sets/simd-isas/neon/intrinsics)
- [SIMD at Insomniac Games](https://deplinenoise.files.wordpress.com/2015/03/gdc2015_afredriksson_simd.pdf)
- [SIMD for C++ Developers](https://www.apress.com/gp/book/9781484255582)

## 贡献

欢迎提交问题和改进建议！如果你有新的SIMD示例或优化技巧，请提交PR。

## 许可证

MIT 