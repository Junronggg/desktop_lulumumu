from PIL import Image

img = Image.open("../assets/touch.png").convert("RGBA")
w, h = img.size

# Patting settings
max_angle = 20        # Rotation angle in degrees
step = 4              # How many degrees per frame
duration = 60         # ms per frame

frames = []

# Create angles: 0 -> 20 -> 0
angles = list(range(0, max_angle + 1, step)) + \
         list(range(max_angle - step, -1, -step))

for angle in angles:
    # We rotate around the bottom-center (w/2, h) to simulate a wrist/arm pivot
    # expand=True ensures the image isn't cut off as it tilts
    rotated = img.rotate(
        angle,
        resample=Image.BICUBIC,
        center=(w // 2, h),
        expand=False
    )
    frames.append(rotated)

# Save as GIF
frames[0].save(
    "../assets/touch.gif",
    save_all=True,
    append_images=frames[1:],
    duration=duration,
    loop=0,
    disposal=2 # Important: clears the previous frame so they don't stack
)