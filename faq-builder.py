import streamlit as st
import streamlit.components.v1 as components

from extract_faq import extract_faq_with_openai
from generate_html import generate_html

def main():
    st.title('PDF to FAQ Generator')
    
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    if uploaded_file is not None:
        faq_items = extract_faq_with_openai(uploaded_file)
        # faq_items = [
        #     {
        #         "question": "How do I change my password?",
        #         "answer": "You can change your password by clicking on the Settings button in the top right corner of the screen."
        #     },
        #     {
        #         "question": "How do I change my email address?",
        #         "answer": "You can change your email address by clicking on the Settings button in the top right corner of the screen."
        #     },
        #     {
        #         "question": "How do I change my profile picture?",
        #         "answer": "You can change your profile picture by clicking on the Settings button in the top right corner of the screen."
        #     },
        # ]
        html_content = generate_html(faq_items=faq_items)

        components.html(html_content, height=800)

if __name__ == '__main__':
    main()
