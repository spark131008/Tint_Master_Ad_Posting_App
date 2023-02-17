import os
import shutil
import json
from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import boto3

region_name = os.environ.get('region_name')
secret_name = os.environ.get('secret_name')
gtechapp_bucket = os.environ.get('gtechapp_bucket')

download_dir = "/tmp/download"

s3_client = boto3.client("s3")

def lambda_handler(event: str, context):
    payload = json.loads(event)
    img_local_download_path = download_ad_image(payload)
    html_content = html_file_reader(payload)
    ad_posting(img_local_download_path, html_content)
    clean_tmp_folder()


def download_ad_image(payload: dict) -> str:
    print("os.getcwd():", os.getcwd())
    listdir = os.listdir(os.getcwd())
    print("listdir:", listdir)

    if not os.path.exists(download_dir):
        print("Creating download folder")
        os.makedirs(download_dir)

    ad_pic_s3_key = find_latest_ad_image(payload)
    print(f"Downloading ad image {ad_pic_s3_key} in {download_dir}")
    file_name_in_download_dir = os.path.join(download_dir, ad_pic_s3_key.split("/")[-1])
    s3_client.download_file(Bucket=gtechapp_bucket,
                            Key=ad_pic_s3_key,
                            Filename=file_name_in_download_dir
                            )
    # os.chmod(newfile, 0o775)
    print("download_dir:", os.listdir(download_dir))
    return file_name_in_download_dir


def find_latest_ad_image(payload: dict) -> str:
    company_name = payload['company_name']
    ad_pic_s3_prefix = payload['ad_pic_s3_prefix']

    s3_keys = s3_client.list_objects_v2(Bucket=gtechapp_bucket,
                                        Prefix=ad_pic_s3_prefix
                                        )
    s3_keys_contents = s3_keys['Contents']

    # Creating a sorted list of keys
    sorted_keys = sorted([key['Key'] for key in s3_keys_contents if key['Key'].contains(company_name) and key['Key'].endswith('.jpeg')])

    # Returning the latest modified file's s3 key name
    return sorted_keys[-1]


def html_file_reader(payload: dict) -> str:
    company_name = payload['company_name']
    ad_html_s3_prefix = payload['ad_html_s3_prefix']

    s3_keys = s3_client.list_objects_v2(Bucket=gtechapp_bucket,
                                        Prefix=ad_html_s3_prefix
                                        )
    s3_keys_contents = s3_keys['Contents']
    html_key = [key['Key'] for key in s3_keys_contents if key['Key'].contains(company_name) and key['Key'].endswith('.html')][0]
    data = s3_client.get_object(Bucket=gtechapp_bucket, Key=html_key)
    contents = data['Body'].read()
    print(contents.decode("utf-8"))
    return contents.decode("utf-8")


def clean_tmp_folder():
    print("Deleting /tmp/download directory")
    shutil.rmtree(download_dir)
    print("Delete completed. os.listdir('/tmp'):", os.listdir("/tmp"))


def ad_posting(local_file_path, html_content):
    print('start')
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
    secret = get_secret()

    driver.get(secret["gtech_login_url"])
    print('opened web browser')


    element_id = driver.find_element(by=By.ID, value="login_id")
    element_id.send_keys(secret["tint_master_id"])
    element_pwd = driver.find_element(by=By.ID, value="login_pw")
    element_pwd.send_keys(secret["tint_master_pw"])
    print('entered id/pwd')

    element_click1 = driver.find_element(by=By.CLASS_NAME, value='btn_submit')
    element_click1.click()
    print('login completed')

    driver.get(secret["gtech_ad_url"])
    print('entering the advertising page')
    element_click2 = driver.find_element(by=By.CLASS_NAME, value="chk_box")
    element_click2.click()
    print('clicked html')

    driver.switch_to.alert.accept()
    print('alert accepted')

    # Subject typed
    element_subject = driver.find_element(by=By.ID, value='wr_subject')
    subject_from_html = html_content.split('<head>')[-1].split('</head>')[0]
    element_subject.send_keys(subject_from_html)
    print('subject typed')

    # Content typed
    element_subject = driver.find_element(by=By.ID, value='wr_content')
    element_subject.send_keys(html_content)
    print('content typed')

    # photo attached
    element_attachment = driver.find_element(by=By.ID, value="bf_file_1")
    element_attachment.send_keys(local_file_path)
    print("Photo attached")

    # submit
    element_submit_btn = driver.find_element(by=By.ID, value='btn_submit')
    element_submit_btn.click()
    print('AD post uploaded')


def get_secret():
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    return json.loads(get_secret_value_response['SecretString'])