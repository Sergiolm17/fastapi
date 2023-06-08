from fastapi import FastAPI, UploadFile, File
from rembg import remove
from PIL import Image
import io


from pydantic import BaseModel

app = FastAPI()

class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}

@app.post("/remove_background")
async def process_image(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read())).convert("RGBA")
    image_bytes = image.tobytes()
    output_image = remove_background(image_bytes)
    output_image_pil = Image.frombytes("RGBA", image.size, output_image)
    output_image_pil_bytes = io.BytesIO()
    output_image_pil.save(output_image_pil_bytes, format="PNG")
    output_image_pil_bytes.seek(0)
    return {"file": output_image_pil_bytes}