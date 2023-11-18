import streamlit as st
import streamlit.components.v1 as components

from generate_html import generate_html

def main():
    st.title('PDF to FAQ Generator')
    
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    if uploaded_file is not None:
        # faq = generate_faq_with_openai(uploaded_file)
        # st.write(faq)

        faq_items = {
            "質問1": "回答1",
            "質問2": "回答2",
            "質問3": "回答3",
            # 他の質問と回答
        }
        html_content = generate_html(faq_items=faq_items)

        components.html(html_content, height=800)

if __name__ == '__main__':
    main()
