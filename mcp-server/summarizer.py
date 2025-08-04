from ollama import Client
from fastapi.responses import StreamingResponse


client = Client(host='http://localhost:11434')

def summarize_and_tag_stream(text: str):
    prompt = f"""
    Summarize this and generate 3 tags as a JSON:
    \"\"\"
    {text}
    \"\"\"
    Example format:
    {{
      "summary": "...",
      "tags": ["tag1", "tag2", "tag3"]
    }}
    """
    def generate():
        try:
            stream = client.chat(
                model='llama2',
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            print("stream", stream)
            for chunk in stream:
                content = chunk.get("message", {}).get("content", "")
                if content:
                    yield content
        except Exception as e:
            yield f'\n[Error]: {str(e)}'
    return StreamingResponse(generate(), media_type="text/plain")
