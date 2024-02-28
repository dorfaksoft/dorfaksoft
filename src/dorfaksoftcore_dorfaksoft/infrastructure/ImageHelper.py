import io

from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from math import ceil


class ImageHelper:
    @staticmethod
    def resize(realPath, width, height, isCenterCrop, bgColor=(255, 255, 255, 0)):
        im = Image.open(realPath)
        owidth, oheight = im.size

        # wpercent = (width / float(im.size[0]))
        # nheight = int((float(im.size[1]) * float(wpercent)))
        # size = (width, nheight)
        # im.thumbnail(size)
        if height == 0:
            wpercent = (width / float(owidth))
            height = int((float(oheight) * float(wpercent)))

        size = (width, height)
        if isCenterCrop:
            osc = owidth / oheight
            sc = width / height
            if osc > sc:
                # fit height
                src_w = ceil(float(owidth) * float(height) / float(oheight))
                im = im.resize((src_w, height), Image.LANCZOS)
                left = ceil((src_w - width) / 2.0)
                right = left + width
                top = 0
                bottom = top + height
            else:
                # fit width
                src_h = ceil(float(oheight) * float(width) / float(owidth))
                im = im.resize((width, src_h), Image.LANCZOS)

                left = 0
                right = left + width
                top = ceil((src_h - height) / 2.0)
                bottom = top + height
            im = im.crop((int(left), int(top), int(right), int(bottom)))

        else:
            im.thumbnail(size, Image.LANCZOS)

        background = Image.new('RGBA', size, bgColor)
        try:
            background.paste(im, (int((size[0] - im.size[0]) / 2), int((size[1] - im.size[1]) / 2)), im)
        except:
            background.paste(im, (int((size[0] - im.size[0]) / 2), int((size[1] - im.size[1]) / 2)))
        return background

    @staticmethod
    def getTextDimensions(text_string, font):
        # https://stackoverflow.com/a/46220683/9263761
        if not text_string:
            return 0, 0
        try:
            ascent, descent = font.getmetrics()

            text_width = font.getmask(text_string).getbbox()[2]
            text_height = font.getmask(text_string).getbbox()[3] + descent
        except:
            box=font.getbbox(text_string)
            text_width = box[2]
            text_height = box[3]
            print("size=",box,text_string)

        return (text_width, text_height)
