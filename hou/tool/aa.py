from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm
from hou.settings import BASE_DIR
import random
import time
import os


# 随机字母:
def rnd_char():
    return chr(random.randint(65, 90))


# 随机颜色2:
def rnd_color2():
    r = random.randint(32, 127)
    g = random.randint(32, 127)
    b = random.randint(32, 127)
    rgb = (r, g, b)
    return rgb


# 更新图片验证码
def create_img():
    width = 385
    height = 250
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), 250)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 输出文字:
    img_char = ''
    for t in range(4):
        chars = rnd_char()
        draw.text((60 * t + 1, 1), chars, font=font, fill=rnd_color2())
        img_char += chars
    img_name = '%s.jpg' % time.time()
    img_path = os.path.join(BASE_DIR, 'media/yan/%s' % img_name)
    image.save(img_path, 'jpeg')
    return img_char, img_name


# 删除文件
def delete_file(file_path):
    video_path = os.path.join(BASE_DIR, file_path)
    if os.path.exists(video_path):
        os.remove(video_path)
        print('删除成功')
    else:
        print('删除失败')
