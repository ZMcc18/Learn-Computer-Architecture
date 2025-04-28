"""
总线模块
这个模块实现了CPU中的总线系统，用于连接各个功能单元
"""

class Bus:
    """总线类，用于在功能单元之间传输数据"""
    
    def __init__(self, name, width=32):
        """
        初始化总线
        
        参数:
            name: 总线名称
            width: 总线位宽
        """
        self.name = name
        self.width = width
        self.value = 0
        self.devices = []  # 连接到总线的设备列表
        self.active_device = None  # 当前活动设备（驱动总线的设备）
    
    def connect(self, device):
        """
        将设备连接到总线
        
        参数:
            device: 要连接的设备
        """
        if device not in self.devices:
            self.devices.append(device)
    
    def disconnect(self, device):
        """
        将设备从总线断开
        
        参数:
            device: 要断开的设备
        """
        if device in self.devices:
            self.devices.remove(device)
            if self.active_device == device:
                self.active_device = None
    
    def set_active_device(self, device):
        """
        设置活动设备（驱动总线的设备）
        
        参数:
            device: 要设置为活动设备的设备
        """
        if device in self.devices:
            self.active_device = device
        else:
            raise ValueError(f"设备 {device} 未连接到总线 {self.name}")
    
    def write(self, value):
        """
        向总线写入数据
        
        参数:
            value: 要写入的数据
        """
        # 截断为总线位宽
        mask = (1 << self.width) - 1
        self.value = value & mask
    
    def read(self):
        """
        从总线读取数据
        
        返回:
            总线上的数据
        """
        return self.value
    
    def __str__(self):
        """返回总线的字符串表示"""
        return f"{self.name}: 0x{self.value:X} ({len(self.devices)}个设备连接)"


class BusDevice:
    """总线设备基类，可以连接到总线并进行数据传输"""
    
    def __init__(self, name):
        """
        初始化总线设备
        
        参数:
            name: 设备名称
        """
        self.name = name
        self.buses = {}  # 连接的总线字典 {总线名称: 总线对象}
    
    def connect_to_bus(self, bus):
        """
        连接到总线
        
        参数:
            bus: 要连接的总线
        """
        self.buses[bus.name] = bus
        bus.connect(self)
    
    def disconnect_from_bus(self, bus_name):
        """
        从总线断开
        
        参数:
            bus_name: 要断开的总线名称
        """
        if bus_name in self.buses:
            bus = self.buses[bus_name]
            bus.disconnect(self)
            del self.buses[bus_name]
    
    def read_from_bus(self, bus_name):
        """
        从总线读取数据
        
        参数:
            bus_name: 要读取的总线名称
            
        返回:
            总线上的数据
        """
        if bus_name in self.buses:
            return self.buses[bus_name].read()
        else:
            raise ValueError(f"设备 {self.name} 未连接到总线 {bus_name}")
    
    def write_to_bus(self, bus_name, value):
        """
        向总线写入数据
        
        参数:
            bus_name: 要写入的总线名称
            value: 要写入的数据
        """
        if bus_name in self.buses:
            bus = self.buses[bus_name]
            bus.set_active_device(self)
            bus.write(value)
        else:
            raise ValueError(f"设备 {self.name} 未连接到总线 {bus_name}")
    
    def __str__(self):
        """返回设备的字符串表示"""
        return f"{self.name} (连接到 {len(self.buses)} 条总线)"


class BusSystem:
    """总线系统，管理多条总线和连接的设备"""
    
    def __init__(self):
        """初始化总线系统"""
        self.buses = {}  # 总线字典 {总线名称: 总线对象}
        self.devices = {}  # 设备字典 {设备名称: 设备对象}
    
    def create_bus(self, name, width=32):
        """
        创建总线
        
        参数:
            name: 总线名称
            width: 总线位宽
            
        返回:
            创建的总线对象
        """
        bus = Bus(name, width)
        self.buses[name] = bus
        return bus
    
    def add_device(self, device):
        """
        添加设备
        
        参数:
            device: 要添加的设备
            
        返回:
            添加的设备对象
        """
        self.devices[device.name] = device
        return device
    
    def connect_device_to_bus(self, device_name, bus_name):
        """
        将设备连接到总线
        
        参数:
            device_name: 设备名称
            bus_name: 总线名称
        """
        if device_name in self.devices and bus_name in self.buses:
            device = self.devices[device_name]
            bus = self.buses[bus_name]
            device.connect_to_bus(bus)
        else:
            if device_name not in self.devices:
                raise ValueError(f"设备 {device_name} 不存在")
            else:
                raise ValueError(f"总线 {bus_name} 不存在")
    
    def disconnect_device_from_bus(self, device_name, bus_name):
        """
        将设备从总线断开
        
        参数:
            device_name: 设备名称
            bus_name: 总线名称
        """
        if device_name in self.devices:
            device = self.devices[device_name]
            device.disconnect_from_bus(bus_name)
    
    def transfer_data(self, source_device, dest_device, bus_name, value):
        """
        通过总线在设备之间传输数据
        
        参数:
            source_device: 源设备名称
            dest_device: 目标设备名称
            bus_name: 总线名称
            value: 要传输的数据
        """
        if source_device in self.devices and dest_device in self.devices and bus_name in self.buses:
            # 源设备写入总线
            self.devices[source_device].write_to_bus(bus_name, value)
            
            # 目标设备从总线读取
            return self.devices[dest_device].read_from_bus(bus_name)
        else:
            if source_device not in self.devices:
                raise ValueError(f"源设备 {source_device} 不存在")
            elif dest_device not in self.devices:
                raise ValueError(f"目标设备 {dest_device} 不存在")
            else:
                raise ValueError(f"总线 {bus_name} 不存在")
    
    def get_bus_state(self, bus_name):
        """
        获取总线状态
        
        参数:
            bus_name: 总线名称
            
        返回:
            总线状态字典
        """
        if bus_name in self.buses:
            bus = self.buses[bus_name]
            return {
                'name': bus.name,
                'width': bus.width,
                'value': bus.value,
                'devices': [device.name for device in bus.devices],
                'active_device': bus.active_device.name if bus.active_device else None
            }
        else:
            raise ValueError(f"总线 {bus_name} 不存在")
    
    def __str__(self):
        """返回总线系统的字符串表示"""
        result = "总线系统:\n"
        
        # 总线信息
        result += "总线:\n"
        for name, bus in self.buses.items():
            result += f"  {bus}\n"
        
        # 设备信息
        result += "设备:\n"
        for name, device in self.devices.items():
            result += f"  {device}\n"
        
        return result


# 示例总线设备实现
class RegisterBusDevice(BusDevice):
    """寄存器总线设备，可以存储数据并通过总线传输"""
    
    def __init__(self, name, width=32):
        """
        初始化寄存器总线设备
        
        参数:
            name: 设备名称
            width: 寄存器位宽
        """
        super().__init__(name)
        self.width = width
        self.value = 0
    
    def read(self):
        """
        读取寄存器值
        
        返回:
            寄存器值
        """
        return self.value
    
    def write(self, value):
        """
        写入寄存器
        
        参数:
            value: 要写入的值
        """
        # 截断为寄存器位宽
        mask = (1 << self.width) - 1
        self.value = value & mask
    
    def __str__(self):
        """返回寄存器总线设备的字符串表示"""
        return f"{self.name}: 0x{self.value:X} (连接到 {len(self.buses)} 条总线)"


class MemoryBusDevice(BusDevice):
    """内存总线设备，可以存储多个数据并通过总线传输"""
    
    def __init__(self, name, size=1024):
        """
        初始化内存总线设备
        
        参数:
            name: 设备名称
            size: 内存大小（字）
        """
        super().__init__(name)
        self.size = size
        self.data = [0] * size
        self.address = 0
    
    def set_address(self, address):
        """
        设置内存地址
        
        参数:
            address: 内存地址
        """
        if 0 <= address < self.size:
            self.address = address
        else:
            raise ValueError(f"内存地址越界: {address}")
    
    def read(self):
        """
        读取内存
        
        返回:
            内存数据
        """
        return self.data[self.address]
    
    def write(self, value):
        """
        写入内存
        
        参数:
            value: 要写入的值
        """
        self.data[self.address] = value & 0xFFFFFFFF
    
    def __str__(self):
        """返回内存总线设备的字符串表示"""
        return f"{self.name}: 大小={self.size}字 (连接到 {len(self.buses)} 条总线)" 