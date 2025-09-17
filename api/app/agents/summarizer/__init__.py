from .graph import summarizer_app

def get_summary(transcript: str) -> str:
    if not transcript:
        return "Error: Transcript cannot be empty."

    inputs = {"transcript": transcript}

    result = summarizer_app.invoke(inputs)

    return result.get("summary", "Error: Could not generate summary.")