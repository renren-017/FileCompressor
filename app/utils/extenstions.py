from app.utils.algorithms.pillow import compress_image

image_exts = [
    ".bmp",
    ".dib",
    ".eps",
    ".gif",
    ".icns",
    ".ico",
    ".im",
    ".jpg",
    ".jpeg",
    ".jpe",
    ".j2k",
    ".j2c",
    ".jp2",
    ".msp",
    ".pcx",
    ".png",
    ".ppm",
    ".spi",
    ".tga",
    ".tif",
    ".tiff",
    ".webp",
    ".xbm",
    ".xv",
]

ext_to_func = {key: compress_image for key in image_exts}
