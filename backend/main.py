import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.pdf_processor import PDFProcessor
from services.qa_service import QAService

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store current QA service
current_qa_service = None

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload PDF and process its content
    """
    global current_qa_service
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Save uploaded file
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Extract text and create QA service
    pdf_text = PDFProcessor.extract_text_from_pdf(file_path)
    current_qa_service = QAService(pdf_text)
    
    return {"message": "PDF uploaded and processed successfully"}

@app.post("/ask")
async def ask_question(question: str):
    """
    Answer a question about the uploaded PDF
    """
    global current_qa_service
    
    if current_qa_service is None:
        raise HTTPException(status_code=400, detail="Please upload a PDF first")
    
    answer = current_qa_service.answer_question(question)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)