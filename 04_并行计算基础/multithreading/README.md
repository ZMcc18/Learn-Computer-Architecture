# 多线程编程示例

这个项目包含了一系列多线程编程示例，展示如何利用现代处理器的多核特性进行并行计算。

## 功能特点

- 展示多种线程库和并行编程模型
- 提供常见并行算法的实现
- 演示线程同步和通信机制
- 比较不同并行策略的性能
- 包含详细的代码注释和教程

## 文件说明

- `basic_examples/`: 基础多线程操作示例
- `algorithms/`: 常见算法的并行实现
- `synchronization/`: 线程同步机制示例
- `patterns/`: 并行设计模式实现
- `benchmarks/`: 性能测试和比较
- `tutorials/`: 详细的多线程编程教程

## 环境要求

- 支持多线程的现代处理器
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
./basic_examples/hello_threads

# 运行算法示例
./algorithms/parallel_sort

# 运行同步示例
./synchronization/producer_consumer

# 运行基准测试
./benchmarks/thread_scaling
```

## 多线程库和模型

### C++标准库

- **std::thread**
  - C++11引入的标准线程库
  - 跨平台，易于使用
  - 包含基本的同步原语（mutex, condition_variable等）

- **std::async 和 std::future**
  - 基于任务的并行模型
  - 自动管理线程生命周期
  - 支持返回值和异常传播

### POSIX线程（pthread）

- 跨平台的线程API标准
- 提供底层线程控制
- 丰富的同步原语

### OpenMP

- 基于指令的高级并行编程模型
- 简单的并行循环和任务并行
- 自动线程管理和负载均衡

### Intel TBB (Threading Building Blocks)

- 基于任务的并行库
- 高效的任务调度和负载均衡
- 丰富的并行算法和容器

## 示例内容

### 基础操作

- 线程创建和管理
- 参数传递和返回值
- 线程池实现
- 异步执行和future

### 同步机制

- 互斥锁（Mutex）
- 读写锁（Reader-Writer Lock）
- 条件变量（Condition Variable）
- 信号量（Semaphore）
- 屏障（Barrier）
- 原子操作（Atomic Operations）

### 并行模式

- 生产者-消费者模式
- 读者-写者模式
- 主从模式（Master-Worker）
- 管道模式（Pipeline）
- 分治模式（Divide and Conquer）
- 工作窃取（Work Stealing）

### 并行算法

- 并行排序
- 并行搜索
- 并行归约（Reduction）
- 并行前缀和（Prefix Sum）
- 并行图算法
- 并行矩阵运算

## 常见问题和解决方案

### 线程安全

- 竞态条件（Race Condition）
- 死锁（Deadlock）
- 活锁（Livelock）
- 饥饿（Starvation）

### 性能优化

- 负载均衡
- 缓存友好的数据布局
- 减少同步开销
- 避免伪共享（False Sharing）
- 细粒度锁定

## 学习路径

1. 从基础示例开始，了解线程创建和管理
2. 学习不同的同步机制及其适用场景
3. 研究并行设计模式和最佳实践
4. 尝试实现自己的并行算法
5. 使用基准测试评估性能和可扩展性

## 性能分析

项目包含多种性能分析工具和脚本：

- 线程扩展性测试
- 同步开销测量
- 缓存效应分析
- 负载均衡评估

## 参考资源

- [C++ Concurrency in Action](https://www.manning.com/books/c-plus-plus-concurrency-in-action-second-edition)
- [The Art of Multiprocessor Programming](https://www.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-415950-1)
- [Intel Threading Building Blocks Documentation](https://software.intel.com/content/www/us/en/develop/documentation/tbb-documentation/top.html)
- [OpenMP Specifications](https://www.openmp.org/specifications/)

## 贡献

欢迎提交问题和改进建议！如果你有新的多线程示例或优化技巧，请提交PR。

## 许可证

MIT 