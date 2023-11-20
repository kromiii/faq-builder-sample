import time
import json

from openai import OpenAI

client = OpenAI()
assistant_id = "asst_4kiIu1akNbn1fnWFzL3slVxa"

def extract_faq_with_openai(pdf_file):
    file = client.files.create(
        file=pdf_file,
        purpose='assistants'
    )
    assistant = client.beta.assistants.retrieve(assistant_id)
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="このマニュアルからFAQを生成してください。",
        file_ids=[file.id]
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    while run.status != "requires_action":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print("run.status:", run.status)
        time.sleep(5)

    result = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
    result = json.loads(result)

    return result["faq_items"]
