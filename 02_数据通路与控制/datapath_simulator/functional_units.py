"""
功能单元模块
这个模块实现了CPU数据通路中的各个功能单元
"""

class Register:
    """通用寄存器类，用于存储数据"""
    
    def __init__(self, name, width=32, initial_value=0):
        """
        初始化寄存器
        
        参数:
            name: 寄存器名称
            width: 寄存器位宽
            initial_value: 初始值
        """
        self.name = name
        self.width = width
        self.value = initial_value
        self.enable = False  # 使能信号
    
    def read(self):
        """读取寄存器值"""
        return self.value
    
    def write(self, value):
        """
        写入寄存器
        
        参数:
            value: 要写入的值
        """
        if self.enable:
            # 截断为指定位宽
            mask = (1 << self.width) - 1
            self.value = value & mask
    
    def set_enable(self, enable):
        """
        设置使能信号
        
        参数:
            enable: 使能信号
        """
        self.enable = enable
    
    def reset(self):
        """重置寄存器值为0"""
        self.value = 0
    
    def __str__(self):
        """返回寄存器的字符串表示"""
        return f"{self.name}: 0x{self.value:08X} ({self.value})"


class ProgramCounter(Register):
    """程序计数器，存储下一条指令的地址"""
    
    def __init__(self, initial_value=0):
        """
        初始化程序计数器
        
        参数:
            initial_value: 初始值
        """
        super().__init__("PC", 32, initial_value)
    
    def increment(self, amount=4):
        """
        增加程序计数器的值
        
        参数:
            amount: 增加的数量
        """
        if self.enable:
            self.value = (self.value + amount) & 0xFFFFFFFF


class RegisterFile:
    """寄存器文件，包含多个通用寄存器"""
    
    def __init__(self, num_registers=32):
        """
        初始化寄存器文件
        
        参数:
            num_registers: 寄存器数量
        """
        self.registers = [Register(f"R{i}", 32, 0) for i in range(num_registers)]
        self.write_enable = False
        self.write_register = 0
    
    def read(self, register_num):
        """
        读取指定寄存器的值
        
        参数:
            register_num: 寄存器编号
            
        返回:
            寄存器的值
        """
        if 0 <= register_num < len(self.registers):
            return self.registers[register_num].read()
        else:
            raise ValueError(f"无效的寄存器编号: {register_num}")
    
    def write(self, register_num, value):
        """
        写入指定寄存器
        
        参数:
            register_num: 寄存器编号
            value: 要写入的值
        """
        if self.write_enable and register_num > 0:  # R0始终为0
            if 0 <= register_num < len(self.registers):
                self.registers[register_num].set_enable(True)
                self.registers[register_num].write(value)
                self.registers[register_num].set_enable(False)
    
    def set_write_enable(self, enable):
        """
        设置写使能信号
        
        参数:
            enable: 使能信号
        """
        self.write_enable = enable
    
    def set_write_register(self, register_num):
        """
        设置要写入的寄存器编号
        
        参数:
            register_num: 寄存器编号
        """
        self.write_register = register_num
    
    def reset(self):
        """重置所有寄存器"""
        for reg in self.registers:
            reg.reset()
    
    def __str__(self):
        """返回寄存器文件的字符串表示"""
        result = "寄存器文件:\n"
        for i, reg in enumerate(self.registers):
            result += f"R{i}: 0x{reg.read():08X}\n"
        return result


class ALU:
    """算术逻辑单元，执行算术和逻辑运算"""
    
    # ALU操作码
    ADD = 0
    SUB = 1
    AND = 2
    OR = 3
    XOR = 4
    SLL = 5  # 逻辑左移
    SRL = 6  # 逻辑右移
    SRA = 7  # 算术右移
    SLT = 8  # 小于则置位
    
    def __init__(self):
        """初始化ALU"""
        self.input_a = 0
        self.input_b = 0
        self.operation = self.ADD
        self.result = 0
        self.zero = False  # 零标志
        self.negative = False  # 负标志
        self.overflow = False  # 溢出标志
    
    def set_inputs(self, a, b):
        """
        设置ALU的输入
        
        参数:
            a: 输入A
            b: 输入B
        """
        self.input_a = a
        self.input_b = b
    
    def set_operation(self, operation):
        """
        设置ALU的操作
        
        参数:
            operation: 操作码
        """
        self.operation = operation
    
    def execute(self):
        """
        执行ALU操作
        
        返回:
            操作结果
        """
        if self.operation == self.ADD:
            self.result = (self.input_a + self.input_b) & 0xFFFFFFFF
        elif self.operation == self.SUB:
            self.result = (self.input_a - self.input_b) & 0xFFFFFFFF
        elif self.operation == self.AND:
            self.result = self.input_a & self.input_b
        elif self.operation == self.OR:
            self.result = self.input_a | self.input_b
        elif self.operation == self.XOR:
            self.result = self.input_a ^ self.input_b
        elif self.operation == self.SLL:
            self.result = (self.input_a << (self.input_b & 0x1F)) & 0xFFFFFFFF
        elif self.operation == self.SRL:
            self.result = (self.input_a >> (self.input_b & 0x1F)) & 0xFFFFFFFF
        elif self.operation == self.SRA:
            # 算术右移需要保持符号位
            shift = self.input_b & 0x1F
            if (self.input_a & 0x80000000) != 0:  # 负数
                mask = (0xFFFFFFFF << (32 - shift)) & 0xFFFFFFFF
                self.result = ((self.input_a >> shift) | mask) & 0xFFFFFFFF
            else:
                self.result = (self.input_a >> shift) & 0xFFFFFFFF
        elif self.operation == self.SLT:
            # 有符号比较
            if ((self.input_a ^ self.input_b) & 0x80000000) != 0:
                # 符号不同
                self.result = 1 if (self.input_a & 0x80000000) != 0 else 0
            else:
                # 符号相同
                self.result = 1 if (self.input_a & 0x7FFFFFFF) < (self.input_b & 0x7FFFFFFF) else 0
        else:
            raise ValueError(f"无效的ALU操作码: {self.operation}")
        
        # 更新标志位
        self.zero = (self.result == 0)
        self.negative = ((self.result & 0x80000000) != 0)
        
        # 检查溢出（仅对ADD和SUB有效）
        if self.operation == self.ADD:
            self.overflow = (((self.input_a & 0x80000000) == (self.input_b & 0x80000000)) and
                            ((self.result & 0x80000000) != (self.input_a & 0x80000000)))
        elif self.operation == self.SUB:
            self.overflow = (((self.input_a & 0x80000000) != (self.input_b & 0x80000000)) and
                            ((self.result & 0x80000000) != (self.input_a & 0x80000000)))
        else:
            self.overflow = False
        
        return self.result
    
    def get_flags(self):
        """
        获取ALU标志位
        
        返回:
            (zero, negative, overflow)
        """
        return (self.zero, self.negative, self.overflow)


class Memory:
    """内存模块，用于存储指令和数据"""
    
    def __init__(self, size=1024):
        """
        初始化内存
        
        参数:
            size: 内存大小（字）
        """
        self.size = size
        self.data = [0] * size
        self.read_enable = False
        self.write_enable = False
    
    def read(self, address):
        """
        从内存读取数据
        
        参数:
            address: 内存地址
            
        返回:
            读取的数据
        """
        if self.read_enable:
            word_address = address >> 2  # 字地址
            if 0 <= word_address < self.size:
                return self.data[word_address]
            else:
                raise ValueError(f"内存地址越界: {address}")
        return 0
    
    def write(self, address, value):
        """
        向内存写入数据
        
        参数:
            address: 内存地址
            value: 要写入的数据
        """
        if self.write_enable:
            word_address = address >> 2  # 字地址
            if 0 <= word_address < self.size:
                self.data[word_address] = value & 0xFFFFFFFF
            else:
                raise ValueError(f"内存地址越界: {address}")
    
    def set_read_enable(self, enable):
        """
        设置读使能信号
        
        参数:
            enable: 使能信号
        """
        self.read_enable = enable
    
    def set_write_enable(self, enable):
        """
        设置写使能信号
        
        参数:
            enable: 使能信号
        """
        self.write_enable = enable
    
    def load_program(self, program, start_address=0):
        """
        加载程序到内存
        
        参数:
            program: 程序数据列表
            start_address: 起始地址
        """
        word_address = start_address >> 2
        for i, word in enumerate(program):
            if 0 <= word_address + i < self.size:
                self.data[word_address + i] = word & 0xFFFFFFFF
            else:
                raise ValueError(f"程序加载地址越界: {(word_address + i) << 2}")
    
    def dump(self, start_address, count):
        """
        转储内存内容
        
        参数:
            start_address: 起始地址
            count: 要转储的字数
            
        返回:
            内存内容的字符串表示
        """
        result = "内存内容:\n"
        word_address = start_address >> 2
        for i in range(count):
            if 0 <= word_address + i < self.size:
                value = self.data[word_address + i]
                result += f"0x{((word_address + i) << 2):08X}: 0x{value:08X}\n"
        return result


class Multiplexer:
    """多路复用器，根据选择信号选择输入"""
    
    def __init__(self, name, num_inputs=2):
        """
        初始化多路复用器
        
        参数:
            name: 多路复用器名称
            num_inputs: 输入数量
        """
        self.name = name
        self.inputs = [0] * num_inputs
        self.select = 0
    
    def set_inputs(self, inputs):
        """
        设置多路复用器的输入
        
        参数:
            inputs: 输入列表
        """
        if len(inputs) <= len(self.inputs):
            for i, value in enumerate(inputs):
                self.inputs[i] = value
        else:
            raise ValueError(f"输入数量超过多路复用器容量: {len(inputs)} > {len(self.inputs)}")
    
    def set_select(self, select):
        """
        设置选择信号
        
        参数:
            select: 选择信号
        """
        if 0 <= select < len(self.inputs):
            self.select = select
        else:
            raise ValueError(f"无效的选择信号: {select}")
    
    def get_output(self):
        """
        获取多路复用器的输出
        
        返回:
            选中的输入
        """
        return self.inputs[self.select]
    
    def __str__(self):
        """返回多路复用器的字符串表示"""
        return f"{self.name}: 选择={self.select}, 输出=0x{self.get_output():08X}" 