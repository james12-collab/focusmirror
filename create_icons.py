from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    img = Image.new('RGB', (size, size), color='#0a0a0a')
    draw = ImageDraw.Draw(img)
    
    # Draw green circle
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 outline='#1D9E75', width=size//20)
    
    # Draw FM text
    font_size = size // 4
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "FM"
    bbox = draw.textbbox((0,0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (size - text_w) // 2
    y = (size - text_h) // 2
    draw.text((x, y), text, fill='#1D9E75', font=font)
    
    img.save(f'static/{filename}')
    print(f"Created {filename}")

create_icon(192, 'icon-192.png')
create_icon(512, 'icon-512.png')
print("Icons created!")