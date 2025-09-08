#run.py
# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from vs import *
import cv2

# 灵敏度设置字典
SENSITIVITY = {
    "eye_up": 1.0,    # 眼球向上灵敏度
    "eye_down": 1.0,  # 眼球向下灵敏度
    "eye_left": 1.0,  # 眼球向左灵敏度
    "eye_right": 1.0, # 眼球向右灵敏度
}

# STEP 2: Create an FaceLandmarker object.
base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

# STEP 3: Load the input image.
try:
    image = mp.Image.create_from_file("tests/xieshi.jpg")
    print("图像加载成功")
except Exception as e:
    print(f"图像加载失败: {e}")
    exit(1)

# STEP 4: Detect face landmarks from the input image.
detection_result = detector.detect(image)

if not detection_result.face_landmarks:
    print("未检测到人脸")
    exit(1)
print("检测到人脸")

# STEP 5: 可视化结果
# annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
# display_image_with_matplotlib(annotated_image,"Face Landmarks")
plot_face_blendshapes_bar_graph(detection_result.face_blendshapes[0])

# 打印所有blendshapes
print("\n所有BlendShape值:")
for i, blend in enumerate(detection_result.face_blendshapes[0]):
    print(f"{i+1}. {blend.category_name}: {blend.score:.6f}")
    
# ========== 眼球上下移动检测 ==========
# 提取四个关键的眼睛动作强度值
eye_look_down_left = None
eye_look_down_right = None
eye_look_up_left = None
eye_look_up_right = None

# 遍历所有blendshapes
for blend in detection_result.face_blendshapes[0]:
    if blend.category_name == "eyeLookDownLeft":
        eye_look_down_left = blend.score
    elif blend.category_name == "eyeLookDownRight":
        eye_look_down_right = blend.score
    elif blend.category_name == "eyeLookUpLeft":
        eye_look_up_left = blend.score
    elif blend.category_name == "eyeLookUpRight":
        eye_look_up_right = blend.score

# 检查是否所有值都已提取
if None in [eye_look_down_left, eye_look_down_right, eye_look_up_left, eye_look_up_right]:
    print("警告：未能提取所有眼睛动作的强度值")
    # 处理缺失值的情况（这里简单设为0）
    eye_look_down_left = eye_look_down_left or 0
    eye_look_down_right = eye_look_down_right or 0
    eye_look_up_left = eye_look_up_left or 0
    eye_look_up_right = eye_look_up_right or 0

# 计算双眼的最大值
down_strength = max(eye_look_down_left, eye_look_down_right)
up_strength = max(eye_look_up_left, eye_look_up_right)

# 判断眼睛方向
if up_strength > down_strength:
    direction = "向上"
    # 映射到0-49.5度范围
    angle_vertical = up_strength * 49.5 * SENSITIVITY["eye_up"]
else:
    direction = "向下"
    # 映射到0到-22.5度范围
    angle_vertical = -down_strength * 22.5 * SENSITIVITY["eye_down"]

# 输出垂直方向结果
print(f"\n垂直方向:")
print(f"眼睛方向: {direction}")
print(f"向上强度: {up_strength:.6f}, 向下强度: {down_strength:.6f}")
print(f"映射角度: {angle_vertical:.2f}度")

# ========== 眼球左右移动检测 ==========
# 提取四个关键的眼睛动作强度值
eye_look_in_left = None
eye_look_in_right = None
eye_look_out_left = None
eye_look_out_right = None

# 遍历所有blendshapes
for blend in detection_result.face_blendshapes[0]:
    if blend.category_name == "eyeLookInLeft":
        eye_look_in_left = blend.score
    elif blend.category_name == "eyeLookInRight":
        eye_look_in_right = blend.score
    elif blend.category_name == "eyeLookOutLeft":
        eye_look_out_left = blend.score
    elif blend.category_name == "eyeLookOutRight":
        eye_look_out_right = blend.score

# 检查是否所有值都已提取
if None in [eye_look_in_left, eye_look_in_right, eye_look_out_left, eye_look_out_right]:
    print("警告：未能提取所有眼睛动作的强度值")
    # 处理缺失值的情况（这里简单设为0）
    eye_look_in_left = eye_look_in_left or 0
    eye_look_in_right = eye_look_in_right or 0
    eye_look_out_left = eye_look_out_left or 0
    eye_look_out_right = eye_look_out_right or 0

# 计算双眼的最大值
left_strength = max(eye_look_out_left, eye_look_in_right)  # 左眼外展或右眼内收表示向左看
right_strength = max(eye_look_out_right, eye_look_in_left)  # 右眼外展或左眼内收表示向右看

# 判断眼睛方向
if left_strength > right_strength:
    direction = "向左"
    # 映射到0-36度范围（左正）
    angle_horizontal = left_strength * 36 * SENSITIVITY["eye_left"]
else:
    direction = "向右"
    # 映射到0到-36度范围（右负）
    angle_horizontal = -right_strength * 36 * SENSITIVITY["eye_right"]

# 输出水平方向结果
print(f"\n水平方向:")
print(f"眼睛方向: {direction}")
print(f"向左强度: {left_strength:.6f}, 向右强度: {right_strength:.6f}")
print(f"映射角度: {angle_horizontal:.2f}度")

# ========== 综合输出 ==========
print(f"\n综合眼球位置:")
print(f"垂直角度: {angle_vertical:.2f}度")
print(f"水平角度: {angle_horizontal:.2f}度")