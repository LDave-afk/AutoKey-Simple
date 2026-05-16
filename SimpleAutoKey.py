'''Criar Janela'''
import customtkinter as ctk
import threading
import pyautogui
import keyboard
import time
import mouse

ctk.set_appearance_mode("dark")

class AutoKeyApp(ctk.CTk):
    #layout
    def __init__(self):
        super().__init__()
        self.title("Simple AutoKey") #nome da janela
        self.geometry("420x300") #tamanho da janela
        #self.iconbitmap("icone.ico") #icone na janela
        

        # Variáveis
        self.running = False
        self.key = ctk.StringVar(value="a")
        self.speed = ctk.DoubleVar(value=0.1)
        self.hold_mode = ctk.BooleanVar(value=False)
        self.selecting_key = False  # controle de estado

        #Linha da tecla
        key_frame = ctk.CTkFrame(self)
        key_frame.pack(pady=(10, 0))

        ctk.CTkLabel(key_frame, text="Auto Key:").pack(side="left", padx=(5, 5))
        self.key_entry = ctk.CTkEntry(key_frame, textvariable=self.key, width=80)
        self.key_entry.pack(side="left", padx=(5, 5))

        self.key_button = ctk.CTkButton(key_frame, text="Select", width=100, command=self.capture_key)
        self.key_button.pack(side="left", padx=(5, 5))

        #Velocidade do auto clique
        ctk.CTkLabel(self, text="Speed (seconds):").pack(pady=(10, 0))
        self.speed_entry = ctk.CTkEntry(self, width=80)
        self.speed_entry.pack()

        self.slider = ctk.CTkSlider(
         self,
         from_=0.005,
        to=1.0,
         variable=self.speed,
         command=self.update_speed,
         number_of_steps=995
        )
        self.slider.pack(padx=20, pady=5)

        # valor inicial
        self.update_speed(self.speed.get())

        #Modo segurar
        ctk.CTkCheckBox(self, text="Hold Key",
                        variable=self.hold_mode).pack(pady=10)

        #Botão principal
        self.start_button = ctk.CTkButton(self, text="Start (F8)", command=self.toggle)
        self.start_button.pack(pady=20)

        #Atalho global para iniciar
        keyboard.add_hotkey("f8", self.toggle)
    #fim do layout

    #capturar tecla
    def capture_key(self):
        if self.selecting_key:
            return  # evita múltiplas capturas simultâneas

        self.selecting_key = True
        self.key_button.configure(text="Set key...")
    
    def update_speed(self, value):
        self.speed_entry.delete(0, "end")
        self.speed_entry.insert(0, f"{float(value):.3f}")
    
        #aguardar o usuario selecionar a tecla
        def get_key():
            tecla = keyboard.read_event(suppress=True)  # Espera o evento de teclado
            if tecla.event_type == keyboard.KEY_DOWN:
                key_name = tecla.name
                self.key.set(key_name)
                self.key_button.configure(text=f"Select ({key_name})")
                self.selecting_key = False

        threading.Thread(target=get_key, daemon=True).start()
    #fim da capturar tecla
    #manter o botao pressionado
    def toggle(self):
        self.running = not self.running
        self.start_button.configure(text="Stor (F8)" if self.running else "Start (F8)")

        if self.running:
            threading.Thread(target=self.autopress, daemon=True).start()

    def autopress(self):
        tecla = self.key.get()
        intervalo = self.speed.get()
        segurar = self.hold_mode.get()

        while self.running:
            if segurar:
                pyautogui.keyDown(tecla)
                time.sleep(intervalo)
                pyautogui.keyUp(tecla)
            else:
                pyautogui.press(tecla)
                time.sleep(intervalo)

#manter a janela aberta
if __name__ == "__main__":
    app = AutoKeyApp()
    app.mainloop()
