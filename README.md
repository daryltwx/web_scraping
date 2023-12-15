# web_scraping
From 100 days of Python, practicing web scraping skills. 

---

Idea is to practice scraping, then save it into an excel file. 

There are some roughness to the code, but will clean it up as the course continues. 


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

---

To the next project!
