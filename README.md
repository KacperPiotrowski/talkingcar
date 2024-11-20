# Dokumentacja projektu Talking Car

## Opis

Projekt "Talking Car" to system oparty na Raspberry Pi, który umożliwia odtwarzanie spersonalizowanego dźwięku powitalnego.

## Wymagania

Aby uruchomić projekt, potrzebujesz następującego sprzętu i oprogramowania:

- **Sprzęt**:

  - Raspberry Pi Zero
  - Akumulator samochodowy
  - Przetwornica step-down LM2596
  - Przewody połączeniowe
  - Płytka stykowa (opcjonalnie)
  - DFPlayer Mini
  - Głośnik (zalecany: 3W 8 Ω)

- **Oprogramowanie**:
  - Raspbian OS
  - Python 3
  - Biblioteki: `pyserial`, `RPi.GPIO`, `pygame`
  
## Instalacja

### Krok 1: Przygotowanie Raspberry Pi

1. **Zainstaluj system operacyjny**:

   - Pobierz obraz Raspberry Pi OS z oficjalnej strony.
   - Użyj narzędzia takiego jak Balena Etcher, aby nagrać obraz na kartę SD.
   - Włóż kartę SD do Raspberry Pi i uruchom urządzenie.

2. **Zaktualizuj system**:
   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```

3. **Dodaj projekt do autostartu**:

    - Edytuj plik `/etc/rc.local`
    ```bash
   b python3 (ścieżka do projektu)/talkingcar.py
    ```
## Krok 2: Przygotowanie projektu

1. **Podłącz elementy**:
    
    - Podłącz bezpiecznik 3A pomiędzy dodatnim biegunem akumulatora a dodatnim wejściem przetwornicy.
    - Podłącz wyjście przetwornicy do Raspberry Pi.
    - podłącz zapłon do portu ustalonego w pliku konfiguracyjnym.
    - Podłączenie modułu dźwiękowego
      - Podłącz pin VCC DFPlayer Mini do pinu 5V na Raspberry Pi. 
      - Podłącz pin GND DFPlayer Mini do pinu GND na Raspberry Pi.
      - Podłącz głośnik do pinów SPK1 i SPK2 na DFPlayer Mini.
      - Podłącz pin TX DFPlayer Mini do jednego z pinów GPIO na Raspberry Pi (np. GPIO 15).
      - Podłącz pin RX DFPlayer Mini do innego pinu GPIO na Raspberry Pi (np. GPIO 14).
    - podłącz ujemne wejście do ujemnego bieguna akumulatora.

2. **Uruchomienie projektu**:

    - Projekt powinien się sam uruchomić

## Testowanie projektu

1. Uruchomienie zapłonu w samochodzie

## Linki
- [SimpleDFPlayerMini-for-RaspberryPi](https://github.com/andreaswatch/SimpleDFPlayerMini-for-RaspberryPi?tab=readme-ov-file)
- [DFPLayer Mini Doc](https://picaxe.com/docs/spe033.pdf)
- 

# FAQ
