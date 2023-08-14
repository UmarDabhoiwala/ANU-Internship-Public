from audio_to_chat import run_chat
from choicer import get_choicer


def main(): 
    
    try:
        duration_of_recording, number_of_responses, choice = get_choicer()
        transcript = run_chat(duration_of_recording, number_of_responses, choice)
    except Exception as e:
        print("Something went wrong")
        print(e)
        
    with open("transcript.txt", "w") as f:
        f.write(transcript)

if __name__ == "__main__":
    main()