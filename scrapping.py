from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np
import pandas as pd
import re

def scrapping(job, where):
    browser = webdriver.Chrome(executable_path="C:/Users/Utilisateur/Desktop/Selenium/chromedriver/chromedriver.exe")
    
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
    getInfo = {'Job Title': [], 'Name Company': [], 'Location': [], 'Type of contract': [], 'Salary': [], 'Minimum level of education required': [], 'Minimum experience level required': [], 'Spoken languages': []}
        
    #Scrapping    
    while True:
                
        #Fermer popup
#         try:
#             time.sleep(1)
#             browser.find_element_by_class_name('popover-x-button-close').click()    
#         except:
#             pass
        
        #Ouvrir descJob
        nameJob = browser.find_elements_by_class_name('jobsearch-SerpJobCard')
        
        for i in nameJob:
            i.click()
            time.sleep(2)
            
            try:
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
                
#                 try:
#                     getWorkTime = re.match('(\btemps plein\b)|(\btemps partiel\b)', descJob)
#                     getInfo['Work time'].append(getWorkTime)
#                 except NoSuchElementException:
#                     getInfo['Work time'].append('No Info')
                
                descJob = i.find_element_by_xpath("//*[@id='vjs-content']").text
        
                #Contract
                matchContract = re.search(r'\bCDI\b|\bCDD\b|\bAlternance\b|\bStage\b|\bSTAGE\b|\bStage\b', descJob)
                try:
                    getInfo['Type of contract'].append(matchContract.group(0))
                except:
                    getInfo['Type of contract'].append('No Info')
                
                #Salary
#                 matchSalary = re.compile(r"([0-9])")
#                 mo1 = matchSalary.search(descJob)
#                 try:
#                     if mo1:
#                         getInfo['Salary'].append(mo1.group())
#                 except NoSuchElementException:
#                     getInfo['Salary'].append('No Info')
                    
                #Education Level
                matchEduLevel = re.search(r"(\bformation supérieure\b|\bBAC\+5\b|\bBac\+5\b|\bbac\+5\b|\bBac \+ 5\b|\bBac \+ 5 \/ M2\b|\bDiplôme ingénieur\b|\bdiplôme ingénieur\b|\bBAC\+4\b|\bBac\+4\b|\bbac\+4\b|\bBac \+ 4\b|\bMaster 2\b|\bmaster 2\b|\bBAC\+3\b|\bBac\+3\b|\bbac\+3\b|\bBac \+ 3\b|\bgrande école d\'ingénieur\b|\bgrande école d\’ingénieur\b|\bBAC\+4\/5\b|\bBac\+4\/5\b|\bbac\+4\/5\b|\bM2\b|\bCursus ingénieur\b|\bcursus ingénieur\b|\bformation Data Science ou IA\b|\bFormation Data Science ou IA\b|\bformation Data Science\b|\bFormation Data Science\b|\buniversité\b|\buniversitaire\b)", descJob)
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
                
            except:
                print('No more data!')
            
        try:
            nextPage = browser.find_element_by_css_selector("[aria-label='Suivant']")
            nextPage.click()
            time.sleep(3)
        except:
            print("No more pages")
        
             
        job = 'Datascientist'
        df = pd.DataFrame({ key:pd.Series(value) for key, value in getInfo.items() })
        df.to_csv(f'{job}.csv', index=False, encoding='utf-8')
        return df
        
scrapping('"Datascientist"', 'France')