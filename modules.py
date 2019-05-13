import itchat
import selenium as se
from selenium.webdriver.common.by import By
import json
import time
from importlib import reload
import speech_recognition as sr 
import os
import argparse
import pyaudio
import wave
from pydub import AudioSegment

def voiceRec():
	r = sr.Recognizer() 
	harvard = sr.AudioFile('voice.wav')
	with harvard as source:
		audio = r.record(source)

	print( type(audio))
	#,language="zh-CN"
	print(r.recognize_google(audio))
	return r.recognize_google(audio,language="zh-CN")
	
formats_to_convert = ['.mp3']
def convert():
	for (dirpath, dirnames, filenames) in os.walk("./"):
		for filename in filenames:
			if filename.endswith(tuple(formats_to_convert)):

				filepath = dirpath + '/' + filename
				(path, file_extension) = os.path.splitext(filepath)
				file_extension_final = file_extension.replace('.', '')
				try:
					track = AudioSegment.from_file(filepath,
							file_extension_final)
					wav_filename = filename.replace(file_extension_final, 'wav')
					#wav_path = dirpath + '/' + wav_filename
					wav_path = dirpath + '/' + "voice.wav"
					print('CONVERTING: ' + str(filepath))
					file_handle = track.export(wav_path, format='wav')
					os.remove(filepath)
				except:
					print("ERROR CONVERTING " + str(filepath))
					
def send_msg(msg,id):
    print(msg)
    if 'image' in msg:
        itchat.send_image(msg,id)
    else:
        itchat.send(msg,id)

def traffic(id):
	options = se.webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = se.webdriver.Chrome(chrome_options=options)
	home = config['home']
	destination = config['destination']
	url = 'https://www.google.com/maps/dir/'+home+','+destination+'/@37.3806044,-122.0178939,12z/data=!3m1!4b1!4m14!4m13!1m5!1m1!1s0x808fcc3e5f95acc3:0x47daf6fd38218ca4!2m2!1d-121.8762513!2d37.3853429!1m5!1m1!1s0x808fb64142d26eaf:0x8192e11989e6e62f!2m2!1d-122.020508!2d37.380601!3e0'
	#urlTest = 'https://www.google.com/maps/dir/'+home+','+destination+'/@37.3806044,-122.0178939,12z/data=!3m1!4b1!4m18!4m17!1m5!1m1!1s0x808fcc3e5f95acc3:0x47daf6fd38218ca4!2m2!1d-121.8762513!2d37.3853429!1m5!1m1!1s0x808fb64142d26eaf:0x8192e11989e6e62f!2m2!1d-122.020508!2d37.380601!2m3!6e0!7e2!8j1545897900!3e0'
	driver.get(url)
	time = driver.find_element(By.XPATH,'//div[@class="section-directions-trip-numbers"]/div')
	distance = driver.find_element(By.XPATH,'//div[@class="section-directions-trip-numbers"]/div[@class="section-directions-trip-distance section-directions-trip-secondary-text"]')
	crowd = time.get_attribute("class").split("delay-")[1]
	strOutput = "Traffic: "+crowd +'\n'+"Time: "+time.text+'\n'+distance.text
	itchat.send(strOutput,toUserName=id)
	print("Traffic: "+crowd)
	print("Time: "+time.text)
	print(distance.text)
	if crowd == 'heavy':
		itchat.send("太堵啦，要不等会儿再出发",toUserName=id)

def weather(city,id):
	options = se.webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = se.webdriver.Chrome(chrome_options=options)
	url = 'https://www.google.com/search?hl=en&authuser=0&ei=M5YkXM_tOYzBjwTu47jABA&q='+city+'&oq=zhuozhou+weather&gs_l=psy-ab.3..35i39.1104929.1106580..1106843...0.0..0.97.684.9......0....1..gws-wiz.......0i71j0i7i30j0i7i5i10i30j0i13j0i13i30j0i8i13i30j35i304i39.kcZOPDwMDfs'
	driver.get(url)
	city = driver.find_element(By.XPATH,'//div[@class="vk_gy vk_h"][@id="wob_loc"]')
	time = driver.find_element(By.XPATH,'//div[@class="vk_gy vk_sh"][@id="wob_dts"]')
	weather = driver.find_element(By.XPATH,'//img[@style="margin:1px 4px 0;height:48px;width:48px"]')
	tempMax = driver.find_element(By.XPATH,'//div[@class="vk_gy"]/span[@class="wob_t"]')
	tempMin = driver.find_element(By.XPATH,'//div[@class="vk_lgy"]/span[@class="wob_t"]')
	strOutput = city.text+'\n'+time.text+'\n'+weather.get_attribute('alt')+'\n'+"Tempature: "+str(FtoC(tempMax.text))+'° -- '+str(FtoC(tempMin.text))+'°'
	itchat.send(strOutput,toUserName=id)

	print(city.text)
	print(time.text)
	print(weather.get_attribute('alt'))
	print("Tempature: "+str(FtoC(tempMax.text))+'° -- '+str(FtoC(tempMin.text))+'°')
	aveTemp = (FtoC(tempMax.text)-FtoC(tempMin.text))/2+FtoC(tempMin.text)
	if aveTemp<=10:
		itchat.send("温度低，多穿点儿哈",toUserName=id)

def FtoC(F):
    C = int((int(F)-32)*5/9+0.5)
    return C
