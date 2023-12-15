"""
Version: v1.0.5

Description: 1. Start new driver, Load website.
             2. Scrape page 1, add to list. Go next page (Repeat till no next page).
             3. Start new driver, Load individual url from list.
             4. Scrape ID & Job Description. 
             5. Save all into CSV. 

Note: 
        Somewhat works. Manage to get listings. 
        One job description did not appear - html class looks the same, may be due to loading issues (requires testing). 
        IDs with 'E' within str will have formatting error in .csv (eg. 2.30007E+13 = 230007E8)
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import datetime
import time

current_date = datetime.date.today()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


## Change website. (Only applicable to careers.ti.com websites.)
# Demo site: 56 items
website = "https://careers.ti.com/search-jobs/?location=United%20States&country=US"



driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

# Get items from page 1
time.sleep(1)
# Get live results
live_results = driver.find_element(By.ID, value="live-results")
live_result = live_results.text
num, live, results = live_result.split(" ")
num = int(num)
print(f"Total of {num} live results from input site.")



####
collected_results = 0
job_titles_list =[]
links_list = []
locations_list = []
posdates_list = []
job_id_list = []
job_description_list = []


# Go next page and continue scraping
current_page_number = 1
while True:
    try:
        time.sleep(2)        
        # Get job_titles
        job_titles = driver.find_elements(By.CLASS_NAME, value="jobTitle")
        for title in job_titles:
            job_titles_list.append(title.text)

        # Get links for job_titles
        links = driver.find_elements(By.CSS_SELECTOR, value="div .jobTitle a")
        for link in links:
            links_list.append(link.get_attribute("href"))

        # Get Locations 
        locations = driver.find_elements(By.CLASS_NAME, value="joblist-location")
        for location in locations:
            locations_list.append(location.text)

        # Get Date_posted
        posdates = driver.find_elements(By.CLASS_NAME, value="joblist-posdate")
        for posdate in posdates:
            posdates_list.append(posdate.text)
            
        print(f"Scrape items: {len(link_list)}")
        
        
        

        
        # Go to next page
        current_page_number += 1
        next_page = driver.find_element(By.CSS_SELECTOR, value=f"#pagination{current_page_number}")
        next_page.click()
        print(f"To next page {current_page_number}")
    except(TimeoutException, WebDriverException) as e:
        driver.close()
        print("Last page reached. First driver closed.")
        
        print("Starting individual listing scrape..")
        
        # Get Job_Description using link_list.
        num_url = len(links_list)
        current_url = 1

        for url in links_list:  
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)

            # Get items from page 1
            time.sleep(1)

            
            # Scrap id
            ids = driver.find_elements(By.CSS_SELECTOR, value="div .fusion-text-1 p")
            for id in ids:     
                job_id_list.append(id.text)

            # Scrap whole chunk of jd
            jds = driver.find_elements(By.CLASS_NAME, value="jd-description")
            job_desc = []
            for jd in jds:
                job_desc.append(jd.text)

            job_description_list.append(job_desc)
            
            print(f"Scrape {current_url} of {num_url}")
            current_url += 1
            driver.close()
            
        print("End individual listing scrape.")
        break



# Merge list to write into csv
print("Saving to csv..")
listing = zip(job_id_list, job_titles_list, links_list, locations_list, posdates_list, job_description_list)
with open(f"[{current_date}]_careers_TI.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Job ID", "Job Title", "URL", "Location", "Posting Date", "Job Description"])
    for list in listing:
        writer.writerow(list)
        
print("Saved.")





print("Finish Running")
