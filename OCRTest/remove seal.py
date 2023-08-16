'pdf文件转图片，并对图片印章进行去除，然后将去除后的印章图片合并成新的PDF'

import os
from itertools import product
import fitz, os, datetime
from PIL import Image


def pyMuPDF_fitz(pdfPath, imagePath, zoomNum):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        # zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_x = zoomNum  # (1.33333333-->1056x816)   (2-->1584x1224)
        # zoom_y = 1.33333333
        zoom_y = zoomNum
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        if pg < 10:
            pg_str = '00' + str(pg)
        elif 10 <= pg < 100:
            pg_str = '0' + str(pg)
        else:
            pg_str = str(pg)
        pix.writePNG(imagePath + '/' + '%s.png' % pg_str)  # 将图片写入指定的文件夹内

    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf2img时间=', (endTime_pdf2img - startTime_pdf2img).seconds, '秒')


def pyMuBinaryzation(binaryzationpath):
    startTime_pdfbinaryzation = datetime.datetime.now()  # 开始时间
    file_list = os.listdir(binaryzationpath)
    pic_name_list = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name_list.append(x)
    for pic_name in pic_name_list:
        image = Image.open(binaryzationpath + '/' + pic_name)
        width, height = image.size  # 获取图片宽高
        for p in product(range(width), range(height)):
            dian_data = image.getpixel(p)[:3]
            if 190 <= dian_data[0] < 255 and 190 <= dian_data[1] < 255 and 190 <= dian_data[2] < 255:  # 进行阈值筛选
                image.putpixel(p, (255, 255, 255))  # 如果满足替换为底色
        cropped = image.crop((89, 209, 1100, 1522))
        cropped.save(binaryzationpath + '/' + pic_name)
        # image.save(binaryzationpath + '/' + pic_name)
    endTime_pdfbinaryzation = datetime.datetime.now()  # 结束时间
    print('pdfpdfbinaryzation时间=', (endTime_pdfbinaryzation - startTime_pdfbinaryzation).seconds, '秒')


def pyMuPicToPdf(picDir, outfilepath):
    startTime_PicToPdf = datetime.datetime.now()  # 开始时间
    file_list = os.listdir(picDir)
    pic_name = []
    im_list = []
    print(file_list)
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)

    pic_name.sort()

    im1 = Image.open(picDir + '/' + pic_name[0])
    pic_name.pop(0)
    for i in pic_name:
        img = Image.open(picDir + '/' + i)
        # im_list.append(img)
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    im1.save(outfilepath, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    print(i)
    endTime_PicToPdf = datetime.datetime.now()  # 结束时间
    print('PicToPdf时间=', (endTime_PicToPdf - startTime_PicToPdf).seconds, '秒')

# def deleteDir(path):
#     try:
#         for i in os.listdir(path):
#             path_file = os.path.join(path, i)
#             if os.path.isfile(path_file):
#                 os.remove(path_file)
#         if os.path.exists(path):  # 如果文件夹
#             # 删除文件，可使用以下两种方法。
#             os.rmdir(path)
#             # os.unlink(path)
#         else:
#             print('no such file:%s' % path)  # 则返回文件不存在
#     except Exception as e:
#         print(e)

def mainProcess(fileName, outfilepath='', zoomNum=2):  # 2或8
    '''
    主函数入口
    :param fileName:需要去章的文件路径
    :param outfilepath:需要输出的文件路径，包括文件名，默认在同目录下生成 xxx_out.pdf 文件
    :param zoomNum:转换成图片的比例，影响运行速度，数值越大，去章效果越好，执行时间越长，默认为2
    :return:
    '''
    startTime = datetime.datetime.now()  # 开始时间
    (filepath, tempfilename) = os.path.split(fileName)  # 解析fileName
    (filename, extension) = os.path.splitext(tempfilename)  # 解析文件名 文件类型
    if not outfilepath:
        outfilepath = filepath + '/' + filename + '_out-1' + extension
    outdir = filepath + '/' + filename
    print(outdir)
    print("将pdf文件解析出图片")
    pyMuPDF_fitz(fileName, outdir, zoomNum)  # 将pdf文件解析出图片
    print("对图片进行去章")
    pyMuBinaryzation(outdir)  # 对图片进行去章
    print("将图片合成pdf")
    pyMuPicToPdf(outdir, outfilepath)  # 将图片合成pdf
    # print("删除图片文件夹")
    # deleteDir(outdir)  # 删除图片文件夹
    endTime = datetime.datetime.now()  # 结束时间
    print('总耗时=', (endTime - startTime).seconds, '秒')
if __name__ == "__main__":
    file_old = r"D:/Desktop/DocVQA数据样例/廊坊千翼千行2020年度财务报告.pdf"
    # out_file = "F:/PythonProject/OCRTest/seal_remove/pdf_deal_out.pdf"
    mainProcess(file_old, )



