"""
CPU核心模块
这个模块实现了CPU的核心功能，包括指令执行和ALU操作
"""

from instruction import OpCode, InstructionDecoder

class ALU:
    """算术逻辑单元，负责执行算术和逻辑运算"""
    
    def __init__(self, register_file):
        """
        初始化ALU
        
        参数:
            register_file: RegisterFile对象
        """
        self.register_file = register_file
    
    def execute(self, opcode, operands):
        """
        执行算术或逻辑运算
        
        参数:
            opcode: 操作码
            operands: 操作数列表
            
        返回:
            运算结果
        """
        # 算术运算
        if opcode == OpCode.ADD:
            # ADD dest, src1, src2
            src1_val = self.register_file.read_register(operands[1])
            src2_val = self.register_file.read_register(operands[2])
            result = src1_val + src2_val
            
            # 检查溢出和进位
            carry = (result > 0xFFFFFFFF)
            overflow = ((src1_val > 0 and src2_val > 0 and result < 0) or 
                        (src1_val < 0 and src2_val < 0 and result > 0))
            
            # 更新标志位
            self.register_file.update_flags(result, carry, overflow)
            
            # 截断为32位
            result &= 0xFFFFFFFF
            
            return result
            
        elif opcode == OpCode.SUB:
            # SUB dest, src1, src2
            src1_val = self.register_file.read_register(operands[1])
            src2_val = self.register_file.read_register(operands[2])
            result = src1_val - src2_val
            
            # 检查溢出和借位
            borrow = (src1_val < src2_val)
            overflow = ((src1_val > 0 and src2_val < 0 and result < 0) or 
                        (src1_val < 0 and src2_val > 0 and result > 0))
            
            # 更新标志位
            self.register_file.update_flags(result, not borrow, overflow)
            
            # 截断为32位
            result &= 0xFFFFFFFF
            
            return result
            
        elif opcode == OpCode.MUL:
            # MUL dest, src1, src2
            src1_val = self.register_file.read_register(operands[1])
            src2_val = self.register_file.read_register(operands[2])
            result = src1_val * src2_val
            
            # 检查溢出
            overflow = (result > 0xFFFFFFFF or result < -0x80000000)
            
            # 更新标志位
            self.register_file.update_flags(result, False, overflow)
            
            # 截断为32位
            result &= 0xFFFFFFFF
            
            return result
            
        elif opcode == OpCode.DIV:
            # DIV dest, src1, src2
            src1_val = self.register_file.read_register(operands[1])
            src2_val = self.register_file.read_register(operands[2])
            
            # 检查除数是否为0
            if src2_val == 0:
                raise ZeroDivisionError("除数不能为0")
            
            result = src1_val // src2_val
            
            # 更新标志位
            self.register_file.update_flags(result)
            
            # 截断为32位
            result &= 0xFFFFFFFF
            
            return result
        
        # 逻辑运算
        elif opcode == OpCode.AND:
            # AND dest, src1, src2
            src1_val = self.register_file.read_register(operands[1])
            src2_val = self.register_file.read_register(operands[2])
            result = src1_val & src2_val
            
            # 更新标志位
            self.register_file.update_flags(result)
            
            return result
            
        elif opcode == OpCode.OR:
            # OR dest, src1, src2
            src1_val = self.register_file.read_register(operands[1])
            src2_val = self.register_file.read_register(operands[2])
            result = src1_val | src2_val
            
            # 更新标志位
            self.register_file.update_flags(result)
            
            return result
            
        elif opcode == OpCode.XOR:
            # XOR dest, src1, src2
            src1_val = self.register_file.read_register(operands[1])
            src2_val = self.register_file.read_register(operands[2])
            result = src1_val ^ src2_val
            
            # 更新标志位
            self.register_file.update_flags(result)
            
            return result
            
        elif opcode == OpCode.NOT:
            # NOT dest, src
            src_val = self.register_file.read_register(operands[1])
            result = ~src_val
            
            # 更新标志位
            self.register_file.update_flags(result)
            
            # 截断为32位
            result &= 0xFFFFFFFF
            
            return result
        
        else:
            raise ValueError(f"ALU不支持的操作码: {opcode}")


class CPU:
    """CPU类，模拟中央处理器的功能"""
    
    def __init__(self, memory, register_file):
        """
        初始化CPU
        
        参数:
            memory: Memory对象
            register_file: RegisterFile对象
        """
        self.memory = memory
        self.register_file = register_file
        self.alu = ALU(register_file)
        self.running = False
        self.instruction_decoder = InstructionDecoder()
        self.breakpoints = set()
    
    def fetch(self):
        """
        取指令阶段
        
        返回:
            二进制指令
        """
        # 从PC指向的内存地址获取指令
        pc = self.register_file.read_pc()
        instruction = self.memory.read(pc)
        
        # 增加PC，指向下一条指令
        self.register_file.increment_pc(4)
        
        return instruction
    
    def decode(self, binary_instruction):
        """
        解码阶段
        
        参数:
            binary_instruction: 二进制指令
            
        返回:
            解码后的Instruction对象
        """
        return self.instruction_decoder.decode(binary_instruction)
    
    def execute(self, instruction):
        """
        执行阶段
        
        参数:
            instruction: Instruction对象
        """
        opcode = instruction.opcode
        operands = instruction.operands
        
        # 算术和逻辑指令
        if opcode in [OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.DIV,
                     OpCode.AND, OpCode.OR, OpCode.XOR, OpCode.NOT]:
            result = self.alu.execute(opcode, operands)
            self.register_file.write_register(operands[0], result)
        
        # 数据传输指令
        elif opcode == OpCode.LOAD:
            # LOAD reg, address
            address = operands[1]
            value = self.memory.read(address)
            self.register_file.write_register(operands[0], value)
            
        elif opcode == OpCode.STORE:
            # STORE reg, address
            reg_val = self.register_file.read_register(operands[0])
            address = operands[1]
            self.memory.write(address, reg_val)
            
        elif opcode == OpCode.MOVE:
            # MOVE dest, src
            src_val = self.register_file.read_register(operands[1])
            self.register_file.write_register(operands[0], src_val)
        
        # 控制指令
        elif opcode == OpCode.JUMP:
            # JUMP address
            self.register_file.write_pc(operands[0])
            
        elif opcode == OpCode.JUMP_EQ:
            # JUMP_EQ reg1, reg2, address
            reg1_val = self.register_file.read_register(operands[0])
            reg2_val = self.register_file.read_register(operands[1])
            if reg1_val == reg2_val:
                self.register_file.write_pc(operands[2])
                
        elif opcode == OpCode.JUMP_NEQ:
            # JUMP_NEQ reg1, reg2, address
            reg1_val = self.register_file.read_register(operands[0])
            reg2_val = self.register_file.read_register(operands[1])
            if reg1_val != reg2_val:
                self.register_file.write_pc(operands[2])
                
        elif opcode == OpCode.JUMP_GT:
            # JUMP_GT reg1, reg2, address
            reg1_val = self.register_file.read_register(operands[0])
            reg2_val = self.register_file.read_register(operands[1])
            if reg1_val > reg2_val:
                self.register_file.write_pc(operands[2])
                
        elif opcode == OpCode.JUMP_LT:
            # JUMP_LT reg1, reg2, address
            reg1_val = self.register_file.read_register(operands[0])
            reg2_val = self.register_file.read_register(operands[1])
            if reg1_val < reg2_val:
                self.register_file.write_pc(operands[2])
        
        # 停止指令
        elif opcode == OpCode.HALT:
            # HALT
            self.running = False
        
        else:
            raise ValueError(f"未知的操作码: {opcode}")
    
    def step(self):
        """
        执行一个指令周期
        
        返回:
            执行的指令
        """
        if not self.running:
            return None
        
        # 检查是否到达断点
        pc = self.register_file.read_pc()
        if pc in self.breakpoints:
            self.running = False
            return None
        
        # 取指令
        binary_instruction = self.fetch()
        
        # 解码
        instruction = self.decode(binary_instruction)
        
        # 执行
        self.execute(instruction)
        
        return instruction
    
    def run(self):
        """
        连续运行CPU，直到遇到HALT指令或断点
        
        返回:
            执行的指令数
        """
        instruction_count = 0
        self.running = True
        
        while self.running:
            instruction = self.step()
            if instruction:
                instruction_count += 1
        
        return instruction_count
    
    def reset(self):
        """重置CPU状态"""
        self.register_file.reset()
        self.running = False
    
    def set_breakpoint(self, address):
        """
        设置断点
        
        参数:
            address: 断点地址
        """
        self.breakpoints.add(address)
    
    def clear_breakpoint(self, address):
        """
        清除断点
        
        参数:
            address: 断点地址
        """
        if address in self.breakpoints:
            self.breakpoints.remove(address)
    
    def clear_all_breakpoints(self):
        """清除所有断点"""
        self.breakpoints.clear() 