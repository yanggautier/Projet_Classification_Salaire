# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:51:16 2020

@author: yangg
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import concurrent.futures
import pandas as pd
#import re


def searchJob(jobName, country):

    # option = webdriver.ChromeOptions()
    # option.add_argument("--incognito")

    driver = webdriver.Chrome()
    driver.get('https://www.indeed.fr')
    driver.maximize_window()

    searchInputwhat = driver.find_element_by_id('text-input-what')
    searchInputwhat.send_keys(jobName)
    # jobsearch-SerpJobCard
    time.sleep(0.2)
    searchInputwhere = driver.find_element_by_id('text-input-where')
    time.sleep(0.2)
    # driver.find_element_by_id('text-input-where').click()

    while len(searchInputwhere.get_attribute('value')) != 0:
        searchInputwhere.send_keys(Keys.BACKSPACE)

    driver.find_element_by_id('text-input-where').send_keys(country)
    # searchInputwhere.send_keys('France')

    bouton_search = driver.find_element_by_class_name('icl-Button')
    bouton_search.click()

    try:
        time.sleep(0.3)
        driver.find_element_by_class_name('popover-x-button-close').click()
    except:
        pass

    try:
        change_country = driver.find_element_by_xpath(
            "//div[@class='invalid_location']/p/a")
        change_country.click()
    except:
        pass

    # Les listes vides pour chaque feature
    getInfo = {'Job Title': [], 'Country': [], 'Name Company': [], 'Location': [], 'Type of contract': [],
               'Salary': [], 'Description': []}

    # getInfo = {'Job Title': [], 'Country': [], 'Name Company': [], 'Location': [], 'Work time': [], 'Type of contract': [],
    #          'Salary': [],
    #          'Python': [], 'R': [], 'SQL': [], 'NoSQL': [], 'GIT': [], 'Spark': [], 'Flask': [], 'Streamlit': [], 'Docker': [], 'Kubernetes': [],
    #          'React': [], 'VueJS': [], 'AngularJS': [],
    #         'Machine Learning': [], 'Deep Learning': [], 'NLP': [],  'Scala': [], 'PySpark': [],
    #          'PowerBI': [], 'SQLServer': [], 'Dataiku': [], 'Keras': [], 'TensorFlow': [], 'NLU': [],
    #         'PyTorch': [], 'ScikitLearn': [], 'Scikit-Learn': [], 'SAS': [],
    #          'Java': [], 'Scikit learn': [], 'Hadoop': [],  'Hive': [], 'ML DL': [], 'Azure': [], 'AWS': [],
    #          'Minimum level of education required': [],
    #         'Minimum experience level required': [], 'Spoken languages': []}

    # skills = ['Python', 'R', 'SQL', 'NoSQL', 'GIT', 'Spark', 'Flask', 'Streamlit', 'Docker', 'docker', 'Kubernetes', 'ReactJS', 'Machine Learning', 'Deep Learning', 'NLP', 'VueJS', 'AngularJS', 'Scala', 'PySpark',
    #          'PowerBI', 'SQLServer', 'Dataiku', 'Keras', 'TensorFlow', 'NLU', 'Pytorch', 'PyTorch', 'ScikitLearn', 'Scikit-Learn', 'SAS', 'Java', 'java', 'Scikit learn', 'Hadoop', 'hive', 'Hive', 'ML DL', 'Azure', 'AWS']

    page = True

    while page:

        # Au cas où y a un pop up
        try:
            time.sleep(0.5)
            driver.find_element_by_class_name('popover-x-button-close').click()
        except:
            pass

        # Trouver la carte de chaque job
        jobcards = driver.find_elements_by_class_name('jobsearch-SerpJobCard')

        # Function récurrente pour scrapping les données
        for job in jobcards:
            job.click()
            time.sleep(0.2)

            # Les noms des posts proposés
            try:
                getInfo['Job Title'].append(
                    job.find_element_by_class_name('title').text.replace('\n', ''))
                getInfo['Country'].append(country)
            except NoSuchElementException:
                getInfo['Job Title'].append("None")
                getInfo['Country'].append(country)

                # Les nom d'entreprise
            try:
                getInfo['Name Company'].append(
                    job.find_element_by_class_name('company').text)
            except NoSuchElementException:
                getInfo['Name Company'].append("None")

                # Les localisations des entreprises
            try:
                getInfo['Location'].append(
                    job.find_element_by_class_name('location').text)
            except NoSuchElementException:
                getInfo['Location'].append("None")

                # Les types de contrat des postes
            try:
                contrat = driver.find_element_by_css_selector(
                    ".jobMetadataHeader-itemWithIcon-icon-jobs + span").text
                getInfo['Type of contract'].append(contrat)
            except:
                getInfo['Type of contract'].append("None")

                # Les salaires des postes recrutées
            try:
                salary = job.find_element_by_class_name("salaryText").text
                getInfo['Salary'].append(salary)
            except NoSuchElementException:
                getInfo['Salary'].append("None")

                # Les descriptions des postes
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "vjs-desc")))
                description = element.text.replace('\n', ' ')
                getInfo['Description'].append(description)
            except TimeoutException:
                getInfo['Description'].append("None")

        try:
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Suivant'] | //a[@aria-label='Next'] | span[contains(text(),'Suivant')] | span[contains(text(),'Next')]")))
            element.click()
        except TimeoutException:
            page = False

    filename = str.lower(jobName.replace(' ', '').replace(
        '"', '') + country) + ".csv".replace(' ', '')
    df = pd.DataFrame(getInfo)

    df.to_csv(filename, index=False, sep=';', encoding="utf-8-sig")

    print(filename + "complete")
    driver.quit()


def main():
    jobs = ['"Data scientist"', '"Python"', '"Javascript"', '"Java"',
            '"Data scientist"', '"Python"', '"Javascript"', '"Java"']
    countrys = ['France', 'France', 'France',
                'France', 'USA', 'USA', 'USA', 'USA']

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(searchJob, jobs, countrys)
    #searchJob('"Data scientist"',  'France')


if __name__ == '__main__':
    main()
