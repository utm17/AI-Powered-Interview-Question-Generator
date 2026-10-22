# AI-Powered Interview Question Generator & Hiring Workflow Automation

An AI-assisted recruitment workflow prototype that streamlines interview question creation, hiring-manager review, and structured candidate evaluation using Generative AI, Streamlit, Google Sheets, and Google Apps Script.

## Overview

Creating role-specific interview questions and evaluating candidates consistently can require significant manual effort from recruiters and hiring managers.

This project explores how Generative AI and lightweight workflow automation can reduce that effort by connecting three stages of the interview process:

1. **AI-powered question generation** — Generate structured interview questions from a job description using Google Gemini.
2. **Human review and approval** — Export questions to CSV and import them into Google Sheets, where a hiring manager can edit, remove, or approve questions.
3. **Structured candidate evaluation** — Present approved questions through a web-based scoring interface and record interviewer ratings, notes, timestamps, and total scores in Google Sheets.

The workflow combines AI-generated content with human oversight rather than relying on AI to make hiring decisions.

## Key Features

- **Job description processing:** Accept job descriptions through pasted text or uploaded TXT and PDF files.
- **AI-generated questions:** Generate 10–15 questions tailored to the role's responsibilities, tools, metrics, and requirements.
- **Competency-based categorization:** Organize questions into five predefined categories.
- **Editable review workflow:** Export questions to CSV for review and approval in Google Sheets.
- **Candidate scoring interface:** Display approved questions alongside individual rating and notes fields.
- **Structured score recording:** Save candidate details, question-level ratings, interviewer notes, and timestamps to Google Sheets.
- **Automatic total calculation:** Calculate the sum of the submitted question scores for each candidate.
- **Lightweight implementation:** Use Streamlit and Google Apps Script without building a separate backend service.

## Workflow Architecture

```text
             Job Description
                    |
                    v
          Streamlit Web Application
                    |
                    v
           Google Gemini API
                    |
                    v
        Generate 10–15 Questions
                    |
                    v
       Categorize and Display Output
                    |
                    v
              CSV Export
                    |
                    v
       Google Sheets Review Layer
       (Edit, Remove, Approve)
                    |
                    v
      Google Apps Script Web App
                    |
                    v
       Interviewer Scores + Notes
                    |
                    v
          Google Sheets Results
       (Timestamp, Ratings, Total)
```

**Important:** The Streamlit-to-review handoff currently uses a CSV export and manual Google Sheets import. The Apps Script scoring interface reads approved questions from the spreadsheet. This is a staged workflow prototype, not a fully automatic ATS integration.

## Competency Framework

The question-generation prompt instructs Gemini to organize questions into five categories:

| Category | Purpose |
|---|---|
| Intent | Understand motivation, role fit, and career direction. |
| Quant Ability | Assess numerical reasoning, estimation, and analytical thinking. |
| Job Competency | Evaluate role-specific skills, tools, methods, and domain knowledge. |
| Core Competency | Assess structured thinking, communication, ownership, and problem-solving. |
| EQ | Explore self-awareness, collaboration, failure handling, and responses to pressure. |

The target is 10–15 questions per job description, with category-specific count ranges defined in the prompt. The generated output should be reviewed before being used in an interview.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core logic for question generation and data processing. |
| Streamlit | Interactive interface for submitting job descriptions and viewing generated questions. |
| Google Gemini API | Generate role-specific interview questions. |
| Pandas | Organize generated questions into tabular data. |
| PyPDF | Extract text from uploaded PDF job descriptions. |
| CSV | Transfer generated questions to the review stage. |
| Google Sheets | Review questions and store candidate evaluation records. |
| Google Apps Script | Connect the scoring interface to Google Sheets. |
| HTML, CSS, JavaScript | Build the browser-based interviewer scoring interface. |

## Getting Started

### Prerequisites

- Python 3.9 or a compatible Python version supported by the installed dependencies.
- A Google Gemini API key.
- A Google account with access to Google Sheets and Google Apps Script.
- A modern web browser.

### 1. Clone the Repository

```bash
git clone https://github.com/utm17/AI-Powered-Interview-Question-Generator.git
cd AI-Powered-Interview-Question-Generator
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Obtain an API key through [Google AI Studio](https://aistudio.google.com/apikey).

You can enter the key directly into the password-protected API-key field in the application's sidebar.

Alternatively, configure the `GEMINI_API_KEY` environment variable before launching the application.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

**macOS/Linux:**

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Do not commit API keys or other credentials to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL in the terminal. Open that URL in your browser.

## How to Use the Question Generator

1. Open the Streamlit application.
2. Enter your Gemini API key if it has not already been configured.
3. Upload a TXT/PDF job description or paste the job description into the text field.
4. Click **Generate Interview Questions**.
5. Review the questions grouped by competency category.
6. Download the generated CSV file for the human-review stage.

The exported CSV contains these columns:

- `Category`
- `Question`
- `Include?`

The generated questions are AI-produced suggestions and should be checked for relevance, clarity, and job-specific accuracy.

## Setting Up the Review and Scoring Interface

The second component uses Google Sheets and Google Apps Script.

### 1. Prepare the Google Spreadsheet

Create a Google spreadsheet with the following sheets:

- `Sheet1` — Stores questions and their approval status.
- `Scores` — Stores submitted evaluation records. The script creates this sheet and its headers when required.

Import the generated CSV into `Sheet1`. Ensure the columns are arranged as follows:

| Column | Field | Purpose |
|---|---|---|
| A | Category | Competency category of the question. |
| B | Question | Interview question text. |
| C | Include? | Boolean approval status; use checkboxes. |

Keep the header row in row 1 and question records from row 2 onward. Ensure the `Include?` cells contain actual Boolean values (`TRUE` or `FALSE`), as the Apps Script filters approved questions using Boolean `TRUE`.

The hiring manager can edit questions and mark the ones to include in the interview.

### 2. Configure Google Apps Script

1. Open the spreadsheet.
2. Navigate to **Extensions → Apps Script**.
3. Copy the contents of `Code.gs` into the script editor.
4. Create an HTML file named `Index.html` and copy the contents of the repository's `Index.html` into it.
5. Save the project.

The Apps Script functions perform the following operations:

- `doGet()` — Serves the candidate-scoring interface.
- `getFinalQuestions()` — Retrieves approved questions from `Sheet1`.
- `submitScores(payload)` — Writes individual evaluation records and the total score to the `Scores` sheet.

### 3. Deploy the Web Application

1. Select **Deploy → New deployment** in Apps Script.
2. Choose **Web app** as the deployment type.
3. Configure access according to your organization's security requirements.
4. Deploy and authorize the required Google Sheets permissions.
5. Open the generated web-app URL to access the scoring interface.

Deployment options and authorization requirements depend on your Google account and organization settings.

### 4. Evaluate a Candidate

1. Open the deployed scoring interface.
2. Enter the candidate's name.
3. Review each approved interview question.
4. Assign a score from 1 to 5.
5. Add optional notes about the candidate's response.
6. Click **Submit Scores**.

The submitted records are stored in Google Sheets with a timestamp, candidate name, category, question, score, and notes. A separate total row records the sum of the question scores.

## Project Structure

```text
AI-Powered-Interview-Question-Generator/
│
├── app.py              # Gemini-powered question generation
├── Code.gs             # Google Apps Script backend
├── Index.html          # Interviewer scoring interface
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
│
└── .devcontainer/      # Development container configuration
```

## Practical Applications

- Recruitment workflow prototyping.
- Interview preparation for role-specific hiring.
- Standardizing interview-question categories.
- Reducing repetitive question-drafting effort.
- Structuring interviewer feedback and candidate evaluation.
- Exploring low-code process automation for HR and operations teams.

## Limitations and Future Improvements

The current implementation is a functional prototype with a manual handoff between its stages.

Potential improvements include:

- Automate CSV-to-Google-Sheets transfer and approval notifications.
- Add validation for missing or malformed AI-generated output.
- Introduce retries and clearer error handling for API failures.
- Add candidate identifiers to improve record tracking.
- Calculate normalized scores or category-level summaries.
- Build a dashboard for comparing candidate evaluations.
- Add authentication and access controls for interviewer data.
- Integrate with an applicant tracking system (ATS).
- Add audit trails for question edits and approval decisions.

## Responsible Use

This project is intended to support recruiters and interviewers, not replace their judgment.

AI-generated questions may contain inaccuracies or introduce bias. Review questions before use, apply consistent evaluation criteria, and protect candidate information. Candidate scores should be interpreted in context rather than used as the sole basis for hiring decisions.

## Author

**Utkarsh Mishra**

- GitHub: [@utm17](https://github.com/utm17)

## License

No license has currently been specified for this repository. Add a `LICENSE` file before distributing the project for reuse.
