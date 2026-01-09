
from PIL import Image, ImageDraw

# Create a simple floor plan image
img = Image.new('RGB', (800, 600), color='white')
d = ImageDraw.Draw(img)

# Draw outer walls
d.rectangle([50, 50, 750, 550], outline='black', width=5)

# Draw some rooms
d.rectangle([50, 50, 350, 300], outline='black', width=3) # Bedroom
d.text((150, 150), "Master Bedroom", fill='black')

d.rectangle([400, 50, 750, 300], outline='black', width=3) # Living
d.text((550, 150), "Living Room", fill='black')

d.rectangle([50, 350, 350, 550], outline='black', width=3) # Kitchen
d.text((150, 450), "Kitchen (SE)", fill='black')

d.rectangle([400, 350, 750, 550], outline='black', width=3) # Bath
d.text((550, 450), "Bathroom", fill='black')

img.save('sample_floorplan.png')
print("Sample floorplan created: sample_floorplan.png")
