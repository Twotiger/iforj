#coding:utf8
import    logging
import    PIL.Image
import    PIL.ImageDraw
import    PIL.ImageFont
        
class    Main(object):
    def text2png(self, text, fontName, fontSize, pngPath):
        font = PIL.ImageFont.truetype(fontName, fontSize)
        width, height = font.getsize(text)
        logging.debug('(width, height) = (%d, %d)' % (width, height))
        image = PIL.Image.new('RGBA', (width, height), (0, 0, 0, 0))  # 设置透明背景
        draw = PIL.ImageDraw.Draw(image)
        draw.text((0, -4), text, font = font, fill = '#000000')
        image.save(pngPath)

    def    Main(self):
        text = u'斐波那契数列第20个数字'
        fontName = 'black.ttf'
        pngPath = 'test.png'
        self.text2png(text, fontName, 37, pngPath)
s=Main()
s.Main()
print 'df'
