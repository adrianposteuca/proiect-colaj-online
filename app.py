import io
from flask import Flask, request, send_file, render_template
# Am adăugat ImageOps pentru a corecta orientarea imaginii
from PIL import Image, ImageDraw, ImageFont, ImageOps 
from datetime import datetime

app = Flask(__name__)

# --- Constante ---
TEMPLATE_SIZE = (2048, 3508)
BOXES = {
    "top_left": (56, 311, 56 + 943, 311 + 1095),
    "top_right": (56 + 943 + 56, 311, 56 + 943 + 56 + 937, 311 + 1095),
    "bottom_left": (56, 1954, 56 + 943, 1954 + 1149),
    "bottom_right": (56 + 943 + 56, 1954, 56 + 943 + 56 + 937, 1954 + 1149),
}
FONT_FILE = "arial.ttf"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/generate-collage', methods=['POST'])
def generate_collage_endpoint():
    try:
        user_images_files = {
            "top_left": request.files['image_top_left'],
            "top_right": request.files['image_top_right'],
            "bottom_left": request.files['image_bottom_left'],
            "bottom_right": request.files['image_bottom_right'],
        }

        scales = {
            "top_left": float(request.form['scale_top_left']),
            "top_right": float(request.form['scale_top_right']),
            "bottom_left": float(request.form['scale_bottom_left']),
            "bottom_right": float(request.form['scale_bottom_right']),
        }

        final_image = Image.new("RGB", TEMPLATE_SIZE, "white")
        template_overlay = Image.open("template_overlay.png").convert("RGBA")

        for name, box_coords in BOXES.items():
            
            # --- BLOCUL DE COD CORECTAT ---
            # 1. Deschidem imaginea
            user_img = Image.open(user_images_files[name])
            # 2. Corectăm imediat orientarea pe aceeași variabilă
            user_img = ImageOps.exif_transpose(user_img)
            # ---------------------------------
            
            scale = scales[name]
            
            box_center_x = (box_coords[0] + box_coords[2]) / 2
            box_center_y = (box_coords[1] + box_coords[3]) / 2

            new_width = int(user_img.width * scale)
            new_height = int(user_img.height * scale)
            scaled_img = user_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            paste_x = int(box_center_x - new_width / 2)
            paste_y = int(box_center_y - new_height / 2)
            
            final_image.paste(scaled_img, (paste_x, paste_y))

        final_image.paste(template_overlay, (0, 0), template_overlay)
        
        draw = ImageDraw.Draw(final_image)
        try:
            font = ImageFont.truetype(FONT_FILE, size=40)
        except IOError:
            font = ImageFont.load_default()
        
        current_date = datetime.now().strftime("%d.%m.%Y")
        draw.text((1750, 3400), current_date, font=font, fill="black")

        img_io = io.BytesIO()
        final_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        print(f"A apărut o eroare: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
