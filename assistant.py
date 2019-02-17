import pyttsx3
import webbrowser
import smtplib
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys
import pyaudio
import wave
import pyglet
import playsound
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from pygame import mixer
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


app = Flask(__name__)
api = Api(app)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
EMAIL_OUTPUT_FILENAME = "email.wav"
FRAMES = []
EMAIL_FRAMES = []
P = pyaudio.PyAudio()
music_folder = 'D:\CodeCombat\mp3Songs'
music = ['\R','\W','\A']
MUSIC = False
EMAIL = False
sender_email = "bsss.3332@gmail.com"
receiver_email = "shubham.sharma@people10.com"
message = MIMEMultipart("alternative")
message["Subject"] = "Message from VoicePI"
message["From"] = sender_email
message["To"] = receiver_email
mixer.init()

CORS(app)

@app.route("/")
def hello():
    speak('Hello Sir, I am your digital assistant')
    greetMe()
    speak('How may I help you?')

    while True:
        global MUSIC
        global EMAIL
        
        query = myCommand()
        query = query.lower()
        
        if 'open youtube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')

        elif 'open google' in query:
            speak('okay')
            webbrowser.open('www.google.co.in')

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))

        elif 'email' in query:
            speak('Who is the recipient? ')
            recipient = myCommand()

            if 'Shubham' in recipient:
                try:
                    speak("What is the body part ?")
                    message["Body"]=myCommand()
                    wf = wave.open(EMAIL_OUTPUT_FILENAME, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(P.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(EMAIL_FRAMES))
                    wf.close()
                    # print(dir(audio))
                    # EMAIL_FRAMES.append(audio.frame_data)
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login(sender_email, 'vinayak2015')
                    server.sendmail(sender_email, receiver_email,message["Body"] )
                    server.close()
                    speak('Email sent!')
                    EMAIL = False

                except:
                    speak('Sorry Sir! I am unable to send your message at this moment!')
                    EMAIL = False

        
        elif 'stop music' in query or (MUSIC == True and 'music' in query): 
               mixer.music.stop()
               MUSIC = False
        
        elif 'nothing' in query or 'abort' in query in query:
            speak('okay')
            speak('Bye Sir, have a good day.')
            print("* done recording")
            stream.stop_stream()
            stream.close()
            P.terminate()
            sys.exit()
            
        elif 'hello' in query:
            speak('Hello Sir')

        elif 'bye' in query:
            speak('Bye Sir, have a good day.')
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(P.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(FRAMES))
            wf.close()
            sys.exit()
                                    
        elif 'play music' in query:
            random_music = music_folder  + random.choice(music) + '.mp3'
            speak('Okay, here is your music! Enjoy!') 
            mixer.music.load(random_music)
            mixer.music.play()
            MUSIC = True
         
        else:
            query = query
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak(results)
                    
                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it.')
                    speak(results)
        
            except:
                webbrowser.open('www.google.com')
        
        speak('Next Command! Sir!')

    return jsonify({'text':'Hello World!'})

engine = pyttsx3.init('sapi5')

client = wolframalpha.Client('THE87U-AXRX25RYLE')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-1].id)


def speak(audio):
    print('Computer: ' + audio)
    engine = pyttsx3.init();
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 16:
        speak('Good Afternoon!')

    if currentH >= 16 and currentH !=0:
        speak('Good Evening!')

def myCommand():
    global EMAIL
    r = sr.Recognizer()   
    # print(dir(sr.Microphone.__dict__))                                                                                
    with sr.Microphone(sample_rate = 16000) as source:                                                                       
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
        print(dir(audio.sample_rate))
        FRAMES.append(audio.frame_data)
        print(EMAIL)
        if EMAIL == True:
            EMAIL_FRAMES.append(audio.frame_data)

    try:
        query = r.recognize_google(audio, language='en-in')
        if "email" in query:
            EMAIL_FRAMES.append(audio.frame_data)
            EMAIL = True
        print('User: ' + query + '\n')

    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))

    return query

     

if __name__ == '__main__':
     app.run(port=5002)
        

