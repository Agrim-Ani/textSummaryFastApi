from fastapi import FastAPI, File, HTTPException, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.utils.file_processing import process_file
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
class TextRequest(BaseModel):
    fileData: str
    model: str
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

available_models = [
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it"
]

@app.post("/summarize")
async def summarize_text(request: TextRequest):
    if request.model not in available_models:
        raise HTTPException(status_code=400, detail="Invalid model selected")

    text = request.fileData
    selected_model = request.model
    print(selected_model)
    
    preview_text, full_summary, key_points = process_file(text, selected_model)
    return {
        "preview_text": preview_text,
        "full_summary": full_summary,
        "key_points": key_points
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

