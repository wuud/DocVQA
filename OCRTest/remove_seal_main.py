"方法一"
# import cv2
# import numpy as np
#
#
# def remove_red_seal(input_img):
#     # 分离图片的通道
#     blue_c, green_c, red_c = cv2.split(input_img)
#     #利用大津法自动选择阈值
#     thresh, ret = cv2.threshold(red_c, 0, 255,cv2.THRESH_OTSU)
#     #对阈值进行调整
#     filter_condition = int(thresh * 0.90)
#     #移除红色的印章
#     _, red_thresh = cv2.threshold(red_c, filter_condition, 255, cv2.THRESH_BINARY)
#     # 把图片转回3通道
#     result_img = np.expand_dims(red_thresh, axis=2)
#     result_img = np.concatenate((result_img, result_img, result_img), axis=-1)
#
#     return result_img
#
# input_img = cv2.imread("paddleocr/True_Picture/2021duchengweiye.png")
# remove_seal = remove_red_seal(input_img)
# cv2.imwrite("./seal_remove/first_remove_seal.jpg",remove_seal)


"方法二"
'''
去除印章很干净
但是同样是对图片整体处理，会影响没有印章部分的后续识别
'''
# 去除印章
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# image0 = cv2.imread("paddleocr/True_Picture/2021duchengweiye.png", cv2.IMREAD_COLOR)  # 以BGR色彩读取图片
# image = image0
# # image = cv2.resize(image0, None, fx=0.5, fy=0.5,
# #                    interpolation=cv2.INTER_CUBIC)  # 缩小图片0.5倍（图片太大了）
# cols, rows, _ = image.shape  # 获取图片高宽
# B_channel, G_channel, R_channel = cv2.split(image)  # 注意cv2.split()返回通道顺序
#
# # cv2.imshow('Blue channel', B_channel)
# # cv2.imshow('Green channel', G_channel)
# # cv2.imshow('Red channel', R_channel)
#
# pixelSequence = R_channel.reshape([rows * cols, ])  # 红色通道的histgram 变换成一维向量
# numberBins = 256  # 统计直方图的组数
# plt.figure()  # 计算直方图
# manager = plt.get_current_fig_manager()
# histogram, bins, patch = plt.hist(pixelSequence,
#                                   numberBins,
#                                   facecolor='black',
#                                   histtype='bar')  # facecolor设置为黑色
# # 设置坐标范围
# y_maxValue = np.max(histogram)
# plt.axis([0, 255, 0, y_maxValue])
# # 设置坐标轴
# plt.xlabel("gray Level", fontsize=20)
# plt.ylabel('number of pixels', fontsize=20)
# plt.title("Histgram of red channel", fontsize=25)
# plt.xticks(range(0, 255, 10))
# # 显示直方图
# # plt.pause(0.05)
# # plt.savefig("histgram.png", dpi=260, bbox_inches="tight")
# # plt.show()
#
# # 红色通道阈值(调节好函数阈值为160时效果最好，太大一片白，太小干扰点太多)
# _, RedThresh = cv2.threshold(R_channel, 170, 255, cv2.THRESH_BINARY)
#
# # 膨胀操作（可以省略）
# # element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# # erode = cv2.erode(RedThresh, element)
#
# # 显示效果
# cv2.imshow('original color image', image)
# cv2.imshow("RedThresh", RedThresh)
# # cv2.imshow("erode", erode)
#
# # 保存图像
# cv2.imwrite('seal_remove/second_scale_image.jpg', image)
# cv2.imwrite('seal_remove/second_RedThresh.jpg', RedThresh)
# # cv2.imwrite("erode.jpg", erode)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

"方法三"
'''
该方法对整个图片都进行了处理
导致图片内容整体变形，删除印章的同时导致表格内容以及线条都出现了模糊的现象
'''
# import cv2
# import numpy as np
#
#
# class SealRemove(object):
#     """
#     印章处理类
#     """
#
#     def remove_red_seal(self, image):
#         """
#         去除红色印章
#         """
#
#         # 获得红色通道
#         blue_c, green_c, red_c = cv2.split(image)
#
#         # 多传入一个参数cv2.THRESH_OTSU，并且把阈值thresh设为0，算法会找到最优阈值
#         thresh, ret = cv2.threshold(red_c, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#         # 实测调整为95%效果好一些
#         filter_condition = int(thresh * 0.95)
#
#         _, red_thresh = cv2.threshold(red_c, filter_condition, 255, cv2.THRESH_BINARY)
#
#         # 把图片转回 3 通道
#         result_img = np.expand_dims(red_thresh, axis=2)
#         result_img = np.concatenate((result_img, result_img, result_img), axis=-1)
#
#         return result_img
#
#
# if __name__ == '__main__':
#     image = 'paddleocr/True_Picture/2021duchengweiye.png'
#     print(image)
#     img = cv2.imread(image)
#     seal_rm = SealRemove()
#     rm_img = seal_rm.remove_red_seal(img)
#     cv2.imwrite("./seal_remove/third_out.png", rm_img)

"方法四"
import numpy as np
import cv2 as cv

# im = cv.imread('paddleocr/True_Picture/2021test2.png')
#
# image = im.copy()
# # print(imgs)
# cv.namedWindow("image", cv.WINDOW_NORMAL)
# cv.imshow('image',image[:, :, 2])
# cv.imwrite("./seal_remove/fourth_image_2.jpg", image[:, :, 2])
# cv.waitKey(0)==ord('q')

"方法五"
'''
删除印章的同时会删掉被印章覆盖的内容，导致识别错误

'''
import cv2
import numpy as np
import fitz
import os


def seal_remove(imagepath):
    # imgs = cv2.imread("F:/PythonProject/OCRTest/paddleocr/True_Picture/2021duchengweiye.png")
    imgs = cv2.imread(imagepath)
    filename = os.path.basename(imagepath)
    print(imgs)
    image = imgs.copy()
    images = imgs.copy()
    print(image.shape)
    rows, cols = image.shape[:2]
    print(rows, cols)
    red_minus_blue = image[:, :, 2] - image[:, :, 0]
    red_minus_green = image[:, :, 2] - image[:, :, 1]

    red_minus_blue = red_minus_blue >= 10
    red_minus_green = red_minus_green >= 10

    red = image[:, :, 2] >= np.mean(image[:, :, 2]) / 1.2

    mask = red_minus_green & red_minus_blue & red
    print(mask)
    images[mask, :] = 255
    mask = (1 - mask).astype(np.bool)
    print(mask)
    image[mask, :] = 255

    # stack = np.vstack([imgs, image, images])
    # cv2.imshow("stack", stack)
    # cv2.imwrite("result.jpg", stack)
    # 显示原图及处理后的图像
    # cv2.imshow("orgin", imgs)
    # cv2.imshow("red", image)

    # cv2.imshow("delete_red", images)
    cv2.imwrite("./OCRTest/dealed_image/" + filename, images)

    cv2.waitKey()


# 红色像素值最大，且大于阈值（中值）
# 其他通道像素值的距离比较小，且与红色像素值的距离比率较大，且大于阈值（自己调）。


def pdf_image(pdfPath, imgPath, pages, path_prefix ,rotation_angle=0):
    # 打开PDF文件
    pdf = fitz.open(pdfPath)
    zoom_x = 2.5
    zoom_y = 2.5
    # 逐页读取PDF
    for pg in range(0, pdf.pageCount):
        if pg in pages:
            page = pdf[pg]
            # 设置缩放和旋转系数
            trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
            pm = page.getPixmap(matrix=trans, alpha=False)
            # 这是括号里面的一个参数 matrix=trans,
            # 开始写图像
            pm.writePNG(imgPath + path_prefix + str(pg) + ".png")
    pdf.close()


# pdf_image(r"D:/Desktop/DocVQA数据样例/廊坊千翼千行2021年度财务报告.pdf", r"./pdf2image/", [6])
