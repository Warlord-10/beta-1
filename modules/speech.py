import os
import pyaudio
import struct
import speech_recognition as sr
import threading
# from modules.logger import MAIN_LOGGER
# from modules.llm import MAIN_LLM
from groq import Groq
import pvporcupine

class Speech:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Speech, cls).__new__(cls)
            cls._instance._initialize(cls, *args, **kwargs)
        return cls._instance

    def _initialize(self, is_background_mic=False):
        self.client = Groq(api_key=os.environ.get("GROQ_API"))
        self.porcupine = pvporcupine.create(
            access_key=os.environ.get("PICOVOICE_API"), 
            keyword_paths=[
                "models/Aur-Bhai-kaisa-hai_en_windows_v3_0_0/Aur-Bhai-kaisa-hai_en_windows_v3_0_0.ppn", 
                "models/Hey-Beta-One_en_windows_v3_0_0/Hey-Beta-One_en_windows_v3_0_0.ppn"
            ],
            sensitivities=[0.8, 0.7]
        )

        self.audio_stream = pyaudio.PyAudio().open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

        self.microphone = sr.Microphone()

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.pause_threshold = 3
        self.recognizer.dynamic_energy_threshold = True


        self.listening_event = threading.Event()
        self.listening_event.set()  # Start with listening enabled
        self.listen_thread = threading.Thread(target=self._backgroundMic)
        if is_background_mic == True:
            self._startThreads()

    def _startThreads(self):
        print("Starting background mic")
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def _backgroundMic(self):
        while True:
            # This will block if the event is cleared
            self.listening_event.wait()

            pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            keyword_index = self.porcupine.process(pcm)

            if keyword_index >= 0:
                print("Wake word detected!")
                self.speechToText()  # Process the speech input
                

    def speechToText(self):
        self.listening_event.clear()  # Pause background listening


        print("Say Something: ")
        with self.microphone as source:
            audio = self.recognizer.listen(source, phrase_time_limit=3)
            print("Done")

        # with open(filename, "wb") as f:
            #f.write(audio.get_wav_data())
        
        transcription = self.client.audio.transcriptions.create(
            file=(".wav", audio.get_wav_data()),
            model="whisper-large-v3",
            # prompt="Specify context or spelling",  # Optional
            response_format="text",  # Optional
            language="en",  # Optional
            temperature=0.0  # Optional
        )
        print(transcription)


        self.listening_event.set()  # Resume background listening
        return transcription
        


MAIN_SPEECH = Speech()

if __name__ == "__main__":
    MAIN_SPEECH = Speech(is_background_mic=False)
    while True:
        pass