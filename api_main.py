from fastapi import FastAPI, File, UploadFile
from face_recog import FaceRecognitionService

app = FastAPI()

@app.get("/")
async def root():
  return {'message': "Hello world!"}

@app.post("/facecomparison/")
async def upload_image(known: UploadFile = File(...)):
  result = FaceRecognitionService().saveImageFromFile(known.file)
  #print(type(known.file.read()))
  return {
    'known': known.filename,
    #'result': result,
  }
