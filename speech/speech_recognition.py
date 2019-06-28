import speech_recognition as sr

WIT_AI_KEY='ZVNP7QNSQRZ76EF7WHBS4PD6B76DQP5U'
def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = .7
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print(audio)
        # command = r.recognize_sphinx(audio)
        command = r.recognize_wit(audio, key=WIT_AI_KEY).lower()
        print('You said: %s\n' % command)

    except sr.UnknownValueError:
        print('Sorry, I could not hear what you said, please try again')
        command = listen_for_command()
    return command