
# Dita Texto - Aplicação Push-to-Talk com Reconhecimento de Fala e Automação

## Descrição

O **Dita Texto** é uma aplicação em Python que implementa uma funcionalidade de "Push-to-Talk" para capturar áudio, transcrever a fala e melhorar o texto utilizando uma API externa. Com uma interface gráfica simples, o usuário pode configurar uma tecla para ativar a captura de áudio, automatizar o processo de transcrição e colar o texto melhorado em qualquer campo de texto.

![1](https://github.com/user-attachments/assets/89ddfccc-ae98-4290-9627-45356dc0aa7e)
![2](https://github.com/user-attachments/assets/d0297917-517d-4d38-bee7-cfa8d63a246e)


## Funcionalidades

- **Reconhecimento de Fala**: Captura e transcrição de áudio em texto usando a biblioteca `speech_recognition`.
- **Configuração de Push-to-Talk**: Permite ao usuário definir uma tecla de "Push-to-Talk" para capturar o áudio enquanto ela é pressionada.
- **Integração com API Externa**: Chama uma API para melhorar a qualidade do texto transcrito, utilizando a biblioteca `requests`.
- **Automação de Colagem de Texto**: Utiliza `pyperclip` e `pyautogui` para copiar o texto melhorado e colá-lo automaticamente no local desejado.
- **Interface Gráfica com Tkinter**: Interface intuitiva para configurar o botão de "Push-to-Talk" e visualizar informações.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python:
  - `tkinter`
  - `json`
  - `os`
  - `keyboard`
  - `requests`
  - `speech_recognition`
  - `pyautogui`
  - `pyperclip`
  - `pyaudio` (dependência para `speech_recognition`)

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/dita-texto.git
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o arquivo principal:
   ```bash
   python main.py
   ```

## Uso

1. Ao iniciar a aplicação, você verá uma interface gráfica.
2. Configure a tecla de "Push-to-Talk" clicando em "Configuração" e escolhendo a tecla desejada.
3. Pressione a tecla configurada para capturar áudio e, em seguida, transcrever e melhorar o texto.
4. O texto melhorado será automaticamente copiado e colado no local onde o cursor estiver ativo.

## Estrutura do Projeto

- `main.py`: Arquivo principal que inicializa a interface gráfica e a lógica do "Push-to-Talk".
- `audio_capture.py`: Módulo que contém a lógica de captura e processamento de áudio.
- `config.json`: Arquivo de configuração que armazena a tecla de "Push-to-Talk" definida pelo usuário.

