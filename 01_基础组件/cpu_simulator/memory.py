"""
内存模块
这个模块实现了CPU的内存系统，包括读写操作和内存映射
"""

class Memory:
    """内存类，模拟计算机的主存储器"""
    
    def __init__(self, size=65536):
        """
        初始化内存
        
        参数:
            size: 内存大小（字节）
        """
        self.size = size
        self.data = [0] * size
    
    def read(self, address):
        """
        从指定地址读取一个字（32位）
        
        参数:
            address: 内存地址
            
        返回:
            读取的值
        """
        if 0 <= address < self.size:
            # 模拟32位字读取（4个字节）
            word = 0
            for i in range(4):
                if address + i < self.size:
                    word |= (self.data[address + i] & 0xFF) << (8 * i)
            return word
        else:
            raise ValueError(f"内存访问越界: {address}")
    
    def write(self, address, value):
        """
        向指定地址写入一个字（32位）
        
        参数:
            address: 内存地址
            value: 要写入的值
        """
        if 0 <= address < self.size:
            # 模拟32位字写入（4个字节）
            for i in range(4):
                if address + i < self.size:
                    self.data[address + i] = (value >> (8 * i)) & 0xFF
        else:
            raise ValueError(f"内存访问越界: {address}")
    
    def read_byte(self, address):
        """
        从指定地址读取一个字节
        
        参数:
            address: 内存地址
            
        返回:
            读取的字节值
        """
        if 0 <= address < self.size:
            return self.data[address]
        else:
            raise ValueError(f"内存访问越界: {address}")
    
    def write_byte(self, address, value):
        """
        向指定地址写入一个字节
        
        参数:
            address: 内存地址
            value: 要写入的字节值
        """
        if 0 <= address < self.size:
            self.data[address] = value & 0xFF
        else:
            raise ValueError(f"内存访问越界: {address}")
    
    def load_program(self, program, start_address=0):
        """
        加载程序到内存
        
        参数:
            program: 指令列表（二进制格式）
            start_address: 起始地址
        """
        address = start_address
        for instruction in program:
            self.write(address, instruction)
            address += 4  # 每条指令占4字节
    
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
        for i in range(count):
            address = start_address + i * 4
            if 0 <= address < self.size:
                value = self.read(address)
                result += f"0x{address:04X}: 0x{value:08X}\n"
        return result
    
    def clear(self):
        """清空内存"""
        for i in range(self.size):
            self.data[i] = 0


class MemoryMapper:
    """内存映射器，用于管理内存映射I/O和设备"""
    
    def __init__(self, memory):
        """
        初始化内存映射器
        
        参数:
            memory: Memory对象
        """
        self.memory = memory
        self.mappings = {}  # 地址范围到设备的映射
    
    def add_mapping(self, start_address, end_address, device):
        """
        添加内存映射
        
        参数:
            start_address: 起始地址
            end_address: 结束地址
            device: 设备对象（需要实现read和write方法）
        """
        self.mappings[(start_address, end_address)] = device
    
    def read(self, address):
        """
        从映射内存读取
        
        参数:
            address: 内存地址
            
        返回:
            读取的值
        """
        # 检查是否有设备映射到该地址
        for (start, end), device in self.mappings.items():
            if start <= address <= end:
                return device.read(address - start)
        
        # 如果没有映射，则从主内存读取
        return self.memory.read(address)
    
    def write(self, address, value):
        """
        向映射内存写入
        
        参数:
            address: 内存地址
            value: 要写入的值
        """
        # 检查是否有设备映射到该地址
        for (start, end), device in self.mappings.items():
            if start <= address <= end:
                device.write(address - start, value)
                return
        
        # 如果没有映射，则写入主内存
        self.memory.write(address, value) 