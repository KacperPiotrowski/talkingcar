import pygame
import RPi.GPIO as GPIO
import logging
import serial
import time
from datetime import datetime
import json

# Konfiguracja logowania
logging.basicConfig(filename='ford_focus_audio.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ConfigLoader:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Wczytuje ustawienia z pliku konfiguracyjnego JSON."""
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error("Plik konfiguracyjny nie został znaleziony.")
            raise
        except json.JSONDecodeError:
            logging.error("Błąd wczytywania pliku konfiguracyjnego. Upewnij się, że jest poprawny.")
            raise

    def get_ignition_pin(self):
        """Zwraca numer pinu zapłonu."""
        return self.config['ignition_pin']

    def get_serial_port(self):
        """Zwraca port szeregowy dla DFPlayer Mini."""
        return self.config['serial_port']

class DFPlayer:
    def __init__(self, serial_port):
        self.serial = serial.Serial(serial_port, 9600, timeout=1)
        self.wait_for_dfplayer_ready()  # Czekaj na gotowość DFPlayer Mini
        logging.info("DFPlayer Mini zainicjowany.")

    def wait_for_dfplayer_ready(self):
        """Czeka na gotowość DFPlayer Mini."""
        while True:
            # Wysyłamy komendę do sprawdzenia statusu
            self.serial.write(bytearray([0x7E, 0xFF, 0x06, 0x00, 0x00, 0x01, 0x7E]))
            response = self.serial.read(10)  # Odczytujemy odpowiedź
            if response:  # Jeśli otrzymaliśmy odpowiedź
                break
            time.sleep(0.1)  # Czekaj krótko przed kolejną próbą

    def play(self, track_number):
        """Odtwarzanie utworu z numerem track_number."""
        # Komenda do odtwarzania utworu
        command = bytearray([0x7E, 0xFF, 0x06, track_number, 0x00, 0x01, 0x7E])
        self.serial.write(command)
        logging.info(f"Odtwarzanie utworu: {track_number}")
        
        # Oczekiwanie na potwierdzenie odtwarzania
        response = self.serial.read(10)  # Odczytujemy odpowiedź
        if response:
            logging.info(f"Otrzymano odpowiedź: {response.hex()}")
        else:
            logging.error("Brak odpowiedzi od DFPlayer Mini po próbie odtwarzania.")

class FordFocusAudio:
    def __init__(self, config_loader):
        self.config_loader = config_loader
        self.ignition_pin = self.config_loader.get_ignition_pin()
        self.serial_port = self.config_loader.get_serial_port()

        # Sprawdzanie poprawności portu szeregowego
        try:
            self.dfplayer = DFPlayer(self.serial_port)
        except serial.SerialException:
            logging.error("Nie można otworzyć portu szeregowego. Sprawdź, czy jest poprawny.")
            raise
        
        self.has_played_today = False
        self.setup_gpio()
        self.running = True
        logging.info("Aplikacja uruchomiona.")

    def setup_gpio(self):
        """Konfiguracja pinów GPIO."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ignition_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.ignition_pin, GPIO.RISING, callback=self.on_ignition_on, bouncetime=300)
        logging.info(f"Pin zapłonu ustawiony na: {self.ignition_pin}")

    def play_message(self):
        """Odtwarzanie wiadomości audio."""
        self.dfplayer.play(1)  # Odtwarzanie utworu o numerze 1
        logging.info("Odtwarzanie wiadomości audio.")

    def on_ignition_on(self, channel):
        """Callback wywoływany przy zapłonie."""
        self.reset_daily_play()
        if not self.has_played_today:
            self.play_message()
            self.has_played_today = True
            logging.info("Zapłon włączony, wiadomość odtworzona.")

    def reset_daily_play(self):
        """Resetowanie flagi odtwarzania po północy."""
        current_time = datetime.now()
        if current_time.hour == 0 and current_time.minute == 0:
            self.has_played_today = False
            logging.info("Flaga odtwarzania zresetowana po północy.")

    def run(self):
        """Główna pętla programu."""
        try:
            while self.running:
                time.sleep(1)  # Utrzymanie programu w działaniu
        except KeyboardInterrupt:
            logging.info("Program zatrzymany przez użytkownika.")
            self.running = False  # Ustawienie na False przy przerwaniu
        except Exception as e:
            logging.error(f"Wystąpił błąd: {e}")
            self.running = False  # Ustawienie na False w przypadku błędu
        finally:
            GPIO.cleanup()
            self.dfplayer.serial.close()  # Zamknięcie portu szeregowego
            logging.info("GPIO oczyszczone, port szeregowy zamknięty, aplikacja zakończona.")

if __name__ == "__main__":
    config_file = "config.json"  # Ścieżka do pliku konfiguracyjnego
    config_loader = ConfigLoader(config_file)
    ford_focus = FordFocusAudio(config_loader)
    ford_focus.run()
