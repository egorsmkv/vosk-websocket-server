from os.path import dirname

from vosk import Model, KaldiRecognizer

CHUNK = 1024 * 4
MODEL_PATH = dirname(__file__) + '/model'
RATE = 8000


def get_ukr_model(sr=None):
    if sr is None:
        sr = RATE

    return KaldiRecognizer(Model(MODEL_PATH), sr)
