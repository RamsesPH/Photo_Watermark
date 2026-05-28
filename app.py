from flask import Flask, render_template, request, send_file
from watermark import WatermarkEngine
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
engine = WatermarkEngine()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/watermark", methods=["POST"])
def watermark():
    if "image" not in request.files:
        return "No image uploaded", 400

    image = request.files["image"]
    text = request.form.get("text", "")

    # Extract name + extension
    original_name, original_ext = os.path.splitext(image.filename)
    original_ext = original_ext.lower().replace(".", "")

    # Build new filename
    new_filename = f"{original_name}_wm.{original_ext}"

    # Apply watermark entirely in memory
    output_buffer = engine.apply_watermark(image.stream, text, original_ext)

    # Correct MIME type
    if original_ext in ["jpg", "jpeg"]:
        mimetype = "image/jpeg"
    elif original_ext == "png":
        mimetype = "image/png"
    elif original_ext in ["tif", "tiff"]:
        mimetype = "image/tiff"
    else:
        mimetype = "application/octet-stream"

    # Send the in-memory file
    return send_file(
        output_buffer,
        mimetype=mimetype,
        as_attachment=True,
        download_name=new_filename
    )


if __name__ == "__main__":
    app.run(debug=True)
