# CPU模拟器

这个简单的CPU模拟器展示了基本的CPU工作原理，包括指令获取、解码和执行的过程。

## 功能特点

- 模拟基本的CPU指令周期（取指令、解码、执行、写回）
- 支持基本的指令集（算术、逻辑、跳转、内存访问）
- 可视化CPU内部状态（寄存器、内存、程序计数器等）
- 支持单步执行和连续执行
- 提供简单的调试功能

## 文件说明

- `cpu.py`: CPU核心实现
- `memory.py`: 内存模块实现
- `instruction.py`: 指令定义和解码
- `register.py`: 寄存器文件实现
- `simulator.py`: 模拟器主程序
- `visualizer.py`: 状态可视化模块
- `examples/`: 示例程序

## 使用方法

1. 运行模拟器：

```bash
python simulator.py [程序文件]
```

2. 交互式命令：

- `step`: 单步执行
- `run`: 连续执行
- `reg`: 显示寄存器状态
- `mem <地址> <数量>`: 显示内存内容
- `break <地址>`: 设置断点
- `help`: 显示帮助信息
- `quit`: 退出模拟器

## 示例程序

### 简单加法

```
# 简单的加法程序
LOAD R1, 10    # 将值10加载到寄存器R1
LOAD R2, 20    # 将值20加载到寄存器R2
ADD R3, R1, R2 # R3 = R1 + R2
STORE R3, 100  # 将R3的值存储到内存地址100
HALT           # 停止执行
```

运行示例：

```bash
python simulator.py examples/simple_add.asm
```

### 循环计算

```
# 循环程序 - 计算1到10的和
LOAD R1, 1     # 初始化计数器
LOAD R2, 10    # 设置上限
LOAD R3, 0     # 初始化累加器
ADD R3, R3, R1 # 累加当前值
ADD R1, R1, 1  # 计数器加1
JUMP_GT R1, R2, 36  # 如果计数器>上限，跳转到结束
JUMP 12        # 跳回循环开始
STORE R3, 100  # 存储结果
HALT           # 停止执行
```

运行示例：

```bash
python simulator.py examples/loop.asm
```

### 阶乘计算

```
# 阶乘计算程序 - 计算5!
LOAD R1, 5     # 初始化要计算阶乘的数
LOAD R2, 1     # 初始化结果
LOAD R3, 0     # 用于比较的0
JUMP_EQ R1, R3, 28  # 如果R1=0，跳转到结束
MUL R2, R2, R1 # 结果乘以当前数
SUB R1, R1, 1  # 计数器减1
JUMP 8         # 跳回循环开始
STORE R2, 100  # 存储结果
HALT           # 停止执行
```

运行示例：

```bash
python simulator.py examples/factorial.asm
```

## 可视化功能

模拟器提供了多种可视化功能，帮助理解CPU的工作原理：

- `vis_reg`: 可视化寄存器状态
- `vis_mem`: 可视化内存内容
- `vis_instr`: 可视化指令执行历史
- `vis_cpu`: 综合可视化CPU状态

## 学习要点

通过这个模拟器，你可以学习：

1. CPU的基本组成部分（ALU、寄存器、控制单元）
2. 指令周期的各个阶段
3. 指令如何被解码和执行
4. 寄存器和内存的交互方式
5. 程序计数器如何控制程序流程

## 扩展思路

1. 添加更多指令类型
2. 实现更复杂的寻址方式
3. 添加中断处理机制
4. 实现简单的缓存系统
5. 添加流水线功能 