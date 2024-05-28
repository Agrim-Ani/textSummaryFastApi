# main.py

import streamlit as st
from utils.file_processing import process_file
from utils.word_count import count_words

def main():
    st.set_page_config(layout="wide")
    st.title('Earning Calls & Investor Reports Analysis')
    st.text('Analyze Calls, Q&A sessions and much more with GROQ - Fastest AI Infererence Infrastructure')

    # List of available models
    available_models = [
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it"
    ]

    # Add a dropdown for model selection in the sidebar
    st.sidebar.title("Configurations")
    selected_model = st.sidebar.selectbox('Select a Large Language Model:', available_models)

    upload_file = st.file_uploader('Upload your transcript file (PDF or TXT)', type=['pdf', 'txt'])

    if upload_file is not None:
        file_data = upload_file.read()
        file_name = upload_file.name

        if st.button('Analyze'):
            with st.spinner('Generating, Please wait...'):
                preview_text, full_summary, key_points = process_file(file_data, file_name, selected_model)

            st.text('File Preview:')
            st.text(preview_text)

            st.subheader('Full Summary:')
            full_summary_without_header = full_summary.replace("Here is a concise summary of the text:", "")
            st.markdown(f"<pre style='white-space: pre-wrap;'>{full_summary_without_header}</pre>", unsafe_allow_html=True)

            st.subheader('Key Points:')
            for idx, point in enumerate(key_points, start=1):
                st.markdown(f"{idx}. {point}", unsafe_allow_html=True)

            original_word_count = count_words(file_data.decode("utf-8"))
            summary_word_count = count_words(full_summary)

            st.subheader('Comparative Analysis:')
            col1, col2 = st.columns(2)
            with col1:
                st.text(f"Original File: {original_word_count} words")
            with col2:
                st.text(f"Generated Summary: {summary_word_count} words")

if __name__ == "__main__":
    main()
