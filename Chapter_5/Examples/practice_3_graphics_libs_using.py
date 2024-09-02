import cv2

# 加载 Haar 级联分类器用于人脸检测
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 打开摄像头
cap = cv2.VideoCapture(0)

# 初始化跟踪器标志
init_tracker = False
tracker = None

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
                p2 = (int(bounding_box[0] + bounding_box[2]), int(bounding_box[1] + bounding_box[3]))
                cv2.rectangle(frame, p1, p2, (0, 0, 255), 2, 1)
                cv2.putText(frame, "Detecting", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
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
                p2 = (int(bounding_box[0] + bounding_box[2]), int(bounding_box[1] + bounding_box[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 0), 2, 1)
                cv2.putText(frame, "Tracking success detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                init_tracker = False

    # 显示结果
    cv2.imshow('Face Tracking', frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()