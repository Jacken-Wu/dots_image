"""
本脚本使用 Unicode 的 braille pattern dots 字符进行字符串图像的绘制。
braille pattern dots由 0 ~ 8 个点构成，共 256 个字符，从 \\u2800 开始，
到 \\u28FF 结束，字符的编码方式如下：
首先对 8 个点位进行编号：     1   4
                            2   5
                            3   6
                            7   8
从 \\u2800 开始，编号为 n 的点位，有连续 2^(n-1) 个字符为空，紧接着连续
2^(n-1) 个字符为填充，如此循环。
例如：对于 3 号点位，\\u2800 ~ \\u2803 均为空白，\\u2804 ~ \\u2807 有
黑点填充，\\u2808 ~ \\u280B 又是空白……
根据这个编码规律，可以找到需要的字符。
"""


import cv2 as cv
import codecs
import os


def generate_dot(array: list) -> str:
    """
    将一个 4 * 2 图像转化为字符。
    """
    num = 0b00000000
    if array[0][0] == 0:
        num |= 0b00000001
    if array[1][0] == 0:
        num |= 0b00000010
    if array[2][0] == 0:
        num |= 0b00000100
    if array[0][1] == 0:
        num |= 0b00001000
    if array[1][1] == 0:
        num |= 0b00010000
    if array[2][1] == 0:
        num |= 0b00100000
    if array[3][0] == 0:
        num |= 0b01000000
    if array[3][1] == 0:
        num |= 0b10000000

    a = '\\u28'
    b = hex(num)[2:]
    if len(b) == 1:
        b = '0' + b
    s = a + b

    return codecs.decode(s, encoding='unicode_escape')


def generate_dots_img(img_name: str, txt_name: str, width_max: int) -> None:
    """
    生成字符串图像并保存。
    """
    origin = cv.imread(img_name, 0)
    height, width = origin.shape

    if width > 300:
        height = int(300 / width * height)
        width = 300

    img_resize = cv.resize(origin, (width, height), interpolation=cv.INTER_LINEAR)
    img_edges = cv.Canny(origin, 10, 200)
    img_edges = cv.convertScaleAbs(img_edges, 1, 120)
    img_edges = cv.resize(img_edges, (width, height), interpolation=cv.INTER_LINEAR)
    img_edges = cv.convertScaleAbs(img_edges, 1, 120)
    ret, img_thresh = cv.threshold(img_resize, 127, 255, cv.THRESH_BINARY)
    ret, img_edges_inv = cv.threshold(img_edges, 127, 255, cv.THRESH_BINARY_INV)

    img_mix = cv.bitwise_and(img_thresh, img_edges_inv)

    # cv.imshow('edges', img_edges)
    # cv.waitKey(0)


    # 二次缩放
    if width > width_max:
        height = int(width_max / width * height)
        width = width_max

    img_resize = cv.resize(img_mix, (width, height), interpolation=cv.INTER_LINEAR)
    img_edges = cv.convertScaleAbs(img_edges, 1, 120)
    img_edges = cv.resize(img_edges, (width, height), interpolation=cv.INTER_LINEAR)
    img_edges = cv.convertScaleAbs(img_edges, 1, 120)
    ret, img_thresh = cv.threshold(img_resize, 200, 255, cv.THRESH_BINARY)
    ret, img_edges_inv = cv.threshold(img_edges, 127, 255, cv.THRESH_BINARY_INV)

    img_mix = cv.bitwise_and(img_thresh, img_edges_inv)

    # cv.imshow('thresh', img_thresh)
    # cv.imshow('edges', img_edges_inv)
    # cv.imshow('mix', img_mix)
    # cv.waitKey(0)


    # 对多余行进行裁剪
    left_col = width % 2
    width -= left_col
    left_row = height % 4
    height -= left_row
    img_cut = img_mix[0: height, 0: width]


    file = open(f'./resault/{txt_name}.txt', 'w', encoding='utf-8')

    for i in range(0, height, 4):
        for j in range(0, width, 2):
            dot_img = img_cut[i: i+4, j: j+2]
            dot = generate_dot(dot_img)
            file.write(dot)
        file.write('\n')
    
    file.close()


def generate(img_width_max: int) -> None:
    """
    将 ./origin 文件夹下的图片转化为字符串图片，以 txt 格式保存在 ./resault 文件夹下。
    @param img_width_max: 每行字符数量限制
    """
    origin_imgs = os.listdir('./origin/')
    print(origin_imgs)
    for img in origin_imgs:
        generate_dots_img('./origin/' + img, img, img_width_max*2)


if __name__ == "__main__":
    # 参数为每行的最大符号数
    generate(40)
