# -*- coding: utf-8 -*-

import cv2
import json
import time
import imutils
import argparse
import datetime
import warnings
import uuid

from requests import Session
from picamera import PiCamera
from picamera.array import PiRGBArray


# 参数解析
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="path to the JSON configuration file")
ap.add_argument('-s', "--show", required=True, help="is show video")
args = vars(ap.parse_args())

# 过滤警告，加载配置文件
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

# 初始化requests session
s_request = Session()

# 初始化摄像头并且获取一个指向原始数据的引用
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

# 等待摄像头启动初始化平均值
print "[INFO] warming up..."
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

# 从摄像头捕获数据
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # 抓取原始NumPy数组来表示图像并且初始化
    frame = f.array
    # 时间戳以及occupied/unoccupied文本
    timestamp = datetime.datetime.now()
    # 无人入侵
    text = "Unoccupied"

    # 调整图像尺寸
    frame = imutils.resize(frame, width=320)
    # bgr 图像转 灰度图像
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 0 是指根据窗口大小（21, 21）来计算高斯函数标准差
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # 初始化平均值
    if avg is None:
        print "[INFO] starting background model..."
        # 浮点数转化
        avg = gray.copy().astype("float")
        # 依据尺寸来截取图像
        rawCapture.truncate(0)
        continue

    # 累计当前帧，计算加权平均值
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # 计算阈值，膨胀阈值图像
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    # 发现入侵图像轮廊
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历轮廊线
    for c in cnts:
        # 如果轮廊小于min_area 则忽略他
        if cv2.contourArea(c) < conf["min_area"]:
            continue
        # 计算轮廊线,
        (x, y, w, h) = cv2.boundingRect(c)
        # 画出轮廊矩阵
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # 更新入侵状态
        text = "Occupied"

    # 在当前帧数上标记文本和时间戳
    ts = timestamp.strftime("%Y %I:%M:%S")
    cv2.putText(
        frame,
        "Room Status: {}".format(text),
        (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 0, 255), 2)
    cv2.putText(
        frame,
        ts, (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35, (0, 0, 255), 1
    )
    
    # 检查房间是否被入侵
    if text == "Occupied":
        # 判断上一次上传数据图像时间是否达到上传间隔
        if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
            # 增加计数器
            motionCounter += 1
            
            # 判断连续运动时间是否已经足够多
            if motionCounter >= conf["min_motion_frames"]:
                # 写入零时图片
                file_uuid = uuid.uuid1()
                if conf.get('tmp_image_path'):
                    tmp_path = os.path.join(
                        conf.get('tmp_image_path'),
                        '{file_uuid}.jpg'.format(file_uuid=file_uuid)
                    )
                else:
                    tmp_path = os.path.join(
                        './result',
                        '{file_uuid}.jpg'.format(file_uuid=file_uuid)
                    )
                cv2.imwrite(tmp_path, frame)
                # 将入侵图像上传到服务器
                try:
                    resp = s_request.request(
                        'POST', conf['web_hook'],
                        files={'file': open(tmp_path, 'r')}
                    )
                    if resp.status_code == 201:
                        print u'上传图片成功'
                except Exception:
                    print u'上传图片失败'
                motionCounter = 0
                lastUploaded = timestamp
    # 房间没有被入侵
    else:
        motionCounter = 0
    # 查看是否将视频显示在桌面
    if args['show'] == 'True':
        # display the security feed
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        # 如果用户键盘输入q则退出程序
        if key == ord("q"):
            break
    # 清理数据
    rawCapture.truncate(0)
