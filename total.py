import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time # ダウンロード待ちや動的なページの読み込み待ち(いずれは暗黙的な感じでやりたい)
import re
import os
from glob import glob
import setting




def get_latest_modified_file_path(dirname):
  target = os.path.join(dirname, '*')
  files = [(f, os.path.getmtime(f)) for f in glob(target)]
  latest_modified_file_path = sorted(files, key=lambda files: files[1])[0]
  return latest_modified_file_path[0]
def accent(text):
    text_a = re.sub(r'à|â', "a", text)
    text_i = re.sub(r'ï|î', "i", text_a)
    text_u = re.sub(r'û|ù', "u", text_i)
    text_e = re.sub(r'è|é|ê|ë', "e", text_u)
    text_o = re.sub(r'Ô', "o", text_e)
    text_A = re.sub(r'À|Â', "A", text_o)
    text_I = re.sub(r'Ï|Î', "I", text_A)
    text_U = re.sub(r'Û|Ù', "U", text_I)
    text_E = re.sub(r'È|É|Ê|Ë', "E", text_U)
    text_O = re.sub(r'Ô', "O", text_E)
    return text_O



def total():
    downloaddir = os.getcwd()+ "\\downloads"
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": downloaddir})


    # WebDriverのパスを指定してChromeを起動
    driver = webdriver.Chrome(options)

    # ウェブページにアクセス
    url = 'https://www.17lands.com/card_data'
    driver.get(url)
    # pack_nameが取得可能になるまで待機
    pack_name_button_selector = '#expansion > option:nth-child(1)'
    wait = WebDriverWait(driver, 10)
    pack_name_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, pack_name_button_selector)))
    if setting.get_other_pack:
        pack_name = setting.Pack_name
        dropdown = driver.find_element(By.ID, 'expansion')
        select = Select(dropdown)
        select.select_by_visible_text(pack_name)
    else:
        pack_name = pack_name_button.text

    print(pack_name)

    # Export_dataボタンがクリック可能になるまで待機
    Export_data_button_selector = '#app > div > div.sc-eywOmQ.fDjuIB > div.ui.dropdown > div.divider.text'
    Export_data_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, Export_data_button_selector)))

    # Export_dataボタンをクリック
    Export_data_button.click()

    # Download_csvボタンがクリック可能になるまで待機 (適切なセレクタを使用してください)
    Download_csv_button_selector = '#app > div > div.sc-eywOmQ.fDjuIB > div.ui.active.visible.dropdown > div.menu.transition.visible > div:nth-child(2) > a'
    Download_csv_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, Download_csv_button_selector)))

    # Download_csvボタンをクリック
    Download_csv_button.click()

    time.sleep(5)  # 仮の待機時間

    # WebDriverを閉じる
    driver.close()


    dirname = "downloads"
    csv_path =get_latest_modified_file_path(dirname)
    datas = pd.read_csv(csv_path)
    print(datas["Name"])
    en_names=[]
    for name in datas["Name"]:
        en_names.append(accent(name))

    driver = webdriver.Chrome()

    driver.get('https://www.wisdom-guild.net/apps/translator/')






    element = driver.find_element(By.XPATH, "//*[@id=\"translator_main\"]/tbody/tr[2]/td[1]/textarea")
    element.send_keys(en_names)


    element = driver.find_element(By.XPATH, "//*[@id=\"translator_main\"]/tbody/tr[3]/td/button[2]")
    element.click()


    element = driver.find_element(By.XPATH, "//*[@id=\"translator_main\"]/tbody/tr[2]/td[2]/textarea")
    en_jp_names = element.get_attribute('value')
    df_en_jp_names = pd.DataFrame(re.split("(?<=》)",en_jp_names))
    df_en_jp_names = df_en_jp_names.drop(df_en_jp_names.index[[-1]])
    datas["Name"]=df_en_jp_names
    print(datas["Name"])


    if not os.path.exists('output'):
        os.mkdir('output')
    datas.to_csv("output/"+pack_name+"-card-ratings.csv", encoding = "shift-jis")