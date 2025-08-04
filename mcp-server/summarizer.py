from ollama import Client
import json

client = Client(host='http://localhost:11434')

def summarize_and_tag(text: str) -> dict:
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
    try:
        response = client.chat(model='llama2', messages=[
            {"role": "user", "content": prompt}
        ])
        content = response.get("message", {}).get("content", "").strip()
        # Debug print for inspection (optional)
        print("Ollama raw content:\n", content)
        # Try parsing JSON from the string
        return json.loads(content)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error parsing response: {e}")
        return {
            "summary": "",
            "tags": [],
            "error": "Invalid response format from model"
        }


