import os
from PIL import Image, ImageDraw, ImageFont

class WatermarkEngine:
    def __init__(self, font_path="assets/fonts/OpenSans-Regular.ttf", font_size=40):
        self.font_path = font_path
        self.font_size = font_size

        if not os.path.exists(self.font_path):
            raise FileNotFoundError(f"Font file not found: {self.font_path}")

    def apply_watermark(self, image_path, text, output_path):
        """Apply a text watermark to an image and save the result."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Load image safely
        image = Image.open(image_path)
        image = image.convert("RGBA")

        # Create watermark layer
        watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)

        # Load font
        font = ImageFont.truetype(self.font_path, self.font_size)

        # Center text
        text_width, text_height = draw.textsize(text, font=font)
        x = (image.width - text_width) // 2
        y = (image.height - text_height) // 2

        draw.text((x, y), text, font=font, fill=(255, 255, 255, 120))

        # Merge layers
        watermarked = Image.alpha_composite(image, watermark_layer)

        # Determine extension
        ext = os.path.splitext(output_path)[1].lower()

        # Save correctly based on extension
        if ext in [".jpg", ".jpeg"]:
            watermarked = watermarked.convert("RGB")
            watermarked.save(output_path, format="JPEG", quality=95)
        elif ext == ".png":
            watermarked.save(output_path, format="PNG")
        elif ext in [".tif", ".tiff"]:
            watermarked.save(output_path, format="TIFF")
        else:
            watermarked = watermarked.convert("RGB")
            watermarked.save(output_path)

        return output_path
