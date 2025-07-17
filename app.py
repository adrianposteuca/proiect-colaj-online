import io
from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont, ImageOps
from whitenoise import WhiteNoise
from datetime import datetime

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")

# --- Constante ---
TEMPLATE_SIZE = (2480, 3508)
BOXES = {
    "top_left": (200, 311, 200 + 943, 311 + 1095),
    "top_right": (200 + 943 + 200, 311, 200 + 943 + 200 + 937, 311 + 1095),
    "bottom_left": (200, 1954, 200 + 943, 1954 + 1149),
    "bottom_right": (200 + 943 + 200, 1954, 200 + 943 + 200 + 937, 1954 + 1149),
}
FONT_FILE = "arial.ttf"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/generate-collage', methods=['POST'])
def generate_collage_endpoint():
    try:
        # --- LINII NOI PENTRU DEBUGGING ---
        # Vom afișa în log-urile OnRender exact ce primește serverul
        print(">>> CERERE NOUĂ PRIMITĂ <<<")
        print(f"Câmpuri TEXT primite (form): {list(request.form.keys())}")
        print(f"Fișiere primite (files): {list(request.files.keys())}")
        print("------------------------------------")
        # ------------------------------------

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

        # ... restul codului rămâne neschimbat ...
        final_image = Image.new("RGB", TEMPLATE_SIZE, "white")
        template_overlay = Image.open("template_overlay.png").convert("RGBA")

        for name, box_coords in BOXES.items():
            user_img = Image.open(user_images_files[name])
            user_img = ImageOps.exif_transpose(user_img)
            
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
        
        draw.text((2100, 3400), current_date, font=font, fill="black")

        img_io = io.BytesIO()
        final_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        # Dacă apare o eroare, o vom vedea în log-uri
        print(f"!!! A APĂRUT O EROARE ÎN TIMPUL PROCESĂRII: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
