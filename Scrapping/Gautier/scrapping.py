from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np
import pandas as pd
import re

def scrapping(job, where):
#     browser = webdriver.Chrome(executable_path="chromedriver/chromedriver.exe")

    browser = webdriver.Firefox(executable_path="geckodriver/geckodriver.exe")

    browser.get('https://www.indeed.fr/')
    browser.maximize_window()
    
    #Search name Job
    searchInput = browser.find_element_by_class_name('icl-TextInput-control')
    searchInput.send_keys(job)
    #Search Where
    searchInputWhere = browser.find_element_by_id('text-input-where')
    while len(searchInputWhere.get_attribute('value')) != 0:
        searchInputWhere.send_keys(Keys.BACKSPACE)
    searchInputWhere.send_keys(where)
    #Click search
    clickSearch = browser.find_element_by_class_name('icl-Button')
    clickSearch.click()
    
    #Dict
    getInfo = {'Job Title': [], 'Name Company': [], 'Location': [], 'Work time': [], 'Type of contract': [], 'Salary': [], 'Desired skills': [], 'Minimum level of education required': [], 'Minimum experience level required': [], 'Spoken languages': []}
    nameJob = browser.find_elements_by_class_name('jobsearch-SerpJobCard')
    
    #Scrapping    
    while True:
        
        #Ouvrir descJob
        for i in nameJob:
            i.click()
            time.sleep(2)
            
            try:
                getInfo['Job Title'].append(i.find_element_by_class_name('title').text)
            except NoSuchElementException:
                getInfo['Job Title'].append('No Info')

            try:
                getInfo['Name Company'].append(i.find_element_by_class_name('company').text)
            except NoSuchElementException:
                getInfo['Name Company'].append('No Info')

            try:
                getInfo['Location'].append(i.find_element_by_class_name('location').text)
            except NoSuchElementException:
                getInfo['Location'].append('No Info')

            descJob = i.find_element_by_xpath("//*[@id='vjs-content']").text
            
            #Work time
            matchWorkTime = re.search(r'\bTemps plein\b|\bTemps partiel\b', descJob)
            try:
                getInfo['Work time'].append(matchWorkTime.group())
            except:
                getInfo['Work time'].append('No Info')

            #Contract
            matchContract = re.search(r'\bCDI\b|\bCDD\b|\bApprentissage\b|\bApprentissage, Contrat pro\b|\bStage\b|\bSTAGE\b|\bStage\b|\bIntérim\b|\bFreelance\b|\bIndépendant\b|\bFreelance \/ Indépendant\b', descJob)
            try:
                getInfo['Type of contract'].append(matchContract.group(0))
            except:
                getInfo['Type of contract'].append('No Info')

            #Salary
            matchSalary = re.search(r"\b(?:\d[ - ]*?){3,5}( € \- )(?:\d[ - ]*?){3,5}( € par jour)\b|\b(?:\d[ - ]*?){3,5}( € \- )(?:\d[ - ]*?){3,5}( € par mois)\b|\b(?:\d[ - ]*?){3,5}( € \- )(?:\d[ - ]*?){3,5}( € par an)\b|\b(?:\d[ - ]*?){3,5}(€ par jour)\b|\b(?:\d[ - ]*?){3,5}( € par jour)\b|\b(?:\d[ - ]*?){3,5}(€ par mois)\b|\b(?:\d[ - ]*?){3,5}( € par mois)\b|\b(?:\d[ - ]*?){3,5}( € par an)\b|\b(?:\d[ - ]*?){3,5}(€ par an)\b", descJob)
            try:
                getInfo['Salary'].append(matchSalary.group(0))
            except:
                getInfo['Salary'].append('No Info')

            #Skills
            matchSkills = re.findall(r'\bPython\b|\bpython\b|\bPYTHON\b|\bR\b|\bSQL\b|\bNoSQL\b|\bGIT\b|\bSpark\b|\bspark\b|\bflask\b|\bFlask\b|\bstreamlit\b|\bStreamlit\b|\bDocker\b|\bdocker\b|\bKubernetes\b|\bkubernetes\b|\bReactJS\b|\bMachine Learning\b|\bDeep Learning\b|\bNLP\b|\bVueJS\b|\bAngularJS\b|\bScala\b|\bscala\b|\bPySpark\b|\bPyspark\b|\bPowerBI\b|\bSQLSERVER\b|\bSQLServer\b|\bDataiku\b|\bdataiku\b|\bKeras\b|\bkeras\b|\btensorflow\b|\bTensorFlow\b|\bTensorflow\b|\bNLU\b|\bPytorch\b|\bpytorch\b|\bPyTorch\b|\bScikitLearn\b|\bscikitlearn\b|\bScikitlearn\b|\bScikit-Learn\b|\bScikit-learn\b|\bSAS\b|\bJava\b|\bjava\b|\bScikit learn\b|\bhadoop\b|\bHadoop\b|\bhive\b|\bHive\b|\bML\/DL\b|\bAzure\b|\bAWS\b', descJob)
            matchSkills = list(dict.fromkeys(matchSkills)) #Supprimer les doublons
            try:
                getInfo['Desired skills'].append(matchSkills)
            except:
                getInfo['Desired skills'].append('No Info')
            
            #Education Level
            matchEduLevel = re.search(r"(\bformation supérieure\b|\bBAC\+5\b|\bBac\+5\b|\bbac\+5\b|\bBac \+ 5\b|\bBac \+ 5 \/ M2\b|\bDiplôme ingénieur\b|\bdiplôme ingénieur\b|\bBAC\+4\b|\bBac\+4\b|\bbac\+4\b|\bBac \+ 4\b|\bMaster 2\b|\bmaster 2\b|\bBAC\+3\b|\bBac\+3\b|\bbac\+3\b|\bBac \+ 3\b|\bgrande école d\'ingénieur\b|\bgrande école d\’ingénieur\b|\bBAC\+4\/5\b|\bBac\+4\/5\b|\bbac\+4\/5\b|\bM2\b|\bCursus ingénieur\b|\bcursus ingénieur\b|\bformation Data Science ou IA\b|\bFormation Data Science ou IA\b|\bformation Data Science\b|\bFormation Data Science\b|\buniversité\b|\bUniversité\b|\bUniversitaire\b|\buniversitaire\b)", descJob)
            try:
                getInfo['Minimum level of education required'].append(matchEduLevel.group(0))
            except:
                getInfo['Minimum level of education required'].append('No Info')

            #Experience Level
            matchExpLevel = re.search(r"(\b0 \- 2 ans\b|\b1 an\b|\b1 ou 2 ans\b|\b2 ans\b|\b2\/3 ans\b|\b3 \- 5 ans\b|\b3 ans\b|\b4 ans\b|\b5 ans\b)", descJob)
            try:
                getInfo['Minimum experience level required'].append(matchExpLevel.group(0))
            except:
                getInfo['Minimum experience level required'].append('No Info')

            #Spoken Languages
            matchSpokenLang = re.search(r"(\bAnglais\b|\bChinois\b|\bArabe\b|\bEspagnol\b|\bItalien\b)", descJob)
            try:
                getInfo['Spoken languages'].append(matchSpokenLang.group(0))
            except:
                getInfo['Spoken languages'].append('No Info')
            
#         try:
#             nextPage = browser.find_element_by_css_selector("[aria-label='Suivant']")
#             nextPage.click()
#             time.sleep(3)
#             #Fermer popup
#             time.sleep(2)
#             browser.find_element_by_class_name('popover-x-button-close').click()
#         except:
#             print("No more pages")
                
        job = 'Datascientist'
        df = pd.DataFrame({ key:pd.Series(value) for key, value in getInfo.items() })
        df.to_csv(f'{job}.csv', index=False, encoding='utf-8')
        return df
        
scrapping('"Datascientist"', 'France')