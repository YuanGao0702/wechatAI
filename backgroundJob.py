import selenium as se
from selenium.webdriver.common.by import By
import json
import time

def main():
    with open('config.json', 'r') as f:
    	config = json.load(f)
    weather(config)
    traffic(config)

    print(config['weather'])
    print(config['traffic'])

def traffic(config):
    options = se.webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = se.webdriver.Chrome(chrome_options=options)
    home = config['home']
    destination = config['destination']
    url = 'https://www.google.com/maps/dir/'+home+','+destination+'/@37.3806044,-122.0178939,12z/data=!3m1!4b1!4m14!4m13!1m5!1m1!1s0x808fcc3e5f95acc3:0x47daf6fd38218ca4!2m2!1d-121.8762513!2d37.3853429!1m5!1m1!1s0x808fb64142d26eaf:0x8192e11989e6e62f!2m2!1d-122.020508!2d37.380601!3e0'
    #url = 'https://www.google.com/maps/dir/'+home+','+destination+'/@37.3806044,-122.0178939,12z/data=!3m1!4b1!4m14!4m13!1m5!1m1!1s0x808fcc3e5f95acc3:0x47daf6fd38218ca4!2m2!1d-121.8762513!2d37.3853429!1m5!1m1!1s0x808fb64142d26eaf:0x8192e11989e6e62f!2m2!1d-122.020508!2d37.380601!3e0'
    urlTest = 'https://www.google.com/maps/dir/'+home+','+destination+'/@37.3806044,-122.0178939,12z/data=!3m1!4b1!4m18!4m17!1m5!1m1!1s0x808fcc3e5f95acc3:0x47daf6fd38218ca4!2m2!1d-121.8762513!2d37.3853429!1m5!1m1!1s0x808fb64142d26eaf:0x8192e11989e6e62f!2m2!1d-122.020508!2d37.380601!2m3!6e0!7e2!8j1545897900!3e0'
    driver.get(url)
    time = driver.find_element(By.XPATH,'//div[@class="section-directions-trip-numbers"]/div')
    distance = driver.find_element(By.XPATH,'//div[@class="section-directions-trip-numbers"]/div[@class="section-directions-trip-distance section-directions-trip-secondary-text"]')
    crowd = time.get_attribute("class").split("delay-")[1]
    strOutput = "Traffic: "+crowd +'\n'+"Time: "+time.text+'\n'+distance.text+'\n'
    if crowd == 'heavy':
    	strOutput = strOutput+ "太堵啦，要不等会儿再出发"
    print(strOutput)
    config['traffic'] = strOutput
    with open("config.json", "w") as jsonFile:
        json.dump(config, jsonFile, indent=4)

def weather(config):
    city = config['city']
    options = se.webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = se.webdriver.Chrome(chrome_options=options)
    url = 'https://www.google.com/search?hl=en&authuser=0&ei=M5YkXM_tOYzBjwTu47jABA&q='+city+'weather&oq=zhuozhou+weather&gs_l=psy-ab.3..35i39.1104929.1106580..1106843...0.0..0.97.684.9......0....1..gws-wiz.......0i71j0i7i30j0i7i5i10i30j0i13j0i13i30j0i8i13i30j35i304i39.kcZOPDwMDfs'
    driver.get(url)
    city = driver.find_element(By.XPATH,'//div[@class="vk_gy vk_h"][@id="wob_loc"]')
    time = driver.find_element(By.XPATH,'//div[@class="vk_gy vk_sh"][@id="wob_dts"]')
    weather = driver.find_element(By.XPATH,'//img[@style="margin:1px 4px 0;height:48px;width:48px"]')
    tempMax = driver.find_element(By.XPATH,'//div[@class="vk_gy"]/span[@class="wob_t"]')
    tempMin = driver.find_element(By.XPATH,'//div[@class="vk_lgy"]/span[@class="wob_t"]')
    strOutput = city.text+'\n'+time.text+'\n'+weather.get_attribute('alt')+'\n'+"Tempature: "+str(FtoC(tempMax.text))+'° -- '+str(FtoC(tempMin.text))+'°'+'\n'
    aveTemp = (FtoC(tempMax.text)-FtoC(tempMin.text))/2+FtoC(tempMin.text)
    if aveTemp<=10:
    	strOutput = strOutput+"温度低，多穿点儿哈"
    print(strOutput)
    config['weather'] = strOutput
    with open("config.json", "w") as jsonFile:
        json.dump(config, jsonFile, indent=4)

def FtoC(F):
    C = int((int(F)-32)*5/9+0.5)
    return C

while(True):
    main()
    time.sleep(300)
