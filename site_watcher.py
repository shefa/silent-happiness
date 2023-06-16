from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import smtplib
import requests
from datetime import datetime

def read_secret(file):
    with open(file) as f:
        return f.read()

def send_discord(url=read_secret("discord_webhook")):
    msg = "@geshalesha [VIPASSANA]"+datetime.now().strftime("%H:%M")+"\nhttps://www.dhamma.org/en/schedules/schsumeru"
    requests.post(url, json={"content": msg})

def send_gmail(username='venom1724', app_pass=read_secret("gmail_app_pass")):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(username, app_pass)
    address = username + "@gmail.com"
    msg = "Subject:[VIPASSANA] site change!\n\nhttps://www.dhamma.org/en/schedules/schsumeru\n"
    s.sendmail(address, address, msg)

def page_test(url="https://www.dhamma.org/en/schedules/schsumeru"):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3)

    assert driver.title == "Vipassana"
    e = driver.find_element(By.XPATH, "//span[text()='16 Aug']").find_element(By.XPATH, ".//ancestor::tr")
    if e.text != "16 Aug - 27 Aug 10-Day\nEnglish / German\nApplications accepted starting 18 Jun\nMont Soleil":
        send_gmail()
        send_discord()
    driver.quit()

page_test()
