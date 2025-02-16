# Summarizer

Summarizer is a tool that turns PDFs into clear, layman-friendly summaries using OpenAI's API. It processes research papers and other documents to generate easy-to-understand summaries.

## Setup

1. **Create a `.env` File:**  
   In the root directory of the project, create a file named `.env`. Add the following line (replace the placeholder with your actual API key):

OPENAI_API_KEY = {insert OpenAI API key here}


2. **Install Dependencies:**  
Open a terminal in the project directory and run:

pip install -r requirements.txt


## How to Summarize a PDF

1. **Place the PDF:**  
Add the desired PDF file to the project directory.

2. **Run the Script:**  
Execute the following command in the terminal:

python main.py


3. **Enter the PDF Path:**  
When prompted, enter the relative path to the PDF file.
