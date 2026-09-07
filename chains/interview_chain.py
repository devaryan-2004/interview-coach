from agents.interviewer import InterviewerAgent


class InterviewChain:

    def __init__(self, memory):
        self.interviewer = InterviewerAgent()
        self.memory = memory

    def generate_question(
        self,
        role,
        difficulty
    ):
        previous_questions = self.memory.get_questions()

        previous_answer = self.memory.get_last_answer()

        question = self.interviewer.ask_question(
            role=role,
            difficulty=difficulty,
            previous_questions=previous_questions,
            candidate_answer=previous_answer
        )

        self.memory.add_question(question)

        return question