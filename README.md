# Photo Watermark App

A lightweight Flask application that applies a centered text watermark to uploaded images (JPG, PNG, TIFF).  
The app uses Pillow for image processing and Bootstrap for a simple, responsive UI.

## ✨ Features
- Upload an image from your computer
- Add custom watermark text
- Download the watermarked image with the correct filename
- Supports JPG, PNG, TIFF formats
- Clean UI with live preview
- Fully client‑side controlled download filename

## 🛠 Tech Stack
- Python 3.9
- Flask
- Pillow (PIL)
- JavaScript (Fetch API)
- Bootstrap 5

## 📦 Installation

```bash
pip install -r requirements.txt

## ▶️ Running the App
Then open your browser and go to:
http://127.0.0.1:5000

## Project Structure

Photo_Watermark/
│── app.py
│── watermark.py
│── README.md
│── .gitignore
│── requirements.txt
│── static/
│   ├── script.js
│   └── style.css
│── templates/
│   └── index.html
│── assets/
│   └── fonts/

## How It Works

- User uploads an image
- Flask saves it temporarily
- Pillow applies the watermark
- Flask returns the processed image
- JavaScript triggers a download with the correct filename

## License

MIT License


