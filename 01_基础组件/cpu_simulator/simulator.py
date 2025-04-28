"""
CPU模拟器主程序
这个模块提供了CPU模拟器的主程序和命令行界面
"""

import os
import sys
import cmd
import argparse
from cpu import CPU
from memory import Memory
from register import RegisterFile
from instruction import InstructionDecoder, AssemblyParser
from visualizer import CPUVisualizer

class CPUSimulator(cmd.Cmd):
    """CPU模拟器命令行界面"""
    
    intro = """
    ===================================
    简单CPU模拟器 v1.0
    输入 'help' 或 '?' 获取帮助
    输入 'quit' 或 'exit' 退出
    ===================================
    """
    prompt = 'CPU> '
    
    def __init__(self, program_file=None):
        """
        初始化模拟器
        
        参数:
            program_file: 程序文件路径
        """
        super().__init__()
        
        # 创建CPU组件
        self.memory = Memory()
        self.register_file = RegisterFile()
        self.cpu = CPU(self.memory, self.register_file)
        self.visualizer = CPUVisualizer(self.cpu, self.memory, self.register_file)
        
        # 指令执行历史
        self.instructions_history = []
        
        # 加载程序
        if program_file:
            self.load_program(program_file)
    
    def load_program(self, program_file):
        """
        加载程序文件
        
        参数:
            program_file: 程序文件路径
        """
        try:
            with open(program_file, 'r') as f:
                assembly_code = f.read()
            
            # 解析汇编代码
            instructions = AssemblyParser.parse_program(assembly_code)
            
            # 编码为二进制指令
            binary_instructions = []
            for instruction in instructions:
                binary_instruction = InstructionDecoder.encode(instruction)
                binary_instructions.append(binary_instruction)
            
            # 加载到内存
            self.memory.load_program(binary_instructions)
            
            print(f"成功加载程序: {program_file}")
            print(f"指令数量: {len(instructions)}")
            
        except Exception as e:
            print(f"加载程序失败: {e}")
    
    def do_step(self, arg):
        """
        单步执行指令
        
        用法: step
        """
        # 设置CPU为运行状态
        self.cpu.running = True
        
        # 执行一条指令
        instruction = self.cpu.step()
        
        if instruction:
            # 添加到历史记录
            self.instructions_history.append(instruction)
            
            # 显示执行的指令
            print(f"执行指令: {instruction}")
            
            # 显示寄存器状态
            print(self.register_file)
        else:
            print("CPU已停止或到达断点")
    
    def do_run(self, arg):
        """
        连续运行程序，直到遇到HALT指令或断点
        
        用法: run
        """
        # 执行程序
        instruction_count = self.cpu.run()
        
        print(f"执行了 {instruction_count} 条指令")
        print("CPU已停止")
        
        # 显示寄存器状态
        print(self.register_file)
    
    def do_reg(self, arg):
        """
        显示寄存器状态
        
        用法: reg
        """
        print(self.register_file)
    
    def do_mem(self, arg):
        """
        显示内存内容
        
        用法: mem <地址> <数量>
        """
        args = arg.split()
        if len(args) != 2:
            print("用法: mem <地址> <数量>")
            return
        
        try:
            address = int(args[0], 0)  # 支持十进制、十六进制等
            count = int(args[1])
            
            print(self.memory.dump(address, count))
        except ValueError:
            print("无效的参数")
        except Exception as e:
            print(f"错误: {e}")
    
    def do_break(self, arg):
        """
        设置断点
        
        用法: break <地址>
        """
        try:
            address = int(arg, 0)  # 支持十进制、十六进制等
            self.cpu.set_breakpoint(address)
            print(f"在地址 0x{address:X} 设置断点")
        except ValueError:
            print("无效的地址")
    
    def do_clear(self, arg):
        """
        清除断点
        
        用法: clear <地址>
        如果不指定地址，则清除所有断点
        """
        if not arg:
            self.cpu.clear_all_breakpoints()
            print("已清除所有断点")
        else:
            try:
                address = int(arg, 0)  # 支持十进制、十六进制等
                self.cpu.clear_breakpoint(address)
                print(f"已清除地址 0x{address:X} 的断点")
            except ValueError:
                print("无效的地址")
    
    def do_reset(self, arg):
        """
        重置CPU状态
        
        用法: reset
        """
        self.cpu.reset()
        self.instructions_history = []
        print("CPU已重置")
    
    def do_load(self, arg):
        """
        加载程序文件
        
        用法: load <文件路径>
        """
        if not arg:
            print("用法: load <文件路径>")
            return
        
        self.load_program(arg)
    
    def do_vis_reg(self, arg):
        """
        可视化寄存器状态
        
        用法: vis_reg
        """
        self.visualizer.visualize_registers()
    
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
    
    def do_vis_instr(self, arg):
        """
        可视化指令执行历史
        
        用法: vis_instr
        """
        self.visualizer.visualize_instruction_execution(self.instructions_history)
    
    def do_vis_cpu(self, arg):
        """
        综合可视化CPU状态
        
        用法: vis_cpu
        """
        self.visualizer.visualize_cpu_state(self.instructions_history)
    
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
            print("  step       - 单步执行指令")
            print("  run        - 连续运行程序")
            print("  reg        - 显示寄存器状态")
            print("  mem        - 显示内存内容")
            print("  break      - 设置断点")
            print("  clear      - 清除断点")
            print("  reset      - 重置CPU状态")
            print("  load       - 加载程序文件")
            print("  vis_reg    - 可视化寄存器状态")
            print("  vis_mem    - 可视化内存内容")
            print("  vis_instr  - 可视化指令执行历史")
            print("  vis_cpu    - 综合可视化CPU状态")
            print("  quit/exit  - 退出模拟器")
            print("  help       - 显示帮助信息")
            print("\n输入 'help <命令>' 获取特定命令的详细帮助")


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='简单CPU模拟器')
    parser.add_argument('program_file', nargs='?', help='程序文件路径')
    args = parser.parse_args()
    
    # 创建并启动模拟器
    simulator = CPUSimulator(args.program_file)
    simulator.cmdloop()


if __name__ == '__main__':
    main() 