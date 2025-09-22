import socket
import random
import time

# Socket配置
ip = '192.168.31.118'  # 示例IP（根据需要调整）
# ip = '127.0.0.1'  # 示例IP（根据需要调整）
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

# 创建并连接socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))

def test_servo(servo_id):
    """测试指定舵机"""
    if servo_id not in servo_ranges:
        print(f"错误：舵机号 {servo_id} 无效！")
        return
    
    min_angle, max_angle = servo_ranges[servo_id]
    print(f"\n=== 测试舵机 {servo_id} ===")
    print(f"角度范围: {min_angle}° 到 {max_angle}°")
    
    # 测试25次随机运动
    for test_count in range(25):
        # 生成随机角度和移动时间
        angle = random.randint(min_angle, max_angle)
        # move_time = random.randint(50,50)  # 移动时间在100-500ms之间
        move_time = 50
        # 创建数据字符串
        if servo_id == 6 or servo_id == 13:
            # 如果测试的是6或13，同时控制两个舵机
            test_data = f"6,{angle} 13,{angle}"
            print(f"测试 {test_count+1}: 舵机6和13同时运动到角度={angle}°, 时间={move_time}ms")
        else:
            test_data = f"{servo_id},{angle}"
            print(f"测试 {test_count+1}: 角度={angle}°, 时间={move_time}ms")
        
        # 发送数据
        client_socket.send(test_data.encode())
        
        # 等待舵机完成运动
        time.sleep(0.3)  # 增加0.3秒缓冲时间
    
    # 返回中间位置
    mid_angle = 0
    
    if servo_id == 6 or servo_id == 13:
        # 如果测试的是6或13，同时复位两个舵机
        reset_data = f"6,{mid_angle} 13,{mid_angle}"
        print(f"舵机6和13已同时返回0位置: {mid_angle}°")
    else:
        reset_data = f"{servo_id},{mid_angle}"
        print(f"舵机 {servo_id} 已返回0位置: {mid_angle}°")
    
    client_socket.send(reset_data.encode())
    time.sleep(0.6)  # 等待复位完成

# 主循环
while True:
    try:
        input_str = input("\n请输入要测试的舵机号 (1-20)，或输入 'q' 退出: ")
        if input_str.lower() == 'q':
            break
        
        servo_id = int(input_str)
        test_servo(servo_id)
    except ValueError:
        print("输入无效，请输入1-20之间的数字或'q'退出")

# 发送完毕后关闭连接
client_socket.close()
print("\n测试结束，连接已关闭。")