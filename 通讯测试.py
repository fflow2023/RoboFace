import socket
import random
import time

# Socket配置
ip = '127.0.0.1'  # 示例IP（根据需要调整）
port = 8888  # 示例端口（根据需要调整）

# 舵机角度范围（最小值，最大值）
servo_ranges = {
    1: (0, 63),  # 左下眼皮
    2: (-45, 63),  # 牙后左上
    3: (-27, 45),  # 牙后左下
    4: (-36, 27),  # 下颚左
    5: (-45, 18),  # 上鄂左
    6: (0, 58),  # 右嘴
    7: (-27, 36),  # 右后牙上
    8: (-27, 45),  # 右后牙下
    9: (-36, 36),  # 下颚右
    10: (-27, 63),  # 上鄂右
    11: (-36, 36),  # 眼左右
    12: (-22, 49),  # 眼上下
    13: (0, 58),  # 右嘴
    14: (0, 90),  # 左上眼皮
    15: (0, 81),  # 右上眼皮
    16: (0, 63),  # 右下眼皮
    17: (-40, 40),  # 右眉头
    18: (-45, 36),  # 右眉尾
    19: (-40, 40),  # 左眉头
    20: (-45, 27)  # 左眉尾
}


# 生成随机的测试数据
def generate_test_data():
    test_data = []
    for servo_id, (min_angle, max_angle) in servo_ranges.items():
        angle = random.randint(min_angle, max_angle)  # 生成随机整数角度
        move_time = random.randint(100, 500)  # 生成随机移动时间（ms），范围在100到500之间
        test_data.append(f"{servo_id},{angle},{move_time}")

    # 每两组数据一行
    data_lines = " ".join(test_data)
    return data_lines


# 创建并连接socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))

# 发送100组测试数据
for i in range(100):
    test_data = generate_test_data()
    print(f"发送测试数据: {test_data}")

    # 发送数据
    client_socket.send(test_data.encode())

    # 每发送一组数据后等待0.5秒
    time.sleep(0.5)

    # 每两组数据换行

    client_socket.send("\n".encode())  # 发送换行符

# 发送完毕后关闭连接
client_socket.close()
print("测试数据已成功发送，连接关闭。")
