import os
import pyaudio
import struct
import speech_recognition as sr
import threading
from groq import Groq
import pvporcupine
from transformers import pipeline
import soundfile as sf
from modules.logger import MAIN_LOGGER

from datasets import load_dataset
import torch

class Speech:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Speech, cls).__new__(cls)
            cls._instance._initialize(cls, *args, **kwargs)
        return cls._instance

    def _initialize(self, is_background_mic=False):
        # For text to speech
        self.synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
        MAIN_LOGGER.info("Text-to-Speech initialized successfully")


        # For speech to text
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
        MAIN_LOGGER.info("Speech-to-Text initialized successfully")

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
        
    def speak(self, text):
        speech = self.synthesiser(str(text), forward_params={"speaker_embeddings": self.speaker_embedding})

        # sf.write("audio/speech.wav", speech["audio"], samplerate=speech["sampling_rate"])
        audio_data = speech["audio"]
        sampling_rate = speech["sampling_rate"]

        # Initialize PyAudio
        p = pyaudio.PyAudio()

        # Open a stream with the correct parameters
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=sampling_rate,
                        output=True)

        # Play the audio by writing the data to the stream
        stream.write(audio_data.astype('float32').tobytes())

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        # Terminate the PyAudio object
        p.terminate()

MAIN_SPEECH = Speech()


if __name__ == "__main__":
    MAIN_SPEECH = Speech(is_background_mic=False)
    while True:
        pass