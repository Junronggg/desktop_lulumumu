from PIL import Image

# 1. Load images
frame1 = Image.open("../assets/gif2.png")
frame2 = Image.open("../assets/gif1.png")

frames = [frame1, frame2]

# 2. Save as GIF
frames[0].save(
    "../assets/hedwig_emocat.gif",
    format="GIF",
    save_all=True,
    append_images=frames[1:],
    duration=500,       # ms per frame
    loop=0,             # loop forever
    transparency=0,
    disposal=2          # ensures transparency works
)

print("GIF generated: assets/hedwig_emocat.gif")
