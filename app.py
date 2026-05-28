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

    # Extract original name and extension
    original_name, original_ext = os.path.splitext(image.filename)
    original_ext = original_ext.lower()

    # Build new filename
    new_filename = f"{original_name}_wm{original_ext}"
    print(f"Original filename: {image.filename}, new filename: {new_filename}")

    # Temporary paths optimized to use the unique new filename 
    # to prevent multiple uploads from overwriting each other
    input_path = f"input_{new_filename}"
    output_path = f"output_{new_filename}"

    # Save uploaded file
    image.save(input_path)

    # Apply watermark
    engine.apply_watermark(input_path, text, output_path)

    # Correct MIME type
    ext = original_ext.replace(".", "")
    if ext in ["jpg", "jpeg"]:
        mimetype = "image/jpeg"
    elif ext == "png":
        mimetype = "image/png"
    elif ext in ["tif", "tiff"]:
        mimetype = "image/tiff"
    else:
        mimetype = "application/octet-stream"

    # Prepare the file response
    response = send_file(
        output_path,
        mimetype=mimetype,
        as_attachment=True,
        download_name=new_filename,
        conditional=False
    )

    # Force browser compliance for the custom filename via standard HTTP headers
    response.headers["Content-Disposition"] = f'attachment; filename="{new_filename}"'

    return response

if __name__ == "__main__":
    app.run(debug=True)
