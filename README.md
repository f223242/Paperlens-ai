# PaperLens AI

PaperLens AI is a research-intelligence project that helps users summarize and understand research papers using AI. The app presents a premium dark landing page and allows users to select a paper, choose a summary style, and generate a concise summary with Hugging Face models.

## Project Overview

This project demonstrates:
- AI-powered research summarization
- Hugging Face LLM integration with LangChain
- Streamlit-based interactive UI
- Dark premium landing page design for a research tool

## Features
- Modern PaperLens AI landing page
- Research paper selection UI
- Summary style selection
- Length selection
- AI-generated summary output
- Error handling for missing API keys or model failures
- Responsive design for browser use

## Tech Stack
- Python
- Streamlit
- LangChain
- LangChain Hugging Face integration
- Hugging Face Hub
- Python-dotenv

## Project Structure

```bash
GenAi(LLMS)/
├── summarize_papers/
│   ├── summarization_by_opensource.py
│   ├── template.py
│   └── template.json
├── .env
├── requirements.txt
├── test.py
├── README.md
└── ...
```

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the environment:

Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Hugging Face token:

```env
huggingface_api_key=your_token_here
```

5. Run the app:

```bash
python -m streamlit run summarize_papers/summarization_by_opensource.py
```

## Usage

- Open the app in your browser.
- Choose a research paper.
- Select the explanation style and length.
- Click the main action button to generate the summary.
- Review the AI-generated summary result.

## Notes

- This project uses the Hugging Face model from the configured repo in the app.
- If the API token is missing or invalid, the app will show an error message instead of failing silently.

## Demo / Social Media Use

You can use this project as a portfolio/demo project to showcase:
- AI product design
- LLM integration workflow
- research summarization UX
- modern dark UI design

## License

This project is for educational and portfolio use.

## Author

Created for AI research and summarization experiments.
