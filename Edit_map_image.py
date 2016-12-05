from PIL import Image,ImageFont,ImageDraw,ImageSequence
import math
from visvis.vvmovie.images2gif import writeGif


if __name__ == '__main__':
    def run():
        im = Image.open('/Users/Timo/Desktop/Efteling_Map.jpg')
        pix = im.load()
        #931/553
        pix[931,553] = (0,0,0)
        print(pix[4,5])
        print(im.getbbox)
        e = EditMap()
        im = e.putOnImage([931,553],5,im)
        im.save('/Users/Timo/Desktop/Efteling_Map_test.png')


class EditMap:
    def __init__(self):
        self.gif = 0

    if __name__ == '__main__':
        def addFrameToGif(self,frame):

            original_duration = im.info['duration']
            frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
            frames.reverse()


            writeGif("reverse_" + os.path.basename(filename), frames, duration=original_duration / 1000.0, dither=0)

        def putOnImage(self,centralPixel,amountOfPeopleWaiting,image):
            pix = image.load()

            # amount of people is proportional with surface of circle.
            # 1 person -> Surface is one -> r = 1
            # 5 people -> Surface is 5 = 2pir -> r = 5/(2pi)
            # 100 people -> surface 100, r = 100/(2pi) -> ong. 16 pixels

            # try scaling with 1.2 or something.

            # what are the coordinates of the circumference?
            #  F(x,y)=(x–h)2+(y–k)2−r2=0F(x,y)=(x–h)2+(y–k)2−r2=0


            # method 1 : go through all points, if point is radius removed from the center-> good
            # method 2: Calculate points on circumference by going through 360 calcs for every degree and check the closest pixel.

            # method 2 is better

            #center = pix[931,553]
            # first point = pix[931,553+radius]        radius^2 = diffX^2 (cosine) + diffY2 (sine)  -> we know the angle
            # sine of the angle * radius = diffX
            # cosine of the angle *radios = diffY
            # do this for one quadrant and then just mess with the signs 3 more times.
            # second point = pix[

            radius = math.sqrt((amountOfPeopleWaiting/(math.pi))) *5   #pi r^2 = surface -> r = sqrt(surface/pi)

            draw = ImageDraw.Draw(image)
            draw.ellipse((centralPixel[0] - radius, centralPixel[1] - radius, centralPixel[0] + radius, centralPixel[1] + radius), fill=(255,255, 255))
            draw.ellipse((centralPixel[0] - radius, centralPixel[1] - radius, centralPixel[0] + radius,
                          centralPixel[1] + radius),outline=(0,0,0))

            #optional fill

            if amountOfPeopleWaiting < 12:
                x=3
                h=12
                m = 6
            elif amountOfPeopleWaiting < 100:
                x = 10
                h = 12
                m =7
            elif amountOfPeopleWaiting < 1000:
                x = 15
                h = 16
                m=8
            else:
                x =25
                h = 24
                m = 10


            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('Aller_Bd.ttf', h)
            draw.text((centralPixel[0]-x, centralPixel[1]-m), str(amountOfPeopleWaiting), (0, 0, 0), font=font)


            return image


if __name__ == "__main__":
    run()


"""
>>> from PIL import Image
>>> from PIL import ImageFont
>>> from PIL import ImageDraw
>>> img = Image.open("sample_in.jpg")
>>> draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
>>> font = ImageFont.truetype("sans-serif.ttf", 16)
# draw.text((x, y),"Sample Text",(r,g,b))
>>> draw.text((0, 0),"Sample Text",(255,255,255),font=font)
>>> img.save('sample-out.jpg')

"""








"""

from PIL import Image
im = Image.open("foo.png")
pix = im.load()

if im.mode == '1':
    value = int(shade >= 127) # Black-and-white (1-bit)
elif im.mode == 'L':
    value = shade # Grayscale (Luminosity)
elif im.mode == 'RGB':
    value = (shade, shade, shade)
elif im.mode == 'RGBA':
    value = (shade, shade, shade, 255)
elif im.mode == 'P':
    raise NotImplementedError("TODO: Look up nearest color in palette")
else:
    raise ValueError("Unexpected mode for PNG image: %s" % im.mode)

pix[x, y] = value

im.save("foo_new.png")

"""
