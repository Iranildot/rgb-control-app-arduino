import wave
import struct
import speech_recognition as sr
from serial_connection import *


class Microphone:
    def __init__(self, root, arduino, duration=5, language="en-US", output_file="output.wav", sample_rate=8000) -> None:
        self.root = root
        self.arduino = arduino
        self.duration = duration
        self.language = language
        self.output_file = output_file
        self.sample_rate = sample_rate
        self.frames = []
        pass
    
    def listen(self):
        self.arduino.write(f"LISTEN:{32000}".encode())
        try:
            while len(self.frames) < int(self.duration * self.sample_rate):
                if self.arduino.in_waiting >= 2:
                    # Lê dois bytes e converte para um inteiro de 16 bits
                    data = self.arduino.read(2)
                    sample = struct.unpack('<H', data)[0]
                    
                    self.frames.append(sample)
                    self.root.update()
        except:
            self.arduino.close()
        
        with wave.open(self.output_file, 'w') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16 bits
            wf.setframerate(self.sample_rate)  # Taxa de amostragem
            wf.writeframes(b''.join([struct.pack('<H', frame) for frame in self.frames]))
            
        self.arduino.write("NOT LISTEN:".encode())
            
        return self.output_file
    
    def audio_to_text(self, audio_file):
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            
            try:
                return recognizer.recognize_google(audio_data, language="pt-BR")
            except:
                ...