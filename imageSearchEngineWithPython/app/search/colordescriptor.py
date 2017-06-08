# coding=utf-8
import numpy as np
import cv2

class ColorDescriptor:
	def __init__(self, bins):
		#定义颜色直方图中的bin数量
		self.bins = bins

	def describe(self, image):
		# 将图像从RGB空间转变成HSV空间，初始化
		# 定义features用于量化图像的特征列表
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		features = []

		# 获取图像尺寸并且初始化图像中心
		(h, w) = image.shape[:2]
		#图像中心点
		(cX, cY) = (int(w * 0.5), int(h * 0.5))

		#将图像分为四个部分（矩阵运算），左上左下右上右下
		#更加准确的实现图像搜索
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
			(0, cX, cY, h)]

		# 构建一个椭圆来表示图像的中央区域
		# 定义一个长短轴分别为图像长度75%的椭圆
		# python3需要将/改为//
		(axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		#所需参数：图像中心，椭圆的两个数值，椭圆的旋转角度，椭圆初始角
		#椭圆终止角，椭圆的颜色， 椭圆边框的大小，负数表示椭圆填充模式
		#创建椭圆掩膜区域 ellipMask <- cv2.ellipse
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

		# 循环每一部分
		for (startX, endX, startY, endY) in segments:
			# 定义边角区域，使用np使其初始化为0(全黑)的区域
			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
			#定义矩阵掩膜，填充为白色
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			#矩阵掩膜和椭圆掩膜相减形成新的边角掩膜，便于计算特征值
			cornerMask = cv2.subtract(cornerMask, ellipMask)

			#计算边角掩膜的特征值，规定只计算掩膜区，其他区域忽略
			hist = self.histogram(image, cornerMask)
			features.extend(hist)

		# 计算椭圆区域的颜色特征值
		# 更新图像特征值
		hist = self.histogram(image, ellipMask)
		features.extend(hist)

		# 返回一幅图的颜色特征值（360bin）
		return features

	def histogram(self, image, mask):
		#计算特征值：8（色相） × 3（饱和度） × 3（明亮度）=72bin数
		#调用 cv2.calcHist计算掩膜区的颜色直方图(3色空间)
		#参数：图像，颜色空间（HSV），mask掩膜，bin数量，像素值范围（H(0-180)S(256)V）
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
			[0, 180, 0, 256, 0, 256])
		#3D直方图归一化，使直方图表示每个bin所占的比例，而不是bin的个数
		hist = cv2.normalize(hist,hist).flatten()

		# 返回归一化后的3Dhsv颜色直方图
		return hist
