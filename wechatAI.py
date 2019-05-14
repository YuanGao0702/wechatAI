import json
import modules
from importlib import reload
import itchat
import selenium as se
from selenium.webdriver.common.by import By
import speech_recognition as sr 
import os
import argparse
import pyaudio
import wave
from pydub import AudioSegment

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
	id = msg.fromUserName
	print(msg.text)
	reload(modules)
	#fetch from server
	if('天气'in msg.text or 'weather' in msg.text):
		modules.weather(msg.text,id)
	#fetch from cache
	with open('config.json', 'rb') as f:
		config = json.load(f)
	for message in config['mapping']:
		if message in msg.text:
			message = config['mapping'][message]
			if(isinstance(message, (list,))):
				for cache in message:
					cache = config['cache'][cache]
					if(isinstance(cache, (list,))):
						for e in cache:
							modules.send_msg(e,id)
					else:
						modules.send_msg(cache,id)
			else:
				cache = config['cache'][message]
				if(isinstance(cache, (list,))):
					for e in cache:
						modules.send_msg(e,id)
				else:
						modules.send_msg(cache,id)
	f.close()
	
@itchat.msg_register(itchat.content.RECORDING)
def print_content(msg): 
	reload(modules)
	print(msg['Text'](msg['FileName']))
	modules.convert()
	str = modules.voiceRec()
	itchat.send(str,msg.fromUserName)
	#fetch from server
	if('天气'in str or 'weather' in str):
		modules.weather(str,msg.fromUserName)
	
itchat.auto_login()
itchat.run()
