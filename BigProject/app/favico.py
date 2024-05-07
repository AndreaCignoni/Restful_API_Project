from PIL import Image

# Create a new image with the required dimensions
image = Image.new('RGB', (16, 16), color = 'red')

# Save the image as favicon.ico
image.save('favicon.ico')