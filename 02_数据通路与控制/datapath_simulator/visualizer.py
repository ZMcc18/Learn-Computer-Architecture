"""
数据通路可视化模块
这个模块提供了CPU数据通路的可视化功能
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

class DatapathVisualizer:
    """数据通路可视化类"""
    
    def __init__(self, datapath):
        """
        初始化可视化器
        
        参数:
            datapath: Datapath对象
        """
        self.datapath = datapath
        
        # 创建自定义颜色映射
        self.cmap = LinearSegmentedColormap.from_list(
            'custom_cmap', ['#f0f0f0', '#4a86e8'], N=256)
        
        # 组件位置和大小
        self.components = {
            'PC': {'pos': (0.1, 0.7), 'width': 0.1, 'height': 0.1, 'color': '#4a86e8'},
            'IM': {'pos': (0.3, 0.7), 'width': 0.1, 'height': 0.1, 'color': '#db4437'},
            'IR': {'pos': (0.5, 0.7), 'width': 0.1, 'height': 0.1, 'color': '#0f9d58'},
            'RF': {'pos': (0.3, 0.5), 'width': 0.1, 'height': 0.1, 'color': '#f4b400'},
            'A': {'pos': (0.2, 0.3), 'width': 0.08, 'height': 0.08, 'color': '#0f9d58'},
            'B': {'pos': (0.4, 0.3), 'width': 0.08, 'height': 0.08, 'color': '#0f9d58'},
            'ALU': {'pos': (0.3, 0.15), 'width': 0.15, 'height': 0.1, 'color': '#4a86e8'},
            'ALU_OUT': {'pos': (0.5, 0.15), 'width': 0.08, 'height': 0.08, 'color': '#0f9d58'},
            'DM': {'pos': (0.7, 0.3), 'width': 0.1, 'height': 0.1, 'color': '#db4437'},
            'MDR': {'pos': (0.7, 0.15), 'width': 0.08, 'height': 0.08, 'color': '#0f9d58'},
            'MUX_ALU_A': {'pos': (0.15, 0.2), 'width': 0.05, 'height': 0.05, 'color': '#f4b400'},
            'MUX_ALU_B': {'pos': (0.45, 0.2), 'width': 0.05, 'height': 0.05, 'color': '#f4b400'},
            'MUX_REG_DST': {'pos': (0.2, 0.5), 'width': 0.05, 'height': 0.05, 'color': '#f4b400'},
            'MUX_MEM_TO_REG': {'pos': (0.6, 0.3), 'width': 0.05, 'height': 0.05, 'color': '#f4b400'},
            'MUX_PC_SRC': {'pos': (0.1, 0.6), 'width': 0.05, 'height': 0.05, 'color': '#f4b400'},
        }
        
        # 连接线
        self.connections = [
            # PC到IM
            {'start': 'PC', 'end': 'IM', 'start_pos': 'right', 'end_pos': 'left', 'color': 'black'},
            # IM到IR
            {'start': 'IM', 'end': 'IR', 'start_pos': 'right', 'end_pos': 'left', 'color': 'black'},
            # IR到RF
            {'start': 'IR', 'end': 'RF', 'start_pos': 'bottom', 'end_pos': 'top', 'color': 'black'},
            # RF到A和B
            {'start': 'RF', 'end': 'A', 'start_pos': 'bottom', 'end_pos': 'top', 'color': 'black'},
            {'start': 'RF', 'end': 'B', 'start_pos': 'bottom', 'end_pos': 'top', 'color': 'black'},
            # A和B到ALU
            {'start': 'A', 'end': 'MUX_ALU_A', 'start_pos': 'bottom', 'end_pos': 'top', 'color': 'black'},
            {'start': 'B', 'end': 'MUX_ALU_B', 'start_pos': 'bottom', 'end_pos': 'top', 'color': 'black'},
            {'start': 'MUX_ALU_A', 'end': 'ALU', 'start_pos': 'bottom', 'end_pos': 'left', 'color': 'black'},
            {'start': 'MUX_ALU_B', 'end': 'ALU', 'start_pos': 'bottom', 'end_pos': 'right', 'color': 'black'},
            # ALU到ALU_OUT
            {'start': 'ALU', 'end': 'ALU_OUT', 'start_pos': 'right', 'end_pos': 'left', 'color': 'black'},
            # ALU_OUT到DM
            {'start': 'ALU_OUT', 'end': 'DM', 'start_pos': 'top', 'end_pos': 'bottom', 'color': 'black'},
            # DM到MDR
            {'start': 'DM', 'end': 'MDR', 'start_pos': 'bottom', 'end_pos': 'top', 'color': 'black'},
            # MDR和ALU_OUT到MUX_MEM_TO_REG
            {'start': 'MDR', 'end': 'MUX_MEM_TO_REG', 'start_pos': 'left', 'end_pos': 'bottom', 'color': 'black'},
            {'start': 'ALU_OUT', 'end': 'MUX_MEM_TO_REG', 'start_pos': 'top', 'end_pos': 'right', 'color': 'black'},
            # MUX_MEM_TO_REG到RF
            {'start': 'MUX_MEM_TO_REG', 'end': 'RF', 'start_pos': 'top', 'end_pos': 'right', 'color': 'black'},
            # MUX_REG_DST到RF
            {'start': 'MUX_REG_DST', 'end': 'RF', 'start_pos': 'right', 'end_pos': 'left', 'color': 'black'},
            # IR到MUX_REG_DST
            {'start': 'IR', 'end': 'MUX_REG_DST', 'start_pos': 'left', 'end_pos': 'top', 'color': 'black'},
            # PC到MUX_ALU_A
            {'start': 'PC', 'end': 'MUX_ALU_A', 'start_pos': 'bottom', 'end_pos': 'left', 'color': 'black'},
            # ALU_OUT到MUX_PC_SRC
            {'start': 'ALU_OUT', 'end': 'MUX_PC_SRC', 'start_pos': 'left', 'end_pos': 'right', 'color': 'black'},
            # MUX_PC_SRC到PC
            {'start': 'MUX_PC_SRC', 'end': 'PC', 'start_pos': 'top', 'end_pos': 'bottom', 'color': 'black'},
        ]
    
    def _get_component_center(self, component_name, pos='center'):
        """
        获取组件的中心坐标
        
        参数:
            component_name: 组件名称
            pos: 位置（'center', 'left', 'right', 'top', 'bottom'）
            
        返回:
            (x, y) 坐标
        """
        component = self.components[component_name]
        x, y = component['pos']
        width, height = component['width'], component['height']
        
        if pos == 'center':
            return (x + width / 2, y + height / 2)
        elif pos == 'left':
            return (x, y + height / 2)
        elif pos == 'right':
            return (x + width, y + height / 2)
        elif pos == 'top':
            return (x + width / 2, y + height)
        elif pos == 'bottom':
            return (x + width / 2, y)
    
    def visualize_datapath(self, active_components=None, active_connections=None):
        """
        可视化数据通路
        
        参数:
            active_components: 活动组件列表
            active_connections: 活动连接列表
        """
        if active_components is None:
            active_components = []
        if active_connections is None:
            active_connections = []
        
        # 创建图形
        plt.figure(figsize=(12, 8))
        ax = plt.gca()
        
        # 绘制组件
        for name, component in self.components.items():
            x, y = component['pos']
            width, height = component['width'], component['height']
            
            # 确定颜色
            color = component['color']
            if name in active_components:
                # 活动组件使用更亮的颜色
                color = self._brighten_color(color)
            
            # 绘制矩形
            rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='black', facecolor=color)
            ax.add_patch(rect)
            
            # 添加标签
            plt.text(x + width / 2, y + height / 2, name, ha='center', va='center')
            
            # 如果是寄存器或内存，显示值
            if name == 'PC':
                value = self.datapath.pc.read()
                plt.text(x + width / 2, y - 0.02, f"0x{value:08X}", ha='center', va='top', fontsize=8)
            elif name == 'IR':
                value = self.datapath.ir.read()
                plt.text(x + width / 2, y - 0.02, f"0x{value:08X}", ha='center', va='top', fontsize=8)
            elif name == 'A':
                value = self.datapath.a.read()
                plt.text(x + width / 2, y - 0.02, f"0x{value:08X}", ha='center', va='top', fontsize=8)
            elif name == 'B':
                value = self.datapath.b.read()
                plt.text(x + width / 2, y - 0.02, f"0x{value:08X}", ha='center', va='top', fontsize=8)
            elif name == 'ALU_OUT':
                value = self.datapath.alu_out.read()
                plt.text(x + width / 2, y - 0.02, f"0x{value:08X}", ha='center', va='top', fontsize=8)
            elif name == 'MDR':
                value = self.datapath.mdr.read()
                plt.text(x + width / 2, y - 0.02, f"0x{value:08X}", ha='center', va='top', fontsize=8)
        
        # 绘制连接线
        for i, conn in enumerate(self.connections):
            start = conn['start']
            end = conn['end']
            start_pos = conn['start_pos']
            end_pos = conn['end_pos']
            
            # 获取起点和终点坐标
            start_x, start_y = self._get_component_center(start, start_pos)
            end_x, end_y = self._get_component_center(end, end_pos)
            
            # 确定颜色
            color = conn['color']
            if i in active_connections:
                # 活动连接使用更亮的颜色
                color = 'red'
            
            # 绘制箭头
            ax.annotate("", xy=(end_x, end_y), xytext=(start_x, start_y),
                       arrowprops=dict(arrowstyle="->", color=color))
        
        # 设置坐标轴
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.axis('off')
        
        # 添加标题
        plt.title("CPU数据通路")
        
        plt.tight_layout()
        plt.show()
    
    def visualize_control_signals(self, signals):
        """
        可视化控制信号
        
        参数:
            signals: ControlSignals对象
        """
        # 创建图形
        plt.figure(figsize=(10, 6))
        
        # 控制信号列表
        signal_names = [
            'pc_write', 'pc_source',
            'mem_read', 'mem_write',
            'reg_write', 'reg_dst',
            'alu_src_a', 'alu_src_b', 'alu_op',
            'mem_to_reg', 'ir_write'
        ]
        
        # 获取信号值
        signal_values = [
            signals.pc_write, signals.pc_source,
            signals.mem_read, signals.mem_write,
            signals.reg_write, signals.reg_dst,
            signals.alu_src_a, signals.alu_src_b, signals.alu_op,
            signals.mem_to_reg, signals.ir_write
        ]
        
        # 将布尔值转换为整数
        signal_values = [int(v) if isinstance(v, bool) else v for v in signal_values]
        
        # 创建条形图
        bars = plt.bar(signal_names, signal_values, color='#4a86e8')
        
        # 添加值标签
        for i, v in enumerate(signal_values):
            plt.text(i, v + 0.1, str(v), ha='center')
        
        # 设置坐标轴
        plt.xlabel('控制信号')
        plt.ylabel('值')
        plt.title('CPU控制信号')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.show()
    
    def visualize_register_file(self):
        """可视化寄存器文件"""
        # 获取寄存器值
        reg_values = [self.datapath.register_file.read(i) for i in range(32)]
        
        # 创建图形
        plt.figure(figsize=(12, 8))
        
        # 绘制寄存器条形图
        bars = plt.bar(range(32), reg_values, color='#4a86e8')
        
        # 添加寄存器值标签
        for i, v in enumerate(reg_values):
            if v != 0:  # 只显示非零值
                plt.text(i, v + 5, f"0x{v:X}", ha='center', rotation=90, fontsize=8)
        
        # 设置坐标轴
        plt.xlabel('寄存器编号')
        plt.ylabel('值')
        plt.title('寄存器文件状态')
        plt.xticks(range(32), [f'R{i}' for i in range(32)])
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.show()
    
    def visualize_memory(self, start_address=0, size=64):
        """
        可视化内存内容
        
        参数:
            start_address: 起始地址
            size: 要显示的内存大小（字）
        """
        # 获取内存内容
        memory_data = []
        for i in range(size):
            address = start_address + i * 4
            value = self.datapath.memory.read(address)
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
        plt.figure(figsize=(10, 8))
        
        # 绘制内存热图
        plt.imshow(memory_grid, cmap=self.cmap, interpolation='nearest')
        
        # 添加颜色条
        plt.colorbar(label='值（归一化）')
        
        # 设置坐标轴
        plt.xlabel('列索引')
        plt.ylabel('行索引')
        plt.title(f'内存内容 (地址 0x{start_address:X} - 0x{start_address + size * 4:X})')
        
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
    
    def visualize_instruction_execution(self, instruction, stage):
        """
        可视化指令执行过程
        
        参数:
            instruction: 当前执行的指令
            stage: 执行阶段（'FETCH', 'DECODE', 'EXECUTE', 'MEMORY', 'WRITEBACK'）
        """
        # 确定活动组件和连接
        active_components = []
        active_connections = []
        
        if stage == 'FETCH':
            active_components = ['PC', 'IM', 'IR']
            active_connections = [0, 1]  # PC到IM, IM到IR
        elif stage == 'DECODE':
            active_components = ['IR', 'RF', 'MUX_REG_DST']
            active_connections = [2, 16]  # IR到RF, IR到MUX_REG_DST
        elif stage == 'EXECUTE':
            active_components = ['A', 'B', 'ALU', 'MUX_ALU_A', 'MUX_ALU_B']
            active_connections = [3, 4, 5, 6, 7, 8]  # RF到A和B, A和B到MUX, MUX到ALU
        elif stage == 'MEMORY':
            active_components = ['ALU_OUT', 'DM', 'MDR']
            active_connections = [9, 10, 11]  # ALU到ALU_OUT, ALU_OUT到DM, DM到MDR
        elif stage == 'WRITEBACK':
            active_components = ['ALU_OUT', 'MDR', 'MUX_MEM_TO_REG', 'RF']
            active_connections = [12, 13, 14]  # MDR和ALU_OUT到MUX, MUX到RF
        
        # 可视化数据通路
        self.visualize_datapath(active_components, active_connections)
        
        # 显示指令信息
        print(f"当前指令: 0x{instruction:08X}")
        print(f"执行阶段: {stage}")
    
    def _brighten_color(self, hex_color):
        """
        使颜色更亮
        
        参数:
            hex_color: 十六进制颜色字符串
            
        返回:
            更亮的颜色
        """
        # 将十六进制颜色转换为RGB
        r = int(hex_color[1:3], 16) / 255.0
        g = int(hex_color[3:5], 16) / 255.0
        b = int(hex_color[5:7], 16) / 255.0
        
        # 使颜色更亮
        r = min(1.0, r * 1.5)
        g = min(1.0, g * 1.5)
        b = min(1.0, b * 1.5)
        
        # 转换回十六进制
        return f"#{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"


class MultiCycleVisualizer(DatapathVisualizer):
    """多周期CPU数据通路可视化类"""
    
    def __init__(self, datapath, control_unit):
        """
        初始化多周期可视化器
        
        参数:
            datapath: MultiCycleDatapath对象
            control_unit: MultiCycleControlUnit对象
        """
        super().__init__(datapath)
        self.control_unit = control_unit
    
    def visualize_state_machine(self):
        """可视化状态机"""
        # 创建图形
        plt.figure(figsize=(10, 8))
        
        # 状态列表
        states = ['FETCH', 'DECODE', 'EXECUTE', 'MEMORY', 'WRITEBACK']
        
        # 状态位置
        state_pos = {
            'FETCH': (0.5, 0.8),
            'DECODE': (0.2, 0.5),
            'EXECUTE': (0.5, 0.2),
            'MEMORY': (0.8, 0.5),
            'WRITEBACK': (0.5, 0.5)
        }
        
        # 状态转换
        transitions = [
            ('FETCH', 'DECODE'),
            ('DECODE', 'EXECUTE'),
            ('EXECUTE', 'MEMORY'),
            ('EXECUTE', 'WRITEBACK'),
            ('EXECUTE', 'FETCH'),
            ('MEMORY', 'WRITEBACK'),
            ('MEMORY', 'FETCH'),
            ('WRITEBACK', 'FETCH')
        ]
        
        # 绘制状态
        for state, pos in state_pos.items():
            x, y = pos
            
            # 确定颜色
            color = '#4a86e8'
            if state == str(self.control_unit.state.name):
                # 当前状态使用更亮的颜色
                color = '#f4b400'
            
            # 绘制圆形
            circle = plt.Circle(pos, 0.1, color=color)
            plt.gca().add_patch(circle)
            
            # 添加标签
            plt.text(x, y, state, ha='center', va='center')
        
        # 绘制转换
        for start, end in transitions:
            start_x, start_y = state_pos[start]
            end_x, end_y = state_pos[end]
            
            # 计算方向向量
            dx = end_x - start_x
            dy = end_y - start_y
            
            # 归一化
            length = np.sqrt(dx**2 + dy**2)
            if length > 0:
                dx /= length
                dy /= length
            
            # 调整起点和终点，使箭头不会从圆心开始或结束
            start_x += dx * 0.1
            start_y += dy * 0.1
            end_x -= dx * 0.1
            end_y -= dy * 0.1
            
            # 绘制箭头
            plt.arrow(start_x, start_y, end_x - start_x, end_y - start_y,
                     head_width=0.02, head_length=0.03, fc='black', ec='black')
        
        # 设置坐标轴
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.axis('off')
        
        # 添加标题
        plt.title("多周期CPU状态机")
        
        plt.tight_layout()
        plt.show()
    
    def visualize_cycle(self, cycle_count):
        """
        可视化特定周期的状态
        
        参数:
            cycle_count: 周期计数
        """
        # 获取当前状态
        state = self.control_unit.state.name
        
        # 可视化状态机
        self.visualize_state_machine()
        
        # 可视化数据通路
        self.visualize_instruction_execution(self.datapath.ir.read(), state)
        
        # 可视化控制信号
        self.visualize_control_signals(self.control_unit.signals)
        
        # 显示周期信息
        print(f"周期: {cycle_count}")
        print(f"状态: {state}")
    
    def visualize_full_execution(self, max_cycles=20):
        """
        可视化完整执行过程
        
        参数:
            max_cycles: 最大周期数
        """
        for i in range(max_cycles):
            # 执行一个周期
            state = self.control_unit.step()
            
            # 更新数据通路
            self.datapath.execute_cycle(state.name)
            
            # 可视化当前状态
            self.visualize_cycle(i + 1)
            
            # 如果是HALT指令且处于FETCH状态，结束执行
            if self.datapath.ir.read() >> 26 == 0x3F and state.name == 'FETCH':
                break
            
            # 等待用户输入继续
            input("按Enter继续...")
        
        print(f"执行完成，共执行 {self.datapath.get_cycle_count()} 个周期") 