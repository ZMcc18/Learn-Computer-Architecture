"""
控制信号模块
这个模块实现了CPU控制单元，负责生成控制数据通路的信号
"""

from enum import Enum, auto

class InstructionType(Enum):
    """指令类型枚举"""
    R_TYPE = auto()  # 寄存器类型指令
    I_TYPE = auto()  # 立即数类型指令
    LOAD = auto()    # 加载指令
    STORE = auto()   # 存储指令
    BRANCH = auto()  # 分支指令
    JUMP = auto()    # 跳转指令
    HALT = auto()    # 停止指令


class ControlSignals:
    """控制信号类，存储所有控制信号的状态"""
    
    def __init__(self):
        """初始化控制信号"""
        # PC控制
        self.pc_write = False
        self.pc_source = 0  # 0: PC+4, 1: 分支地址, 2: 跳转地址
        
        # 内存控制
        self.mem_read = False
        self.mem_write = False
        
        # 寄存器控制
        self.reg_write = False
        self.reg_dst = 0  # 0: rt, 1: rd
        
        # ALU控制
        self.alu_src_a = 0  # 0: rs, 1: PC
        self.alu_src_b = 0  # 0: rt, 1: 立即数, 2: 4(PC+4)
        self.alu_op = 0     # ALU操作码
        
        # 数据路径控制
        self.mem_to_reg = 0  # 0: ALU结果, 1: 内存数据
        
        # 指令寄存器控制
        self.ir_write = False
    
    def reset(self):
        """重置所有控制信号"""
        self.__init__()
    
    def __str__(self):
        """返回控制信号的字符串表示"""
        return f"""控制信号:
  PC控制: pc_write={self.pc_write}, pc_source={self.pc_source}
  内存控制: mem_read={self.mem_read}, mem_write={self.mem_write}
  寄存器控制: reg_write={self.reg_write}, reg_dst={self.reg_dst}
  ALU控制: alu_src_a={self.alu_src_a}, alu_src_b={self.alu_src_b}, alu_op={self.alu_op}
  数据路径控制: mem_to_reg={self.mem_to_reg}
  指令寄存器控制: ir_write={self.ir_write}"""


class ControlUnit:
    """控制单元，根据指令生成控制信号"""
    
    def __init__(self):
        """初始化控制单元"""
        self.signals = ControlSignals()
        self.current_instruction = 0
        self.opcode = 0
        self.funct = 0
    
    def decode_instruction(self, instruction):
        """
        解码指令，提取操作码和功能码
        
        参数:
            instruction: 32位指令
        """
        self.current_instruction = instruction
        self.opcode = (instruction >> 26) & 0x3F
        self.funct = instruction & 0x3F
    
    def get_instruction_type(self):
        """
        获取指令类型
        
        返回:
            InstructionType枚举值
        """
        if self.opcode == 0:  # R类型指令
            return InstructionType.R_TYPE
        elif self.opcode == 0x23:  # lw
            return InstructionType.LOAD
        elif self.opcode == 0x2B:  # sw
            return InstructionType.STORE
        elif self.opcode in [0x04, 0x05]:  # beq, bne
            return InstructionType.BRANCH
        elif self.opcode in [0x02, 0x03]:  # j, jal
            return InstructionType.JUMP
        elif self.opcode == 0x3F:  # 自定义HALT指令
            return InstructionType.HALT
        else:  # 其他I类型指令
            return InstructionType.I_TYPE
    
    def generate_control_signals(self):
        """
        根据指令生成控制信号
        
        返回:
            ControlSignals对象
        """
        # 重置控制信号
        self.signals.reset()
        
        # 根据指令类型设置控制信号
        instr_type = self.get_instruction_type()
        
        if instr_type == InstructionType.R_TYPE:
            # R类型指令（如add, sub, and, or等）
            self.signals.reg_dst = 1  # 目标寄存器是rd
            self.signals.reg_write = True  # 需要写寄存器
            self.signals.alu_src_a = 0  # ALU输入A来自rs
            self.signals.alu_src_b = 0  # ALU输入B来自rt
            
            # 根据功能码设置ALU操作
            if self.funct == 0x20:  # add
                self.signals.alu_op = 0  # ADD
            elif self.funct == 0x22:  # sub
                self.signals.alu_op = 1  # SUB
            elif self.funct == 0x24:  # and
                self.signals.alu_op = 2  # AND
            elif self.funct == 0x25:  # or
                self.signals.alu_op = 3  # OR
            elif self.funct == 0x26:  # xor
                self.signals.alu_op = 4  # XOR
            elif self.funct == 0x00:  # sll
                self.signals.alu_op = 5  # SLL
            elif self.funct == 0x02:  # srl
                self.signals.alu_op = 6  # SRL
            elif self.funct == 0x03:  # sra
                self.signals.alu_op = 7  # SRA
            elif self.funct == 0x2A:  # slt
                self.signals.alu_op = 8  # SLT
            
            # PC更新
            self.signals.pc_write = True
            self.signals.pc_source = 0  # PC+4
            
        elif instr_type == InstructionType.I_TYPE:
            # I类型指令（如addi, andi, ori等）
            self.signals.reg_dst = 0  # 目标寄存器是rt
            self.signals.reg_write = True  # 需要写寄存器
            self.signals.alu_src_a = 0  # ALU输入A来自rs
            self.signals.alu_src_b = 1  # ALU输入B来自立即数
            
            # 根据操作码设置ALU操作
            if self.opcode == 0x08:  # addi
                self.signals.alu_op = 0  # ADD
            elif self.opcode == 0x0C:  # andi
                self.signals.alu_op = 2  # AND
            elif self.opcode == 0x0D:  # ori
                self.signals.alu_op = 3  # OR
            elif self.opcode == 0x0E:  # xori
                self.signals.alu_op = 4  # XOR
            elif self.opcode == 0x0A:  # slti
                self.signals.alu_op = 8  # SLT
            
            # PC更新
            self.signals.pc_write = True
            self.signals.pc_source = 0  # PC+4
            
        elif instr_type == InstructionType.LOAD:
            # 加载指令（如lw）
            self.signals.mem_read = True  # 需要读内存
            self.signals.reg_dst = 0  # 目标寄存器是rt
            self.signals.reg_write = True  # 需要写寄存器
            self.signals.alu_src_a = 0  # ALU输入A来自rs
            self.signals.alu_src_b = 1  # ALU输入B来自立即数
            self.signals.alu_op = 0  # ADD（计算地址）
            self.signals.mem_to_reg = 1  # 寄存器写入数据来自内存
            
            # PC更新
            self.signals.pc_write = True
            self.signals.pc_source = 0  # PC+4
            
        elif instr_type == InstructionType.STORE:
            # 存储指令（如sw）
            self.signals.mem_write = True  # 需要写内存
            self.signals.alu_src_a = 0  # ALU输入A来自rs
            self.signals.alu_src_b = 1  # ALU输入B来自立即数
            self.signals.alu_op = 0  # ADD（计算地址）
            
            # PC更新
            self.signals.pc_write = True
            self.signals.pc_source = 0  # PC+4
            
        elif instr_type == InstructionType.BRANCH:
            # 分支指令（如beq, bne）
            self.signals.alu_src_a = 0  # ALU输入A来自rs
            self.signals.alu_src_b = 0  # ALU输入B来自rt
            self.signals.alu_op = 1  # SUB（比较）
            
            # PC更新（条件性）
            if (self.opcode == 0x04 and self.signals.alu_op == 0) or (self.opcode == 0x05 and self.signals.alu_op != 0):
                self.signals.pc_write = True
                self.signals.pc_source = 1  # 分支地址
            else:
                self.signals.pc_write = True
                self.signals.pc_source = 0  # PC+4
            
        elif instr_type == InstructionType.JUMP:
            # 跳转指令（如j, jal）
            if self.opcode == 0x03:  # jal
                self.signals.reg_write = True  # 需要写寄存器（$ra）
                self.signals.reg_dst = 2  # 目标寄存器是$ra（31）
                self.signals.alu_src_a = 1  # ALU输入A来自PC
                self.signals.alu_src_b = 2  # ALU输入B是4
                self.signals.alu_op = 0  # ADD（计算PC+4）
            
            # PC更新
            self.signals.pc_write = True
            self.signals.pc_source = 2  # 跳转地址
            
        elif instr_type == InstructionType.HALT:
            # 停止指令
            self.signals.pc_write = False  # 不更新PC
        
        return self.signals
    
    def get_control_signals(self):
        """
        获取当前控制信号
        
        返回:
            ControlSignals对象
        """
        return self.signals


class MultiCycleControlUnit(ControlUnit):
    """多周期CPU的控制单元，实现状态机控制"""
    
    # 状态枚举
    class State(Enum):
        FETCH = auto()       # 取指令
        DECODE = auto()      # 解码
        EXECUTE = auto()     # 执行
        MEMORY = auto()      # 访存
        WRITEBACK = auto()   # 写回
    
    def __init__(self):
        """初始化多周期控制单元"""
        super().__init__()
        self.state = self.State.FETCH
        self.next_state = self.State.FETCH
    
    def reset(self):
        """重置控制单元状态"""
        super().reset()
        self.state = self.State.FETCH
        self.next_state = self.State.FETCH
    
    def update_state(self):
        """更新状态机状态"""
        self.state = self.next_state
    
    def compute_next_state(self):
        """
        计算下一个状态
        
        返回:
            下一个状态
        """
        instr_type = self.get_instruction_type()
        
        if self.state == self.State.FETCH:
            self.next_state = self.State.DECODE
            
        elif self.state == self.State.DECODE:
            self.next_state = self.State.EXECUTE
            
        elif self.state == self.State.EXECUTE:
            if instr_type in [InstructionType.LOAD, InstructionType.STORE]:
                self.next_state = self.State.MEMORY
            elif instr_type in [InstructionType.R_TYPE, InstructionType.I_TYPE]:
                self.next_state = self.State.WRITEBACK
            else:  # BRANCH, JUMP, HALT
                self.next_state = self.State.FETCH
                
        elif self.state == self.State.MEMORY:
            if instr_type == InstructionType.LOAD:
                self.next_state = self.State.WRITEBACK
            else:  # STORE
                self.next_state = self.State.FETCH
                
        elif self.state == self.State.WRITEBACK:
            self.next_state = self.State.FETCH
        
        return self.next_state
    
    def generate_control_signals(self):
        """
        根据当前状态和指令生成控制信号
        
        返回:
            ControlSignals对象
        """
        # 重置控制信号
        self.signals.reset()
        
        # 根据当前状态设置控制信号
        if self.state == self.State.FETCH:
            # 取指令阶段
            self.signals.mem_read = True  # 读取指令
            self.signals.ir_write = True  # 写入指令寄存器
            self.signals.alu_src_a = 1  # ALU输入A来自PC
            self.signals.alu_src_b = 2  # ALU输入B是4
            self.signals.alu_op = 0  # ADD（计算PC+4）
            self.signals.pc_source = 0  # PC+4
            self.signals.pc_write = True  # 更新PC
            
        elif self.state == self.State.DECODE:
            # 解码阶段
            # 不需要特殊控制信号
            pass
            
        elif self.state == self.State.EXECUTE:
            # 执行阶段
            instr_type = self.get_instruction_type()
            
            if instr_type == InstructionType.R_TYPE:
                # R类型指令
                self.signals.alu_src_a = 0  # ALU输入A来自rs
                self.signals.alu_src_b = 0  # ALU输入B来自rt
                
                # 根据功能码设置ALU操作
                if self.funct == 0x20:  # add
                    self.signals.alu_op = 0  # ADD
                elif self.funct == 0x22:  # sub
                    self.signals.alu_op = 1  # SUB
                elif self.funct == 0x24:  # and
                    self.signals.alu_op = 2  # AND
                elif self.funct == 0x25:  # or
                    self.signals.alu_op = 3  # OR
                elif self.funct == 0x26:  # xor
                    self.signals.alu_op = 4  # XOR
                elif self.funct == 0x00:  # sll
                    self.signals.alu_op = 5  # SLL
                elif self.funct == 0x02:  # srl
                    self.signals.alu_op = 6  # SRL
                elif self.funct == 0x03:  # sra
                    self.signals.alu_op = 7  # SRA
                elif self.funct == 0x2A:  # slt
                    self.signals.alu_op = 8  # SLT
                
            elif instr_type == InstructionType.I_TYPE:
                # I类型指令
                self.signals.alu_src_a = 0  # ALU输入A来自rs
                self.signals.alu_src_b = 1  # ALU输入B来自立即数
                
                # 根据操作码设置ALU操作
                if self.opcode == 0x08:  # addi
                    self.signals.alu_op = 0  # ADD
                elif self.opcode == 0x0C:  # andi
                    self.signals.alu_op = 2  # AND
                elif self.opcode == 0x0D:  # ori
                    self.signals.alu_op = 3  # OR
                elif self.opcode == 0x0E:  # xori
                    self.signals.alu_op = 4  # XOR
                elif self.opcode == 0x0A:  # slti
                    self.signals.alu_op = 8  # SLT
                
            elif instr_type in [InstructionType.LOAD, InstructionType.STORE]:
                # 加载/存储指令
                self.signals.alu_src_a = 0  # ALU输入A来自rs
                self.signals.alu_src_b = 1  # ALU输入B来自立即数
                self.signals.alu_op = 0  # ADD（计算地址）
                
            elif instr_type == InstructionType.BRANCH:
                # 分支指令
                self.signals.alu_src_a = 0  # ALU输入A来自rs
                self.signals.alu_src_b = 0  # ALU输入B来自rt
                self.signals.alu_op = 1  # SUB（比较）
                
                # 计算分支目标地址
                self.signals.pc_source = 1  # 分支地址
                
                # 根据比较结果决定是否跳转
                if (self.opcode == 0x04 and self.signals.alu_op == 0) or (self.opcode == 0x05 and self.signals.alu_op != 0):
                    self.signals.pc_write = True
                
            elif instr_type == InstructionType.JUMP:
                # 跳转指令
                self.signals.pc_source = 2  # 跳转地址
                self.signals.pc_write = True
                
                if self.opcode == 0x03:  # jal
                    # 计算返回地址（PC+4）
                    self.signals.alu_src_a = 1  # ALU输入A来自PC
                    self.signals.alu_src_b = 2  # ALU输入B是4
                    self.signals.alu_op = 0  # ADD
            
        elif self.state == self.State.MEMORY:
            # 访存阶段
            instr_type = self.get_instruction_type()
            
            if instr_type == InstructionType.LOAD:
                # 加载指令
                self.signals.mem_read = True
                
            elif instr_type == InstructionType.STORE:
                # 存储指令
                self.signals.mem_write = True
            
        elif self.state == self.State.WRITEBACK:
            # 写回阶段
            instr_type = self.get_instruction_type()
            
            if instr_type == InstructionType.R_TYPE:
                # R类型指令
                self.signals.reg_dst = 1  # 目标寄存器是rd
                self.signals.reg_write = True
                self.signals.mem_to_reg = 0  # 寄存器写入数据来自ALU
                
            elif instr_type == InstructionType.I_TYPE:
                # I类型指令
                self.signals.reg_dst = 0  # 目标寄存器是rt
                self.signals.reg_write = True
                self.signals.mem_to_reg = 0  # 寄存器写入数据来自ALU
                
            elif instr_type == InstructionType.LOAD:
                # 加载指令
                self.signals.reg_dst = 0  # 目标寄存器是rt
                self.signals.reg_write = True
                self.signals.mem_to_reg = 1  # 寄存器写入数据来自内存
                
            elif instr_type == InstructionType.JUMP and self.opcode == 0x03:  # jal
                # jal指令
                self.signals.reg_dst = 2  # 目标寄存器是$ra（31）
                self.signals.reg_write = True
                self.signals.mem_to_reg = 0  # 寄存器写入数据来自ALU（PC+4）
        
        return self.signals
    
    def step(self):
        """
        执行一个时钟周期
        
        返回:
            当前状态
        """
        # 生成当前状态的控制信号
        self.generate_control_signals()
        
        # 计算下一个状态
        self.compute_next_state()
        
        # 更新状态
        self.update_state()
        
        return self.state 