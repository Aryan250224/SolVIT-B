import speech_recognition as sr
import pyttsx3
import requests
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()

# API endpoints
CHATBOT_API_URL = "https://your-chatbot-api.com/chat"  
DID_API_URL = "https://api.d-id.com/talks"

# Your Avatar Image URL (Upload to a free image hosting site)
AVATAR_IMAGE_URL = "https://www.google.com/imgres?q=genie&imgurl=https%3A%2F%2Fmedia.istockphoto.com%2Fid%2F501284440%2Fvector%2Fcartoon-genie-and-lamp.jpg%3Fs%3D612x612%26w%3D0%26k%3D20%26c%3DdqPwonMJlkzfOMe1qusv1hvynq4LM1g3IbK8zfRbQ7Q%3D&imgrefurl=https%3A%2F%2Fwww.istockphoto.com%2Fillustrations%2Faladdin-and-genie%3Fpage%3D2&docid=81kGDOh9Os4m5M&tbnid=uJOTIibCuXe1BM&vet=12ahUKEwjljPqi8Z6MAxXjzzgGHYtDEvsQM3oECGYQAA..i&w=321&h=612&hcb=2&ved=2ahUKEwjljPqi8Z6MAxXjzzgGHYtDEvsQM3oECGYQAA" 

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's voice and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        print("Could not connect to the voice recognition service.")
        return None

def chat_with_bot(user_input):
    """Send user input to chatbot API and get a response."""
    try:
        response = requests.post(CHATBOT_API_URL, json={"message": user_input})
        response_data = response.json()
        return response_data.get("reply", "I'm not sure how to respond.")
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't connect to the chatbot."

def get_avatar_response(text):
    """Generate a talking avatar video from chatbot response."""
    headers = {
        "Authorization": f"Bearer",
        "Content-Type": "application/json"
    }
    payload = {
        "source_url": AVATAR_IMAGE_URL,  # Use your custom avatar image
        "script": {"type": "text", "input": text}
    }

    try:
        response = requests.post(DID_API_URL, json=payload, headers=headers)
        result = response.json()
        
        if "id" in result:
            avatar_id = result["id"]
            time.sleep(5)  # Wait for processing
            return f"https://api.d-id.com/talks/{avatar_id}"
        else:
            return "Error generating avatar response."
    except Exception as e:
        print(f"Error: {e}")
        return "Failed to get avatar response."

def virtual_assistant():
    """Runs the virtual assistant in a loop."""
    speak("Hello! How can I help you?")
    
    while True:
        user_text = listen()
        
        if user_text is None:
            continue

        if "exit" in user_text or "stop" in user_text:
            speak("Goodbye!")
            break

        bot_response = chat_with_bot(user_text)
        print(f"Assistant: {bot_response}")
        
        avatar_url = get_avatar_response(bot_response)
        print(f"Avatar Video: {avatar_url}")

        speak(bot_response)  # Speak the response
        print("Watch the avatar speak here:", avatar_url)  # Display video link

# Run the assistant
virtual_assistant()
