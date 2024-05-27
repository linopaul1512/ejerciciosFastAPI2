from typing import Annotated
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}

<<<<<<< HEAD
@app.post("/uploadfiles")
=======
@app.post("uploadfiles")
>>>>>>> 379a9588bcea96afeabd4cc0d6520a1b0aabd2d3
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}