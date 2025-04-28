"""
CPU状态可视化模块
这个模块提供了CPU内部状态的可视化功能
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

class CPUVisualizer:
    """CPU状态可视化类"""
    
    def __init__(self, cpu, memory, register_file):
        """
        初始化可视化器
        
        参数:
            cpu: CPU对象
            memory: Memory对象
            register_file: RegisterFile对象
        """
        self.cpu = cpu
        self.memory = memory
        self.register_file = register_file
        
        # 创建自定义颜色映射
        self.cmap = LinearSegmentedColormap.from_list(
            'custom_cmap', ['#f0f0f0', '#4a86e8'], N=256)
    
    def visualize_registers(self):
        """可视化寄存器状态"""
        # 获取寄存器值
        reg_values = [self.register_file.read_register(i) for i in range(len(self.register_file.registers))]
        
        # 创建图形
        plt.figure(figsize=(10, 6))
        
        # 绘制寄存器条形图
        bars = plt.bar(range(len(reg_values)), reg_values, color='#4a86e8')
        
        # 添加寄存器值标签
        for i, v in enumerate(reg_values):
            plt.text(i, v + 5, str(v), ha='center')
        
        # 设置坐标轴
        plt.xlabel('寄存器编号')
        plt.ylabel('值')
        plt.title('寄存器状态')
        plt.xticks(range(len(reg_values)), [f'R{i}' for i in range(len(reg_values))])
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # 显示PC值
        pc = self.register_file.read_pc()
        plt.figtext(0.02, 0.02, f'PC: {pc}', fontsize=12)
        
        # 显示标志位
        flags_text = 'Flags: '
        for flag, value in self.register_file.sr.items():
            if value:
                flags_text += flag
            else:
                flags_text += '-'
        plt.figtext(0.5, 0.02, flags_text, fontsize=12, ha='center')
        
        plt.tight_layout()
        plt.show()
    
    def visualize_memory(self, start_address=0, size=64):
        """
        可视化内存内容
        
        参数:
            start_address: 起始地址
            size: 要显示的内存大小（字节）
        """
        # 获取内存内容
        memory_data = []
        for i in range(0, size, 4):
            address = start_address + i
            if address < self.memory.size:
                value = self.memory.read(address)
                memory_data.append(value)
        
        # 将内存数据转换为2D网格
        grid_size = int(np.sqrt(len(memory_data)) + 0.5)
        memory_grid = np.zeros((grid_size, grid_size))
        
        for i, value in enumerate(memory_data):
            if i < grid_size * grid_size:
                row = i // grid_size
                col = i % grid_size
                # 将值归一化到0-1范围
                memory_grid[row, col] = min(1.0, value / 255)
        
        # 创建图形
        plt.figure(figsize=(8, 8))
        
        # 绘制内存热图
        plt.imshow(memory_grid, cmap=self.cmap, interpolation='nearest')
        
        # 添加颜色条
        plt.colorbar(label='值（归一化）')
        
        # 设置坐标轴
        plt.xlabel('列索引')
        plt.ylabel('行索引')
        plt.title(f'内存内容 (地址 0x{start_address:X} - 0x{start_address + size:X})')
        
        # 添加网格
        plt.grid(False)
        
        # 添加地址标签
        for i in range(grid_size):
            for j in range(grid_size):
                idx = i * grid_size + j
                if idx < len(memory_data):
                    address = start_address + idx * 4
                    plt.text(j, i, f'{address:X}', ha='center', va='center', 
                             color='black' if memory_grid[i, j] < 0.5 else 'white',
                             fontsize=8)
        
        plt.tight_layout()
        plt.show()
    
    def visualize_instruction_execution(self, instructions_history):
        """
        可视化指令执行历史
        
        参数:
            instructions_history: 执行过的指令列表
        """
        if not instructions_history:
            print("没有指令执行历史")
            return
        
        # 统计各类指令的数量
        instruction_types = {}
        for instr in instructions_history:
            instr_type = instr.type.name
            if instr_type in instruction_types:
                instruction_types[instr_type] += 1
            else:
                instruction_types[instr_type] = 1
        
        # 创建图形
        plt.figure(figsize=(10, 6))
        
        # 绘制饼图
        plt.pie(instruction_types.values(), labels=instruction_types.keys(), 
                autopct='%1.1f%%', startangle=90, shadow=True)
        plt.axis('equal')  # 保持饼图为圆形
        plt.title('指令类型分布')
        
        plt.tight_layout()
        plt.show()
    
    def visualize_cpu_state(self, instructions_history=None):
        """
        综合可视化CPU状态
        
        参数:
            instructions_history: 执行过的指令列表
        """
        # 创建图形
        plt.figure(figsize=(15, 10))
        
        # 设置子图
        plt.subplot(2, 2, 1)
        self._plot_registers_state()
        
        plt.subplot(2, 2, 2)
        self._plot_memory_state()
        
        plt.subplot(2, 2, 3)
        self._plot_flags_state()
        
        if instructions_history:
            plt.subplot(2, 2, 4)
            self._plot_instruction_history(instructions_history)
        
        plt.tight_layout()
        plt.show()
    
    def _plot_registers_state(self):
        """绘制寄存器状态子图"""
        # 获取寄存器值
        reg_values = [self.register_file.read_register(i) for i in range(len(self.register_file.registers))]
        
        # 绘制寄存器条形图
        bars = plt.bar(range(len(reg_values)), reg_values, color='#4a86e8')
        
        # 设置坐标轴
        plt.xlabel('寄存器编号')
        plt.ylabel('值')
        plt.title('寄存器状态')
        plt.xticks(range(len(reg_values)), [f'R{i}' for i in range(len(reg_values))])
        plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    def _plot_memory_state(self):
        """绘制内存状态子图"""
        # 获取PC附近的内存内容
        pc = self.register_file.read_pc()
        start_address = max(0, pc - 16)
        memory_data = []
        
        for i in range(0, 32, 4):
            address = start_address + i
            if address < self.memory.size:
                value = self.memory.read(address)
                memory_data.append(value)
        
        # 绘制内存条形图
        bars = plt.bar(range(len(memory_data)), memory_data, color='#db4437')
        
        # 标记PC位置
        pc_idx = (pc - start_address) // 4
        if 0 <= pc_idx < len(memory_data):
            bars[pc_idx].set_color('#0f9d58')
        
        # 设置坐标轴
        plt.xlabel('内存地址')
        plt.ylabel('值')
        plt.title('内存状态 (PC附近)')
        plt.xticks(range(len(memory_data)), [f'0x{start_address + i * 4:X}' for i in range(len(memory_data))], 
                  rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    def _plot_flags_state(self):
        """绘制标志位状态子图"""
        # 获取标志位值
        flags = list(self.register_file.sr.keys())
        values = [int(self.register_file.sr[flag]) for flag in flags]
        
        # 绘制标志位条形图
        bars = plt.bar(range(len(flags)), values, color=['#4a86e8' if v else '#f0f0f0' for v in values])
        
        # 设置坐标轴
        plt.xlabel('标志位')
        plt.ylabel('状态')
        plt.title('标志位状态')
        plt.xticks(range(len(flags)), flags)
        plt.yticks([0, 1], ['未设置', '已设置'])
        plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    def _plot_instruction_history(self, instructions_history):
        """绘制指令执行历史子图"""
        # 统计最近的指令类型
        recent_history = instructions_history[-10:] if len(instructions_history) > 10 else instructions_history
        
        # 创建指令类型列表
        instr_types = [instr.type.name for instr in recent_history]
        
        # 绘制指令历史条形图
        y_pos = np.arange(len(instr_types))
        plt.barh(y_pos, [1] * len(instr_types), color='#f4b400')
        
        # 设置坐标轴
        plt.xlabel('执行顺序')
        plt.title('最近执行的指令')
        plt.yticks(y_pos, [f'{i}: {t}' for i, t in enumerate(instr_types)])
        plt.gca().invert_yaxis()  # 最新的指令在顶部 