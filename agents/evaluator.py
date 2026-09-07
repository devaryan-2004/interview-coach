import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class EvaluatorAgent:

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

    def evaluate(
        self,
        question,
        answer,
        role
    ):

        prompt = f"""
You are a professional technical interview evaluator.

Candidate Job Role:
{role}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the candidate's answer.

Provide:

1. Score out of 10
2. What the candidate did well
3. What could be improved
4. Missing technical points
5. A better sample answer
6. Communication feedback
7. Whether the candidate should move to the next question

Be honest but constructive.

The candidate may be a fresher, so explain technical
concepts in a simple and understandable way.

Use clear headings and bullet points.
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