#vs.py
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from config import BS_CN
import cv2
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']  # 支持中文的字体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def draw_landmarks_on_image(rgb_image, detection_result):
    """
    在图像上绘制人脸关键点
    """
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(rgb_image)

    # 如果没有检测到人脸，直接返回原图
    if not face_landmarks_list:
        return annotated_image

    # 循环检测到的每个人脸
    for idx in range(len(face_landmarks_list)):
        face_landmarks = face_landmarks_list[idx]

        # 绘制人脸关键点
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
        ])

        # 绘制网格
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles
            .get_default_face_mesh_tesselation_style())
        
        # 绘制轮廓
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles
            .get_default_face_mesh_contours_style())
        
        # 绘制虹膜
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles
            .get_default_face_mesh_iris_connections_style())

    return annotated_image

def display_image_with_matplotlib(image, title="人脸关键点检测结果"):
    """
    使用Matplotlib显示图像，解决大图像显示问题
    """
    rgb_image = image
    
    # 创建图形
    dpi = 100
    height, width = rgb_image.shape[:2]
    
    # 计算合适的显示尺寸（限制最大尺寸）
    max_display_size = 1000  # 最大显示尺寸
    scale = min(1.0, max_display_size / max(height, width))
    
    # 设置图形尺寸
    fig = plt.figure(figsize=(width * scale / dpi, height * scale / dpi), dpi=dpi)
    ax = fig.add_subplot(111)
    
    # 显示图像
    ax.imshow(rgb_image)
    ax.set_title(title, fontsize=12)
    ax.axis('on')  # 关闭坐标轴
    
    # 调整布局并显示
    plt.tight_layout()
    plt.show()

def plot_face_blendshapes_bar_graph(face_blendshapes):
    """
    绘制人脸52维BlendShape强度条形图，显示英文+中文动作名，按强度降序排列
    """
    # 1. 按得分降序排列
    sorted_bs = sorted(face_blendshapes, key=lambda x: x.score, reverse=True)
    
    # 2. 提取数据
    en_names = [c.category_name for c in sorted_bs]
    scores = [c.score for c in sorted_bs]
    
    # 3. 创建中英文标签
    labels = []
    for en in en_names:
        cn = BS_CN.get(en, en)  # 获取中文翻译，如果没有则使用英文
        labels.append(f"{en} ({cn})")  # 英文在上，中文在下
    
    # 4. 创建图形 - 固定大小，避免超出屏幕
    fig, ax = plt.subplots(figsize=(10, 12))
    
    # 5. 绘制水平条形图
    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, scores, color='steelblue')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()  # 最高分放最上面
    ax.set_xlabel('强度系数')
    ax.set_title('BlendShape')
    
    # 6. 在条上添加数值标签
    for i, (score, bar) in enumerate(zip(scores, bars)):
        width = bar.get_width()
        ax.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                f'{score:.4f}', ha='left', va='center', fontsize=8)
    
    # 7. 自动调整布局并显示
    plt.tight_layout()
    plt.show()