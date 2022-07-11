import urllib.request
import urllib.error
import webbrowser
from webbot import Browser
import time
import os

id_gtech = os.environ.get('id_gtech')
pwd_gtech = os.environ.get('pwd_gtech')
url_gtech_1 = os.enviorn.get('url_gtech_1')
url_gtech_2 = os.enviorn.get('url_gtech_2')
ad_pic_s3_bucket = os.enviorn.get('ad_pic_s3_bucket')
ad_pic_s3_key = os.enviorn.get('ad_pic_s3_key')

def lambda_handler(event, context):
    openURL(url_gtech_1)

def openURL(url_gtech_1):
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

        web = Browser()
        web.go_to(url_gtech_1)
        web.type(id_gtech, into='mb_id', id='login_id')
        web.type(pwd_gtech, into='mb_password', id='login_pw')
        web.click(text='로그인')
        web.click(text='광고')
        web.go_to(url_gtech_2)
        web.click(text="html", tag='input')
        web.driver.switch_to.alert.accept()

        # Subject typed
        web.type('◆ 자동차 썬팅/블랙박스 전문점 틴트 마스터, 아이나비 블랙박스 특별세일!!! ◆', into='wr_subject', id='wr_subject')

        # Content typed
        web.type(content, into='wr_content', id='wr_content')

        # photo attached
        web.click(text="bf_file[]", tag='input', id='bf_file_1')
        web.driver.find_element_by_id("bf_file_1").send_keys(ad_pic_s3_bucket)
        web.press(key=web.Key.ESCAPE)

        # submit
        web.click(text="작성완료", id='btn_submit')

    except Exception as e:
        print(e)

    finally:
        time.sleep(5)