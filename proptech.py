import pandas
import requests
import time
import xlsxwriter
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.chrome.options import Options


# initialize webdriver
driver = webdriver.Safari()
driver.implicitly_wait(10)

"""
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options = chrome_options)
"""


# load unissu main page
def open_main_page():
    url = "https://www.unissu.com/proptech-companies"
    driver.get(url)
    driver.find_element_by_css_selector("title")


# close pop-up if necessary
def close_popup():
    try:
        modal = driver.find_element_by_css_selector("div[class*='modalClose']")
        modal.click()
    except NoSuchElementException:
        pass


# load all companies
def load_companies():
    while True:
        try:
            load_more = driver.find_element_by_css_selector(".loadMoreButton button")
            load_more.click()
        except NoSuchElementException:
            return


# get links of all companies' profiles from main page
def get_companies_links():
    companies = []
    company_elems = driver.find_elements_by_css_selector(".results-container .company-box a")
    for company_link in company_elems:
        company = company_link.get_attribute("href")
        companies.append(company)
    return companies


# load each company's profile
def open_company_profile(unissu_url):
    driver.get(unissu_url)
    driver.find_element_by_css_selector(".company-info")


# get company's name
def get_company_name():
    name_elem = driver.find_element_by_css_selector(".company-name")
    driver.execute_script("arguments[0].scrollIntoView(true);", name_elem)
    time.sleep(1)
    return name_elem.text


# get company's tags
# accounting for the possibility of multiple tags or no tags
def get_company_tags():
    tags = ''
    try:
        more_tag = driver.find_element_by_css_selector(".tags-row span[class*='green-tag']")
        more_tag.click()
        time.sleep(1)
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
    return tags


# get company's description
def get_company_description():
    return driver.find_element_by_css_selector(".description").text


# get company's website
def get_company_website():
    return driver.find_element_by_css_selector("div[class*='websiteLink'] a").get_attribute("href")


# get company's linkedin 
# accounting for the possibility of company not having linkedin profile
def get_company_linkedin():
    linkedin = '-'
    try:
        linkedin_link = driver.find_element_by_xpath("//img[@alt='linkedin']/parent::a")
        linkedin = linkedin_link.get_attribute("href")
    except NoSuchElementException:
        pass
    return linkedin


# go to each company's unissu profile
# get name, tags, description, website, and linkedin
def get_companies_information():
    companies = get_companies_links()

    # create dataframe object to write to excel
    keys = ["Name", "Unissu URL", "Tags", "Description", "Website", "Linkedin"]
    data = dict.fromkeys(keys, [])
    dataframe = pandas.DataFrame(data)
    dataframe.to_excel("companies.xlsx", index = False, engine = "xlsxwriter")

    # get company's information from company's profile
    for company in companies:
        unissu_url = company
        open_company_profile(unissu_url)

        tags = get_company_tags()
        name = get_company_name()
        description = get_company_description()
        website = get_company_website()
        linkedin = get_company_linkedin()

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
        dataframe.to_excel("companies.xlsx", index = False, engine = "xlsxwriter")


if __name__ == "__main__":
    open_main_page()
    close_popup()
    load_companies()
    get_companies_information()
    driver.close()

