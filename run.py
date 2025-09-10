# run.py - 主程序
import sys, cv2, time, os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from vs import draw_landmarks_on_image, plot_face_blendshapes_bar_graph
from config import *
from tools import *

def blendshapes_to_dict(blendshapes):
    """把 FaceLandmarker 返回的 list 转成 dict"""
    return {b.category_name: b.score for b in blendshapes}

# ------------------ 构造检测器 ------------------
try:
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1)
    detector = vision.FaceLandmarker.create_from_options(options)
except Exception as e:
    print(f"创建检测器失败: {str(e)}")
    sys.exit(1)

# ------------------ 模式1：静态图片 ------------------
def mode_static(img_path):
    if not os.path.exists(img_path):
        print(f"错误: 图片路径不存在 - {img_path}")
        return
    
    print(f'[Mode1] 读取静态图片: {img_path}')
    try:
        image = mp.Image.create_from_file(img_path)
    except Exception as e:
        print(f"读取图片失败: {str(e)}")
        return
    
    result = detector.detect(image)
    if not result.face_landmarks:
        print('未检测到人脸')
        return
    
    # 初始化socket连接
    init_socket_connection()
    
    try:
        # 可视化
        annotated = draw_landmarks_on_image(image.numpy_view(), result)
        
        # 处理blendshapes并控制舵机
        if result.face_blendshapes:
            bs_dict = blendshapes_to_dict(result.face_blendshapes[0])
            commands = process_all_servos(bs_dict)
            send_servo_commands(commands)
            
            # 显示blendshapes图表
            plot_face_blendshapes_bar_graph(result.face_blendshapes[0])
        
        cv2.imshow('Static Result', cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
    finally:
        # 确保关闭连接
        close_socket_connection()

# ------------------ 模式2：24 FPS 实时摄像头 ------------------
def mode_camera():
    print(f'[Mode2] 打开摄像头，{FPS} FPS 实时推理（按 q 退出）')
    # 初始化socket连接
    init_socket_connection()
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print('错误: 摄像头打开失败，请检查设备连接')
            return

        # 控制帧率
        interval = 1/FPS
        t_last = 0

        while True:
            ret, frame_bgr = cap.read()
            if not ret:
                print("错误: 无法从摄像头读取帧")
                break
            # 限帧
            t = time.time()
            if t - t_last < interval:
                continue
            t_last = t

            # BGR→RGB→MediaPipe Image
            rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result = detector.detect(mp_image)

            # 画关键点
            annotated = draw_landmarks_on_image(rgb, result)
            
            # 处理blendshapes并控制舵机
            if result.face_blendshapes:
                bs_dict = blendshapes_to_dict(result.face_blendshapes[0])
                commands = process_all_servos(bs_dict)
                send_servo_commands(commands)
            
            cv2.imshow(WIN_NAME, cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"摄像头处理过程中出错: {str(e)}")
    finally:
        # 确保关闭连接
        close_socket_connection()

# ------------------ 模式3：视频文件处理 ------------------
def mode_video(video_path):
    if not os.path.exists(video_path):
        print(f"错误: 视频路径不存在 - {video_path}")
        return
    
    print(f'[Mode3] 处理视频文件: {video_path} (按 q 退出)')
    
    # 初始化socket连接
    init_socket_connection()
    
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f'错误: 无法打开视频文件: {video_path}')
            print('可能原因: 文件格式不支持、文件损坏或编解码器缺失')
            return
        
        # 获取视频原始帧率
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        print(f'视频原始帧率: {original_fps:.2f} FPS')
        print(f'目标处理帧率: {FPS} FPS')
        
        # 计算每帧应该显示的时间（秒）
        frame_delay = 1 / FPS
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            # 记录帧开始时间
            frame_start = time.time()
            
            ret, frame_bgr = cap.read()
            if not ret:
                print("\n视频处理完成")
                break
            
            # BGR→RGB→MediaPipe Image
            rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result = detector.detect(mp_image)
            
            # 画关键点
            annotated = draw_landmarks_on_image(rgb, result)
            
            # 处理blendshapes并控制舵机
            if result.face_blendshapes:
                bs_dict = blendshapes_to_dict(result.face_blendshapes[0])
                commands = process_all_servos(bs_dict)
                send_servo_commands(commands)
            
            # 显示处理后的帧
            cv2.imshow(WIN_NAME, cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
            
            # 计算处理时间并调整显示延迟
            processing_time = time.time() - frame_start
            remaining_time = max(0.001, frame_delay - processing_time)  # 至少1ms
            
            # 等待剩余时间或用户输入
            if cv2.waitKey(int(remaining_time * 1000)) & 0xFF == ord('q'):
                print("\n用户中断处理")
                break
            
            frame_count += 1
        
        # 计算实际处理帧率
        end_time = time.time()
        total_time = end_time - start_time
        actual_fps = frame_count / total_time if total_time > 0 else 0
        print(f'\n实际处理帧率: {actual_fps:.2f} FPS')
        print(f'总处理帧数: {frame_count}')
        print(f'总耗时: {total_time:.2f} 秒')
        
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"视频处理过程中出错: {str(e)}")
    finally:
        # 确保关闭连接
        close_socket_connection()

# ------------------ main ------------------
if __name__ == '__main__':
    # 设置默认路径
    img_path = DEFAULT_IMG_PATH
    video_path = DEFAULT_VIDEO_PATH
    
    if len(sys.argv) < 2:
        print('Usage:')
        print('  python run.py 1 [image_path]   # 静态图模式 ')
        print('  python run.py 2                # 实时摄像头模式')
        print('  python run.py 3 [video_path]   # 视频文件模式 ')
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == '1':
        # 如果有指定图片路径，则使用它
        if len(sys.argv) >= 3:
            img_path = sys.argv[2]
        mode_static(img_path)
    elif mode == '2':
        mode_camera()
    elif mode == '3':
        # 如果有指定视频路径，则使用它
        if len(sys.argv) >= 3:
            video_path = sys.argv[2]
        mode_video(video_path)
    else:
        print('错误: 无效的模式选择')
        print('可用模式: 1 (静态图), 2 (摄像头), 3 (视频文件)')
        sys.exit(1)