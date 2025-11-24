from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import csv
import os
from datetime import datetime


def get_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless=new")
    driver = Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


#Creating jobs folder 
save_path = "/app/jobs"

if not os.path.exists(save_path):
    os.makedirs(save_path)


url = "https://www.linkedin.com/jobs/search?keywords=&location=Kathmandu&geoId=100665265&distance=25&f_TPR=r86400&position=1&pageNum=0"
driver = get_driver()
driver.get(url)
time.sleep(5) 

#Quiting sign in pop up
button=driver.find_element(By.XPATH,'//*[@id="base-contextual-sign-in-modal"]/div/section/button')
button.click()
time.sleep(3)  

#Initializing empty set to store jobs
jobs_set = set()
scroll_attempts = 0
max_scroll_attempts = 3 # Stopping after 3 failed scrolls

while scroll_attempts < max_scroll_attempts:
    #Scrolling down
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN) 
    
    #Selecting all job cards
    job_cards = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")

    count_before = len(jobs_set)

    for card in job_cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, "h3.base-search-card__title").text.strip()
            company = card.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle").text.strip()
            location = card.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text.strip()
            date_posted = card.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
            try:
                link = card.find_element(By.CSS_SELECTOR, "a.base-card__full-link").get_attribute("href")
            except:
                link="Job Link not available"
                
            jobs_set.add((title, company, location, date_posted,link))
        
        except Exception as e:
                print("Error occured",e)
    
    #Checking if new jobs were found           
    if len(jobs_set) == count_before:
        scroll_attempts += 1
        print(f"No new jobs found. Scroll attempts: {scroll_attempts}/{max_scroll_attempts}")
    else:
        scroll_attempts = 0
        print(f"Total Jobs Found:{len(jobs_set)}")
   
#Saving to csv according to date     
timestamp=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename=f"{save_path}/job_listing_{timestamp}.csv"

try:   
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Date Posted", "Link"])
        
        for title, company, location, date_posted, job_link in jobs_set:
            writer.writerow([title, company, location, date_posted, job_link])
            print(f"Saved: {title} at {company}")
            
except Exception as e:
    print("Error while saving to CSV:", e)
    
        
print(f"\n Saved {len(jobs_set)} jobs to {filename}")


driver.quit()
