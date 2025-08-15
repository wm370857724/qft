from PIL import Image
# 查询256位BMP文件调色板
image=Image.open("example256.bmp")

palette = image.getpalette()

with open('palettePrgbPvalues.txt','w') as file:
    for i in range(0,len(palette),3):
        r,g,b=palette[i:i+3]
        print(f"'{int(i/3)}':({r},{g},{b}),",end='')
        # file.write(f"({r},{g},{b})\n")
        file.write(f"'{int(i/3)}':({r},{g},{b}),")