from audioToChat import audio_to_chat
import ast
from pydub import AudioSegment
import os

def run_chat(messages, choice):
    
    if messages == []:
        init_prompt = """You are to act as a helpful assistant. 
        The assistant is helpful, creative, clever, and very friendly. 
        Reply in a conversational manner and very concisely, 
        attempt to mimic a real person and act as a friend"""
        
        messages = [{"role": "system", "content": init_prompt}]
        
    text = audio_to_chat.transcribe("audio_uploads/input.webm")
    
    messages, text = audio_to_chat.get_assistant_response(messages, text)
    
    audio_to_chat.gen_ai_sound(text, choice, "/home/umar.dabhoiwala/Documents/webapp/static/audio/output.wav")
    
    return messages


def get_transcript(messages):
    
    transcript = audio_to_chat.chat_transcript(messages)
    
    return transcript

def webmToWav ():
     # Set the path of the input file
    input_file = "audio_uploads/input.webm"

    # Set the path of the output file
    output_file = "audio_uploads/input.wav"
    
    audio = AudioSegment.from_file(input_file, format="webm")
    
    if os.path.exists('audio_uploads/input.wav'):
        os.remove('audio_uploads/input.wav')
        print("File deleted successfully")
    else:
        print("File not found")
        
    audio.export(output_file, format="wav")

