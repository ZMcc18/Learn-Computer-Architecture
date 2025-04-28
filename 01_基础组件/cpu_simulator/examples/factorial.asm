# 阶乘计算程序
# 这个程序计算5的阶乘 (5!)

# 初始化要计算阶乘的数 R1 = 5
LOAD R1, 5

# 初始化结果 R2 = 1
LOAD R2, 1

# 循环开始
# 标签: LOOP (地址: 8)

# 如果 R1 <= 0，跳转到 DONE
LOAD R3, 0
JUMP_EQ R1, R3, 28  # 如果 R1 == 0，跳转到 DONE

# 将当前数乘以结果
MUL R2, R2, R1

# 计数器减1
LOAD R4, 1
SUB R1, R1, R4

# 跳回循环开始
JUMP 8

# 循环结束
# 标签: DONE (地址: 28)

# 将结果存储到内存
STORE R2, 100

# 停止执行
HALT 