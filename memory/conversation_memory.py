class ConversationMemory:

    def __init__(self):
        self.history = []

    def add_question(self, question):
        self.history.append({
            "question": question,
            "answer": None
        })

    def add_answer(self, answer):
        if self.history:
            self.history[-1]["answer"] = answer

    def get_questions(self):
        return [
            item["question"]
            for item in self.history
        ]

    def get_answers(self):
        return [
            item["answer"]
            for item in self.history
            if item["answer"]
        ]

    def get_last_answer(self):
        answers = self.get_answers()

        if answers:
            return answers[-1]

        return None

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []