import speech_recognition as sr
import keyboard
import pyautogui
import pyperclip

class AudioCapture:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.push_to_talk_key = "space"
        self.transcribed_text = ""

    def set_push_to_talk_key(self, key):
        self.push_to_talk_key = key

    def listen_microphone(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Fale algo: ")
                audio_chunks = []

                while keyboard.is_pressed(self.push_to_talk_key):
                    try:
                        audio = self.recognizer.listen(source, timeout=0.5)
                        audio_chunks.append(audio)
                    except sr.WaitTimeoutError:
                        continue

                if audio_chunks:
                    combined_audio = sr.AudioData(
                        b''.join([chunk.get_raw_data() for chunk in audio_chunks]),
                        sample_rate=audio_chunks[0].sample_rate,
                        sample_width=audio_chunks[0].sample_width
                    )
                    self.process_audio(combined_audio)
        except OSError as e:
            print(f"Erro no acesso ao microfone: {e}")
            return

    def process_audio(self, audio):
        try:
            self.transcribed_text = self.recognizer.recognize_google(audio, language="pt-BR")
            print("Você falou: " + self.transcribed_text)
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio.")
        except sr.RequestError as e:
            print(f"Erro na requisição ao serviço de reconhecimento: {e}")

    def get_transcribed_text(self):
        return self.transcribed_text
