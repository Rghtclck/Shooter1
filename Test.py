from PIL import Image

#img = Image.open(r"C:\Users\pavel\Downloads\\image.png")


img = Image.open("1111.png")
W = img.size[0] // 4
H = img.size[1] // 4

x_start = 0
y_start = 0
k = 1

for i in range(4):
    for j in range(4):
        img_crop = img.crop((x_start,y_start,x_start+W,y_start +H))
        img_crop.save(f'./images1/{k}.png')
        k += 1
        x_start += W
    
    x_start = 0
    y_start += H