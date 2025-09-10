# tools.py - 工具函数和舵机控制函数
import socket
import random
import time
import numpy as np
import cv2
from config import *

# 全局socket连接
client_socket = None
intervaltime = int(1/FPS * 1000)

# 调试模式开关
DEBUG_MODE = False  # 设置为True启用详细调试信息

# 用于存储上次舵机角度值，用于检测变化
last_servo_angles = {}

def init_socket_connection():
    """初始化socket连接"""
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        print(f"已连接到舵机控制服务器: {ip}:{port}")
    except Exception as e:
        print(f"连接失败: {e}")
        client_socket = None

def close_socket_connection():
    """关闭socket连接"""
    global client_socket
    if client_socket:
        client_socket.close()
        client_socket = None
    print(" \n 已关闭舵机控制连接")

def send_servo_commands(commands):
    """发送舵机控制命令"""
    if not client_socket:
        print(" | 未连接到舵机服务器，跳过发送", end='', flush=True)
        return
    
    try:
        command_str = " ".join(commands)  # 添加换行符
        if DEBUG_MODE:
            print(f"  | 已发送命令: {command_str}", end='', flush=True)
        command_str += "\n"  # 添加换行符
        client_socket.send(command_str.encode())
    except Exception as e:
        print(f" | 命令发送失败: {e}", end='', flush=True)

def map_value(value, from_min, from_max, to_min, to_max):
    """
    将值从一个范围映射到另一个范围
    """
    # 确保值在原始范围内
    value = max(min(value, from_max), from_min)
    
    # 计算映射后的值
    from_range = from_max - from_min
    to_range = to_max - to_min
    scaled_value = (value - from_min) / from_range
    return to_min + (scaled_value * to_range)

def debug_servo_angle(servo_id, angle):
    """调试函数，显示舵机角度变化"""
    global last_servo_angles
    
    # 初始化上次角度值
    if servo_id not in last_servo_angles:
        last_servo_angles[servo_id] = angle
    
    # 如果角度变化超过1度，显示变化
    if abs(angle - last_servo_angles[servo_id]) > 1 or DEBUG_MODE:
        print(f"\n舵机 {servo_id:2d}: {angle:6.1f}°", end='', flush=True)
        last_servo_angles[servo_id] = angle

# 舵机控制函数
def control_servo_1(bs):
    """左下眼皮控制"""
    value = bs.get("eyeBlinkLeft", 0) * SENSITIVITY["eyelid_left_close"]
    min_angle, max_angle = servo_ranges[1]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(1, angle)
    return f"1,{int(angle)},{intervaltime}"

def control_servo_2(bs):
    """牙后左上控制"""
    value = bs.get("jawOpen", 0) * SENSITIVITY["jaw_open"]
    min_angle, max_angle = servo_ranges[2]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(2, angle)
    return f"2,{int(angle)},{intervaltime}"

def control_servo_3(bs):
    """牙后左下控制"""
    value = bs.get("jawOpen", 0) * SENSITIVITY["jaw_open"]
    min_angle, max_angle = servo_ranges[3]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(3, angle)
    return f"3,{int(angle)},{intervaltime}"

def control_servo_4(bs):
    """下颚颚左控制"""
    value = bs.get("jawLeft", 0) * SENSITIVITY["jaw_open"]
    min_angle, max_angle = servo_ranges[4]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(4, angle)
    return f"4,{int(angle)},{intervaltime}"

def control_servo_5(bs):
    """上鄂左控制"""
    value = bs.get("jawOpen", 0) * SENSITIVITY["jaw_open"]
    min_angle, max_angle = servo_ranges[5]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(5, angle)
    return f"5,{int(angle)},{intervaltime}"

def control_servo_6(bs):
    """左嘴控制"""
    value = (bs.get("mouthSmileLeft", 0) + bs.get("mouthStretchLeft", 0)) / 2 * SENSITIVITY["mouth_left_smile"]
    min_angle, max_angle = servo_ranges[6]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(6, angle)
    return f"6,{int(angle)},{intervaltime}"

def control_servo_7(bs):
    """右后牙上控制"""
    value = bs.get("jawOpen", 0) * SENSITIVITY["jaw_open"]
    min_angle, max_angle = servo_ranges[7]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(7, angle)
    return f"7,{int(angle)},{intervaltime}"

def control_servo_8(bs):
    """右后牙下控制"""
    value = bs.get("jawOpen", 0) * SENSITIVITY["jaw_open"]
    min_angle, max_angle = servo_ranges[8]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(8, angle)
    return f"8,{int(angle)},{intervaltime}"

def control_servo_9(bs):
    """下颚颚右控制"""
    value = bs.get("jawRight", 0) * SENSITIVITY["jaw_open"]
    min_angle, max_angle = servo_ranges[9]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(9, angle)
    return f"9,{int(angle)},{intervaltime}"

def control_servo_10(bs):
    """上鄂右控制"""
    value = bs.get("jawOpen", 0) * SENSITIVITY["jaw_open"]
    min_angle, max_angle = servo_ranges[10]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(10, angle)
    return f"10,{int(angle)},{intervaltime}"

def control_servo_11(bs):
    """眼球左右控制"""
    left = max(bs.get("eyeLookOutLeft", 0), bs.get("eyeLookInRight", 0))
    right = max(bs.get("eyeLookOutRight", 0), bs.get("eyeLookInLeft", 0))
    
    if left > right:
        value = left * SENSITIVITY["eye_left"]
        min_angle, max_angle = servo_ranges[11]
        angle = map_value(value, 0, 1, 0, max_angle)  # 向左为正
    else:
        value = right * SENSITIVITY["eye_right"]
        min_angle, max_angle = servo_ranges[11]
        angle = map_value(value, 0, 1, min_angle, 0)  # 向右为负
    
    if DEBUG_MODE: debug_servo_angle(11, angle)
    return f"11,{int(angle)},{intervaltime}"

def control_servo_12(bs):
    """眼球上下控制"""
    up = max(bs.get("eyeLookUpLeft", 0), bs.get("eyeLookUpRight", 0))
    down = max(bs.get("eyeLookDownLeft", 0), bs.get("eyeLookDownRight", 0))
    
    if up > down:
        value = up * SENSITIVITY["eye_up"]
        min_angle, max_angle = servo_ranges[12]
        angle = map_value(value, 0, 1, 0, max_angle)  # 向上为正
    else:
        value = down * SENSITIVITY["eye_down"]
        min_angle, max_angle = servo_ranges[12]
        angle = map_value(value, 0, 1, min_angle, 0)  # 向下为负
    
    if DEBUG_MODE: debug_servo_angle(12, angle)
    return f"12,{int(angle)},{intervaltime}"

def control_servo_13(bs):
    """右嘴控制（与左嘴对称）"""
    # 与舵机6保持相同角度
    value = (bs.get("mouthSmileRight", 0) + bs.get("mouthStretchRight", 0)) / 2 * SENSITIVITY["mouth_right_smile"]
    min_angle, max_angle = servo_ranges[13]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(13, angle)
    return f"13,{int(angle)},{intervaltime}"

def control_servo_14(bs):
    """左上眼皮控制"""
    value = bs.get("eyeBlinkLeft", 0) * SENSITIVITY["eyelid_left_close"]
    min_angle, max_angle = servo_ranges[14]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(14, angle)
    return f"14,{int(angle)},{intervaltime}"

def control_servo_15(bs):
    """右上眼皮控制"""
    value = bs.get("eyeBlinkRight", 0) * SENSITIVITY["eyelid_right_close"]
    min_angle, max_angle = servo_ranges[15]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(15, angle)
    return f"15,{int(angle)},{intervaltime}"

def control_servo_16(bs):
    """右下眼皮控制"""
    value = bs.get("eyeBlinkRight", 0) * SENSITIVITY["eyelid_right_close"]
    min_angle, max_angle = servo_ranges[16]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(16, angle)
    return f"16,{int(angle)},{intervaltime}"

def control_servo_17(bs):
    """右眉头控制"""
    value = bs.get("browDownRight", 0) * SENSITIVITY["eyebrow_right_down"]
    min_angle, max_angle = servo_ranges[17]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(17, angle)
    return f"17,{int(angle)},{intervaltime}"

def control_servo_18(bs):
    """右眉尾控制"""
    value = bs.get("browOuterUpRight", 0) * SENSITIVITY["eyebrow_right_up"]
    min_angle, max_angle = servo_ranges[18]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(18, angle)
    return f"18,{int(angle)},{intervaltime}"

def control_servo_19(bs):
    """左眉头控制"""
    value = bs.get("browDownLeft", 0) * SENSITIVITY["eyebrow_left_down"]
    min_angle, max_angle = servo_ranges[19]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(19, angle)
    return f"19,{int(angle)},{intervaltime}"

def control_servo_20(bs):
    """左眉尾控制"""
    value = bs.get("browOuterUpLeft", 0) * SENSITIVITY["eyebrow_left_up"]
    min_angle, max_angle = servo_ranges[20]
    angle = map_value(value, 0, 1, min_angle, max_angle)
    if DEBUG_MODE: debug_servo_angle(20, angle)
    return f"20,{int(angle)},{intervaltime}"

def process_all_servos(blendshapes_dict):
    """
    处理所有舵机控制的总入口函数
    返回: 舵机命令列表
    """
    commands = []
    
    # 打印头部
    if DEBUG_MODE:
        print("\n" + "="*80)
        print("舵机角度调试信息:")
        print("="*80)
    
    # 调用每个舵机的控制函数
    for servo_id in range(1, 21):
        try:
            # 获取舵机控制函数
            control_func = globals().get(f"control_servo_{servo_id}")
            if control_func:
                cmd = control_func(blendshapes_dict)
                if cmd:
                    commands.append(cmd)
        except Exception as e:
            print(f" | 舵机{servo_id}控制出错: {e}")
    
    # 打印眼球位置信息
    eye_v_cmd = next((c for c in commands if c.startswith("12,")), None)
    eye_h_cmd = next((c for c in commands if c.startswith("11,")), None)
    if eye_v_cmd and eye_h_cmd:
        v_angle = eye_v_cmd.split(",")[1]
        h_angle = eye_h_cmd.split(",")[1]
        print(f"\r眼球垂直: {v_angle}° | 水平: {h_angle}°    ", end='', flush=True)
    
    # 打印分隔线
    if DEBUG_MODE:
        print("="*80)
    
    return commands