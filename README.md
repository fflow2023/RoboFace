# Robot facial expression recognition Demo
> [Google MediaPipe FaceLandmarker 官方文档](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker?hl=zh-cn) 


**输入**:静态图片、已解码的视频帧、实时视频画面

**模型**: `MediaPipe FaceLandmarker` 识别478个3D关键点

**输出**：`Blendshape` 包含全部52组表情运动因子，每一组运动因子表示一个人脸表情特征，包括一个表示人脸特定表情的定位符与一个表示表情程度的浮点类型值，表情程度值的范围为［0,1］，其中0表示没有表情，1表示完全表情。

然后设计一种规则将相应运动因子映射到每台舵机上，并通过改变灵敏度的方式微调。

tools.py为映射和控制代码 config.py中修改灵敏度

运行方法：
```
  python run.py 1 [image_path]    # 静态图片模式
  python run.py 2                 # 摄像头实时模式
  python run.py 3 [video_path]    # 视频文件模式
  （如果不填路径的话会使用默认测试文件）
  python 服务器.py  # 模拟服务器，接收舵机指令通讯
```

- 目前已完成的映射:   眼球、眼皮  
由于不了解面部表情控制机理，基本都是AI做的，具体参数仍待进一步调试...
 
## MediaPipe 52维面部运动因子对照表
| 英文名称 | 中文名称 | 类别 |
|---------|---------|------|
| `browDownLeft` | 左眉头下降 | 眉毛 |
| `browDownRight` | 右眉头下降 | 眉毛 |
| `browInnerUp` | 蹙眉 | 眉毛 |
| `browOuterUpLeft` | 左眉尾上升 | 眉毛 |
| `browOuterUpRight` | 右眉尾上升 | 眉毛 |
| `cheekPuff` | 鼓腮 | 脸颊 |
| `cheekSquintLeft` | 左颊眯紧 | 脸颊 |
| `cheekSquintRight` | 右颊眯紧 | 脸颊 |
| `eyeBlinkLeft` | 左眼眨 | 眼睛 |
| `eyeBlinkRight` | 右眼眨 | 眼睛 |
| `eyeLookDownLeft` | 左眼向下 | 眼睛 |
| `eyeLookDownRight` | 右眼向下 | 眼睛 |
| `eyeLookInLeft` | 左眼内收 | 眼睛 |
| `eyeLookInRight` | 右眼内收 | 眼睛 |
| `eyeLookOutLeft` | 左眼外展 | 眼睛 |
| `eyeLookOutRight` | 右眼外展 | 眼睛 |
| `eyeLookUpLeft` | 左眼向上 | 眼睛 |
| `eyeLookUpRight` | 右眼向上 | 眼睛 |
| `eyeSquintLeft` | 左眼眯紧 | 眼睛 |
| `eyeSquintRight` | 右眼眯紧 | 眼睛 |
| `eyeWideLeft` | 左眼瞪大 | 眼睛 |
| `eyeWideRight` | 右眼瞪大 | 眼睛 |
| `jawForward` | 下颌前伸 | 下颌 |
| `jawLeft` | 下颌左偏 | 下颌 |
| `jawRight` | 下颌右偏 | 下颌 |
| `jawOpen` | 张口 | 下颌 |
| `mouthClose` | 闭口 | 嘴巴 |
| `mouthFrownLeft` | 左嘴角下垂 | 嘴巴 |
| `mouthFrownRight` | 右嘴角下垂 | 嘴巴 |
| `mouthFunnel` | 噘嘴圆孔 | 嘴巴 |
| `mouthPucker` | 噘嘴 | 嘴巴 |
| `mouthLeft` | 嘴向左 | 嘴巴 |
| `mouthRight` | 嘴向右 | 嘴巴 |
| `mouthSmileLeft` | 左嘴角上扬 | 嘴巴 |
| `mouthSmileRight` | 右嘴角上扬 | 嘴巴 |
| `mouthDimpleLeft` | 左酒窝 | 嘴巴 |
| `mouthDimpleRight` | 右酒窝 | 嘴巴 |
| `mouthStretchLeft` | 左嘴角拉伸 | 嘴巴 |
| `mouthStretchRight` | 右嘴角拉伸 | 嘴巴 |
| `mouthRollLower` | 下唇卷 | 嘴唇 |
| `mouthRollUpper` | 上唇卷 | 嘴唇 |
| `mouthShrugLower` | 下唇耸 | 嘴唇 |
| `mouthShrugUpper` | 上唇耸 | 嘴唇 |
| `mouthPressLeft` | 左唇压紧 | 嘴唇 |
| `mouthPressRight` | 右唇压紧 | 嘴唇 |
| `mouthLowerDownLeft` | 左下唇下降 | 嘴唇 |
| `mouthLowerDownRight` | 右下唇下降 | 嘴唇 |
| `mouthUpperUpLeft` | 左上唇上升 | 嘴唇 |
| `mouthUpperUpRight` | 右上唇上升 | 嘴唇 |
| `noseSneerLeft` | 左鼻皱 | 鼻子 |
| `noseSneerRight` | 右鼻皱 | 鼻子 |
| `tongueOut` | 吐舌 | 舌头 |
