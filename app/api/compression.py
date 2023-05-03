import codecs
import io
import os
import pathlib
import tempfile
import zipfile
import zlib
from io import BytesIO
from PIL import Image
from fastapi import APIRouter, File, UploadFile
from typing import Generator
from fastapi.responses import StreamingResponse, JSONResponse
import gzip

from app.utils.algorithms.lzw import compress_lzw
from app.utils.algorithms.pillow import compress_image
from app.utils.algorithms.rle import rle_encode
from app.utils.algorithms.huffman import compress_huffman
from app.utils.extenstions import ext_to_func

router = APIRouter()


async def get_data_from_file(file_path) -> Generator:
    with open(file_path, mode="rb") as file:
        yield file.read()


@router.post("/compress/huffman")
async def compress_file(file: UploadFile = File()):
    ext = "." + file.filename.split(".")[-1]
    if ext not in ext_to_func:
        return JSONResponse(
            {"Detail": f"File extension {ext} is not supported"}, status_code=422
        )

    compressed_data = await ext_to_func[ext](file)
    headers = {
        "Content-Disposition": f"attachment; filename={file.filename.split('.')[0]}_compressed{ext}"
    }
    return StreamingResponse(io.BytesIO(compressed_data), headers=headers)


@router.post("/compress/image")
async def compress_file(file: UploadFile = File()):
    ext = "." + file.filename.split(".")[-1]
    if ext not in ext_to_func:
        return JSONResponse(
            {"Detail": f"File extension {ext} is not supported"}, status_code=422
        )

    compressed_data = await ext_to_func[ext](file)
    headers = {
        "Content-Disposition": f"attachment; filename={file.filename.split('.')[0]}_compressed{ext}"
    }
    return StreamingResponse(io.BytesIO(compressed_data), headers=headers)


@router.post("/compress/rle")
async def compress_file(file: UploadFile = File()):
    ext = "." + file.filename.split(".")[-1]
    if ext not in ext_to_func:
        return JSONResponse(
            {"Detail": f"File extension {ext} is not supported"}, status_code=422
        )

    compressed_data = await ext_to_func[ext](file)
    headers = {
        "Content-Disposition": f"attachment; filename={file.filename.split('.')[0]}_compressed{ext}"
    }
    return StreamingResponse(io.BytesIO(compressed_data), headers=headers)


@router.post("/compress/lzw")
async def compress_file(file: UploadFile = File()):
    ext = "." + file.filename.split(".")[-1]
    if ext not in ext_to_func:
        return JSONResponse(
            {"Detail": f"File extension {ext} is not supported"}, status_code=422
        )

    compressed_data = await ext_to_func[ext](file)
    headers = {
        "Content-Disposition": f"attachment; filename={file.filename.split('.')[0]}_compressed{ext}"
    }
    return StreamingResponse(io.BytesIO(compressed_data), headers=headers)
