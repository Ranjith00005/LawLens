import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
import PyPDF2
import io
from typing import List
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
chat = ChatGroq(model="llama-3.1-8b-instant", api_key=groq_api_key)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Legal Research API! Please use one of the endpoints for requests."}

async def extract_pdf_text(files: List[UploadFile]):
    pdf_text = ""
    for file in files:
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() + "\n"
    return pdf_text

@app.post("/legal-advisory/")
async def legal_advisory_endpoint(
    query: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    
    pdf_text = await extract_pdf_text(files)
    
    # can be processed?
    if len(pdf_text.strip()) == 0:
        return {"result": "ERROR: Cannot process this document."}
    
    # Limit document size 
    if len(pdf_text) > 8000:
        pdf_text = pdf_text[:8000] + "\n\n[Document truncated due to length...]"
    
    prompt = f"""
    You are a legal advisor. Based on the following legal document and query, provide comprehensive legal advice.
    
    Document Content:
    {pdf_text}
    
    Query: {query}
    
    Please provide:
    1. Legal analysis of the situation
    2. Available legal options
    3. Recommended actions
    4. Potential risks and considerations
    """
    
    try:
        response = chat.invoke(prompt)
        return {"result": response.content}
    except Exception as e:
        print(f"Error details: {str(e)}")
        # Dynamic fallback based on document content
        doc_preview = pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text
        basic_analysis = f"""
LEGAL ADVISORY ANALYSIS

Query: {query}

Document Preview:
{doc_preview}

1. DOCUMENT ANALYSIS:
- Document contains {len(pdf_text)} characters
- Appears to be a legal document requiring analysis
- Content suggests contractual or legal matter

2. GENERAL LEGAL OPTIONS:
- Review all terms and conditions carefully
- Seek professional legal counsel
- Document all relevant communications
- Consider response timelines

3. NEXT STEPS:
- Consult with qualified attorney
- Gather supporting documentation
- Assess legal risks and options

Note: AI processing temporarily unavailable. This is a basic analysis.
"""
        return {"result": basic_analysis}

@app.post("/case-outcome-prediction/")
async def case_outcome_prediction_endpoint(
    query: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    
    pdf_text = await extract_pdf_text(files)
    
    # Check if document can be processed
    if len(pdf_text.strip()) == 0:
        return {"prediction": "ERROR: Cannot process this document. The PDF appears to be image-based or contains no extractable text. Please convert to a text-based PDF or use OCR to extract text first."}
    
    prompt = f"""
    You are a legal case outcome predictor. Based on the following legal document and query, predict the likely case outcome.
    
    Document Content:
    {pdf_text}
    
    Query: {query}
    
    Please provide:
    1. Likelihood assessment (High/Medium/Low probability)
    2. Key factors influencing the outcome
    3. Potential scenarios
    4. Recommendations for improving chances
    """
    
    try:
        response = chat.invoke(prompt)
        return {"prediction": response.content}
    except Exception as e:
        doc_preview = pdf_text[:300] + "..." if len(pdf_text) > 300 else pdf_text
        return {"prediction": f"""
CASE OUTCOME PREDICTION

Query: {query}

Document Analysis:
{doc_preview}

Prediction Assessment:
- LIKELIHOOD: Requires detailed legal analysis
- KEY FACTORS: Document content, legal precedents, jurisdiction
- SCENARIOS: Multiple outcomes possible based on case specifics
- RECOMMENDATION: Seek professional legal evaluation

Note: AI prediction temporarily unavailable. Professional consultation recommended.
"""}

@app.post("/report-generator/")
async def report_generator_endpoint(
    query: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a query.")
    
    pdf_text = await extract_pdf_text(files)
    
    # Check if document can be processed
    if len(pdf_text.strip()) == 0:
        return {"report": "ERROR: Cannot process this document. The PDF appears to be image-based or contains no extractable text. Please convert to a text-based PDF or use OCR to extract text first."}
    
    prompt = f"""
    You are a legal report generator. Create a comprehensive legal report based on the following document and query.
    
    Document Content:
    {pdf_text}
    
    Query: {query}
    
    Generate a structured legal report with:
    1. Executive Summary
    2. Key Findings
    3. Legal Analysis
    4. Recommendations
    5. Conclusion
    """
    
    try:
        response = chat.invoke(prompt)
        return {"report": response.content}
    except Exception as e:
        doc_preview = pdf_text[:400] + "..." if len(pdf_text) > 400 else pdf_text
        return {"report": f"""
LEGAL REPORT

Executive Summary:
Analysis requested for: {query}

Document Overview:
{doc_preview}

Key Findings:
- Document length: {len(pdf_text)} characters
- Content type: Legal document
- Analysis scope: {query}

Recommendations:
- Professional legal review required
- Document appears to contain important legal information
- Consultation with qualified attorney advised

Conclusion:
This document requires comprehensive legal analysis by a qualified professional.

Note: AI report generation temporarily unavailable.
"""}