from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    files = request.files.getlist("images")

    if not files:
        return "No se subieron imágenes"

    images = []

    for file in files:
        if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        try:
            img = Image.open(file).convert("RGB")
            images.append(img)
        except:
            continue

    if not images:
        return "No hay imágenes válidas"

    pdf_bytes = io.BytesIO()
    images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, download_name="anacrazy.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)