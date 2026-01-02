from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

User = get_user_model()

class Photo(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    capture_date = models.DateField(null=True, blank=True)
    original_image = models.ImageField(upload_to='photos/originals/')
    watermarked_image = models.ImageField(upload_to='photos/watermarked/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check if this is an existing object to avoid re-processing if not needed
        # Or simply check if a new original_image is set but watermarked_image isn't.
        # Here we process if we have an original_image and no watermarked_image.
        # (A robust real-world app might track field changes better)
        
        process_watermark = False
        if self.original_image and not self.watermarked_image:
            process_watermark = True

        super().save(*args, **kwargs) # Save first to ensure file is available/referenced if needed

        if process_watermark and self.original_image:
            self._process_image()
            # Save again to update the watermarked_image field
            # Avoid endless loop by passing update_fields? 
            # OR better: do it before super().save() but accessing file content
            # might require the file to be readable. 
            # In memory files (uploads) are readable.
            # Let's adjust: call processing *after* save to be safe with storage backends
            # then save again.
            super().save(update_fields=['watermarked_image'])

    def _process_image(self):
        if not self.original_image:
            return

        # Open the original image
        # Note: 'self.original_image' is a FieldFile. We can open it.
        try:
            with self.original_image.open('rb') as f:
                image = Image.open(f)
                image = image.convert('RGB') # Ensure RGB for JPEG

                # 1. Compress / Resize if needed (Optional: maintain aspect ratio)
                # For this task, we'll just re-save as JPEG which handles compression.
                # Let's ensure it's not massive, max width 1920? User didn't specify size, just "compressed".
                # We'll stick to quality reduction.
                
                # 2. Add Watermark
                draw = ImageDraw.Draw(image)
                text = "TMF-Marketplace"
                
                # Try to load a font, fall back to default
                try:
                    # Generic font availability varies by OS
                    font = ImageFont.truetype("arial.ttf", 36)
                except IOError:
                    font = ImageFont.load_default()

                # Basic positioning: Bottom Right
                # Calculate text size (rudimentary for default font)
                # For default font, getbbox might not be perfect or available in older PIL
                # but 'getbbox' is standard in newer Pillow.
                
                if hasattr(font, 'getbbox'):
                     bbox = font.getbbox(text)
                     text_width = bbox[2] - bbox[0]
                     text_height = bbox[3] - bbox[1]
                else:
                     text_width, text_height = draw.textsize(text, font) # Deprecated in newer Pillow

                width, height = image.size
                x = width - text_width - 20
                y = height - text_height - 20
                
                # Draw text (White with black outline for visibility?)
                # Simple white text for now as per "Add a text watermark" request.
                draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))

                # 3. Save to BytesIO
                output_io = BytesIO()
                image.save(output_io, format='JPEG', quality=70) # Compressed quality
                
                # Create a simple filename
                name_parts = self.original_image.name.split('/')[-1].split('.')
                filename = f"{name_parts[0]}_watermarked.jpg"

                self.watermarked_image.save(filename, ContentFile(output_io.getvalue()), save=False)
        except Exception as e:
            print(f"Error processing image: {e}")
            # In production, log this error propertly
