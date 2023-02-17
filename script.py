from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import re

url = "https://totallyhistory.com/biography/famous-african-americans/"
driver = webdriver.Chrome()

with open('data.csv','w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Date", "Nationality", "Summary", "Description"])
    driver.get(url)

    links = driver.find_elements(by=By.CSS_SELECTOR, value="li>a")
    links = [l.get_attribute('href') for l in links][3:]
    # get links
    for l in links:
        # get name
        fulltext = driver.find_elements(by=By.CSS_SELECTOR, value="td.textpart")
        for t in fulltext:
            t = t.text
            name = re.search('^[^(]+', t)
            dates = re.search('\(([^)]+)', t)
            nationality = re.search('(?<=Nationality: )(\w+)', t)
            rst = t.splitlines()
            summary = re.sub(r"Known [F|f]or:","", rst[-2])
            desc = rst[-1]
            if not nationality:
                nationality = "Not found"
            else:
                nationality = nationality.group(1).strip()
            if not dates:
                dates = "Not found"
            else:
                dates = dates.group(1)
            row = [name.group(0), dates, nationality, summary, desc]
            writer.writerow(row)
            print(row)
        driver.get(l)
        driver.implicitly_wait(1)

    driver.quit()