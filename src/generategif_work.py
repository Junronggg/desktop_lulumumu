from PIL import Image

img = Image.open("../assets/workmode.png").convert("RGBA")
w, h = img.size

jump_height = 20      # how high it jumps (pixels)
step = 3              # smaller = smoother
duration = 60         # ms per frame

frames = []

# Up then down
offsets = list(range(0, jump_height + 1, step)) + \
          list(range(jump_height - step, -1, -step))

for y in offsets:
    frame = Image.new("RGBA", (w, h + jump_height), (0, 0, 0, 0))
    frame.paste(img, (0, jump_height - y), img)
    frames.append(frame)

frames[0].save(
    "../assets/workmode.gif",
    save_all=True,
    append_images=frames[1:],
    duration=70,
    loop=0,
    disposal=2
)
