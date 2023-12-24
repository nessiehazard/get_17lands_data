import pandas as pd
from selenium import webdriver
import time # ダウンロード待ちや動的なページの読み込み待ち(いずれは暗黙的な感じでやりたい)
from selenium.webdriver.common.by import By
import re
import os
from glob import glob



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





downloaddir = os.getcwd()+ "\\downloads"
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"download.default_directory": downloaddir})

# ブラウザの起動

driver = webdriver.Chrome(options)

driver.get('https://www.17lands.com/card_data')

time.sleep(5)
element = driver.find_element(By.XPATH, "//*[@id=\"expansion\"]/option[1]")
pack_name = element.text

time.sleep(5)

# Export　data部分の要素を取得
element = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[1]')
# Export　dataをクリック
element.click()

time.sleep(5)

# Download as CSV部分の要素を取得
element_csv = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div[2]/div[2]/a')
# Download as CSVをクリック
element_csv.click()


time.sleep(5)
# ブラウザを閉じる
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




time.sleep(5)

element = driver.find_element(By.XPATH, "//*[@id=\"translator_main\"]/tbody/tr[2]/td[1]/textarea")
element.send_keys(en_names)

time.sleep(5)
element = driver.find_element(By.XPATH, "//*[@id=\"translator_main\"]/tbody/tr[3]/td/button[2]")
element.click()


element = driver.find_element(By.XPATH, "//*[@id=\"translator_main\"]/tbody/tr[2]/td[2]/textarea")
en_jp_names = element.get_attribute('value')
df_en_jp_names = pd.DataFrame(re.split("(?<=》)",en_jp_names))
df_en_jp_names = df_en_jp_names.drop(df_en_jp_names.index[[-1]])
datas["Name"]=df_en_jp_names
print(datas["Name"])

datas.to_csv("output/"+pack_name+"-card-ratings.csv", encoding = "shift-jis")