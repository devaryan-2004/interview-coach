import re


class SimpleRetriever:

    def __init__(self, text=""):
        self.text = text

    def set_text(self, text):
        self.text = text

    def retrieve(self, query, max_chunks=3):
        if not self.text:
            return []

        paragraphs = re.split(
            r"\n\s*\n",
            self.text
        )

        query_words = set(
            word.lower()
            for word in re.findall(
                r"\b\w+\b",
                query
            )
            if len(word) > 2
        )

        scored = []

        for paragraph in paragraphs:

            paragraph_words = set(
                word.lower()
                for word in re.findall(
                    r"\b\w+\b",
                    paragraph
                )
            )

            score = len(
                query_words.intersection(
                    paragraph_words
                )
            )

            if score > 0:
                scored.append(
                    (score, paragraph.strip())
                )

        scored.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            paragraph
            for _, paragraph in scored[:max_chunks]
        ]