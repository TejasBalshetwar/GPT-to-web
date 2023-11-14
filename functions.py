import json
import os
import re


def remove_citations(text):
    # Updated regex pattern to match citations like &#8203;``【oaicite:1】``&#8203;
    return re.sub(r"&#8203;``【oaicite:0】``&#8203;", "", text)


def create_assistant(client):
    assistant_file_path = "assistant.json"

    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, "r") as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data["assistant_id"]
            print("Loaded existing assistant ID.")
    else:
        file = client.files.create(file=open("docs.pdf", "rb"), purpose="assistants")

        assistant = client.beta.assistants.create(
            instructions="""
          The assistant,HexaBot HR Assistant, has been programmed to help employees with their day to day queries regarding the              company policies and procedures.
          A document has been provided which is the employee handbook.
          """,
            model="gpt-3.5-turbo-1106",
            tools=[{"type": "retrieval"}],
            file_ids=[file.id],
        )

        with open(assistant_file_path, "w") as file:
            json.dump({"assistant_id": assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

    return assistant_id
