import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import time


def main():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        browser = webdriver.Chrome(options=chrome_options)
        url = 'https://www.taifex.com.tw/cht/3/optPrevious30DaysSalesData'
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        allData = soup.find_all('input', {"id": "button7"})

        currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print(currentTime, 'start task...')
        print('Current path', os.getcwd())

        path = os.getcwd()+'\\OptionsData\\'
        if not os.path.exists(path):
            os.mkdir(path)
            print('Make a directory OptionsData to store downloaded data')
            
        new = 0
        for data in allData:
            url = data.get('onclick')[24:-2]
            if '/OptionsDailydownloadCSV/OptionsDaily' in url:
                fileName = url[-27:-4] + '.zip'
                yearDir = path+fileName[13:17]
                if not os.path.exists(yearDir):
                    os.mkdir(yearDir)
                    print('Make a folder',
                          fileName[13:17], 'to store this year\'s data')

                dataList = os.listdir(yearDir)
                if(fileName not in dataList):
                    file = urlopen(url)
                    with open(os.path.join(yearDir, fileName), 'wb') as f:
                        f.write(file.read())
                        print('Download', fileName)
                    with open(os.path.join(path, 'log.txt'), 'a') as l:
                        l.write(currentTime+' download '+fileName+'\n')
                    new = 1
        if new == 0:
            print('No new data need to download')
            with open(os.path.join(path, 'log.txt'), 'a') as l:
                l.write(currentTime+' no new data need to download'+'\n')

        print('Task done')
        
    except:
        path = os.getcwd()+'\\OptionsData\\'
        if not os.path.exists(path):
            os.mkdir(path)
            print('Make a directory OptionsData to store downloaded data')

        currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        with open(os.path.join(path, 'error.txt'), 'a') as l:
            l.write(currentTime+'\n'+traceback.format_exc())
            print('An error occurred, please check the error.txt')

        print('Task done')


main()
