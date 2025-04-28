"""
CPU模拟器测试脚本
这个脚本测试CPU模拟器的基本功能
"""

import unittest
from cpu import CPU
from memory import Memory
from register import RegisterFile
from instruction import InstructionDecoder, AssemblyParser, OpCode, Instruction

class TestCPUSimulator(unittest.TestCase):
    """CPU模拟器测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.memory = Memory()
        self.register_file = RegisterFile()
        self.cpu = CPU(self.memory, self.register_file)
    
    def test_instruction_encoding_decoding(self):
        """测试指令编码和解码"""
        # 创建一个ADD指令
        original_instruction = Instruction(OpCode.ADD, [1, 2, 3])
        
        # 编码
        binary = InstructionDecoder.encode(original_instruction)
        
        # 解码
        decoded_instruction = InstructionDecoder.decode(binary)
        
        # 验证解码后的指令与原始指令相同
        self.assertEqual(decoded_instruction.opcode, original_instruction.opcode)
        self.assertEqual(decoded_instruction.operands, original_instruction.operands)
    
    def test_assembly_parsing(self):
        """测试汇编代码解析"""
        # 简单的汇编程序
        assembly_code = """
        # 这是一个注释
        LOAD R1, 10
        LOAD R2, 20
        ADD R3, R1, R2
        STORE R3, 100
        HALT
        """
        
        # 解析汇编代码
        instructions = AssemblyParser.parse_program(assembly_code)
        
        # 验证解析结果
        self.assertEqual(len(instructions), 5)
        self.assertEqual(instructions[0].opcode, OpCode.LOAD)
        self.assertEqual(instructions[0].operands, [1, 10])
        self.assertEqual(instructions[2].opcode, OpCode.ADD)
        self.assertEqual(instructions[2].operands, [3, 1, 2])
    
    def test_cpu_execution(self):
        """测试CPU执行"""
        # 创建一个简单的程序
        program = [
            Instruction(OpCode.LOAD, [1, 10]),  # R1 = 10
            Instruction(OpCode.LOAD, [2, 20]),  # R2 = 20
            Instruction(OpCode.ADD, [3, 1, 2]), # R3 = R1 + R2
            Instruction(OpCode.STORE, [3, 100]), # MEM[100] = R3
            Instruction(OpCode.HALT, [])        # 停止
        ]
        
        # 将程序编码为二进制指令
        binary_program = [InstructionDecoder.encode(instr) for instr in program]
        
        # 加载程序到内存
        self.memory.load_program(binary_program)
        
        # 执行程序
        self.cpu.running = True
        instruction_count = self.cpu.run()
        
        # 验证执行结果
        self.assertEqual(instruction_count, 5)
        self.assertEqual(self.register_file.read_register(1), 10)
        self.assertEqual(self.register_file.read_register(2), 20)
        self.assertEqual(self.register_file.read_register(3), 30)
        self.assertEqual(self.memory.read(100), 30)
    
    def test_jump_instructions(self):
        """测试跳转指令"""
        # 创建一个包含跳转的程序
        program = [
            Instruction(OpCode.LOAD, [1, 5]),    # R1 = 5
            Instruction(OpCode.LOAD, [2, 10]),   # R2 = 10
            Instruction(OpCode.JUMP_LT, [1, 2, 16]), # 如果R1 < R2，跳转到地址16
            Instruction(OpCode.LOAD, [3, 0]),    # R3 = 0 (这条指令会被跳过)
            Instruction(OpCode.LOAD, [3, 1]),    # R3 = 1
            Instruction(OpCode.HALT, [])         # 停止
        ]
        
        # 将程序编码为二进制指令
        binary_program = [InstructionDecoder.encode(instr) for instr in program]
        
        # 加载程序到内存
        self.memory.load_program(binary_program)
        
        # 执行程序
        self.cpu.running = True
        self.cpu.run()
        
        # 验证执行结果
        self.assertEqual(self.register_file.read_register(3), 1)
    
    def test_arithmetic_operations(self):
        """测试算术运算"""
        # 创建一个包含各种算术运算的程序
        program = [
            Instruction(OpCode.LOAD, [1, 10]),    # R1 = 10
            Instruction(OpCode.LOAD, [2, 5]),     # R2 = 5
            Instruction(OpCode.ADD, [3, 1, 2]),   # R3 = R1 + R2 = 15
            Instruction(OpCode.SUB, [4, 1, 2]),   # R4 = R1 - R2 = 5
            Instruction(OpCode.MUL, [5, 1, 2]),   # R5 = R1 * R2 = 50
            Instruction(OpCode.DIV, [6, 1, 2]),   # R6 = R1 / R2 = 2
            Instruction(OpCode.HALT, [])          # 停止
        ]
        
        # 将程序编码为二进制指令
        binary_program = [InstructionDecoder.encode(instr) for instr in program]
        
        # 加载程序到内存
        self.memory.load_program(binary_program)
        
        # 执行程序
        self.cpu.running = True
        self.cpu.run()
        
        # 验证执行结果
        self.assertEqual(self.register_file.read_register(3), 15)
        self.assertEqual(self.register_file.read_register(4), 5)
        self.assertEqual(self.register_file.read_register(5), 50)
        self.assertEqual(self.register_file.read_register(6), 2)


if __name__ == '__main__':
    unittest.main() 