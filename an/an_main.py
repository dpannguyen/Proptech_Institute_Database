import re
import requests
import time
from company import Company
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
"""from selenium.webdriver.chrome.options import Options"""


url = "https://www.unissu.com/proptech-companies"


# Chrome Options
"""
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options = chrome_options)
"""


# initialize webdriver
driver = webdriver.Safari()
driver.implicitly_wait(5)

driver.get(url)
# wait for page to finish loading
driver.find_element_by_css_selector("title")

# close pop-up if necessary
try:
    modal = driver.find_element_by_css_selector("div[class*='modalClose']")
    modal.click()
except NoSuchElementException:
    pass

# get total number of companies 
"""
search_result = driver.find_element_by_css_selector(".match-count-container").text
companies_count = int(re.search("[0-9]+", search_result).group())
"""

# load all companies
while True:
    try:
        load_more = driver.find_element_by_css_selector(".loadMoreButton button")
        load_more.click()
    except NoSuchElementException:
        break

# get links of all companies' profiles
companies = []
company_elems = driver.find_elements_by_css_selector(".results-container .company-box a")
for company_link in company_elems:
    company = Company(company_link.get_attribute("href"))
    companies.append(company)

# go to each company's unissu profile
# get name, tags, description, website, and linkedin
for company in companies:
    driver.get(company.get_url())
    driver.find_element_by_css_selector(".company-info")

    # get company's name
    name_elem = driver.find_element_by_css_selector(".company-name")
    driver.execute_script("arguments[0].scrollIntoView(true);", name_elem)
    time.sleep(1)
    name = name_elem.text

    # get company's tags
    # (accounting for the possibility of multiple tags e.g. Wallabe)
    tags = []
    try:
        more_tag = driver.find_element_by_css_selector(".tags-row span[class*='green-tag']")
        more_tag.click()
    except NoSuchElementException:
        pass

    tag_elems = driver.find_elements_by_css_selector(".tags-row span")
    for tag in tag_elems:
        tags.append(tag.text)
    
    # get company's description
    description = driver.find_element_by_css_selector(".description").text
    # get company's website
    website = driver.find_element_by_css_selector("div[class*='websiteLink'] a").get_attribute("href")

    # get company's linkedin 
    # (accounting for the possibility of company not having linkedin profile)
    linkedin = '-'
    try:
        linkedin_link = driver.find_element_by_xpath("//img[@alt='linkedin']/parent::a")
        linkedin = linkedin_link.get_attribute("href")
    except NoSuchElementException:
        pass

    # store all info into company's profile
    company.set_name(name)
    company.set_tags(tags)
    company.set_description(description)
    company.set_website(website)
    company.set_linkedin(linkedin)


# print company's profile info for testing
"""
for company in companies:
    tags = ''
    for tag in company.get_tags():
        tags += tag + " "
    print(company.get_url() + " " + company.get_name() + " " + tags + company.get_description() + " " + company.get_website() + " " + company.get_linkedin() + "\n")
"""

driver.close()