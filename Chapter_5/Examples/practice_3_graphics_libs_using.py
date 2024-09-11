import cv2
import numpy as np
import colour
from collections import deque

# 加载 Haar 级联分类器用于人脸检测
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 打开摄像头
cap = cv2.VideoCapture(0)

# 初始化跟踪器标志
init_tracker = False
tracker = None

# 定义一个队列来保存历史颜色数据
history_length = 100  # 只保留最近 100 帧的数据
history_rgb = [deque(maxlen=history_length) for _ in range(3)]
history_xyz = [deque(maxlen=history_length) for _ in range(3)]
history_lab = [deque(maxlen=history_length) for _ in range(3)]


def calculate_colour_metrics(frame, bounding_box):
    x, y, w, h = bounding_box
    face_roi = frame[int(y):int(y + h), int(x):int(x + w)]

    # 计算 RGB 平均值
    mean_rgb = np.mean(face_roi, axis=(0, 1)) / 255.0  # 归一化到 [0, 1] 范围

    # 获取 D65 光源的色度坐标
    illuminant = colour.CCS_ILLUMINANTS['CIE 1931 2 Degree Standard Observer']['D65']

    # 转换到 XYZ 颜色空间
    mean_xyz = colour.RGB_to_XYZ(mean_rgb, colour.RGB_COLOURSPACES['sRGB'], illuminant=illuminant)

    # 转换到 Lab 颜色空间
    mean_lab = colour.XYZ_to_Lab(mean_xyz, illuminant)

    return mean_rgb, mean_xyz, mean_lab


def draw_graph(frame, data, position, colors, title):
    """
    在 frame 上绘制图表
    :param frame: 要绘制图表的帧
    :param data: 要绘制的数据（deque）
    :param position: 图表的位置
    :param colors: 图表的颜色列表
    :param title: 图表的名称
    """
    graph_height = 100
    graph_width = 200
    x, y = position

    # 创建半透明背景
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y - graph_height), (x + graph_width, y), (0, 0, 0), -1)  # 黑色背景
    alpha = 0.5  # 透明度
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # 绘制坐标轴
    cv2.line(frame, (x, y), (x + graph_width, y), (0, 0, 0), 1)
    cv2.line(frame, (x, y), (x, y - graph_height), (0, 0, 0), 1)

    # 绘制图表名称
    cv2.putText(
        frame, title, (x, y - graph_height - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1
    )

    # 绘制数据曲线
    for channel, color in enumerate(colors):
        if len(data[channel]) > 1:
            for i in range(1, len(data[channel])):
                cv2.line(
                    frame,
                    (x + int((i - 1) * graph_width / (history_length - 1)),
                     y - int(data[channel][i - 1] * graph_height)),
                    (x + int(i * graph_width / (history_length - 1)),
                     y - int(data[channel][i] * graph_height)),
                         color, 1
                )


while True:
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:
        break

    # 转换为灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if not init_tracker:
        # 检测人脸
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(120, 120),  # 增大最小尺寸以减少局部特征检测
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # 如果检测到人脸，选择最大的矩形框初始化跟踪器
        if len(faces) > 0:
            # 选择最大的矩形框
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = largest_face
            bounding_box = (x, y, w, h)

            # 确保检测到的是整张人脸而不是局部特征（例如通过宽高比）
            aspect_ratio = w / h
            if 0.75 < aspect_ratio < 1.5:  # 简单的宽高比过滤
                # 创建 KCF 跟踪器
                tracker = cv2.TrackerKCF_create()
                tracker.init(frame, bounding_box)
                # 绘制跟踪框
                p1 = (int(bounding_box[0]), int(bounding_box[1]))
                p2 = (int(bounding_box[0] + bounding_box[2]),
                      int(bounding_box[1] + bounding_box[3]))
                cv2.rectangle(frame, p1, p2, (0, 0, 255), 2, 1)
                cv2.putText(
                    frame, "Detecting", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2
                )
                init_tracker = True
    else:
        # 确保 tracker 已初始化
        if tracker:
            # 更新跟踪器
            success, bounding_box = tracker.update(frame)
            if success:
                # 检查跟踪窗口是否仍然包含整张人脸
                x, y, w, h = bounding_box
                aspect_ratio = w / h
                # 绘制跟踪框
                p1 = (int(bounding_box[0]), int(bounding_box[1]))
                p2 = (int(bounding_box[0] + bounding_box[2]),
                      int(bounding_box[1] + bounding_box[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
                cv2.putText(
                    frame, "Tracking", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2
                )

                # 计算并显示 Colour-Science 相关分析
                mean_rgb, mean_xyz, mean_lab = calculate_colour_metrics(
                    frame, bounding_box
                )
                text = (f"RGB: {mean_rgb[0]:.2f}, {mean_rgb[1]:.2f}, {mean_rgb[2]:.2f}\n"
                        f"XYZ: {mean_xyz[0]:.2f}, {mean_xyz[1]:.2f}, {mean_xyz[2]:.2f}\n"
                        f"Lab: {mean_lab[0]:.2f}, {mean_lab[1]:.2f}, {mean_lab[2]:.2f}")
                y0, dy = 20, 20
                for i, line in enumerate(text.split('\n')):
                    y = y0 + i * dy
                    cv2.putText(
                        frame, line, (100, y + 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2
                    )

                # 将数据添加到历史记录中
                for i in range(3):
                    history_rgb[i].append(mean_rgb[i])
                    history_xyz[i].append(mean_xyz[i] / max(mean_xyz))  # 归一化
                    history_lab[i].append(mean_lab[i] / 100.0)  # 归一化为 [0, 1]

                # 绘制图表
                draw_graph(frame, history_rgb,
                           (10, frame.shape[0] - 10), [(0, 0, 255), (0, 255, 0), (255, 0, 0)],
                           "RGB")  # R红色, G绿色, B蓝色
                draw_graph(frame, history_xyz,
                           (220, frame.shape[0] - 10), [(0, 0, 255), (0, 255, 0), (255, 0, 0)],
                           "XYZ")  # X红色, Y绿色, Z蓝色
                draw_graph(frame, history_lab,
                           (430, frame.shape[0] - 10), [(0, 0, 255), (0, 255, 0), (255, 0, 0)],
                           "Lab")  # L红色, A绿色, B蓝色

            else:
                cv2.putText(
                    frame, "Tracking failure detected", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 0, 255), 2
                )
                init_tracker = False

    # 显示结果
    cv2.imshow('Face Tracking', frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()