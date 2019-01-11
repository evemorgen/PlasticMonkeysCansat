from PIL import Image

img = Image.open("testimage.jpg")
print("Original size: {}".format(img.size))

img = img.resize((160, 120), Image.ANTIALIAS)
img.save("testimage_scaled.jpg", optimize=True, quality=75)
