from selenium import webdriver
import time

browser = webdriver.Firefox()
browser.get('https://www.pinnacle.com/en/basketball/nba/matchups')

time.sleep(2)

print(browser.page_source)

browser.quit()
