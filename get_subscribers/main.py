from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome

from bs4 import BeautifulSoup

import time, config


url = "https://www.instagram.com/"
driver = Chrome()

driver.get(url)
driver.implicitly_wait(5)
time.sleep(3)

def get_subscribers(page_source):
    soup = BeautifulSoup(page_source, 'lxml')
    block_subscribers = soup.find_all('div', class_='x1dm5mii x16mil14 xiojian x1yutycm x1lliihq x193iq5w xh8yej3')
    subscribers = []
    for block in block_subscribers:
        username = block.find('a')
        if username:
            subscribers.append(username.get('href').strip('/'))
    return subscribers


inputs = driver.find_elements(By.TAG_NAME, 'input')
login_input = inputs[0]
password_input = inputs[1]

login_input.send_keys(config.login)
password_input.send_keys(config.password)

driver.find_elements(By.TAG_NAME, 'button')[1].click()
time.sleep(5)

driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a').click()
time.sleep(1)

driver.find_element(By.TAG_NAME, 'input').send_keys(config.username)
time.sleep(0.5)

driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/a[1]').click()
driver.implicitly_wait(5)
time.sleep(3)

driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a').click()
time.sleep(2)

driver.execute_script("let menu = document.querySelector('._aano');")
h_prev = 0
while True:
    h = driver.execute_script("""return menu.scrollHeight""")
    driver.execute_script(f"menu.scrollTo(0,{h});")
    time.sleep(2)
    if h == h_prev:
        break
    h_prev = h

time.sleep(1)

with open('subscribers.txt', 'w', encoding='utf-8') as file:
    subscribers = get_subscribers(driver.page_source)
    file.write('\n'.join(subscribers))
file.close()

print('Script ended!')