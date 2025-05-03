import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3

# === CONFIG ===
openai.api_key = "your-openai-api-key"  # Replace with your actual OpenAI key

# === Initialize Text-to-Speech Engine ===
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def speak_text(text):
    """Convert text to speech using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

def get_solution(prompt):
    """Use OpenAI GPT to generate a technical resolution."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or "gpt-3.5-turbo" if you're using that
            messages=[
                {"role": "system", "content": "You are a helpful technical support assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error from OpenAI API: {str(e)}"

def transcribe_speech():
    """Capture and convert speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak clearly.")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            st.error("Timeout: No speech detected.")
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Speech recognition error: {e}")
        return ""

    # === Streamlit UI ===
    st.set_page_config(page_title="AI Tech Support", layout="centered")
    st.title("🎧 AI Voice Assistant for Tech Support")

    input_method = st.radio("Choose how to submit your issue:", ["🎤 Speak", "⌨️ Type"])

    user_input = ""

    if input_method == "🎤 Speak":
        if st.button("🎙️ Start Speaking"):
            user_input = transcribe_speech()
    else:
        user_input = st.text_area("Type your technical issue here")

    if user_input:
        with st.spinner("Analyzing issue..."):
            response = get_solution(user_input)
        st.markdown("### 💡 Suggested Solution:")
        st.write(response)

        if st.button("🔊 Read it aloud"):
            speak_text(response)
