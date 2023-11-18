import time
import json

from openai import OpenAI

client = OpenAI()

custom_function = {
    "name": "generate_faq",
    "description": "Generates a FAQ from a manual.",
    "parameters": {
        "type": "object",
        "properties": {
            "faq_items": {
                "type": "array",
                "description": "A list of FAQ items.",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The question."
                        },
                        "answer": {
                            "type": "string",
                            "description": "The answer."
                        }
                    },
                    "required": ["question", "answer"]
                }
            }
        },
        "required": ["faq_items"]
    }
}

def extract_faq_with_openai(pdf_file):
    file = client.files.create(
        file=pdf_file,
        purpose='assistants'
    )
    assistant = client.beta.assistants.create(
        name="FAQ Builder",
        instructions="PDFのマニュアルを受け取って FAQ サイトを生成してください。FAQは日本語で生成してください。",
        tools=[
            {"type": "retrieval"},
            {"type": "function", "function": custom_function}
        ],
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
    while run.status != "requires_action":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print("run.status:", run.status)
        time.sleep(5)
    
    result = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
    result = json.loads(result)

    return result["faq_items"]
