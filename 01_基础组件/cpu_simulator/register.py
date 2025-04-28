"""
寄存器文件模块
这个模块实现了CPU的寄存器文件，包括通用寄存器和特殊寄存器
"""

class RegisterFile:
    """寄存器文件类，管理CPU的所有寄存器"""
    
    def __init__(self, num_registers=16):
        """
        初始化寄存器文件
        
        参数:
            num_registers: 通用寄存器数量
        """
        # 通用寄存器 (R0-R15)
        self.registers = [0] * num_registers
        
        # 程序计数器 (PC)
        self.pc = 0
        
        # 状态寄存器 (SR)
        # 包含标志位: 零标志(Z), 负标志(N), 进位标志(C), 溢出标志(V)
        self.sr = {
            'Z': False,  # 零标志
            'N': False,  # 负标志
            'C': False,  # 进位标志
            'V': False   # 溢出标志
        }
    
    def read_register(self, reg_num):
        """
        读取通用寄存器的值
        
        参数:
            reg_num: 寄存器编号
            
        返回:
            寄存器的值
        """
        if 0 <= reg_num < len(self.registers):
            return self.registers[reg_num]
        else:
            raise ValueError(f"无效的寄存器编号: {reg_num}")
    
    def write_register(self, reg_num, value):
        """
        写入通用寄存器
        
        参数:
            reg_num: 寄存器编号
            value: 要写入的值
        """
        if 0 <= reg_num < len(self.registers):
            self.registers[reg_num] = value
        else:
            raise ValueError(f"无效的寄存器编号: {reg_num}")
    
    def read_pc(self):
        """
        读取程序计数器的值
        
        返回:
            程序计数器的值
        """
        return self.pc
    
    def write_pc(self, value):
        """
        写入程序计数器
        
        参数:
            value: 要写入的值
        """
        self.pc = value
    
    def increment_pc(self, amount=1):
        """
        增加程序计数器的值
        
        参数:
            amount: 增加的数量
        """
        self.pc += amount
    
    def read_flag(self, flag):
        """
        读取状态寄存器中的标志位
        
        参数:
            flag: 标志位名称 ('Z', 'N', 'C', 'V')
            
        返回:
            标志位的值
        """
        if flag in self.sr:
            return self.sr[flag]
        else:
            raise ValueError(f"无效的标志位: {flag}")
    
    def write_flag(self, flag, value):
        """
        写入状态寄存器中的标志位
        
        参数:
            flag: 标志位名称 ('Z', 'N', 'C', 'V')
            value: 要写入的值 (True/False)
        """
        if flag in self.sr:
            self.sr[flag] = bool(value)
        else:
            raise ValueError(f"无效的标志位: {flag}")
    
    def update_flags(self, result, carry=False, overflow=False):
        """
        根据运算结果更新状态寄存器的标志位
        
        参数:
            result: 运算结果
            carry: 是否有进位
            overflow: 是否有溢出
        """
        # 更新零标志 (Z)
        self.sr['Z'] = (result == 0)
        
        # 更新负标志 (N)
        self.sr['N'] = (result < 0)
        
        # 更新进位标志 (C)
        self.sr['C'] = carry
        
        # 更新溢出标志 (V)
        self.sr['V'] = overflow
    
    def reset(self):
        """重置所有寄存器"""
        # 重置通用寄存器
        for i in range(len(self.registers)):
            self.registers[i] = 0
        
        # 重置程序计数器
        self.pc = 0
        
        # 重置状态寄存器
        for flag in self.sr:
            self.sr[flag] = False
    
    def __str__(self):
        """返回寄存器文件的字符串表示"""
        result = "寄存器状态:\n"
        
        # 通用寄存器
        for i, value in enumerate(self.registers):
            result += f"R{i}: {value}\n"
        
        # 程序计数器
        result += f"PC: {self.pc}\n"
        
        # 状态寄存器
        result += "SR: "
        for flag, value in self.sr.items():
            if value:
                result += flag
            else:
                result += "-"
        
        return result 