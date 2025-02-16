import os
import fitz # this is for PyMuPDF
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()  # load .env file

api_key  = os.getenv("OPENAI_API_KEY") # change openai key in .env file, if you don't have an .env file, follow instructions below:
# 1. make a new .env in root directory
# 2. make one line of code  "OPENAI_API_KEY = {insert OPENaiAPI key here}"

if not api_key:
     raise ValueError("OPENAI_API_KEY not found in .env file")
else:
    print("API Key retrieved successfully.")

client = OpenAI(api_key=api_key)

# prompt for model which summarizes the text
SUMMARY_PROMPT = """
You are an expert in science communication. Your task is to read a research abstract and generate a clear, layman-friendly summary. Follow these guidelines:
- Clarity: Explain the abstract in simple, everyday language.
- Accuracy: Do not add any new information or interpretations.
- Structure: Cover four key points: Purpose, Methods, Results, and Conclusion.
- Length: Keep the summary under 150 words.
Here is the research:
{research}
Now, generate a lay summary.
"""
EVALUATION_PROMPT = """
You have the following abstract and the lay summary. Now evaluate the lay summary using chain-of-thought:

### Step 2: Self-Evaluation (Chain-of-Thought Reasoning)
1. Contradiction Check: Does the lay summary contradict any information in the abstract? If yes, explain how.
2. Unsupported Claims Check: Does the summary include any information that is not explicitly stated in the abstract? If yes, list the unsupported claims.
3. Overall Accuracy Check: Does the summary fully and correctly capture the abstract’s main points without omission or misinterpretation?

### Final Output
Return a final Boolean decision:
- True if the summary is accurate.
- False if it contains contradictions or unsupported claims.

**Abstract**:
{abstract}

**Lay Summary**:
{summary}

Provide your chain-of-thought reasoning and then a final True/False decision.
"""


def parse_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    extracted_text = []
    for page in doc:
        page_text = page.get_text("text")
        extracted_text.append(page_text)
    return "\n".join(extracted_text).strip()


def summarize_text(text: str) -> str:
    # summarizes the given text using GPT-4 mini
    prompt = SUMMARY_PROMPT.format(research=text)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini", # <- change model if you want
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    
    # extract the summary from the response
    summary = response.choices[0].message.content.strip()
    return summary

def evaluate_summary(abstract: str, summary: str) -> str:
    prompt_text = EVALUATION_PROMPT.format(abstract=abstract, summary=summary)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # <- change model if you want
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.0,
    )
    
    evaluation_output = response.choices[0].message.content.strip()
    return evaluation_output


def main():
    # prompt for the PDF path
    pdf_path = input("Enter the path to the PDF file: ").strip()
    if not pdf_path:
        raise ValueError("No PDF path provided.")
    
    # extract text from PDF
    full_text = parse_pdf(pdf_path)
    
    # summarize using model
    summary = summarize_text(full_text)

    
    # Evaluate the generated summary against the full paper
    evaluation = evaluate_summary(full_text, summary)
    
    # print summary
    print("\n-------------- Generated Summary ------------------------\n")
    print(summary)
    print("\n-----------------------------------------------\n")
    print(evaluation)
    print("\n-----------------------------------------------------------------------")


if __name__ == "__main__":
    main()