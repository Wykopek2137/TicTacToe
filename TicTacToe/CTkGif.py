from PIL import Image
import customtkinter as ctk


class CTkGif(ctk.CTkLabel):
    """ Wyświetlanie pliku GIF """

    def __init__(self, master: any, path, loop=True, acceleration=1, repeat=100, **kwargs):
        super().__init__(master, **kwargs)
        if acceleration <= 0:
            raise ValueError('Acceleration musi być większe niż zero')
        self.master = master  # główny
        self.repeat = repeat  # maksymalna liczba powtórzeń
        self.configure(text='')  # Usunięcie domyślnego tekstu
        self.path = path  # ścieżka do pliku GIF
        self.count = 0  # liczba wykonanych animacji
        self.loop = loop  # czy zapętlać w nieskończoność?
        self.acceleration = acceleration  # współczynnik przyspieszenia
        self.index = 0  # wyświetlana klatka
        self.is_playing = False  # stan odtwarzania
        self.gif = Image.open(path)  # otwarcie obrazu
        self.n_frame = self.gif.n_frames  # liczba klatek animacji
        self.frame_duration = self.gif.info['duration'] * 1/self.acceleration  # czas trwania jednej klatki
        self.force_stop = False

    def update(self):  # Aktualizuje wyświetlanie pliku GIF
        if self.index < self.n_frame:  # Jeśli nie doszliśmy do końca animacji
            if not self.force_stop:  # Jeśli nie jesteśmy zmuszeni do zatrzymania
                self.gif.seek(self.index)  # Następna klatka
                self.configure(image=ctk.CTkImage(self.gif, size=(50, 50)))  # Wyświetlenie
                self.index += 1  # Indeksacja
                self.after(int(self.frame_duration), self.update)  # Zaplanowanie następnej klatki
            else:
                self.force_stop = False  # Przechodzimy do stanu off
        else:  # Jeśli doszliśmy do końca
            self.index = 0  # Wróć do początku
            self.count += 1  # Inkrementuj licznik
            if self.is_playing and (self.count < self.repeat or self.loop):  # brak zatrzymania i ponowne rozpoczęcie
                self.after(int(self.frame_duration), self.update)  # Zaplanowanie następnej klatki
            else:
                self.is_playing = False  # Przechodzimy do stanu off

    def start(self):
        """ Rozpoczyna animację, jeśli zatrzymana """
        if not self.is_playing:
            self.count = 0
            self.is_playing = True
            self.after(int(self.frame_duration), self.update)

    def stop(self, forced=False):
        """ Natychmiast zatrzymuje animację, jeśli wymuszone, w przeciwnym razie czeka na zakończenie """
        if self.is_playing:
            self.is_playing = False
            self.force_stop = forced

    def toggle(self, forced=False):
        """ Zmienia status odtwarzania """
        if self.is_playing:
            self.stop(forced=forced)
        else:
            self.start()


