import io
import PyPDF2


class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}


def load_document(filename, content):
    documents = []
    if filename.endswith(".pdf"):
        f = io.BytesIO(content)
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            content_text = page.extract_text()
            if content_text:
                text += content_text + "\n"
        documents.append(Document(page_content=text, metadata={"source": filename}))
    else:
        text = content.decode("utf-8")
        documents.append(Document(page_content=text, metadata={"source": filename}))

    return documents