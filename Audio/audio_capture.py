import speech_recognition as sr
import keyboard
import pyautogui
import pyperclip

class AudioCapture:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.push_to_talk_key = "space"

    def set_push_to_talk_key(self, key):
        self.push_to_talk_key = key

    def listen_microphone(self):
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

    def process_audio(self, audio):
        try:
            captured = self.recognizer.recognize_google(audio, language="pt-BR")
            print("Você falou: " + captured)
            pyperclip.copy(captured)
            pyautogui.hotkey("ctrl", "v")

        except sr.UnknownValueError:
            print("Não foi possível entender o áudio.")
        except sr.RequestError as e:
            print(f"Erro na requisição ao serviço de reconhecimento: {e}")
