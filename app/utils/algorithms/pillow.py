from fastapi import UploadFile
from PIL import Image
import io


async def compress_image(file: UploadFile) -> bytes:
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    if image.mode == "RGBA":
        image = image.convert("RGB")
    output = io.BytesIO()
    image.save(output, format="JPEG", optimize=True, quality=85)
    return output.getvalue()
