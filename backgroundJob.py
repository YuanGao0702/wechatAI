import selenium as se
from selenium.webdriver.common.by import By
import json
import time

def main():
    with open('config.json', 'r') as f:
    	config = json.load(f)
    weather(config)
    traffic(config)
    dealmoon(config)

    # print(config['weather'])
    # print(config['traffic'])

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
    config['cache']['traffic'] = strOutput
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
    #time = driver.find_element(By.XPATH,'//div[@class="vk_gy vk_sh"][@id="wob_dts"]')
    weather = driver.find_element(By.XPATH,'//img[@style="margin:1px 4px 0;height:48px;width:48px"]')
    tempMax = driver.find_element(By.XPATH,'//div[@class="vk_gy"]/span[@class="wob_t"]')
    tempMin = driver.find_element(By.XPATH,'//div[@class="vk_lgy"]/span[@class="wob_t"]')
    strOutput = city.text+'\n'+weather.get_attribute('alt')+'\n'+"Tempature: "+str(FtoC(tempMax.text))+'° -- '+str(FtoC(tempMin.text))+'°'+'\n'
    aveTemp = (FtoC(tempMax.text)-FtoC(tempMin.text))/2+FtoC(tempMin.text)
    if aveTemp<=10:
    	strOutput = strOutput+"温度低，多穿点儿哈"
    print(strOutput)
    config['cache']['weather'] = strOutput
    with open("config.json", "w") as jsonFile:
        json.dump(config, jsonFile, indent=4)

def FtoC(F):
    C = int((int(F)-32)*5/9+0.5)
    return C

def dealmoon(config):
    options = se.webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = se.webdriver.Chrome(chrome_options=options)
    # url = 'https://cn.dealmoon.com/Most-Clicked-Deals-Clothing-Jewelry-Bags-2'
    # url = 'https://cn.dealmoon.com/Most-Clicked-Deals-Beauty-2'
    #url = 'https://www.dealmoon.com/Most-Clicked-Deals-Automotive-2'
    # print(url)
    for category in config["dealmoon"]:
        url = config["dealmoon"][category]
        driver.get(url)
        xpath = '//div[@trkrip="chart_category"]'
        # includes ID
        elements = driver.find_elements(By.XPATH,xpath)
        # href+description
        elements2 = driver.find_elements(By.XPATH,'//div[@trkrip="chart_category"]/a')
        map_id={}
        map_cont={}
        map_href={}
        count = driver.find_elements_by_tag_name('s')
        for i in range(len(count)-15):
            xpath = elements[i].get_attribute('data-id')
            xpath = '//span[@data-id="'+xpath+'"]/em[@class="j-count"]'
            id = str(i+1)
            title = elements2[i].get_attribute('title')
            href = elements2[i].get_attribute('href')
            fav = driver.find_element(By.XPATH,xpath).get_attribute("data-count")
            if(fav=='9999+'):
                fav = '9999'
            fav = int(fav)
            map_id[id]=fav
            map_cont[id]=title
            map_href[id]=href
            #print (id+': '+title+'\n   收藏:'+fav)
        map_id = sorted(map_id.items(), key=lambda x: x[1])
        map_id.reverse()
        id = 1
        result = ""
        for x in map_id[:10]:
            # result = result+str(id)+' '+map_cont[x[0]]+"(#"+str(x[0])+')' +'\n'
            result = result+str(id)+' '+map_cont[x[0]]+'\n'
            result = result + map_href[x[0]] +'\n'
            result = result + 'Subscribe:'+str(x[1])+'\n'
            id = id+1
        print(result)
        config['cache'][category] = result
        with open("config.json", "w") as jsonFile:
            json.dump(config, jsonFile, indent=4)

while(True):
    main()
    time.sleep(1800)
