# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 14:12:33 2021

@author: Anshul Gautam
"""
# importing webdriver from selenium
from selenium import webdriver
import time
import creds #Credentials
from telethon import TelegramClient, events #Handles Telegram requests
import tele_creds

# Here Chrome will be used
driver = webdriver.Chrome()

# Opening the website
driver.maximize_window()
driver.get(creds.url)

#xPath initialisation
email_input = '//*[@id="qa_auth_LoginEmailInput"]/vui-input/div[1]/div[2]/vui-input-text/input'
password_input = '//*[@id="qa_auth_LoginPasswordInput"]/vui-input/div[1]/div[2]/vui-input-password/input'
sign_in_button = '//*[@id="qa_auth_LoginBtn"]/button'
deal_up_button = '//*[@id="qa_trading_dealUpButton"]/button'
deal_down_button = '//*[@id="qa_trading_dealDownButton"]/button'
time_dropdwon = '//*[@id="qa_trading_dealTimeInput"]/div[1]/div[1]/vui-input-number/input'
fifth_time_interval = '//*[@id="qa_trading_dealTimeInput"]/div[1]/vui-popover/div[2]/app-scroll/div/div/div/div[1]/vui-option[5]'

#credential input
time.sleep(5)
driver.find_element_by_xpath(email_input).send_keys(creds.username)
print('\n\nEmail Entered')
driver.find_element_by_xpath(password_input).send_keys(creds.password)
print('Password Entered')
driver.find_element_by_xpath(sign_in_button).click()
print('Verifying Captcha...\n')

started_at = time.localtime()
current_time = time.strftime("%H:%M:%S", started_at)
print("BOT started operations at",current_time)

#Telegram client initialisation
client = TelegramClient('anon', tele_creds.api_id, tele_creds.api_hash)
client.start()
client.run_until_disconnected()

@client.on(events.NewMessage(chats=tele_creds.user_input_channel))
async def my_event_handler(event):
    if 'DOWN' in event.raw_text:
        # await event.reply('hid!')
        drop_down_button = driver.find_element_by_xpath(time_dropdwon)
        driver.execute_script("arguments[0].click();", drop_down_button)
        print('Time dropdown selected')
        
        fifth_time_button = driver.find_element_by_xpath(fifth_time_interval)
        driver.execute_script("arguments[0].click();", fifth_time_button)
        print('5-min interval selected')
        
        put_button = driver.find_element_by_xpath(deal_down_button)
        driver.execute_script("arguments[0].click();", put_button)
        
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print('PUT placed at ', current_time)
        
        print('\n')
    elif 'UP' in event.raw_text:
        #await event.reply('hiU!')
        drop_down_button = driver.find_element_by_xpath(time_dropdwon)
        driver.execute_script("arguments[0].click();", drop_down_button)
        print('Time dropdown selected')
        
        fifth_time_button = driver.find_element_by_xpath(fifth_time_interval)
        driver.execute_script("arguments[0].click();", fifth_time_button)
        print('5-min interval selected')
        
        call_button = driver.find_element_by_xpath(deal_up_button)
        driver.execute_script("arguments[0].click();", call_button)
        
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print('CALL placed at', current_time)
        
        print("\n")
