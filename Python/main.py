import tkinter as tk
from tkinter import messagebox
from audio_capture import AudioCapture
import keyboard
import json
import os

CONFIG_FILE = "config.json"
DEFAULT_PUSH_TO_TALK_KEY = "space"  # Tecla padrão

class PushToTalkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Push to Talk")
        self.root.geometry("600x400")
        self.root.minsize(600, 400)
        self.root.configure(bg='#34495e')

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)

        self.audio_capture = AudioCapture()
        self.sidebar_frame = tk.Frame(root, width=150, bg='#2c3e50')
        self.sidebar_frame.grid(row=0, column=0, sticky='ns')
        self.sidebar_frame.grid_propagate(False)

        self.about_button = self.create_button(self.sidebar_frame, "Sobre", self.show_about)
        self.config_button = self.create_button(self.sidebar_frame, "Configuração", self.show_config)
        self.plans_button = self.create_button(self.sidebar_frame, "Planos", self.show_plans)

        self.main_frame = tk.Frame(root, bg='#ecf0f1')
        self.main_frame.grid(row=0, column=1, sticky='nsew')

        self.title_label = tk.Label(self.main_frame, text="Bem-vindo ao Push to Talk", bg='#ecf0f1', font=('Arial', 16))
        self.title_label.pack(pady=20)

        self.instructions_label = tk.Label(self.main_frame, text="Altere o botão do Push to Talk:", bg='#ecf0f1', font=('Arial', 12))
        self.instructions_label.pack_forget()

        self.key_display_label = tk.Label(self.main_frame, text="Tecla Atual: Nenhuma", bg='#ecf0f1', font=('Arial', 12))
        self.key_display_label.pack_forget()

        self.change_key_button = self.create_button(self.main_frame, "Escolher Tecla", self.bind_key, '#007bff', hover_color='#0056b3', show=False)

        self.load_config()

        self.root.after(100, self.check_for_keypress)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_button(self, parent, text, command, bg_color='#34495e', hover_color='#2c3e50', show=True):
        button = tk.Button(parent, text=text, command=command, bg=bg_color, fg='white', borderwidth=0, padx=10, pady=5, relief='flat', font=('Arial', 10))
        if show:
            button.pack(pady=10, fill='x')
        button.config(width=20)
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=bg_color))
        return button

    def show_about(self):
        messagebox.showinfo("Sobre", "Aplicação Push to Talk - versão 1.0\nDesenvolvido por [Seu Nome]")

    def show_plans(self):
        messagebox.showinfo("Planos", "Aqui você pode adicionar seus planos futuros para a aplicação.")

    def show_config(self):
        self.change_key_button.pack(pady=20)
        self.title_label.config(text="Configuração de Tecla")
        self.instructions_label.pack(pady=10)
        self.key_display_label.pack(pady=10)

        if hasattr(self.audio_capture, 'push_to_talk_key'):
            self.key_display_label.config(text=f"Tecla Atual: {self.audio_capture.push_to_talk_key}")
        else:
            self.key_display_label.config(text="Tecla Atual: Nenhuma")

    def bind_key(self):
        self.change_key_button.config(text="Aguardando tecla...")
        self.root.bind("<Key>", self.set_push_to_talk_key)

    def set_push_to_talk_key(self, event):
        try:
            self.audio_capture.set_push_to_talk_key(event.keysym)
            self.key_display_label.config(text=f"Tecla Atual: {event.keysym}")
            messagebox.showinfo("Configuração", f"Tecla 'push to talk' configurada para: {event.keysym}")
            self.change_key_button.config(text="Escolher Tecla")
            self.root.unbind("<Key>")
        except ValueError as e:
            messagebox.showerror("Erro", f"Tecla inválida: {event.keysym}. Por favor, escolha outra tecla.")
            self.audio_capture.set_push_to_talk_key(DEFAULT_PUSH_TO_TALK_KEY)  # Redefine a tecla para a padrão
            self.key_display_label.config(text=f"Tecla Atual: {DEFAULT_PUSH_TO_TALK_KEY}")
            messagebox.showinfo("Configuração", f"Tecla 'push to talk' configurada para a tecla padrão: {DEFAULT_PUSH_TO_TALK_KEY}")
            self.change_key_button.config(text="Escolher Tecla")
            self.root.unbind("<Key>")

    def check_for_keypress(self):
        try:
            if hasattr(self.audio_capture, 'push_to_talk_key'):
                if keyboard.is_pressed(self.audio_capture.push_to_talk_key):
                    self.audio_capture.listen_microphone()
        except ValueError:
            # Se a tecla configurada for inválida, altera para a tecla padrão
            self.audio_capture.set_push_to_talk_key(DEFAULT_PUSH_TO_TALK_KEY)
            self.key_display_label.config(text=f"Tecla Atual: {DEFAULT_PUSH_TO_TALK_KEY}")
            messagebox.showinfo("Atenção", f"A tecla configurada não é válida. Alterada para: {DEFAULT_PUSH_TO_TALK_KEY}")
        self.root.after(100, self.check_for_keypress)

    def save_config(self):
        config = {
            "push_to_talk_key": self.audio_capture.push_to_talk_key
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                push_to_talk_key = config.get("push_to_talk_key", None)
                if push_to_talk_key:
                    try:
                        self.audio_capture.set_push_to_talk_key(push_to_talk_key)
                    except ValueError:
                        # Se a tecla carregada for inválida, configura para a tecla padrão
                        self.audio_capture.set_push_to_talk_key(DEFAULT_PUSH_TO_TALK_KEY)

    def on_closing(self):
        self.save_config()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PushToTalkApp(root)
    root.mainloop()
