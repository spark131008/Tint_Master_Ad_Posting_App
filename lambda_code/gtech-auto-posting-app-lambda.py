import urllib.request
import urllib.error
import time
import os
from selenium import webdriver

id_gtech = os.environ.get('id_gtech')
pwd_gtech = os.environ.get('pwd_gtech')
url_gtech_1 = os.environ.get('url_gtech_1')
url_gtech_2 = os.environ.get('url_gtech_2')
ad_pic_s3_bucket = os.environ.get('ad_pic_s3_bucket')
ad_pic_s3_key = os.environ.get('ad_pic_s3_key')

def lambda_handler(event, context):
    openURL()

def openURL():
    print('start')
    try:
        content = '''
<p class="li1" style="font-size:12px;line-height:0.5;font-family:'Helvetica Neue';"><span style="font-size:26px;">
<span style="color:rgb(241,196,15);"><span style="font-size:36px;"><span style="background-color:rgb(0,0,204);">틴트마스터 블랙박스 스페셜</span></span></span> <br><br>
(최신형) 아이나비 QXD7000  <br><br>
(최신형) 아이나비 X1000  <br><br>
(최신형) 아이나비 X700  <br><br>
(최신형) 아이나비 Z3000  <br><br>
             아이나비 A500  <br><br>
             아이나비 F200 Pro <br><br>
<span style="font-size:20px;"><span style="line-height:1.5;">**블랙박스는 반드시 전문가에게 맡기셔야 합니다. 블랙박스 설치 시, 배선작업을 잘못할 경우 심각한 전기문제를 초래할 수 있습니다. 틴트 마스터에서는 30년 경험의 전문가가 책임지고 설치해 드립니다. 블랙박스 설치전, 사전상담은 필수입니다.**</span></span><br>
</span></p>

<p class="p1" style="font-size:12px;line-height:0.8;font-family:'Helvetica Neue';"><span style="font-size:26px;">
틴팅과 블랙박스를 같이 설치하시면, <br>
콤보 스페셜 할인 있습니다. <br>
가격 문의주세요. <br>
2856 Buford Hwy. #5, Duluth, GA 30096 <br>
</span></p>
<p class="p1" style="font-size:12px;line-height:0.8;font-family:'Helvetica Neue';"><span style="font-size:36px;"><span style="color:rgb(192,57,43);"><span style="background-color:rgb(241,196,15);">Tint Master 틴트 마스터</span></p>

<p class="p3" style="font-size:12px;line-height:0.5;font-family:'Helvetica Neue';color:rgb(220,161,13);"><span style="font-size:26px;"><a href="mailto:tintmasteratl@gmail.com">tintmasteratl@gmail.com</a></span></p>

<p class="p1" style="font-size:12px;line-height:0.9;font-family:'Helvetica Neue';"><span style="font-size:48px;">678-731-7177</span></p>
        '''

        a = urllib.request.urlopen(url_gtech_1)
        print(a.getcode())

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1696')
        chrome_options.add_argument('--user-data-dir=/tmp/user-data')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path=/tmp/data-path')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir=/tmp')
        chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url_gtech_1)
        print('open web browser')

        driver.type(id_gtech, into='mb_id', id='login_id')
        driver.type(pwd_gtech, into='mb_password', id='login_pw')
        print('entered id/pwd')

        driver.click(text='로그인')
        driver.click(text='광고')

        driver.get(url_gtech_2)
        driver.click(text="html", tag='input')


        # web.go_to(url_gtech_1)
        # web.type(id_gtech, into='mb_id', id='login_id')
        # web.type(pwd_gtech, into='mb_password', id='login_pw')
        # web.click(text='로그인')
        # web.click(text='광고')
        # web.go_to(url_gtech_2)
        # web.click(text="html", tag='input')
        driver.switch_to.alert.accept()

        # Subject typed
        driver.type('◆ 자동차 썬팅/블랙박스 전문점 틴트 마스터, 아이나비 블랙박스 특별세일!!! ◆', into='wr_subject', id='wr_subject')

        # Content typed
        driver.type(content, into='wr_content', id='wr_content')

        # photo attached
        driver.click(text="bf_file[]", tag='input', id='bf_file_1')
        driver.driver.find_element_by_id("bf_file_1").send_keys(ad_pic_s3_bucket)
        # web.press(key=web.Key.ESCAPE)

        # submit
        # web.click(text="작성완료", id='btn_submit')

    except Exception as e:
        print(e)

    finally:
        time.sleep(5)