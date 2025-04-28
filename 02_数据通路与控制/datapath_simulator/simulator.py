"""
数据通路模拟器主程序
这个模块提供了数据通路模拟器的主程序和命令行界面
"""

import os
import sys
import cmd
import argparse
import numpy as np

from datapath import Datapath, SingleCycleDatapath, MultiCycleDatapath
from control_signals import ControlUnit, MultiCycleControlUnit
from visualizer import DatapathVisualizer, MultiCycleVisualizer

class DatapathSimulator(cmd.Cmd):
    """数据通路模拟器命令行界面"""
    
    intro = """
    ===================================
    数据通路模拟器 v1.0
    输入 'help' 或 '?' 获取帮助
    输入 'quit' 或 'exit' 退出
    ===================================
    """
    prompt = 'Datapath> '
    
    def __init__(self, instruction_file=None, mode='single'):
        """
        初始化模拟器
        
        参数:
            instruction_file: 指令文件路径
            mode: 模拟器模式 ('single' 或 'multi')
        """
        super().__init__()
        
        self.mode = mode
        
        # 创建数据通路和控制单元
        if mode == 'single':
            self.datapath = SingleCycleDatapath()
            self.control_unit = ControlUnit()
            self.visualizer = DatapathVisualizer(self.datapath)
        else:  # 'multi'
            self.datapath = MultiCycleDatapath()
            self.control_unit = MultiCycleControlUnit()
            self.visualizer = MultiCycleVisualizer(self.datapath, self.control_unit)
        
        # 指令历史
        self.instruction_history = []
        
        # 加载指令
        if instruction_file:
            self.load_instructions(instruction_file)
    
    def load_instructions(self, instruction_file):
        """
        加载指令文件
        
        参数:
            instruction_file: 指令文件路径
        """
        try:
            instructions = []
            
            with open(instruction_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # 解析十六进制指令
                        if line.startswith('0x'):
                            instruction = int(line, 16)
                        else:
                            instruction = int(line, 16)
                        instructions.append(instruction)
            
            # 加载指令到数据通路
            self.datapath.load_program(instructions)
            
            print(f"成功加载 {len(instructions)} 条指令")
            
        except Exception as e:
            print(f"加载指令失败: {e}")
    
    def do_step(self, arg):
        """
        单步执行
        
        用法: step
        """
        if self.mode == 'single':
            # 单周期模式
            # 解码当前指令
            self.datapath.decode_instruction()
            
            # 生成控制信号
            self.control_unit.decode_instruction(self.datapath.ir.read())
            signals = self.control_unit.generate_control_signals()
            
            # 设置控制信号
            self.datapath.set_control_signals(signals)
            
            # 执行指令
            instruction = self.datapath.execute_instruction()
            
            # 添加到历史记录
            self.instruction_history.append(instruction)
            
            print(f"执行指令: 0x{instruction:08X}")
            
        else:  # 'multi'
            # 多周期模式
            # 执行一个时钟周期
            state = self.control_unit.step()
            
            # 更新数据通路
            operation = self.datapath.execute_cycle(state.name)
            
            print(f"执行周期: {state.name}")
            print(f"操作: {operation}")
    
    def do_run(self, arg):
        """
        连续执行
        
        用法: run [n]
        n: 执行的指令数/周期数（默认为10）
        """
        try:
            n = int(arg) if arg else 10
        except ValueError:
            print("参数必须是整数")
            return
        
        if self.mode == 'single':
            # 单周期模式
            for _ in range(n):
                # 解码当前指令
                self.datapath.decode_instruction()
                
                # 检查是否是HALT指令
                if (self.datapath.ir.read() >> 26) == 0x3F:
                    print("遇到HALT指令，停止执行")
                    break
                
                # 生成控制信号
                self.control_unit.decode_instruction(self.datapath.ir.read())
                signals = self.control_unit.generate_control_signals()
                
                # 设置控制信号
                self.datapath.set_control_signals(signals)
                
                # 执行指令
                instruction = self.datapath.execute_instruction()
                
                # 添加到历史记录
                self.instruction_history.append(instruction)
            
            print(f"执行了 {len(self.instruction_history)} 条指令")
            
        else:  # 'multi'
            # 多周期模式
            cycle_count = 0
            
            for _ in range(n):
                # 执行一个时钟周期
                state = self.control_unit.step()
                
                # 更新数据通路
                self.datapath.execute_cycle(state.name)
                
                cycle_count += 1
                
                # 如果是HALT指令且处于FETCH状态，结束执行
                if (self.datapath.ir.read() >> 26) == 0x3F and state.name == 'FETCH':
                    print("遇到HALT指令，停止执行")
                    break
            
            print(f"执行了 {cycle_count} 个周期")
    
    def do_show(self, arg):
        """
        显示当前数据通路状态
        
        用法: show
        """
        print(self.datapath)
    
    def do_signal(self, arg):
        """
        显示控制信号状态
        
        用法: signal
        """
        if self.mode == 'single':
            # 单周期模式
            self.control_unit.decode_instruction(self.datapath.ir.read())
            signals = self.control_unit.generate_control_signals()
        else:  # 'multi'
            # 多周期模式
            signals = self.control_unit.signals
        
        print(signals)
    
    def do_vis_datapath(self, arg):
        """
        可视化数据通路
        
        用法: vis_datapath
        """
        self.visualizer.visualize_datapath()
    
    def do_vis_signals(self, arg):
        """
        可视化控制信号
        
        用法: vis_signals
        """
        if self.mode == 'single':
            # 单周期模式
            self.control_unit.decode_instruction(self.datapath.ir.read())
            signals = self.control_unit.generate_control_signals()
        else:  # 'multi'
            # 多周期模式
            signals = self.control_unit.signals
        
        self.visualizer.visualize_control_signals(signals)
    
    def do_vis_reg(self, arg):
        """
        可视化寄存器文件
        
        用法: vis_reg
        """
        self.visualizer.visualize_register_file()
    
    def do_vis_mem(self, arg):
        """
        可视化内存内容
        
        用法: vis_mem [起始地址] [大小]
        """
        args = arg.split()
        start_address = 0
        size = 64
        
        if len(args) >= 1:
            try:
                start_address = int(args[0], 0)
            except ValueError:
                print("无效的起始地址")
                return
        
        if len(args) >= 2:
            try:
                size = int(args[1])
            except ValueError:
                print("无效的大小")
                return
        
        self.visualizer.visualize_memory(start_address, size)
    
    def do_vis_exec(self, arg):
        """
        可视化指令执行过程
        
        用法: vis_exec
        """
        if self.mode == 'single':
            # 单周期模式
            instruction = self.datapath.ir.read()
            self.visualizer.visualize_instruction_execution(instruction, "EXECUTE")
        else:  # 'multi'
            # 多周期模式
            instruction = self.datapath.ir.read()
            state = self.control_unit.state.name
            self.visualizer.visualize_instruction_execution(instruction, state)
    
    def do_vis_state(self, arg):
        """
        可视化状态机（仅多周期模式）
        
        用法: vis_state
        """
        if self.mode == 'multi':
            # 多周期模式
            self.visualizer.visualize_state_machine()
        else:
            print("此命令仅在多周期模式下可用")
    
    def do_vis_cycle(self, arg):
        """
        可视化当前周期状态（仅多周期模式）
        
        用法: vis_cycle
        """
        if self.mode == 'multi':
            # 多周期模式
            self.visualizer.visualize_cycle(self.datapath.get_cycle_count())
        else:
            print("此命令仅在多周期模式下可用")
    
    def do_vis_full(self, arg):
        """
        可视化完整执行过程（仅多周期模式）
        
        用法: vis_full [最大周期数]
        """
        if self.mode == 'multi':
            # 多周期模式
            try:
                max_cycles = int(arg) if arg else 20
            except ValueError:
                print("参数必须是整数")
                return
            
            self.visualizer.visualize_full_execution(max_cycles)
        else:
            print("此命令仅在多周期模式下可用")
    
    def do_reset(self, arg):
        """
        重置模拟器状态
        
        用法: reset
        """
        self.datapath.reset()
        if self.mode == 'multi':
            self.control_unit.reset()
        self.instruction_history = []
        print("模拟器已重置")
    
    def do_load(self, arg):
        """
        加载指令文件
        
        用法: load <文件路径>
        """
        if not arg:
            print("用法: load <文件路径>")
            return
        
        self.load_instructions(arg)
    
    def do_quit(self, arg):
        """
        退出模拟器
        
        用法: quit
        """
        print("退出模拟器")
        return True
    
    def do_exit(self, arg):
        """
        退出模拟器
        
        用法: exit
        """
        return self.do_quit(arg)
    
    def do_help(self, arg):
        """
        显示帮助信息
        
        用法: help [命令]
        """
        if arg:
            # 显示特定命令的帮助
            super().do_help(arg)
        else:
            # 显示所有命令
            print("\n可用命令:")
            print("  step       - 单步执行")
            print("  run [n]    - 连续执行n条指令/周期")
            print("  show       - 显示当前数据通路状态")
            print("  signal     - 显示控制信号状态")
            print("  vis_datapath - 可视化数据通路")
            print("  vis_signals  - 可视化控制信号")
            print("  vis_reg      - 可视化寄存器文件")
            print("  vis_mem      - 可视化内存内容")
            print("  vis_exec     - 可视化指令执行过程")
            
            if self.mode == 'multi':
                print("  vis_state    - 可视化状态机（仅多周期模式）")
                print("  vis_cycle    - 可视化当前周期状态（仅多周期模式）")
                print("  vis_full     - 可视化完整执行过程（仅多周期模式）")
            
            print("  reset       - 重置模拟器状态")
            print("  load        - 加载指令文件")
            print("  quit/exit   - 退出模拟器")
            print("  help        - 显示帮助信息")
            print("\n输入 'help <命令>' 获取特定命令的详细帮助")


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='数据通路模拟器')
    parser.add_argument('instruction_file', nargs='?', help='指令文件路径')
    parser.add_argument('--mode', choices=['single', 'multi'], default='single',
                        help='模拟器模式 (single: 单周期, multi: 多周期)')
    args = parser.parse_args()
    
    # 创建并启动模拟器
    simulator = DatapathSimulator(args.instruction_file, args.mode)
    simulator.cmdloop()


if __name__ == '__main__':
    main() 