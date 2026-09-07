import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class InterviewerAgent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Please add it to the .env file."
            )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def ask_question(
        self,
        role,
        difficulty,
        previous_questions=None,
        candidate_answer=None
    ):

        previous_questions = previous_questions or []

        previous_text = "\n".join(
            f"- {question}"
            for question in previous_questions
        )

        prompt = f"""
You are an experienced technical interviewer.

Candidate Job Role:
{role}

Interview Difficulty:
{difficulty}

Previously Asked Questions:
{previous_text if previous_text else "None"}

Candidate's Previous Answer:
{candidate_answer if candidate_answer else "This is the first question."}

Your task is to generate the NEXT interview question.

Rules:

1. Ask only ONE question.
2. Do not repeat any previous question.
3. Keep the question relevant to the candidate's job role.
4. Match the requested difficulty.
5. Prefer practical and real-world interview questions.
6. Do not provide the answer.
7. If the candidate has answered a previous question,
   use that answer to ask a deeper follow-up question when appropriate.
8. Keep the question suitable for a technical job interview.

Return ONLY the interview question.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()