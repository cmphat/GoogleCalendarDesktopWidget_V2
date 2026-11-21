import os
from PIL import Image, ImageDraw

def create_calendar_icon(output_path):
    # Create high-res 64x64 RGBA canvas
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Rounded base calendar body (Google Blue)
    draw.rounded_rectangle([4, 8, 60, 60], radius=8, fill='#1A73E8')
    
    # White page area
    draw.rounded_rectangle([8, 22, 56, 56], radius=6, fill='#FFFFFF')
    
    # Spiral / Ring binder loops at the top
    draw.rounded_rectangle([14, 4, 18, 14], radius=2, fill='#DADCE0')
    draw.rounded_rectangle([46, 4, 50, 14], radius=2, fill='#DADCE0')
    
    # Mini calendar grid / colored dots inside
    # Row 1: Google Blue dots
    draw.rectangle([14, 28, 22, 34], fill='#4285F4')
    draw.rectangle([28, 28, 36, 34], fill='#34A853')
    draw.rectangle([42, 28, 50, 34], fill='#FBBC05')
    
    # Row 2: Google colors
    draw.rectangle([14, 40, 22, 46], fill='#EA4335')
    draw.rectangle([28, 40, 36, 46], fill='#4285F4')
    draw.rectangle([42, 40, 50, 46], fill='#34A853')
    
    # Save as multi-size ICO
    img.save(output_path, format='ICO', sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)])
    print(f'Successfully created icon at: {output_path}')

if __name__ == '__main__':
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    out_ico = os.path.join(cur_dir, 'calendar.ico')
    create_calendar_icon(out_ico)
