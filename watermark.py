
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os


class WatermarkEngine:
    def __init__(self, font_path="assets/fonts/OpenSans-Regular.ttf", font_size=40):
        self.font_path = font_path
        self.font_size = font_size

        if not os.path.exists(self.font_path):
            raise FileNotFoundError(f"Font file not found: {self.font_path}")

    def apply_watermark(self, file_stream, text, ext):
        """Apply watermark entirely in memory and return a BytesIO."""
        
        # Load image from memory
        image = Image.open(file_stream).convert("RGBA")

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

        # Prepare output buffer
        output_buffer = BytesIO()

        # Save based on extension
        if ext in ["jpg", "jpeg"]:
            watermarked = watermarked.convert("RGB")
            watermarked.save(output_buffer, format="JPEG", quality=95)
        elif ext == "png":
            watermarked.save(output_buffer, format="PNG")
        elif ext in ["tif", "tiff"]:
            watermarked.save(output_buffer, format="TIFF")
        else:
            watermarked = watermarked.convert("RGB")
            watermarked.save(output_buffer, format="JPEG")

        output_buffer.seek(0)
        return output_buffer

