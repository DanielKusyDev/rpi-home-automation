import base64
import os
from typing import Tuple
from uuid import uuid4

from app.config.settings import MEDIA_ROOT
from fastapi import UploadFile


async def save_multipart_file(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1]
    file_path = os.path.join(MEDIA_ROOT, f"{uuid4().hex}.{ext}")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path


def save_base64_encoded_file(b64_string: str, ext: str) -> Tuple[str, str]:
    file_name = f"{uuid4().hex}.{ext}"
    file_path = os.path.join(MEDIA_ROOT, file_name)
    with open(file_path, "wb") as f:
        encoded_image = base64.b64decode(b64_string.split("base64")[-1])
        f.write(encoded_image)
    return file_path, file_name
