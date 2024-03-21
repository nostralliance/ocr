from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import easyocr
import io
import requests

app = FastAPI()
reader = easyocr.Reader(['en', 'fr'], gpu=False)

def img2text(image_content):
    # Detect text in the image using OCR
    detection_result = reader.detect(image_content, width_ths=0.7, mag_ratio=1.5)
    recognition_results = reader.recognize(image_content, horizontal_list=detection_result[0][0], free_list=[])

    textList = []
    for result in recognition_results:
        textList.append(result[1])

    # Return the list of extracted texts from the image
    return " ".join(textList)

@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Read the image file and extract text
        image_content = await file.read()
        print(type(image_content))
        extracted_text = img2text(image_content)
        return JSONResponse(content={"text": extracted_text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
