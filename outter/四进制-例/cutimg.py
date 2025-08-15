from PIL import Image

original_image = Image.open('example.bmp')

left = 10
top = 62
width = 1900
height = 950

cropped_image = original_image.crop((left,top,left+width,top+height))

cropped_image.save('example.bmp','BMP')

print('done')

