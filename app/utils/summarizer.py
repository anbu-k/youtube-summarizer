import openai

def summarize_text(text):
    openai.api_key = 'your-openai-api-key'
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following text in 3-5 bullet points:\n\n{text}"}
        ]
    )
    return response['choices'][0]['message']['content']