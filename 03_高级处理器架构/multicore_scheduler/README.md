# 多核处理器任务调度模拟器

这个模拟器展示了多核处理器中的任务调度原理和各种调度算法的性能比较。

## 功能特点

- 模拟多核处理器的任务调度过程
- 实现多种调度算法和负载均衡策略
- 可视化任务执行和核心利用率
- 分析调度算法对性能和能耗的影响
- 支持异构多核架构模拟

## 文件说明

- `scheduler.py`: 调度器基类和各种实现
- `task.py`: 任务模型和工作负载生成
- `processor.py`: 处理器核心模型
- `simulator.py`: 模拟器主程序
- `visualizer.py`: 调度过程可视化
- `analysis.py`: 性能分析工具
- `workloads/`: 示例工作负载
- `configs/`: 处理器配置文件

## 使用方法

1. 运行模拟器：

```bash
python simulator.py [工作负载文件] [--cores 核心数] [--scheduler 调度器类型]
```

调度器类型选项：
- `round_robin`: 轮询调度
- `static`: 静态分配
- `dynamic`: 动态负载均衡
- `work_stealing`: 工作窃取
- `priority`: 优先级调度
- `heterogeneous`: 异构感知调度

2. 交互式命令：

- `step [n]`: 模拟n个时间片
- `run`: 模拟直到所有任务完成
- `stats`: 显示调度统计
- `cores`: 显示各核心状态
- `tasks`: 显示任务状态
- `visualize`: 可视化调度过程
- `help`: 显示帮助信息
- `quit`: 退出模拟器

## 调度算法

### 基本调度算法

- **轮询调度(Round Robin)**: 循环分配任务给各个核心
- **静态分配(Static Assignment)**: 预先将任务分配给固定核心
- **动态负载均衡(Dynamic Load Balancing)**: 根据核心负载动态分配任务
- **优先级调度(Priority Scheduling)**: 根据任务优先级分配资源

### 高级调度策略

- **工作窃取(Work Stealing)**: 空闲核心从忙碌核心"窃取"任务
- **亲和性调度(Affinity Scheduling)**: 考虑缓存亲和性的任务分配
- **能耗感知调度(Energy-Aware Scheduling)**: 优化能耗的任务分配
- **异构感知调度(Heterogeneous-Aware Scheduling)**: 针对异构核心的特殊调度

### 多级队列

- **全局队列(Global Queue)**: 所有核心共享一个任务队列
- **每核心队列(Per-Core Queue)**: 每个核心有自己的任务队列
- **多级反馈队列(Multilevel Feedback Queue)**: 根据任务特性动态调整优先级

## 处理器模型

模拟器支持多种处理器模型：

- **同构多核(Homogeneous Multicore)**: 所有核心具有相同性能
- **异构多核(Heterogeneous Multicore)**: 大小核架构，核心性能不同
- **NUMA架构(Non-Uniform Memory Access)**: 内存访问延迟不均匀
- **SMT处理器(Simultaneous Multithreading)**: 每个核心支持多线程

## 性能指标

模拟器提供以下性能指标：

- **吞吐量(Throughput)**: 单位时间内完成的任务数
- **平均周转时间(Average Turnaround Time)**: 任务从提交到完成的平均时间
- **平均响应时间(Average Response Time)**: 任务从提交到首次执行的平均时间
- **核心利用率(Core Utilization)**: 各核心的使用率
- **负载均衡度(Load Balance)**: 任务在各核心间的分布均匀性
- **能耗效率(Energy Efficiency)**: 完成任务所需的能量

## 学习要点

通过这个模拟器，你可以学习：

1. 多核处理器的基本架构和工作原理
2. 各种任务调度算法的优缺点
3. 负载均衡和工作窃取的实现方法
4. 调度决策对系统性能的影响
5. 异构多核架构的特殊调度考虑

## 扩展思路

1. 实现更复杂的任务依赖模型
2. 添加缓存和内存模拟
3. 实现动态电压频率调整(DVFS)
4. 添加实时调度算法
5. 集成机器学习优化的调度策略 