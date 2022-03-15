
from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def div_freq(sentence):
    freq = []

    for i in sentence:
        for a in i:
            freq.append(a)

    a = np.array(freq)
    unique_elements, counts_elements = np.unique(a, return_counts=True)
    return unique_elements, counts_elements


def excel(data1, data2, data3, data4):

    data = pd.DataFrame.from_dict({
        'title': data1[0],
        'title fr': data1[1],
        'content': data2[0],
        'content fr': data2[1],
        'date': data3[0],
        'date fr': data3[1],
        'category': data4[0],
        'category fr': data4[1]
    }, orient='index')

    data.transpose()
    data_to_excel = pd.ExcelWriter("webscrapingexc.xlsx", engine='xlsxwriter')
    data.to_excel(data_to_excel, sheet_name='Sheet1')
    data_to_excel.save()


def plot(data1, data2, data3, data4):
    plt.figure(figsize=(10, 20))
    plt.xlabel('Frequency')
    plt.ylabel('Title')
    plt.barh(data1[0], data1[1])
    plt.show()

    plt.figure(figsize=(10, 20))
    plt.xlabel('Frequency')
    plt.ylabel('Content')
    plt.barh(data2[0], data2[1])
    plt.show()

    plt.xlabel('Frequency')
    plt.ylabel('Category')
    plt.barh(data4[0], data4[1])
    plt.title(data3[0][0])
    plt.show()


path = "C:\\Program Files (x86)\\chromedriver.exe"
driver = webdriver.Chrome(path)
url = "https://www.sozcu.com.tr/"
driver.get(url)
driver.execute_script("window.scrollTo(0, 400)")
title = []
content = []
date = []
category = []

link1 = driver.find_element_by_xpath(f'//*[@id="onetrust-accept-btn-handler"]') # trust accept link
link1.click()

loop = 1
while loop <= 5:


    link = driver.find_element_by_xpath(f'//*[@id="sz_manset"]/div[4]/span[{loop}]')
    link.click()
    control_ad = driver.current_url
    if 'sozcu' in control_ad:

        driver.switch_to.window(driver.window_handles[1])
        Soup = BeautifulSoup(driver.page_source, "html.parser")
        title.append(
            Soup.find("div", {"class": "row mb-4"}).find("div", {"class": "col-lg-8 content mb-4"}).find("h1").text.split())

        content.append(Soup.find("div", {"class": "col-lg-8 content mb-4"}).find("h2").text.split())

        date.append(
            Soup.find("div", {"class": "content-meta-dates"}).find("span").text.split("Yayınlanma:,"))


        category.append(Soup.find("div", {"class": "breadcrumb mb-3 fw-bold d-flex justify-content-between align-items-center"}).text.split("Haberler"))
        del category[loop - 1][0]
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        loop += 1
    else:
        window_after = driver.window_handles[0]
        driver.close()
        driver.switch_to.window(window_after)
        loop += 1

driver.close()

f_title = div_freq(title)

f_content = div_freq(content)

f_date = div_freq(date)

f_category = div_freq(category)

excel(f_title, f_content, f_date, f_category)

plot(f_title, f_content, f_date, f_category)
