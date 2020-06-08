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
import re


def searchJob(jobName, country):

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
    getInfo = {'Job Title': [], 'Country': [], 'Name Company': [], 'Location': [], 'Work time': [], 'Type of contract': [],
               'Salary': [],
               'Python': [], 'R': [], 'SQL': [], 'NoSQL': [], 'GIT': [], 'Spark': [], 'Flask': [], 'Streamlit': [], 'Docker': [], 'Kubernetes': [],
               'React': [], 'VueJS': [], 'AngularJS': [],
               'Machine Learning': [], 'Deep Learning': [], 'NLP': [],  'Scala': [], 'PySpark': [],
               'PowerBI': [], 'SQLServer': [], 'Dataiku': [], 'Keras': [], 'TensorFlow': [], 'NLU': [],
               'PyTorch': [], 'ScikitLearn': [], 'Scikit-Learn': [], 'SAS': [],
               'Java': [], 'Scikit learn': [], 'Hadoop': [],  'Hive': [], 'ML DL': [], 'Azure': [], 'AWS': [],
               'Minimum level of education required': [],
               'Minimum experience level required': [], 'Spoken languages': []}

    skills = ['Python', 'R', 'SQL', 'NoSQL', 'GIT', 'Spark', 'Flask', 'Streamlit', 'Docker', 'docker', 'Kubernetes', 'ReactJS', 'Machine Learning', 'Deep Learning', 'NLP', 'VueJS', 'AngularJS', 'Scala', 'PySpark',
              'PowerBI', 'SQLServer', 'Dataiku', 'Keras', 'TensorFlow', 'NLU', 'Pytorch', 'PyTorch', 'ScikitLearn', 'Scikit-Learn', 'SAS', 'Java', 'java', 'Scikit learn', 'Hadoop', 'hive', 'Hive', 'ML DL', 'Azure', 'AWS']

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
            # try:
            #    contrat = driver.find_element_by_css_selector(".jobMetadataHeader-itemWithIcon-icon-jobs + span").text
            #    getInfo['Type de contrat'].append(contrat)
            # except:
            #    getInfo['Type de contrat'].append("None")

                # Les salaires des postes recrutées
            # try:
            #    salary = job.find_element_by_class_name("salaryText").text
            #    getInfo['Salaire'].append(salary)
            # except NoSuchElementException:
            #    getInfo['Salaire'].append("None")

                # Les descriptions des postes
            # try:
            #    element = WebDriverWait(driver, 10).until(
            #        EC.presence_of_element_located((By.ID, "vjs-desc")))
            #    description = element.text.replace('\n', ' ')
            #   getInfo['Description'].append(description)
            # except TimeoutException:
            #    getInfo['Description'].append("None")

            try:
                desc = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,
                                                                                       "//*[@id='vjs-content']")))
                descJob = desc.text
            except TimeoutException:
                break

            # Work time
            matchWorkTime = re.search(
                r'\bTemps plein\b|\bTemps partiel\b', descJob)
            try:
                getInfo['Work time'].append(matchWorkTime.group())
            except:
                getInfo['Work time'].append('No Info')

            # Contract
            matchContract = re.search(
                r'\bCDI\b|\bCDD\b|\bApprentissage\b|\bApprentissage, Contrat pro\b|\bStage\b|\bSTAGE\b|\bStage\b|\bIntérim\b|\bFreelance\b|\bIndépendant\b|\bFreelance \/ Indépendant\b',
                descJob)
            try:
                getInfo['Type of contract'].append(matchContract.group(0))
            except:
                getInfo['Type of contract'].append('No Info')

            # Salary
            matchSalary = re.search(
                r"\b(?:\d[ - ]*?){3,5}( € \- )(?:\d[ - ]*?){3,5}( € par jour)\b|\b(?:\d[ - ]*?){3,5}( € \- )(?:\d[ - ]*?){3,5}( € par mois)\b|\b(?:\d[ - ]*?){3,5}( € \- )(?:\d[ - ]*?){3,5}( € par an)\b|\b(?:\d[ - ]*?){3,5}(€ par jour)\b|\b(?:\d[ - ]*?){3,5}( € par jour)\b|\b(?:\d[ - ]*?){3,5}(€ par mois)\b|\b(?:\d[ - ]*?){3,5}( € par mois)\b|\b(?:\d[ - ]*?){3,5}( € par an)\b|\b(?:\d[ - ]*?){3,5}(€ par an)\b",
                descJob)
            try:
                getInfo['Salary'].append(matchSalary.group(0))
            except:
                getInfo['Salary'].append('No Info')

            # Skills
            matchSkills = re.findall(
                r'\bPython\b|\bpython\b|\bPYTHON\b|\bR\b|\bSQL\b|\bNoSQL\b|\bGIT\b|\bSpark\b|\bspark\b|\bflask\b|\bFlask\b|\bstreamlit\b|\bStreamlit\b|\bDocker\b|\bdocker\b|\bKubernetes\b|\bkubernetes\b|\bReactJS\b|\bMachine Learning\b|\bDeep Learning\b|\bNLP\b|\bVueJS\b|\bAngularJS\b|\bScala\b|\bscala\b|\bPySpark\b|\bPyspark\b|\bPowerBI\b|\bSQLSERVER\b|\bSQLServer\b|\bDataiku\b|\bdataiku\b|\bKeras\b|\bkeras\b|\btensorflow\b|\bTensorFlow\b|\bTensorflow\b|\bNLU\b|\bPytorch\b|\bpytorch\b|\bPyTorch\b|\bScikitLearn\b|\bscikitlearn\b|\bScikitlearn\b|\bScikit-Learn\b|\bScikit-learn\b|\bSAS\b|\bJava\b|\bjava\b|\bScikit learn\b|\bhadoop\b|\bHadoop\b|\bhive\b|\bHive\b|\bML\/DL\b|\bAzure\b|\bAWS\b',
                descJob)
            matchSkills = list(dict.fromkeys(matchSkills)
                               )  # Supprimer les doublons
            for skill in skills:
                if re.match(str.lower(skill), str.lower(descJob)):
                    getInfo[skill] = 1
                else:
                    getInfo[skill] = 0

            try:
                getInfo['Desired skills'].append(matchSkills)
            except:
                getInfo['Desired skills'].append('No Info')

            # Education Level
            matchEduLevel = re.search(
                r"(\bformation supérieure\b|\bBAC\+5\b|\bBac\+5\b|\bbac\+5\b|\bBac \+ 5\b|\bBac \+ 5 \/ M2\b|\bDiplôme ingénieur\b|\bdiplôme ingénieur\b|\bBAC\+4\b|\bBac\+4\b|\bbac\+4\b|\bBac \+ 4\b|\bMaster 2\b|\bmaster 2\b|\bBAC\+3\b|\bBac\+3\b|\bbac\+3\b|\bBac \+ 3\b|\bgrande école d\'ingénieur\b|\bgrande école d\’ingénieur\b|\bBAC\+4\/5\b|\bBac\+4\/5\b|\bbac\+4\/5\b|\bM2\b|\bCursus ingénieur\b|\bcursus ingénieur\b|\bformation Data Science ou IA\b|\bFormation Data Science ou IA\b|\bformation Data Science\b|\bFormation Data Science\b|\buniversité\b|\bUniversité\b|\bUniversitaire\b|\buniversitaire\b)",
                descJob)
            try:
                getInfo['Minimum level of education required'].append(
                    matchEduLevel.group(0))
            except:
                getInfo['Minimum level of education required'].append(
                    'No Info')

            # Experience Level
            matchExpLevel = re.search(
                r"(\b0 \- 2 ans\b|\b1 an\b|\b1 ou 2 ans\b|\b2 ans\b|\b2\/3 ans\b|\b3 \- 5 ans\b|\b3 ans\b|\b4 ans\b|\b5 ans\b)",
                descJob)
            try:
                getInfo['Minimum experience level required'].append(
                    matchExpLevel.group(0))
            except:
                getInfo['Minimum experience level required'].append('No Info')

            # Spoken Languages
            matchSpokenLang = re.search(
                r"(\bAnglais\b|\bChinois\b|\bArabe\b|\bEspagnol\b|\bItalien\b)", descJob)
            try:
                getInfo['Spoken languages'].append(matchSpokenLang.group(0))
            except:
                getInfo['Spoken languages'].append('No Info')

        try:
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//a[@aria-label='Suivant'] | //a[@aria-label='Next'] | a[contains(text(),'Suivant')] | a[contains(text(),'Next')]")))
            element.click()
        except TimeoutException:
            page = False

    filename = str.lower(jobName.replace(' ', '') +
                         country) + ".csv".replace(' ', '')
    df = pd.DataFrame(getInfo)
    df.to_csv(filename, index=False, sep=';', encoding="utf-8-sig")
    print(filename + "complete")
    driver.quit()


def main():
    jobs = ['"Data scientist"', '"Python"', '"Javascript"', '"Java"',
            '"Data scientist"', '"Python"', '"Javascript"', '"Java"']
    countrys = ['France', 'France', 'France',
                'France', 'USA', 'USA', 'USA', 'USA']
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #    executor.map(searchJob, jobs, countrys)
    searchJob('"Data scientist"',  'France')


if __name__ == '__main__':
    main()
