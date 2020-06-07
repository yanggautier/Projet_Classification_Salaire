import pandas as pd
import re
import numpy as np

jobs = ['Data scientist', 'Python', 'Javascript', 'Java',
        'Data scientist', 'Python', 'Javascript', 'Java']
countrys = ['France', 'France', 'France', 'France', 'USA', 'USA', 'USA', 'USA']

# Les mots clés des compétences

skills = {'Python': ['Python', 'python'],
          'R': ['"R"', 'langage R', 'R/' '/R', 'R studio', 'RStudio'],
          'Matlab': ['MATLAB'],
          'Kubernetes': ['Kubernetes'],
          'Bash': ['Bash'],
          'Fortran': ['FORTRAN'],
          'Ruby': ['Ruby'],
          'Golang': ['Golang'],
          'C': ['C++', 'C#'],
          'Java': ['Java'],
          'JEE': ['JEE', 'J2EE'],
          'JSP': ['JSP'],
          'J2ME': ['J2ME'],
          'BREW': ['BREW'],
          'MVC': ['MVC'],
          'SASS': ['Sass'],
          'XML': ['XML'],
          'Eclipse': ['Eclipse'],
          'Spring': ['Spring'],
          'Atlassian': ['Atlassian'],
          'Jenkin': ['Jenkin'],
          'FIX': ['Fix'],
          'Nexus': ['Nexus'],
          'Maven': ['Maven'],
          'Flutter': ['Flutter'],
          'Bootstrap': ['Bootstrap'],
          'Kafka': ['Kafka'],
          'Data software': ['Stata', 'PowerBI', 'Gis', 'EMR', 'RDS', 'S3', 'Athena'],
          'Data analysis': ['analyze', 'analysis', 'analyzing', 'analyst', 'analyser', 'analytics'],
          'Data preprocessing': ['Clearn', 'Prepare', 'Preprocessing', 'gestion de données', 'Traitement',
                                 'Data mining'],
          'Report': ['Report', 'Presentation'],
          'Math': ['Math'],
          'Development': ['Développement', 'Development'],
          'Integration': ['intégration', 'integration'],
          'ReactNative': ['React Native', 'ReactNative'],
          'Dataiku': ['Dataiku', 'Data Iku'],
          'Data viz': ['Seaborn', 'Matplotlib', 'Plotly', 'visualization', 'ggplot2', 'visual', 'viz'],
          'Data skills': ['Numpy', 'Pandas'],
          'Data pipeline': ['pipeline'],
          'Git': ['Github', 'Git', 'Gitlab', 'BitBucket'],
          'SQL': ['SQL', 'NoSQL', 'BigQuery', 'Oracle'],
          'Djanbo': ['Djanbo'],
          'Database': ['MongoDB', 'SGBD', 'MySQL', 'MariaDB', 'Hive', 'HBase', 'BDD', 'base de donnée',
                       'bases de données'],
          'Javascrpit': ['Javascript'],
          'POO': ['Orientée Objet', 'POO', 'OOP', 'Object Oriented', 'OO', 'object-oriented', 'Object Oriented'],
          'Regex': ['regex', 'pattern'],
          'Mobile Programming': ['Swift', 'Kotlin', 'Android', 'Androïd', 'mobile'],
          'Team Work': ['team', 'Agile', 'équipe', 'equipe'],
          'Machine Learning': ['Machine-Learning', 'IA', 'AI', 'Machine Learning', 'Machine learning', 'ML', ' Scikit',
                               'scikit', 'Artificial intelligence'],
          'Web langage': ['CSS', 'HTML'],
          'System unix': ['Linux', 'GNU', 'Unix'],
          'Scratch': ['Scratch'],
          'Scala': ['Scala'],
          'API': ['API'],
          'RestAPI': ['REST', 'JSon'],
          '.Net': ['.Net'],
          'Kafka': ['Kafka'],
          'Visual Studio': ['Visual Studio'],
          'Responsive': ['Responsive'],
          'Javascript Skills': ['Webpack', 'JQuery', 'AJAX', 'React', 'Angular', 'Vue', 'Node', 'full stack', 'npm'],
          'Outil bureautique': ['Excel', 'Office'],
          'Deep Learning': ['Deep Learning', 'DL', 'Deep-Learning', 'Deep-learning', 'Sequential', 'TensorFlow',
                            'PyTorch', 'Caffe', 'Keras', 'Tensor Flow'],
          'Text analytics': ['NLP', 'Natural Language Processing', 'Text Analytics', 'Text mining'],
          'Marketing': ['Marketing', 'Pricing', 'prix', 'publicitaires', 'vente', 'cible', 'ciblage'],
          'Finance': ['Insurance', 'Finance', 'Economic'],
          'Communication': ['Communic'],
          'Statistics': ['Statistic', 'Statistique'],
          'Cloud': ['Google Cloud', 'Azur', 'AWS', 'Cloud'],
          'Big data': ['Big data', 'Spark', 'Hadoop', 'Yarn', 'Pig', 'Morphline', 'ETL', 'gros volume de donnée',
                       'PySpark'],
          'Computer science': ['Computer science', 'Computer Engineering'],
          'Djanbo': ['Djanbo'],
          'Flask': ['Flask'],
          'Streamlit': ['Streamlit'],
          'Docker': ['Docker'],
          'Saas': ['Saas'],
          'Back-end': ['Back-end', 'PHP', 'backend'],
          'Front-end': ['front'],
          'Design': ['Design', 'UI', 'UX'],
          'SAS': ['SAS'],
          'Business intelligence': ['Business Intelligence'],
          'Statistic': ['Statistic', 'statas'],
          'Redis': ['Redis'],
          'Web Scrapping': ['Selenium', 'BeautifulSoup', 'Scipy'],
          'Server': ['ElasticSearch', 'Server', 'Elastic Search'],
          'Blockchain': ['blockchain', 'Bitcoin'],
          'English': ['English', 'international', 'anglais', 'anglophone'],
          'French': ['français', 'francophone'],
          'Postman': ['Postman'],
          'Websphere': ['Websphere'],
          'Conception': ['Conception'],
          'Documentation': ['Documentation', 'plan'],
          'Teach': ['teach', 'Education'],
          'Debug': ['Debug', 'problem solver', 'Solution'],
          'Test': ['test'],
          'Redux': ['Redux'],
          'JQuery': ['JQuery'],
          'Maintenance': ['Maintenance', 'Maintain'],
          'Microservices': ['micro-service', 'microservice']
          }
# }
# contrats = ['CDI','CDD','Apprentissage','Contrat pro','Stage','Intérim','Freelance','Indépendant','Freelance']

# Les mots clés des niveaux d'études
studylevel_keywords = {'High School': ['High School', 'Baccalauréat'],
                       'Guaduate': ['Université', 'B.S.', 'BA', 'BS', 'Universitaire', 'Formation supérieure',
                                    'Guaduate', 'Bac +2', 'Bac +3', 'Bachelor'],
                       'Master': ['Master', 'M.S.', 'Master 2', 'Master +2', 'Bac +5', 'Bac+5', 'Bac +4', 'Bac+4',
                                  'Grande école d\'ingénieur', 'Bac +4/5', 'M2', 'Cursus ingénieur', 'engineer',
                                  'Diplôme ingénieur', 'MBA'],
                       'Doctor': ['Doctorat', 'Doctor', 'PhD', 'Ph.D', 'bac+8', 'bac +8']
                       }

# Les mots clés des niveaux d'expériences
explevel_keywords = {
    'Entry': ['Entry', 'Débutant', 'Beginer', 'No experience', 'Apprenant', 'Stage', 'Stagiaire', 'Pas d`\'expérience',
              '0-1 an', '0 - 1 an', '0/1 an', '0 / 1 an', 'Junior', '1 an'],
    'Intermediate': ['Intermédiaire', 'Intermediate', '2+ year', '2 year', '3 year', '2-3 year', '2 ans', '2/3 an',
                     '1-2 an', '1-3  years', 'two (2) year', '(2) year', '1ère expérience', '> 1 an',
                     'première expérience', '2 à 3 an'],
    'Confirmed': ['Confirm', '3 an', '4 an', '5 an', '3+ year', '4+ year', '5+ year', '3 year', '4 year', '5 year',
                  '3-5 year', '3-5 an', '2-5 an', '3/5 year', '3/5 an', '4-6+ year', '4-6+ an', '2-7 years', 'two year',
                  'three year', 'four year', 'five year', '2/5 an', 'ADVANCED', '5 yrs'],
    'Expert': ['Expert', 'six year', 'seven year', 'eight year', 'nine year', '6 year', '6+ years', '7 year', '7+ year',
               '8 year', '8+ year', '9 year', '9+ year', '6 an', '6+ an', '7 an', '7+ an', '8 an', '8+ an', '9 an',
               '9+ an', '10 an', '5-10 year', '5-10 an', '5 - 10 an', '5/10 year', '5/10 an', '6-8 year', 'six an',
               'six+ an', 'sept an', 'sept+ an', 'huit an', 'huit+ an', 'neuf an', 'neuf+ an'],
    'Senior': ['Senior', '10+ year', '10+ an', '10 ans +', 'plus de 10 an', 'ten year', 'dix+ an', 'dix ans +',
               'plus de 10 an']
    }


# Regex pour récupérer les chaînes pour indique les salaires


# La fonction vérifie si un terme existe dans une chaîne de caractère
def exist_in_array(x, dicto):
    for key in dicto:
        if any(str.lower(term) in str.lower(x) for term in dicto[key]):
            return key
        else:
            pass
    return None


# La fonction vérifie si un terme existe dans la colonne ['Poste'] et ['Description']
def exist_experience(row, dicto):
    poste_lower = str.lower(row['Poste'])
    desc_lower = str.lower(row['Description'])

    for key in dicto:
        if any(str.lower(term) in poste_lower for term in dicto[key]):
            return key
        elif any(str.lower(term) in desc_lower for term in dicto[key]):
            return key
        else:
            pass
    return row


# La fonction retourne le résultat obtenu à partir d'un string et regex
def searchBy(x, pattern):
    match = re.search(pattern, str.lower(x))
    if match:
        return match.group(0)


# Fonction qui retourne un numbre de format correcte à partir des nombres en format de string
def correct_number(string):
    numb_string = str(string).replace(' ', '').replace('k', '000')

    # Si le nombre a un virgule devant les deux dernier chiffres
    if re.match('^.+[.]\d{2}$', numb_string):
        numb = numb_string.replace(',', '')
        return (float(numb))

    # Si le nombre a un point devant les deux dernier chiffres
    elif re.match('^.+[,]\d{2}$', numb_string):
        numb = numb_string.replace(',', '.')
        return (float(numb))

    # Si le nombre n'a pas de point ni virgule devant les deux dernier chiffres
    else:
        numb = numb_string.replace(',', '').replace('\.', '')
        return (float(numb))


# fonction qui sépare les salaire minimum et salaire maximum en 2 colonnes différents
def minmaxSalary(row):
    match = re.match(
        r'(?:\D*)(?:[\$€]?\s?)((?:\d+)(?:[\.,\s]?\d{3})*(?:[\s]?k)?(?:[\.,\s]\d{2})?)(?:[\s]?[\$€]?[\s]?(?:à|au|et|\/|->?|to|and)?[\s]?[\$€]?\s?)((?:\d+)(?:[\.,\s]?\d{3})*(?:[\s]?k)?(?:[\.,\s]\d{2})?)?',
        row['Salaire'])

    # Si on obtient les salaire minimum et salaire maximum
    if (len(match.groups(0)) == 2) and (match.groups(0)[1] != 0):

        minSalary = correct_number(match.groups(0)[0])
        maxSalary = correct_number(match.groups(0)[1])

    # Si on obtient juste un salaire
    elif match.groups(0)[1] == 0:

        minSalary = correct_number(match.groups(0)[0])
        maxSalary = minSalary

    # Non retrouvé
    else:

        minSalary = np.nan
        maxSalary = np.nan

    # Si dans le salaire est indiqué le salaire par an
    if re.search(r'(annually)|(year)|(((par)|(per)|(by)|(\/)|(every)|(un)|(une))[\s]?an)', row['Salaire']):
        row['Salaire minimum par an'] = minSalary
        row['Salaire maximum par an'] = maxSalary

    # Si dans le salaire est indiqué le salaire par mois
    elif re.search(r'(month)|(mensuel)|(mois)', row['Salaire']):
        row['Salaire minimum par an'] = minSalary * 12
        row['Salaire maximum par an'] = maxSalary * 12

    # Si dans le salaire est indiqué le salaire par semaine
    elif re.search(r'(week)|(semaine)|(hebdomadaire)', row['Salaire']):
        row['Salaire minimum par an'] = minSalary * 4 * 12
        row['Salaire maximum par an'] = maxSalary * 4 * 12

    # Si dans le salaire est indiqué le salaire par jour
    elif re.search(r'(day)|(jour)', row['Salaire']):
        row['Salaire minimum par an'] = minSalary * 22 * 12
        row['Salaire maximum par an'] = maxSalary * 22 * 12

    # Si dans le salaire est indiqué le salaire par heure
    elif re.search(r'(hour)|(heur)', row['Salaire']):
        row['Salaire minimum par an'] = minSalary * 8 * 22 * 12
        row['Salaire maximum par an'] = maxSalary * 8 * 22 * 12

    # pour tout autres cas return np.nan
    else:
        row['Salaire minimum par an'] = np.nan
        row['Salaire maximum par an'] = np.nan
    return row


# La fonction vérifie si dans la colonne ['Description'] de chaque ligne, s'il trouve descompétences dans le dictionnaire, si oui, il met un 1
def skill_required(row, skills):
    desc_low = str.lower(row['Description'])

    for key in skills:
        if any(str.lower(term) in desc_low for term in skills[key]):
            row[key] = 1
        else:
            pass

    return row


# La fonction qui donne un array de quantile à partir de ['Salaire minimum par an'] et ['Salaire maximum par an']
def separe_quantile(df, number):
    list_prob = [1 / number * i for i in range(1, number + 1)]
    array_min = df['Salaire minimum par an'].quantile(
        q=list_prob, interpolation="linear")
    array_max = df['Salaire maximum par an'].quantile(
        q=list_prob, interpolation="linear")

    liste_classe = [0]

    for i in range(number):
        liste_classe.append((array_min.values[i] + array_max.values[i]) / 2)

    liste_classe.pop()
    liste_classe.append(array_max.values[-1])
    return (liste_classe)

    # La fonction qui mets la classe de salaire de chaque ligne


def put_class_salaire(row, classes):
    mean = (row['Salaire minimum par an'] + row['Salaire maximum par an']) / 2
    for i in range(len(classes) - 1):
        if (classes[i] <= mean) and (mean <= classes[i + 1]):
            row['Classe de salaire par an'] = str(
                int(classes[i])) + (' - ') + str(int(classes[i + 1]))
    return row


# La fonction qui prend la colonne ['Ville'] en réduisant la taille pour devenir la colonne ['City']
def extract_city(x):
    regex = re.compile(
        r'(?:\D*)(?:\()(\d{2})(?:\))|(?:.*)([A-Z]{2})(?:.*)|(?:)')
    resultat = re.match(regex, str(x)).groups(0)
    if (resultat[0] != 0):
        if (int(resultat[0]) == 75) or (int(resultat[0]) > 90 and int(resultat[0]) <= 95):
            return "ILE DE FRANCE"
        else:
            return "AUTRE VILLEFR"
    elif (resultat[1] != 0):
        return resultat[1]
    else:
        pass


def in_colonne(row, column_name):
    try:
        row[row[column_name]] = 1
    except:
        pass
    return row

def main():
    # prendres tout les noms de fichiers csv dans le array
    filenames = [
        'C:/Users/yangg/Python/Projet_Classification_Salaire/Flask/csv/' + str.lower(job).replace(' ', '') + str.lower(
            country) + '.csv' for job, country in
        zip(jobs, countrys)]

    dfs = [pd.read_csv(filename, sep=';', encoding="utf-8-sig")
           for filename in filenames]

    # Ajouter une colonne indique le métier
    dfs[0]['Métier'] = 'Data Scientist'
    dfs[1]['Métier'] = 'Développeur Python'
    dfs[2]['Métier'] = 'Développeur JavaScript'
    dfs[3]['Métier'] = 'Développeur Java'
    dfs[4]['Métier'] = 'Data Scientist'
    dfs[5]['Métier'] = 'Développeur Python'
    dfs[6]['Métier'] = 'Développeur JavaScript'
    dfs[7]['Métier'] = 'Développeur Java'

    # Créer le dataframe à partir de la concaténations de ces fichiers
    df = pd.concat(dfs)
    df = df[df.Description.isna() == False]

    salaryMatch = re.compile(
        r'((([\$€]\s?\d+([\.,\s]?\d{3})*[\s]?k?([\.,\s]\d{2})?([\s]?((à)|(au)|(et)|(\/)|(->?)|(to)|(and))?[\s]?[\$€]?[\s]?\d{1,3}([\.,\s]?\d{3})*\s?k?([\.,\s]?\d{2})?)?)|((\d+([\.,\s]?\d{3})*\s?k?([\.,\s]\d{2})?\s?[\$€]?([\s]?((à)|(au)|(et)|(and)|(\/)|(->?)|(to))?[\s]?\d{1,3}([\.,\s]?\d{3})*\s?k?([\.,\s]\d{2})?)?)[€\$])[\s]?)(\s*(brut)?\s*((par)|(a)|(an)|(per)|(by)|(\/)|(every)|(un)|(une))[\s]*((annually)|(heure)|(jour)|(hebdomadaire)|(mois)|(mensuel)|(hour)|(day)|(month)|(year)|(an))))')

    datascientist = df[
        (df['Poste'].str.lower().str.contains('data')) & (df['Poste'].str.lower().str.contains('scientist')) & (
            df['Poste'].str.lower().str.contains(str.lower('Machine Learning'))) & (
            df['Poste'].str.lower().str.contains(str.lower('Data science')))]
    df = pd.concat([df[df['Métier'] != 'Data Scientist'],
                    datascientist], ignore_index=True)

    df = pd.concat([df, pd.DataFrame(
        columns=["Data Scientist", "Développeur Python", "Développeur JavaScript", "Développeur Java"])])

    df = pd.concat([df, pd.DataFrame(columns=["France", "USA"])])
    df = pd.concat([df, pd.DataFrame(columns=studylevel_keywords)])
    df = pd.concat([df, pd.DataFrame(columns=explevel_keywords)])


    # Extraire des niveaux d'étude requis à partir de la colonne ['Description']
    df['Study required'] = df['Description'].apply(
        lambda x: exist_in_array(x, studylevel_keywords))

    # Extraire des niveaux d'expérience requis à partir de la colonne ['Description']
    df['Experience required'] = df['Description'].apply(
        lambda x: exist_in_array(x, explevel_keywords))

    df = df.apply(lambda row: in_colonne(row, 'Pays'), axis=1)
    df = df.apply(lambda row: in_colonne(row, 'Métier'), axis=1)
    df = df.apply(lambda row: in_colonne(row, 'Study required'), axis=1)
    df = df.apply(lambda row: in_colonne(row, 'Experience required'), axis=1)

    # Ajouter les colonnes de compétence et extraire la valeur à partir de la colonne ['Description']
    df = pd.concat([df, pd.DataFrame(columns=skills)])
    df = df.apply(lambda row: skill_required(row, skills), axis=1)

    # Extraire des salaires à partir de la colonne  ['Description']
    df['SalaryExtract'] = df['Description'].apply(
        lambda x: searchBy(x, salaryMatch))

    # Remplacer la colonne ['Salaire'] nulle par ['SalaryExtract'], si ['SalaryExtract'] est non nulle aussi
    df['Salaire'].update(df['SalaryExtract'])

    # Supprimer les lignes dont le salaire n'ont pas de valeur
    df = df[df['Salaire'].isna() == False]

    # Supprimela colonne ['Type de contrat']  dont on n'a pas besoin
    try:
        df.drop('Contrat', axis=1, inplace=True)
    except:
        pass

    # Supprimela colonne ['SalaryExtract']  dont on n'a plus besoin
    try:
        df.drop('SalaryExtract', axis=1, inplace=True)
    except:
        pass

    # Supprimer les lignes doublants
    df = df.drop_duplicates()

    # Ajouter les colonnes ['Salaire minimum par an'] et ['Salaire maximum par an']
    df = pd.concat([df, pd.DataFrame(
        columns=['Salaire minimum par an', 'Salaire maximum par an'])])

    # Assigner les colonnes ['Salaire minimum par an'] et ['Salaire maximum par an'] par les valeurs de la colonne ['Salaire']
    df = df.apply(lambda row: minmaxSalary(row), axis=1)

    df['Classe de salaire par an'] = np.nan
    df = df.apply(lambda row: put_class_salaire(
        row, separe_quantile(df, 3)), axis=1)

    try:
        df = df.drop(['Salaire', 'Salaire minimum par an', 'Salaire maximum par an', 'Entreprise', 'Description'],
                     axis=1)
    except:
        pass

    #df = pd.get_dummies(df, prefix=['Profession', 'Pays', 'Experience', 'Level'],
                        #columns=['Métier', 'Pays', 'Experience required', 'Study required'])

    try:
        df.drop(['Description', 'Entreprise'], axis=1, inplace=True)
    except:
        pass

    try:
        df.drop('Pays', axis=1, inplace=True)
    except:
        pass

    try:
        df.drop('Métier', axis=1, inplace=True)
    except:
        pass

    try:
        df.drop('Study required', axis=1, inplace=True)
    except:
        pass

    try:
        df.drop('Experience required', axis=1, inplace=True)
    except:
        pass

    try:
        df.drop('Poste', axis=1, inplace=True)
    except:
        pass

    df.reset_index(drop=True, inplace=True)

    # df['City'] = df['Ville'].apply(lambda x: extract_city(x))

    # df = pd.get_dummies(df, prefix=['City'], columns=['City'])
    try:
        df.drop(['Ville'], axis=1, inplace=True)
    except:
        pass

    df = df.fillna(0)

    df.to_csv('csv/Prepo.csv', index=False, sep=';', encoding="utf-8-sig")


if __name__ == '__main__':
    main()
