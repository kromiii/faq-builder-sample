import streamlit as st
import os
import time
from openai import OpenAI

client = OpenAI()

def generate_faq_with_openai(pdf_file):
    file = client.files.create(
        file=pdf_file,
        purpose='assistants'
    )
    assistant = client.beta.assistants.create(
        name="FAQ Builder",
        instructions="PDFのマニュアルを受け取って FAQ サイトを生成してください。FAQは日本語で生成してください。",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file.id]
    )
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="このマニュアルからFAQを生成してください。",
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    completed = False
    while not completed:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print("run.status:", run.status)
        if run.status == 'completed':
            completed = True
        else:
            time.sleep(5)
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    messages_value_list = []
    for message in messages:
        message_content = message.content[0].text

        annotations = message_content.annotations

        citations = []

        # アノテーションを反復処理し、脚注を追加
        for index, annotation in enumerate(annotations):
            # テキストを脚注で置き換える
            message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

            # アノテーションの種類毎に引用を収集
            if (file_citation := getattr(annotation, 'file_citation', None)):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
            elif (file_path := getattr(annotation, 'file_path', None)):
                cited_file = client.files.retrieve(file_path.file_id)
                citations.append(f'[{index}] Click <here> to download {cited_file.filename}')

        # ユーザーに表示する前に、メッセージの末尾に脚注を追加
        message_content.value += '\n' + '\n'.join(citations)
        messages_value_list.append(message_content.value)
    return '\n\n'.join(messages_value_list)

def main():
    st.title('PDF to FAQ Generator')

    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    if uploaded_file is not None:
        faq = generate_faq_with_openai(uploaded_file)
        st.write(faq)

if __name__ == '__main__':
    main()
