import openai
import os

def summarize_text(text):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text in bullet points, make sure that you cover the important information so that it makes as much sense as possible to the reader, also make it so that the summary is an actual summary rather than saying phrases like the speaker, make it so that the summary fits the context of the actual video:\n\n{text}"}
        ]
    )

    return response.choices[0].message.content  
