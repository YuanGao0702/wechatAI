
import selenium as se
from selenium.webdriver.common.by import By

def sel3():
	options = se.webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = se.webdriver.Chrome(chrome_options=options)
	url = 'https://github.com/YuanGao0702?tab=repositories'
	print(url)
	driver.get(url)
	elements = driver.find_elements(By.XPATH,'//a[@itemprop="name codeRepository"]')
	print("total repositories: " + str(len(elements)))
	for e in elements:
		print (e.text)

def weather():
    options = se.webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = se.webdriver.Chrome(chrome_options=options)
    url = 'https://www.google.com/search?hl=en&authuser=0&ei=-I4kXMStC8rGjwTqqb6wBA&q=weather&oq=weather&gs_l=psy-ab.12...0.0..19695...0.0..0.0.0.......0......gws-wiz.zvb8D-7d61M'
    driver.get(url)
    city = driver.find_element(By.XPATH,'//div[@class="vk_gy vk_h"][@id="wob_loc"]')
    print(city.text)
    time = driver.find_element(By.XPATH,'//div[@class="vk_gy vk_sh"][@id="wob_dts"]')
    print(time.text)
    weather = driver.find_element(By.XPATH,'//img[@style="margin:1px 4px 0;height:48px;width:48px"]')
    print(weather.get_attribute('alt'))
    tempMax = driver.find_element(By.XPATH,'//div[@class="vk_gy"]/span[@class="wob_t"]')
    print("Tempature: "+str(FtoC(tempMax.text))+'° -- ', end ="")
    tempMin = driver.find_element(By.XPATH,'//div[@class="vk_lgy"]/span[@class="wob_t"]')
    print(str(FtoC(tempMin.text))+'°')

def FtoC(F):
    C = int((int(F)-32)*5/9+0.5)
    return C

def traffic():
    options = se.webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = se.webdriver.Chrome(chrome_options=options)
    url = 'https://www.google.com/maps/dir/1424+Goldenlake+Rd,+San+Jose,+CA+95131/555+E+California+Ave,+Sunnyvale,+CA+94086/@37.3806044,-122.0178939,12z/data=!3m1!4b1!4m18!4m17!1m5!1m1!1s0x808fcc3e5f95acc3:0x47daf6fd38218ca4!2m2!1d-121.8762513!2d37.3853429!1m5!1m1!1s0x808fb64142d26eaf:0x8192e11989e6e62f!2m2!1d-122.020508!2d37.380601!2m3!6e0!7e2!8j1545903000!3e0'
    driver.get(url)
    time = driver.find_element(By.XPATH,'//div[@class="section-directions-trip-numbers"]/div')
    distance = driver.find_element(By.XPATH,'//div[@class="section-directions-trip-numbers"]/div[@class="section-directions-trip-distance section-directions-trip-secondary-text"]')
    crowd = time.get_attribute("class").split("delay-")[1]
    print("Traffic: "+crowd)
    print("Time: "+time.text)
    print(distance.text)
traffic()
