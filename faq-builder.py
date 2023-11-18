import streamlit as st
import streamlit.components.v1 as components

from extract_faq import extract_faq_with_openai
from generate_html import generate_html

def main():
    st.title('PDF to FAQ Generator')
    
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    if uploaded_file is not None:
        faq_items = extract_faq_with_openai(uploaded_file)
        html_content = generate_html(faq_items=faq_items)

        components.html(html_content, height=800)

if __name__ == '__main__':
    main()
