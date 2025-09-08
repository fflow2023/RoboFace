import socket
import time

# 服务器配置
HOST = '0.0.0.0'  # 监听所有网络接口
PORT = 8888       # 监听端口

def parse_data(data):
    """解析接收到的舵机控制数据"""
    commands = []
    # 按空格分割成单个舵机命令
    parts = data.strip().split()
    for part in parts:
        try:
            # 每个命令格式为 "舵机ID,角度,移动时间"
            servo_id, angle, move_time = part.split(',')
            commands.append({
                'servo_id': int(servo_id),
                'angle': int(angle),
                'move_time': int(move_time)
            })
        except Exception as e:
            print(f"解析错误: {part} - {e}")
    return commands

def simulate_servo_control(commands):
    """模拟舵机控制（实际应用中替换为硬件控制）"""
    print(f"执行 {len(commands)} 个舵机命令:")
    for cmd in commands:
        print(f"舵机 {cmd['servo_id']:2d}: 角度={cmd['angle']:3d}, 时间={cmd['move_time']}ms")
        # 这里可以添加实际的舵机控制代码
        # 例如: control_servo(cmd['servo_id'], cmd['angle'], cmd['move_time'])
    
    # 模拟执行时间
    time.sleep(0.01)

def main():
    # 创建TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 设置端口重用选项
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # 绑定到指定地址和端口
        server_socket.bind((HOST, PORT))
        print(f"服务器启动，监听 {HOST}:{PORT}")
        
        # 开始监听，最多5个等待连接
        server_socket.listen(5)
        
        while True:
            print("等待客户端连接...")
            client_socket, addr = server_socket.accept()
            print(f"客户端已连接: {addr[0]}:{addr[1]}")
            
            try:
                # 接收数据缓冲区
                buffer = b""
                
                while True:
                    # 接收数据
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    # 添加到缓冲区
                    buffer += data
                    
                    # 检查是否包含换行符（表示完整命令）
                    while b"\n" in buffer:
                        # 分割出第一个完整命令
                        line, buffer = buffer.split(b"\n", 1)
                        
                        # 解码为字符串
                        try:
                            data_str = line.decode('utf-8')
                        except UnicodeDecodeError:
                            print("解码错误，跳过数据")
                            continue
                        
                        print(f"接收数据: {data_str}")
                        
                        # 解析数据
                        commands = parse_data(data_str)
                        
                        # 模拟舵机控制
                        simulate_servo_control(commands)
                
                print("客户端断开连接")
            except ConnectionResetError:
                print("客户端强制断开连接")
            except Exception as e:
                print(f"处理客户端时出错: {e}")
            finally:
                client_socket.close()
                print("客户端连接已关闭")
                
    except KeyboardInterrupt:
        print("\n服务器关闭中...")
    except Exception as e:
        print(f"服务器错误: {e}")
    finally:
        server_socket.close()
        print("服务器已关闭")

if __name__ == "__main__":
    main()