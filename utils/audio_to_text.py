import whisper


def transcribe_audio_to_text(audio_file_path):
    """
    Transcribe an audio file to text using OpenAI's Whisper model.

    Args:
        audio_file_path (str): The path to the audio file to be transcribed.

    Returns:
        str: The transcribed text from the audio file.
    """
    # Load the model. Options: tiny, base, small, medium, large
    model = whisper.load_model("base")

    # Transcribe an audio file
    result = model.transcribe("audio.mp3")
    print(result["text"])

    # You can also just get the transcription text directly
    # print(result["text"])
    transcription_text = result["text"]
    return transcription_text
