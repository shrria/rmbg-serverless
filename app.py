from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return render_template("index.html")

    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    if file.filename == "":
        return "No file selected", 400

    input_image = Image.open(file.stream)
    output_image = remove(input_image, post_process_mask=True)
    img_io = BytesIO()
    output_image.save(img_io, "PNG")
    img_io.seek(0)

    original_filename = file.filename
    output_filename = original_filename.split(".")[0] + "_rmbg.png"

    return send_file(
        img_io, mimetype="image/png", as_attachment=True, download_name=output_filename
    )


if __name__ == "__main__":
    port = 5000
    app.run(host="0.0.0.0", port=port)
