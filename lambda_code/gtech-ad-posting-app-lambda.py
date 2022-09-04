# import time
import os
import shutil
from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import boto3

login_id = os.environ.get('login_id')
login_pw = os.environ.get('login_pw')
url_gtech_1 = os.environ.get('url_gtech_1')
url_gtech_2 = os.environ.get('url_gtech_2')
ad_pic_s3_bucket = os.environ.get('ad_pic_s3_bucket')
ad_pic_s3_prefix = os.environ.get('ad_pic_s3_prefix')

download_dir = "/tmp/download"

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    img_full_path = download_ad_image()
    openURL(img_full_path)
    clean_tmp_folder()


def find_latest_ad_image():
    s3_keys = s3_client.list_objects_v2(Bucket=ad_pic_s3_bucket,
                                        Prefix=ad_pic_s3_prefix
                                        )
    s3_keys_Contents = s3_keys['Contents']

    # Creating a dictionary with s3key_name and its modified date
    key_dict = {key['Key']: key['LastModified'] for key in s3_keys_Contents if key['Key'].endswith('.jpeg')}

    # Sorting the dictionary based on the modified date
    key_dict = dict(sorted(key_dict.items(), key=lambda x: (x[1], x[0])))

    # Returning the latest modified file's s3 key name
    return list(key_dict)[-1]


def download_ad_image():
    print("os.getcwd():", os.getcwd())
    listdir = os.listdir(os.getcwd())
    print("listdir:", listdir)

    if not os.path.exists(download_dir):
        print("Creating download folder")
        os.makedirs(download_dir)

    ad_pic_s3_key = find_latest_ad_image()
    print(f"Downloading ad image {ad_pic_s3_key} in {download_dir}")
    file_name_in_download_dir = os.path.join(download_dir, ad_pic_s3_key.split("/")[-1])
    s3_client.download_file(Bucket=ad_pic_s3_bucket,
                            Key=ad_pic_s3_key,
                            Filename=file_name_in_download_dir
                            )
    # os.chmod(newfile, 0o775)
    print("download_dir:", os.listdir(download_dir))
    return file_name_in_download_dir


def clean_tmp_folder():
    print("Deleting /tmp/download directory")
    shutil.rmtree(download_dir)
    print("Delete completed. os.listdir('/tmp'):", os.listdir("/tmp"))


def openURL(img_full_path):
    print('start')
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

    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome("/opt/chromedriver",
                              options=options)

    driver.get(url_gtech_1)
    print('opened web browser')

    element_id = driver.find_element(by=By.ID, value="login_id")
    element_id.send_keys(login_id)
    element_pwd = driver.find_element(by=By.ID, value="login_pw")
    element_pwd.send_keys(login_pw)
    print('entered id/pwd')

    element_click1 = driver.find_element(by=By.CLASS_NAME, value='btn_submit')
    element_click1.click()
    print('login completed')

    driver.get(url_gtech_2)
    print('entering the advertising page')
    element_click2 = driver.find_element(by=By.CLASS_NAME, value="chk_box")
    element_click2.click()
    print('clicked html')

    driver.switch_to.alert.accept()
    print('alert accepted')

    # Subject typed
    element_subject = driver.find_element(by=By.ID, value='wr_subject')
    element_subject.send_keys('◆ 자동차 썬팅/블랙박스 전문점 틴트 마스터, 아이나비 블랙박스 특별세일!!! ◆')
    print('subject typed')

    # Content typed
    element_subject = driver.find_element(by=By.ID, value='wr_content')
    element_subject.send_keys(content)
    print('content typed')

    # photo attached
    element_attachment = driver.find_element(by=By.ID, value="bf_file_1")
    element_attachment.send_keys(img_full_path)
    print("Photo attached")

    # submit
    element_submit_btn = driver.find_element(by=By.ID, value='btn_submit')
    element_submit_btn.click()
    print('AD post uploaded')
