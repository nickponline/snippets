from PIL import Image
import numpy as np

img = Image.open("faces.jpg")

print img.format, img.size, img.mode

img = img.convert('1') # convert image to black and white

img.show()

#Conver to numpy
num = np.array(img)

print num
print num.shape
