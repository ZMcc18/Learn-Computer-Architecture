"""
数据通路模块
这个模块实现了CPU的数据通路，连接各个功能单元
"""

from functional_units import Register, ProgramCounter, RegisterFile, ALU, Memory, Multiplexer

class Datapath:
    """数据通路类，连接CPU的各个功能单元"""
    
    def __init__(self):
        """初始化数据通路"""
        # 程序计数器
        self.pc = ProgramCounter()
        
        # 寄存器文件
        self.register_file = RegisterFile()
        
        # 指令寄存器
        self.ir = Register("IR", 32)
        
        # 内存数据寄存器
        self.mdr = Register("MDR", 32)
        
        # 算术逻辑单元
        self.alu = ALU()
        
        # ALU输出寄存器
        self.alu_out = Register("ALU_OUT", 32)
        
        # A和B寄存器（用于存储从寄存器文件读取的值）
        self.a = Register("A", 32)
        self.b = Register("B", 32)
        
        # 内存
        self.memory = Memory()
        
        # 多路复用器
        self.alu_src_a_mux = Multiplexer("ALU_SRC_A", 2)  # 0: A, 1: PC
        self.alu_src_b_mux = Multiplexer("ALU_SRC_B", 3)  # 0: B, 1: 立即数, 2: 4
        self.reg_dst_mux = Multiplexer("REG_DST", 3)      # 0: rt, 1: rd, 2: 31($ra)
        self.mem_to_reg_mux = Multiplexer("MEM_TO_REG", 2)  # 0: ALU_OUT, 1: MDR
        self.pc_source_mux = Multiplexer("PC_SOURCE", 3)  # 0: ALU结果(PC+4), 1: 分支地址, 2: 跳转地址
        
        # 控制信号
        self.pc_write = False
        self.mem_read = False
        self.mem_write = False
        self.ir_write = False
        self.reg_write = False
        
        # 当前指令
        self.current_instruction = 0
        
        # 指令字段
        self.opcode = 0
        self.rs = 0
        self.rt = 0
        self.rd = 0
        self.shamt = 0
        self.funct = 0
        self.immediate = 0
        self.address = 0
    
    def set_control_signals(self, signals):
        """
        设置控制信号
        
        参数:
            signals: ControlSignals对象
        """
        # PC控制
        self.pc_write = signals.pc_write
        self.pc_source_mux.set_select(signals.pc_source)
        
        # 内存控制
        self.memory.set_read_enable(signals.mem_read)
        self.memory.set_write_enable(signals.mem_write)
        
        # 寄存器控制
        self.register_file.set_write_enable(signals.reg_write)
        self.reg_dst_mux.set_select(signals.reg_dst)
        
        # ALU控制
        self.alu_src_a_mux.set_select(signals.alu_src_a)
        self.alu_src_b_mux.set_select(signals.alu_src_b)
        self.alu.set_operation(signals.alu_op)
        
        # 数据路径控制
        self.mem_to_reg_mux.set_select(signals.mem_to_reg)
        
        # 指令寄存器控制
        self.ir.set_enable(signals.ir_write)
    
    def decode_instruction(self):
        """解码当前指令，提取各个字段"""
        self.current_instruction = self.ir.read()
        self.opcode = (self.current_instruction >> 26) & 0x3F
        self.rs = (self.current_instruction >> 21) & 0x1F
        self.rt = (self.current_instruction >> 16) & 0x1F
        self.rd = (self.current_instruction >> 11) & 0x1F
        self.shamt = (self.current_instruction >> 6) & 0x1F
        self.funct = self.current_instruction & 0x3F
        self.immediate = self.current_instruction & 0xFFFF
        
        # 符号扩展立即数
        if self.immediate & 0x8000:
            self.immediate |= 0xFFFF0000
        
        # 跳转地址
        self.address = self.current_instruction & 0x3FFFFFF
    
    def fetch_instruction(self):
        """
        取指令阶段
        
        返回:
            取出的指令
        """
        # 从PC指向的地址读取指令
        self.memory.set_read_enable(True)
        instruction = self.memory.read(self.pc.read())
        self.memory.set_read_enable(False)
        
        # 如果IR写使能有效，将指令写入IR
        if self.ir_write:
            self.ir.set_enable(True)
            self.ir.write(instruction)
            self.ir.set_enable(False)
        
        # 计算PC+4
        self.alu_src_a_mux.set_inputs([0, self.pc.read()])
        self.alu_src_b_mux.set_inputs([0, 0, 4])
        self.alu.set_inputs(self.alu_src_a_mux.get_output(), self.alu_src_b_mux.get_output())
        self.alu.set_operation(0)  # ADD
        next_pc = self.alu.execute()
        
        # 如果PC写使能有效，更新PC
        if self.pc_write:
            self.pc.set_enable(True)
            self.pc.write(next_pc)
            self.pc.set_enable(False)
        
        return instruction
    
    def read_registers(self):
        """读取寄存器阶段"""
        # 读取rs和rt寄存器的值
        rs_value = self.register_file.read(self.rs)
        rt_value = self.register_file.read(self.rt)
        
        # 将值存入A和B寄存器
        self.a.set_enable(True)
        self.a.write(rs_value)
        self.a.set_enable(False)
        
        self.b.set_enable(True)
        self.b.write(rt_value)
        self.b.set_enable(False)
    
    def execute(self):
        """
        执行阶段
        
        返回:
            ALU执行结果
        """
        # 设置ALU输入
        alu_input_a = self.a.read() if self.alu_src_a_mux.get_output() == 0 else self.pc.read()
        
        if self.alu_src_b_mux.get_output() == 0:
            alu_input_b = self.b.read()
        elif self.alu_src_b_mux.get_output() == 1:
            alu_input_b = self.immediate
        else:  # 2
            alu_input_b = 4
        
        self.alu.set_inputs(alu_input_a, alu_input_b)
        
        # 执行ALU操作
        result = self.alu.execute()
        
        # 将结果存入ALU_OUT寄存器
        self.alu_out.set_enable(True)
        self.alu_out.write(result)
        self.alu_out.set_enable(False)
        
        return result
    
    def memory_access(self):
        """
        访存阶段
        
        返回:
            从内存读取的数据（如果是加载指令）
        """
        address = self.alu_out.read()
        
        if self.mem_read:
            # 读内存
            self.memory.set_read_enable(True)
            data = self.memory.read(address)
            self.memory.set_read_enable(False)
            
            # 将数据存入MDR
            self.mdr.set_enable(True)
            self.mdr.write(data)
            self.mdr.set_enable(False)
            
            return data
        
        elif self.mem_write:
            # 写内存
            self.memory.set_write_enable(True)
            self.memory.write(address, self.b.read())
            self.memory.set_write_enable(False)
        
        return None
    
    def write_back(self):
        """写回阶段"""
        if self.reg_write:
            # 确定写入的寄存器编号
            if self.reg_dst_mux.get_output() == 0:
                reg_num = self.rt
            elif self.reg_dst_mux.get_output() == 1:
                reg_num = self.rd
            else:  # 2
                reg_num = 31  # $ra
            
            # 确定写入的数据
            if self.mem_to_reg_mux.get_output() == 0:
                data = self.alu_out.read()
            else:  # 1
                data = self.mdr.read()
            
            # 写入寄存器
            self.register_file.set_write_enable(True)
            self.register_file.write(reg_num, data)
            self.register_file.set_write_enable(False)
    
    def update_pc(self):
        """更新程序计数器"""
        if self.pc_write:
            # 确定PC的下一个值
            if self.pc_source_mux.get_output() == 0:
                # PC+4
                next_pc = self.alu_out.read()
            elif self.pc_source_mux.get_output() == 1:
                # 分支地址
                offset = self.immediate << 2
                next_pc = self.pc.read() + offset
            else:  # 2
                # 跳转地址
                next_pc = (self.pc.read() & 0xF0000000) | (self.address << 2)
            
            # 更新PC
            self.pc.set_enable(True)
            self.pc.write(next_pc)
            self.pc.set_enable(False)
    
    def reset(self):
        """重置数据通路状态"""
        self.pc.reset()
        self.register_file.reset()
        self.ir.reset()
        self.mdr.reset()
        self.alu_out.reset()
        self.a.reset()
        self.b.reset()
    
    def load_program(self, program, start_address=0):
        """
        加载程序到内存
        
        参数:
            program: 程序指令列表
            start_address: 起始地址
        """
        self.memory.load_program(program, start_address)
    
    def get_state(self):
        """
        获取数据通路当前状态
        
        返回:
            状态字典
        """
        return {
            'pc': self.pc.read(),
            'ir': self.ir.read(),
            'mdr': self.mdr.read(),
            'alu_out': self.alu_out.read(),
            'a': self.a.read(),
            'b': self.b.read(),
            'registers': [self.register_file.read(i) for i in range(32)],
            'alu_flags': self.alu.get_flags()
        }
    
    def __str__(self):
        """返回数据通路的字符串表示"""
        state = self.get_state()
        result = "数据通路状态:\n"
        result += f"PC: 0x{state['pc']:08X}\n"
        result += f"IR: 0x{state['ir']:08X}\n"
        result += f"MDR: 0x{state['mdr']:08X}\n"
        result += f"ALU_OUT: 0x{state['alu_out']:08X}\n"
        result += f"A: 0x{state['a']:08X}\n"
        result += f"B: 0x{state['b']:08X}\n"
        result += "寄存器:\n"
        for i, value in enumerate(state['registers']):
            result += f"  R{i}: 0x{value:08X}\n"
        zero, negative, overflow = state['alu_flags']
        result += f"ALU标志: Z={zero}, N={negative}, V={overflow}\n"
        return result


class SingleCycleDatapath(Datapath):
    """单周期CPU的数据通路"""
    
    def __init__(self):
        """初始化单周期数据通路"""
        super().__init__()
    
    def execute_instruction(self):
        """
        执行一条指令（单周期）
        
        返回:
            执行的指令
        """
        # 取指令
        instruction = self.fetch_instruction()
        
        # 解码指令
        self.decode_instruction()
        
        # 读取寄存器
        self.read_registers()
        
        # 执行
        self.execute()
        
        # 访存
        self.memory_access()
        
        # 写回
        self.write_back()
        
        # 更新PC
        self.update_pc()
        
        return instruction


class MultiCycleDatapath(Datapath):
    """多周期CPU的数据通路"""
    
    def __init__(self):
        """初始化多周期数据通路"""
        super().__init__()
        self.cycle_count = 0
    
    def execute_cycle(self, state):
        """
        执行一个时钟周期
        
        参数:
            state: 当前状态（FETCH, DECODE, EXECUTE, MEMORY, WRITEBACK）
            
        返回:
            执行的操作
        """
        self.cycle_count += 1
        
        if state == "FETCH":
            # 取指令阶段
            instruction = self.fetch_instruction()
            return f"取指令: 0x{instruction:08X}"
            
        elif state == "DECODE":
            # 解码阶段
            self.decode_instruction()
            self.read_registers()
            return f"解码指令: opcode={self.opcode}, rs={self.rs}, rt={self.rt}, rd={self.rd}, funct={self.funct}"
            
        elif state == "EXECUTE":
            # 执行阶段
            result = self.execute()
            return f"执行: ALU结果=0x{result:08X}"
            
        elif state == "MEMORY":
            # 访存阶段
            data = self.memory_access()
            if data is not None:
                return f"访存: 读取数据=0x{data:08X}"
            else:
                return "访存: 写入数据"
                
        elif state == "WRITEBACK":
            # 写回阶段
            self.write_back()
            return "写回: 更新寄存器"
            
        return "未知状态"
    
    def get_cycle_count(self):
        """
        获取执行的时钟周期数
        
        返回:
            周期数
        """
        return self.cycle_count 