# ⚖️ LawLens - Legal Research Assistant

An AI-powered legal research assistant that provides legal advisory, case outcome prediction, and report generation services.

## Features

- **Legal Advisory**: Get comprehensive legal advice based on uploaded documents
- **Case Outcome Prediction**: Predict likely case outcomes with probability assessments
- **Legal Report Generation**: Generate structured legal reports with key findings and recommendations

## Tech Stack

- **Backend**: FastAPI, LangChain, Groq API
- **Frontend**: Streamlit
- **Document Processing**: PyPDF2
- **AI Model**: Llama-3.1-8b-instant via Groq

## Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LawLens.git
cd LawLens
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn hybrid_main:app --host 0.0.0.0 --port 9001 --reload
```

2. Start the frontend (in a new terminal):
```bash
cd frontend
streamlit run app.py
```

3. Open your browser and navigate to the Streamlit URL (typically `http://localhost:8501`)

## Usage

1. Upload one or more PDF legal documents
2. Enter your legal query
3. Select the desired service:
   - Legal Advisory
   - Legal Report Generation
   - Case Outcome Prediction
4. Click "Get Response" to receive AI-powered insights

## API Endpoints

- `GET /` - Welcome message
- `POST /legal-advisory/` - Get legal advice
- `POST /case-outcome-prediction/` - Predict case outcomes
- `POST /report-generator/` - Generate legal reports

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for informational purposes only and does not constitute legal advice. Always consult with qualified legal professionals for actual legal matters.