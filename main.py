from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
import time


path = 'name.txt'


# - - - - - - - - - 
# 関数
# - - - - - - - - - 


# Slackへテキストを通知
def send_text(text):
    slack_url = 'YOUR WEBHOOK URL' ###
    data = json.dumps({
        'username': 'bot',
        'text': text
    })
    requests.post(slack_url, data=data)


# - - - - - - - - - 
# メイン関数
# - - - - - - - - - 
if __name__ == '__main__':

    # HeadlessなChromeの設定
    options = Options()
    options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    # Topページへアクセス
    browser.get('http://dushu.baidu.com/pc/detail?gid=4305535599')


    # 新章を取得
    elems = browser.find_elements_by_class_name('latest-chapter')
    new = elems[0].find_element_by_class_name('title').text
    
    with open(path) as f:
        old = f.read()
               

        # ITカテゴリーであれば Slack へ通知
        if new != old:
            # Slack へ通知
            send_text(new)
            
            with open(path, mode='w') as f:
                f.write(new)
        
        # 3秒待機
        time.sleep(3)

    # ブラウザを閉じる
    browser.quit()
        
