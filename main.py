import cv2 as cv
import numpy as np


def contrast_image_correction(img_dir):
    # 读取图片并将长宽高减半
    src = cv.imread(img_dir)
    h, w, _ = src.shape
    h, w = h // 4 * 2, w // 4 * 2
    src = cv.resize(src, (w, h))
    cv.imshow('Original picture', src)

    old_y = cv.cvtColor(src, cv.COLOR_BGRA2YUV_I420)
    temp = cv.bilateralFilter(old_y, 9, 50, 50)
    dst = np.zeros((h, w, 3))

    # 类型转化, 否则后续赋值会出现溢出
    src = src.astype(np.int16)
    old_y = old_y.astype(np.int16)
    temp = temp.astype(np.int16)
    dst = dst.astype(np.int16)

    # temp数组赋值
    for i in range(h):
        for j in range(w):
            exp = 2 ** ((128 - (255 - temp[i][j])) / 128.0)
            value = int(255 * ((old_y[i][j] / 255.0) ** exp))
            temp[i][j] = value

    # dst数组赋值
    for i in range(h):
        for j in range(w):
            if old_y[i][j] == 0:
                for k in range(3):
                    dst[i][j][k] = 0
            else:
                dst[i][j][0] = (int(temp[i][j]) * (src[i][j][0] + old_y[i][j]) / (old_y[i][j]) + (
                    src[i][j][0]) - old_y[i][j]) / 2
                dst[i][j][1] = (int(temp[i][j]) * (src[i][j][1] + old_y[i][j]) / (old_y[i][j]) + (
                    src[i][j][1]) - old_y[i][j]) / 2
                dst[i][j][2] = (int(temp[i][j]) * (src[i][j][2] + old_y[i][j]) / (old_y[i][j]) + (
                    src[i][j][2]) - old_y[i][j]) / 2

    # 展示并保存修改后的突破
    dst = dst.astype(np.uint8)
    cv.imshow('Changed picture', dst)
    cv.waitKey()
    cv.imwrite('Changed picture.jpg', dst)


if __name__ == '__main__':
    image_dir = 'Original picture.png'  # 图片路径
    contrast_image_correction(image_dir)
