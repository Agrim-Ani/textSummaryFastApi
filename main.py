import streamlit as st
import numpy as np
from models.groq_model import generate_summary
from utils.nlp_utils import generate_key_points
from PyPDF2 import PdfReader
import io

# List of available models
available_models = [
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it"
]

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

def main():
    st.set_page_config(layout="wide")
    st.title('Earning Calls & Investor Reports Analysis')
    st.text('Analyze Calls, Q&A sessions and much more with GROQ - Fastest AI Infererence Infrastructure')

    # Add a dropdown for model selection in the sidebar
    st.sidebar.title("Configurations")
    selected_model = st.sidebar.selectbox('Select a Large Language Model:', available_models)

    upload_file = st.file_uploader('Upload your transcript file (PDF or TXT)', type=['pdf', 'txt'])

    if upload_file is not None:
        file_data = upload_file.read()
        file_name = upload_file.name

        if st.button('Analyze'):
            preview_text, full_summary, key_points = process_file(file_data, file_name, selected_model)

            st.text('File Preview:')
            st.text(preview_text)

            st.subheader('Full Summary:')
            full_summary_without_header = full_summary.replace("Here is a concise summary of the text:", "")
            st.markdown(f"<pre style='white-space: pre-wrap;'>{full_summary_without_header}</pre>", unsafe_allow_html=True)

            st.subheader('Key Points:')
            for idx, point in enumerate(key_points, start=1):
                st.markdown(f"{idx}. {point}", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
