# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:51:16 2020

@author: yangg
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

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

    from webdriver_manager.chrome import ChromeDriverManager

    driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver = webdriver.Chrome()
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

        try:
            time.sleep(0.5)

            where = driver.find_element_by_id('where')
            time.sleep(0.2)
            # driver.find_element_by_id('text-input-where').click()

            while len(where.get_attribute('value')) != 0:
                where.send_keys(Keys.BACKSPACE)

            driver.find_element_by_id('where').send_keys(country)
            bouton = driver.find_element_by_id('fj')
            bouton.click()
        except:
            pass
    except:
        pass

    # Les listes vides pour chaque feature
    data = pd.DataFrame({'Poste': [], 'Métier': [], 'Pays': [], 'Ville': [
    ], 'Entreprise': [], 'Contrat': [], 'Salaire': [], 'Description': []})

    page = True

    while page:

        # Au cas où y a un pop up
        try:
            time.sleep(0.5)
            driver.find_element_by_class_name('popover-x-button-close').click()
        except:
            pass

        #jobcards = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, 'jobsearch-SerpJobCard')))

        # Trouver la carte de chaque job
        jobcards = driver.find_elements_by_class_name('jobsearch-SerpJobCard')

        # Function récurrente pour scrapping les données
        for job in jobcards:
            job.click()
            time.sleep(0.2)

            job_name = jobName.replace('"', '')

            # Les noms des posts proposés
            try:
                title = job.find_element_by_class_name(
                    'title').text.replace('\n', '')
            except NoSuchElementException:
                title = None

                # Les nom d'entreprise
            try:
                entreprise = job.find_element_by_class_name('company').text
            except NoSuchElementException:
                entreprise = None

                # Les localisations des entreprises
            try:
                ville = job.find_element_by_class_name('location').text
            except NoSuchElementException:
                ville = None

                # Les types de contrat des postes
            try:
                contrat = driver.find_element_by_css_selector(
                    ".jobMetadataHeader-itemWithIcon-icon-jobs + span").text
            except:
                contrat = None

                # Les salaires des postes recrutées
            try:
                salaire = job.find_element_by_class_name("salaryText").text
            except NoSuchElementException:
                salaire = None

                # Les descriptions des postes
            try:
                element = WebDriverWait(driver, 420).until(
                    EC.presence_of_element_located((By.ID, "vjs-content")))
                description = element.text.replace('\n', ' ')
            except TimeoutException:
                description = None

            data = pd.concat([data, pd.DataFrame({'Poste': title, 'Métier': job_name, 'Pays': country, 'Ville': ville, 'Entreprise': entreprise,
                                                  'Contrat': contrat,  'Salaire': salaire, 'Description': description}, index=[0])], ignore_index=True)

        try:
            element = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Suivant'] | //a[@aria-label='Next'] | span[contains(text(),'Suivant')] | span[contains(text(),'Next')]")))
            element.click()
        except TimeoutException:
            page = False

    filename = str.lower(jobName.replace(' ', '').replace(
        '"', '') + country) + ".csv".replace(' ', '')

    data.to_csv(filename, index=False, sep=';', encoding="utf-8-sig")

    print("Traitement de fichier " + filename + " fini")
    driver.quit()


def main():
    jobs = ['"Data scientist"', '"Python"', '"Javascript"', '"Java"',
            '"Data scientist"', '"Python"', '"Javascript"', '"Java"']
    countrys = ['France', 'France', 'France',
                'France', 'USA', 'USA', 'USA', 'USA']

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(searchJob, jobs, countrys)

    #searchJob('"Java"',  'USA')


if __name__ == '__main__':
    main()
