from flask import Flask, render_template, request
from rembg import remove
from PIL import Image
import os
import uuid
import threading
import time

app = Flask(__name__)

TEMP_DIR = 'temp'
os.makedirs(TEMP_DIR, exist_ok=True)

def delete_file_later(filepath, delay=60):
    def delete():
        time.sleep(delay)
        if os.path.exists(filepath):
            os.remove(filepath)
    threading.Thread(target=delete, daemon=True).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    output_file = None
    if request.method == 'POST':
        image = request.files['image']
        if image:
            file_id = str(uuid.uuid4())
            input_path = os.path.join(TEMP_DIR, f"{file_id}_input.png")
            output_path = os.path.join(TEMP_DIR, f"{file_id}_output.png")

            image.save(input_path)

            with Image.open(input_path) as img:
                result = remove(img)
                result.save(output_path)

            delete_file_later(input_path)
            delete_file_later(output_path)

            output_file = os.path.basename(output_path)

    return render_template('index.html', filename=output_file)

@app.route('/temp/<filename>')
def serve_temp_file(filename):
    return app.send_static_file(os.path.join(TEMP_DIR, filename))

if __name__ == '__main__':
    app.run(debug=True)