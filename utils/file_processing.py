import numpy as np
from models.groq_model import generate_summary
from utils.nlp_utils import generate_key_points
from PyPDF2 import PdfReader
import io

def process_file(file_data, file_name, selected_model):
    if file_name.endswith('.pdf'):
        reader = PdfReader(io.BytesIO(file_data))
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
    else:
        text = file_data.decode("utf-8")

    lines = text.split('\n')
    if len(lines) > 3:
        preview_text = '\n'.join(lines[:3]) + " ..."
    else:
        preview_text = '\n'.join(lines)

    summary_responses = []
    words = text.split(" ")
    chunks = np.array_split(words, 10)

    for chunk in chunks:
        sentences = ' '.join(list(chunk))
        prompt = f"Generate a concise summary of the following text:\n\n{sentences}\n\n"
        response_text = generate_summary(prompt, selected_model)
        summary_responses.append(response_text)

    full_summary = " ".join(summary_responses)

    last_sentence = full_summary.split('.')[-1].strip()
    if last_sentence and last_sentence[-1] != '.':
        full_summary = full_summary[:-(len(last_sentence))].strip()

    key_points = generate_key_points(full_summary)

    return preview_text, full_summary, key_points
