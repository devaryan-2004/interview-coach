from agents.evaluator import EvaluatorAgent


class EvaluationChain:

    def __init__(self):
        self.evaluator = EvaluatorAgent()

    def evaluate_answer(
        self,
        question,
        answer,
        role
    ):
        return self.evaluator.evaluate(
            question=question,
            answer=answer,
            role=role
        )