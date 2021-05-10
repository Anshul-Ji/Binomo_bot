# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 10:04:32 2021

@author: Anshul Gautam
"""


# importing webdriver from selenium
from datetime import date
from selenium import webdriver
import time
import creds #Credentials
from telethon import TelegramClient, events #Handles Telegram requests
import tele_creds
import re

# Here Chrome will be used
driver = webdriver.Chrome()

# Opening the website
driver.maximize_window()
driver.get(creds.url)


#xPath initialisation
#Login Elements
email_input_xpath = '//*[@id="qa_auth_LoginEmailInput"]/vui-input/div[1]/div[2]/vui-input-text/input'
password_input_xpath = '//*[@id="qa_auth_LoginPasswordInput"]/vui-input/div[1]/div[2]/vui-input-password/input'
sign_in_button_xpath = '//*[@id="qa_auth_LoginBtn"]/button'
#Trade placement Elements
call_xpath = '//*[@id="qa_trading_dealUpButton"]/button'
put_xpath = '//*[@id="qa_trading_dealDownButton"]/button'
time_dropdwon_xpath = '//*[@id="qa_trading_dealTimeInput"]/div[1]/div[1]/vui-input-number/input'
# fifth_time_interval_xpath = '//*[@id="qa_trading_dealTimeInput"]/div[1]/vui-popover/div[2]/app-scroll/div/div/div/div[1]/vui-option[5]'
#Below one is 1 min time interval for testing purposes
fifth_time_interval_xpath = '//*[@id="qa_trading_dealTimeInput"]/div[1]/vui-popover/div[2]/app-scroll/div/div/div/div[1]/vui-option[1]'
#Internal Server Error (Binomo Screen Fadeout)
internal_close_button_xpath = '/html/body/ng-component/vui-modal/div/div[1]/button'
#Trade result Elements
trade_result_xpath = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/div/option-item[1]/div/div[2]/div[2]/p[1]'
trade_amount_xpath = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[2]/app-virtual-scroll/app-scroll/div/div/div[1]/ng-component/ng-component/div/option-item[1]/div/div[2]/div[2]/p[2]'
history_button_xpath = '//*[@id="qa_historyButton"]/vui-badge'
history_close_xpath  = '//*[@id="qa_trading_abilityDashboard"]/div/vui-sidebar/div/div/div[1]/vui-icon/i'
#Trade Result Global variables
global investment,result
investment = 0
result = 0

#credential input
time.sleep(10)
driver.find_element_by_xpath(email_input_xpath).send_keys(creds.username)
print('\n\nEmail Entered')
driver.find_element_by_xpath(password_input_xpath).send_keys(creds.password)
print('Password Entered')
driver.find_element_by_xpath(sign_in_button_xpath).click()
print('Verifying Captcha...\n')

#Trade_logging file name generator
def get_filename_datetime():
    # Use current date to get a text file name.
    return "log_" + str(date.today()) + ".txt"

log_name = get_filename_datetime()
log_file_path = "C:\\Users\\Anshul Gautam\\Desktop\\Binomo_auto\\Final_bot\\Trade_log\\" + log_name

started_at = time.localtime()
current_time = time.strftime("%H:%M:%S", started_at)
print("BOT started operations at",current_time)
with open(log_file_path, "a") as f:
    f.write('\n{0} {1}\n'.format("BOT started operations at",current_time))
    f.close()


#Telegram client initialisation
client = TelegramClient('anon', tele_creds.api_id, tele_creds.api_hash)

@client.on(events.NewMessage(chats=tele_creds.user_input_channel))
async def my_event_handler(event):
    if 'DOWN' in event.raw_text:
        try:
            time_dropdown_button = driver.find_element_by_xpath(time_dropdwon_xpath)
            driver.execute_script("arguments[0].click();", time_dropdown_button)
            print('Time dropdown selected')
            
            fifth_time_interval_button = driver.find_element_by_xpath(fifth_time_interval_xpath)
            driver.execute_script("arguments[0].click();", fifth_time_interval_button)
            print('5-min interval selected')
            
            put_button = driver.find_element_by_xpath(put_xpath)
            driver.execute_script("arguments[0].click();", put_button)
            
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('PUT placed at ', current_time)
            print('\n')
            
            f = open(log_file_path, "a")
            f.write('{0} {1}\n'.format("PUT placed at ", current_time))
            
            time.sleep(5)
            history_button = driver.find_element_by_xpath(history_button_xpath)
            driver.execute_script("arguments[0].click();", history_button)
            time.sleep(5)
            result_string = driver.find_element_by_xpath(trade_result_xpath).text
            amount_string = driver.find_element_by_xpath(trade_amount_xpath).text
            
            history_close_button = driver.find_element_by_xpath(history_close_xpath)
            driver.execute_script("arguments[0].click();", history_close_button)
            
            result_list = re.findall('[\d]*[.][\d]+',result_string)
            result_value = float(result_list[0])
            
            amount_list = re.findall('[\d]*[.][\d]+',amount_string)
            amount_value = float(amount_list[0])
            print('flag1')
            
            if result_value > 0:
                investment += amount_value
                result += result_value
            else:
                investment += amount_value
             
            print('flag2')
            print("Investment:", investment)
            print("Result:", result)
            print("Gain/Loss:",result-investment)
            f.write('{0} {1}\n'.format("Investment:", investment))
            f.write('{0} {1}\n'.format("Result:", result))
            f.write('{0} {1}\n\n'.format("Gain/Loss:", result-investment))
            f.close()
            
            # await event.reply('hid!')
        except:
            f = open(log_file_path, "a")
            if driver.find_element_by_xpath(internal_close_button_xpath).size() != 0:
                int_error_close_button = driver.find_element_by_xpath(close_button)
                driver.execute_script("arguments[0].click();", int_error_close_button)
                print("\nInternal server error occured in Binomo.")
                f.write("\nInternal server error occured in Binomo.\n")
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('Some error occured, page refreshed at', current_time, "\n\n")
            f.write('{0} {1}\n\n'.format('Some error occured, page refreshed at', current_time))
            f.close()
            driver.refresh() 
            
    elif 'UP' in event.raw_text:
        
        try:
            time_dropdown_button = driver.find_element_by_xpath(time_dropdwon_xpath)
            driver.execute_script("arguments[0].click();", time_dropdown_button)
            print('Time dropdown selected')
            
            fifth_time_interval_button = driver.find_element_by_xpath(fifth_time_interval_xpath)
            driver.execute_script("arguments[0].click();", fifth_time_interval_button)
            print('5-min interval selected')
            
            call_button = driver.find_element_by_xpath(call_xpath)
            driver.execute_script("arguments[0].click();", call_button)
            
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('CALL placed at', current_time)
            print("\n")
            
            f = open(log_file_path, "a")
            f.write('{0} {1}\n'.format("CALL placed at ", current_time))
            
            time.sleep(5)
            
            history_button = driver.find_element_by_xpath(history_button_xpath)
            driver.execute_script("arguments[0].click();", history_button)
            time.sleep(5)

            result_string = driver.find_element_by_xpath(trade_result_xpath).text
            amount_string = driver.find_element_by_xpath(trade_amount_xpath).text
            
            history_close_button = driver.find_element_by_xpath(history_close_xpath)
            driver.execute_script("arguments[0].click();", history_close_button)
            
            result_list = re.findall('[\d]*[.][\d]+',result_string)
            result_value = float(result_list[0])
            
            amount_list = re.findall('[\d]*[.][\d]+',amount_string)
            amount_value = float(amount_list[0])
            
            if result_value > 0:
                investment += amount_value
                result += result_value
            else:
                investment += amount_value
                
            print("Investment:", investment)
            print("Result:", result)
            print("Gain/Loss:",result-investment)
            f.write('{0} {1}\n'.format("Investment:", investment))
            f.write('{0} {1}\n'.format("Result:", result))
            f.write('{0} {1}\n\n'.format("Gain/Loss:", result-investment))
            f.close()
            
            
            # await event.reply('hiU!')
        except:
            f = open(log_file_path, "a")
            if driver.find_element_by_xpath(close_button).size() != 0:
                int_error_close_button = driver.find_element_by_xpath(internal_close_button_xpath)
                driver.execute_script("arguments[0].click();", int_error_close_button)
                print("\nInternal server error occured in Binomo.")
                f.write("\nInternal server error occured in Binomo.\n")
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('Some error occured, page refreshed at', current_time, "\n\n")
            f.write('{0} {1}\n\n'.format('Some error occured, page refreshed at', current_time))
            f.close()
            driver.refresh()  
        
client.start()
client.run_until_disconnected()
