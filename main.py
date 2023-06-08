from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import io

app = FastAPI()

# Configurar CORS
origins = ["*"]  # Puedes ajustar los orígenes permitidos según tus necesidades

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/remove_background")
async def remove_background(file: UploadFile = File(...)):
    # Leer imagen
    image = Image.open(file.file)

    # Remover fondo
    output_image = remove(image)

    # Convertir imagen de salida a bytes
    output_bytes = io.BytesIO()
    output_image.save(output_bytes, format="PNG")
    output_bytes.seek(0)

    return {"background_removed_image": output_bytes}


# Punto de entrada principal
if __name__ == "__main__":
    import uvicorn
    import os

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host=host, port=port)
