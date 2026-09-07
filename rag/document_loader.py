from pathlib import Path
from pypdf import PdfReader


class DocumentLoader:

    def load_pdf(self, file_path):
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        reader = PdfReader(str(path))

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)

    def load_text(self, file_path):
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        return path.read_text(
            encoding="utf-8"
        )

    def load(self, file_path):
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self.load_pdf(file_path)

        if extension == ".txt":
            return self.load_text(file_path)

        raise ValueError(
            "Only PDF and TXT files are supported."
        )