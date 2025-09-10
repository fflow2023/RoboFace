# config.py - 参数配置文件
# Socket配置

ip = '127.0.0.1'  # 示例IP（根据需要调整）
port = 8888  # 示例端口（根据需要调整）


# 模型路径
MODEL_PATH = 'face_landmarker_v2_with_blendshapes.task'

# 默认文件路径
DEFAULT_IMG_PATH = 'tests/test_image.jpg'      # 模式1默认测试图
DEFAULT_VIDEO_PATH = 'tests/test_video.mp4'  # 模式3默认测试视频

# 窗口名称
FPS = 20
WIN_NAME = 'MediaPipe FaceLandmarker (' + str(FPS) + ' FPS)'

# 灵敏度设置
SENSITIVITY = {
    # 眼球控制
    "eye_up": 1.0,
    "eye_down": 1.0,
    "eye_left": 1.0,
    "eye_right": 1.0,
    
    # 眼皮控制 (预留)
    "eyelid_left_open": 1.0,
    "eyelid_left_close": 1.0,
    "eyelid_right_open": 1.0,
    "eyelid_right_close": 1.0,
    
    # 眉毛控制 (预留)
    "eyebrow_left_up": 1.0,
    "eyebrow_left_down": 1.0,
    "eyebrow_right_up": 1.0,
    "eyebrow_right_down": 1.0,
    
    # 嘴巴控制 (预留)
    "mouth_left_smile": 1.0,
    "mouth_left_frown": 1.0,
    "mouth_right_smile": 1.0,
    "mouth_right_frown": 1.0,
    
    # 下颌控制 (预留)
    "jaw_open": 1.0,
    "jaw_close": 1.0,
}


# 舵机角度范围（最小值，最大值）
servo_ranges = {
    # 除标注外，所有角度均为正上负下；初始值角度均为0
    1: (0, 63),  # 左下眼皮 （小闭大张）
    2: (-45, 63),  # 牙后左上 
    3: (-27, 45),  # 牙后左下
    4: (-36, 27),  # 下颚左
    5: (-45, 18),  # 上鄂左
    6: (0, 58),  # 左嘴 （小闭大张 左右嘴的角度必须相同!）
    7: (-27, 36),  # 右后牙上
    8: (-27, 45),  # 右后牙下
    9: (-36, 36),  # 下颚右
    10: (-27, 63),  # 上鄂右
    11: (-36, 36),  # 眼左右 （右负左正）
    12: (-22, 49),  # 眼上下
    13: (0, 58),  # 右嘴（小闭大张 左右嘴的角度必须相同!）
    14: (0, 90),  # 左上眼皮 （小闭大张）
    15: (0, 81),  # 右上眼皮 （小闭大张）
    16: (0, 63),  # 右下眼皮 （小闭大张）
    17: (-40, 40),  # 右眉头
    18: (-45, 36),  # 右眉尾
    19: (-40, 40),  # 左眉头
    20: (-45, 27)  # 左眉尾
}

# ========== 52 维 BlendShape → 中文动作对照表 ==========
BS_CN = {
    "browDownLeft": "左眉下降", "browDownRight": "右眉下降",
    "browInnerUp": "眉心上升", "browOuterUpLeft": "左眉尾上升", "browOuterUpRight": "右眉尾上升",
    "cheekPuff": "鼓腮", "cheekSquintLeft": "左颊眯紧", "cheekSquintRight": "右颊眯紧",
    "eyeBlinkLeft": "左眼眨", "eyeBlinkRight": "右眼眨",
    "eyeLookDownLeft": "左眼向下", "eyeLookDownRight": "右眼向下",
    "eyeLookInLeft": "左眼内收", "eyeLookInRight": "右眼内收",
    "eyeLookOutLeft": "左眼外展", "eyeLookOutRight": "右眼外展",
    "eyeLookUpLeft": "左眼向上", "eyeLookUpRight": "右眼向上",
    "eyeSquintLeft": "左眼眯紧", "eyeSquintRight": "右眼眯紧",
    "eyeWideLeft": "左眼瞪大", "eyeWideRight": "右眼瞪大",
    "jawForward": "下颌前伸", "jawLeft": "下颌左偏", "jawRight": "下颌右偏",
    "jawOpen": "张口", "mouthClose": "闭口", "mouthFrownLeft": "左嘴角下垂",
    "mouthFrownRight": "右嘴角下垂", "mouthFunnel": "噘嘴圆孔", "mouthPucker": "噘嘴",
    "mouthLeft": "嘴向左", "mouthRight": "嘴向右",
    "mouthSmileLeft": "左嘴角上扬", "mouthSmileRight": "右嘴角上扬",
    "mouthDimpleLeft": "左酒窝", "mouthDimpleRight": "右酒窝",
    "mouthStretchLeft": "左嘴角拉伸", "mouthStretchRight": "右嘴角拉伸",
    "mouthRollLower": "下唇卷", "mouthRollUpper": "上唇卷",
    "mouthShrugLower": "下唇耸", "mouthShrugUpper": "上唇耸",
    "mouthPressLeft": "左唇压紧", "mouthPressRight": "右唇压紧",
    "mouthLowerDownLeft": "左下唇下降", "mouthLowerDownRight": "右下唇下降",
    "mouthUpperUpLeft": "左上唇上升", "mouthUpperUpRight": "右上唇上升",
    "noseSneerLeft": "左鼻皱", "noseSneerRight": "右鼻皱",
    "tongueOut": "吐舌"
}