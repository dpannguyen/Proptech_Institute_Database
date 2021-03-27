import pandas
import requests
import time
import xlsxwriter
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
"""from selenium.webdriver.chrome.options import Options"""


url = "https://www.unissu.com/proptech-companies"


# initialize webdriver (Chrome)
"""
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options = chrome_options)
"""


# initialize webdriver (Safari)
driver = webdriver.Safari()


driver.implicitly_wait(10)
driver.get(url)
# wait for page to finish loading
driver.find_element_by_css_selector("title")


# close pop-up if necessary
try:
    modal = driver.find_element_by_css_selector("div[class*='modalClose']")
    modal.click()
except NoSuchElementException:
    pass


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
    company = company_link.get_attribute("href")
    companies.append(company)


# create dataframe object to write to excel
keys = ["Name", "Unissu URL", "Tags", "Description", "Website", "Linkedin"]
data = dict.fromkeys(keys, [])
dataframe = pandas.DataFrame(data)
dataframe.to_excel("companies_1000.xlsx", index = False, engine = "xlsxwriter")


# go to each company's unissu profile
# get name, tags, description, website, and linkedin
for i in range(len(companies)):
    unissu_url = companies[i]
    driver.get(unissu_url)
    driver.find_element_by_css_selector(".company-info")

    # get company's tags
    # (accounting for the possibility of multiple tags e.g. Wallabe or no tags)
    tags = ''
    try:
        more_tag = driver.find_element_by_css_selector(".tags-row span[class*='green-tag']")
        more_tag.click()
    except NoSuchElementException:
        pass

    tag_elems = driver.find_elements_by_css_selector(".tags-row span")
    if len(tag_elems) != 0:
        for tag in tag_elems[:-1]:
            tags += tag.text + ", "
        if tag_elems[-1].text != 'Show Less':
            tags += tag_elems[-1].text
        else:
            tags = tags[:-2]

    # get company's name
    name_elem = driver.find_element_by_css_selector(".company-name")
    driver.execute_script("arguments[0].scrollIntoView(true);", name_elem)
    time.sleep(1)
    name = name_elem.text
    
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
    company_data = dict.fromkeys(keys, '')
    company_data["Name"] = name
    company_data["Unissu URL"] = unissu_url
    company_data["Tags"] = tags
    company_data["Description"] = description
    company_data["Website"] = website
    company_data["Linkedin"] = linkedin

    # write to excel
    dataframe = dataframe.append(company_data, ignore_index = True)
    dataframe.to_excel("companies_1000.xlsx", index = False, engine = "xlsxwriter")


driver.close()