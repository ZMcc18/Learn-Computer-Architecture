"""
指令定义和解码模块
这个模块定义了CPU支持的指令集和指令解码逻辑
"""

from enum import Enum, auto

class InstructionType(Enum):
    """指令类型枚举"""
    ARITHMETIC = auto()  # 算术指令
    LOGICAL = auto()     # 逻辑指令
    DATA_TRANSFER = auto()  # 数据传输指令
    CONTROL = auto()     # 控制指令
    HALT = auto()        # 停止指令

class OpCode(Enum):
    """操作码枚举"""
    # 算术指令
    ADD = 0x01
    SUB = 0x02
    MUL = 0x03
    DIV = 0x04
    
    # 逻辑指令
    AND = 0x11
    OR = 0x12
    XOR = 0x13
    NOT = 0x14
    
    # 数据传输指令
    LOAD = 0x21
    STORE = 0x22
    MOVE = 0x23
    
    # 控制指令
    JUMP = 0x31
    JUMP_EQ = 0x32
    JUMP_NEQ = 0x33
    JUMP_GT = 0x34
    JUMP_LT = 0x35
    
    # 停止指令
    HALT = 0xFF

class Instruction:
    """指令类，表示一条CPU指令"""
    
    def __init__(self, opcode, operands=None):
        """
        初始化一条指令
        
        参数:
            opcode: 操作码
            operands: 操作数列表
        """
        self.opcode = opcode
        self.operands = operands if operands else []
        
    def __str__(self):
        """返回指令的字符串表示"""
        opcode_name = self.opcode.name if isinstance(self.opcode, OpCode) else str(self.opcode)
        operands_str = ", ".join(map(str, self.operands))
        return f"{opcode_name} {operands_str}"
    
    @property
    def type(self):
        """返回指令类型"""
        if self.opcode in [OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.DIV]:
            return InstructionType.ARITHMETIC
        elif self.opcode in [OpCode.AND, OpCode.OR, OpCode.XOR, OpCode.NOT]:
            return InstructionType.LOGICAL
        elif self.opcode in [OpCode.LOAD, OpCode.STORE, OpCode.MOVE]:
            return InstructionType.DATA_TRANSFER
        elif self.opcode in [OpCode.JUMP, OpCode.JUMP_EQ, OpCode.JUMP_NEQ, OpCode.JUMP_GT, OpCode.JUMP_LT]:
            return InstructionType.CONTROL
        elif self.opcode == OpCode.HALT:
            return InstructionType.HALT
        else:
            raise ValueError(f"未知的操作码: {self.opcode}")

class InstructionDecoder:
    """指令解码器，负责将二进制指令解码为Instruction对象"""
    
    @staticmethod
    def decode(binary_instruction):
        """
        解码二进制指令
        
        参数:
            binary_instruction: 32位二进制指令
            
        返回:
            Instruction对象
        """
        # 提取操作码 (高8位)
        opcode_value = (binary_instruction >> 24) & 0xFF
        
        # 将操作码值转换为OpCode枚举
        try:
            opcode = OpCode(opcode_value)
        except ValueError:
            raise ValueError(f"无效的操作码: {opcode_value:#x}")
        
        # 根据指令类型提取操作数
        operands = []
        
        if opcode in [OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.DIV, 
                     OpCode.AND, OpCode.OR, OpCode.XOR]:
            # 三操作数指令: 目标寄存器, 源寄存器1, 源寄存器2
            dest_reg = (binary_instruction >> 16) & 0xFF
            src_reg1 = (binary_instruction >> 8) & 0xFF
            src_reg2 = binary_instruction & 0xFF
            operands = [dest_reg, src_reg1, src_reg2]
            
        elif opcode == OpCode.NOT:
            # 两操作数指令: 目标寄存器, 源寄存器
            dest_reg = (binary_instruction >> 16) & 0xFF
            src_reg = (binary_instruction >> 8) & 0xFF
            operands = [dest_reg, src_reg]
            
        elif opcode in [OpCode.LOAD, OpCode.STORE]:
            # 两操作数指令: 寄存器, 内存地址
            reg = (binary_instruction >> 16) & 0xFF
            address = binary_instruction & 0xFFFF
            operands = [reg, address]
            
        elif opcode == OpCode.MOVE:
            # 两操作数指令: 目标寄存器, 源寄存器
            dest_reg = (binary_instruction >> 16) & 0xFF
            src_reg = (binary_instruction >> 8) & 0xFF
            operands = [dest_reg, src_reg]
            
        elif opcode == OpCode.JUMP:
            # 一操作数指令: 跳转地址
            address = binary_instruction & 0xFFFFFF
            operands = [address]
            
        elif opcode in [OpCode.JUMP_EQ, OpCode.JUMP_NEQ, OpCode.JUMP_GT, OpCode.JUMP_LT]:
            # 三操作数指令: 寄存器1, 寄存器2, 跳转地址
            reg1 = (binary_instruction >> 16) & 0xFF
            reg2 = (binary_instruction >> 8) & 0xFF
            address = binary_instruction & 0xFF
            operands = [reg1, reg2, address]
            
        elif opcode == OpCode.HALT:
            # 无操作数指令
            pass
        
        return Instruction(opcode, operands)
    
    @staticmethod
    def encode(instruction):
        """
        将Instruction对象编码为32位二进制指令
        
        参数:
            instruction: Instruction对象
            
        返回:
            32位二进制指令
        """
        opcode_value = instruction.opcode.value
        binary_instruction = opcode_value << 24
        
        if instruction.opcode in [OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.DIV, 
                                OpCode.AND, OpCode.OR, OpCode.XOR]:
            # 三操作数指令: 目标寄存器, 源寄存器1, 源寄存器2
            binary_instruction |= (instruction.operands[0] & 0xFF) << 16
            binary_instruction |= (instruction.operands[1] & 0xFF) << 8
            binary_instruction |= instruction.operands[2] & 0xFF
            
        elif instruction.opcode == OpCode.NOT:
            # 两操作数指令: 目标寄存器, 源寄存器
            binary_instruction |= (instruction.operands[0] & 0xFF) << 16
            binary_instruction |= (instruction.operands[1] & 0xFF) << 8
            
        elif instruction.opcode in [OpCode.LOAD, OpCode.STORE]:
            # 两操作数指令: 寄存器, 内存地址
            binary_instruction |= (instruction.operands[0] & 0xFF) << 16
            binary_instruction |= instruction.operands[1] & 0xFFFF
            
        elif instruction.opcode == OpCode.MOVE:
            # 两操作数指令: 目标寄存器, 源寄存器
            binary_instruction |= (instruction.operands[0] & 0xFF) << 16
            binary_instruction |= (instruction.operands[1] & 0xFF) << 8
            
        elif instruction.opcode == OpCode.JUMP:
            # 一操作数指令: 跳转地址
            binary_instruction |= instruction.operands[0] & 0xFFFFFF
            
        elif instruction.opcode in [OpCode.JUMP_EQ, OpCode.JUMP_NEQ, OpCode.JUMP_GT, OpCode.JUMP_LT]:
            # 三操作数指令: 寄存器1, 寄存器2, 跳转地址
            binary_instruction |= (instruction.operands[0] & 0xFF) << 16
            binary_instruction |= (instruction.operands[1] & 0xFF) << 8
            binary_instruction |= instruction.operands[2] & 0xFF
            
        return binary_instruction

class AssemblyParser:
    """汇编代码解析器，将汇编代码转换为指令对象"""
    
    @staticmethod
    def parse_line(line):
        """
        解析一行汇编代码
        
        参数:
            line: 汇编代码行
            
        返回:
            Instruction对象或None（如果是注释或空行）
        """
        # 移除注释
        if '#' in line:
            line = line[:line.index('#')]
        
        # 去除前后空白
        line = line.strip()
        
        # 跳过空行
        if not line:
            return None
        
        # 分割操作码和操作数
        parts = line.split()
        opcode_str = parts[0].upper()
        operands_str = ' '.join(parts[1:])
        
        # 解析操作数
        operands = []
        if operands_str:
            # 按逗号分割，并去除空白
            operands = [op.strip() for op in operands_str.split(',')]
        
        # 将操作码字符串转换为OpCode枚举
        try:
            opcode = getattr(OpCode, opcode_str)
        except AttributeError:
            raise ValueError(f"未知的操作码: {opcode_str}")
        
        # 解析操作数
        parsed_operands = []
        for op in operands:
            if op.startswith('R'):
                # 寄存器
                try:
                    reg_num = int(op[1:])
                    parsed_operands.append(reg_num)
                except ValueError:
                    raise ValueError(f"无效的寄存器编号: {op}")
            else:
                # 立即数或地址
                try:
                    value = int(op)
                    parsed_operands.append(value)
                except ValueError:
                    raise ValueError(f"无效的操作数: {op}")
        
        return Instruction(opcode, parsed_operands)
    
    @staticmethod
    def parse_program(assembly_code):
        """
        解析完整的汇编程序
        
        参数:
            assembly_code: 多行汇编代码
            
        返回:
            Instruction对象列表
        """
        instructions = []
        for line_num, line in enumerate(assembly_code.splitlines(), 1):
            try:
                instruction = AssemblyParser.parse_line(line)
                if instruction:
                    instructions.append(instruction)
            except ValueError as e:
                raise ValueError(f"第{line_num}行解析错误: {e}")
        
        return instructions 