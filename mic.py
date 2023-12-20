import json
import queue
import os
import sys

from sklearn.feature_extraction.text import CountVectorizer  # pip install scikit-learn
from sklearn.linear_model import LogisticRegression
import sounddevice as sd  # pip install sounddevice
import vosk  # pip install vosk

import words
import commands  # <<----- так нужно, функции из модуля запускаются через exec(...)
import voices
import chat

q = queue.Queue()

model = vosk.Model('model_small')

try:
    device = sd.default.device = 1, 4
    samplerate = int(sd.query_devices(device, 'input')['default_samplerate'])
except:
    voices.speaker_silero('Включи микрофон!')
    sys.exit(1)


def callback(indata, frames, time, status):
    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    if len(data) < 7:
        return

    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        if not int(os.getenv("CHATGPT")):
            return
        voices.speaker_gtts(chat.start_dialogue(data))
        return

    data = data.split()
    filtered_data = [word for word in data if word not in words.TRIGGERS]
    data = ' '.join(filtered_data)

    user_command_vector = vectorizer.transform([data])

    predicted_probabilities = clf.predict_proba(user_command_vector)

    threshold = 0.12

    max_probability = max(predicted_probabilities[0])
    print(max_probability)
    if max_probability >= threshold:
        answer = clf.classes_[predicted_probabilities[0].argmax()]
    else:
        voices.speaker_silero("Команда не распознана")
        return

    func_name = answer.split()[0]

    voices.speaker_silero(answer.replace(func_name, ''))

    exec('commands.' + func_name + '()')


def recognize_wheel():
    print('Слушаем')

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    # постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device, dtype='int16',
                           channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True and int(os.getenv('MIC')):
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)

    print('Микрофон отключен')
