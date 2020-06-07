import oyaml as yaml
from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
model = pickle.load(open('./Flask/model.pkl', 'rb'))


@app.route('/')
@app.route('/index')
def index():
    websitedata = yaml.load(open('./Flask/_config.yaml', encoding='utf-8'))
    return render_template('index.html', data=websitedata)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    job = request.form.getlist('gridRadioJob')

    if job[0] == "dscientist":
        metier = "Data Scientist"
    elif job[0] == "python":
        metier = "Développeur Python"
    elif job[0] == "js":
        metier = "Développeur JavaScript"
    elif job[0] == "java":
        metier = "Développeur Java"
    else:
        metier = None

    test = {'Confirmed': 0, 'Data Scientist': 0, 'Doctor': 0, 'Développeur Java': 0,
            'Développeur JavaScript': 0, 'Développeur Python': 0, 'Entry': 0, 'Expert': 0,
            'France': 0, 'Guaduate': 0, 'High School': 0, 'Intermediate': 0, 'Master': 0,
            'Senior': 0, 'USA': 0, 'Unnamed: 15': 0, 'Python': 0, 'R': 0, 'Matlab': 0,
            'Kubernetes': 0, 'Bash': 0, 'Fortran': 0, 'Ruby': 0, 'Golang': 0, 'C': 0, 'Java': 0,
            'JEE': 0, 'JSP': 0, 'J2ME': 0, 'BREW': 0, 'MVC': 0, 'SASS': 0, 'XML': 0, 'Eclipse': 0,
            'Spring': 0, 'Atlassian': 0, 'Jenkin': 0, 'FIX': 0, 'Nexus': 0, 'Maven': 0,
            'Flutter': 0, 'Bootstrap': 0, 'Kafka': 0, 'Data software': 0, 'Data analysis': 0,
            'Data preprocessing': 0, 'Report': 0, 'Math': 0, 'Development': 0,
            'Integration': 0, 'ReactNative': 0, 'Dataiku': 0, 'Data viz': 0, 'Data skills': 0,
            'Data pipeline': 0, 'Git': 0, 'SQL': 0, 'Djanbo': 0, 'Database': 0, 'Javascrpit': 0,
            'POO': 0, 'Regex': 0, 'Mobile Programming': 0, 'Team Work': 0,
            'Machine Learning': 0, 'Web langage': 0, 'System unix': 0, 'Scratch': 0,
            'Scala': 0, 'API': 0, 'RestAPI': 0, '.Net': 0, 'Visual Studio': 0, 'Responsive': 0,
            'Javascript Skills': 0, 'Outil bureautique': 0, 'Deep Learning': 0,
            'Text analytics': 0, 'Marketing': 0, 'Finance': 0, 'Communication': 0,
            'Statistics': 0, 'Cloud': 0, 'Big data': 0, 'Computer science': 0, 'Flask': 0,
            'Streamlit': 0, 'Docker': 0, 'Saas': 0, 'Back-end': 0, 'Front-end': 0, 'Design': 0,
            'SAS': 0, 'Business intelligence': 0, 'Statistic': 0, 'Redis': 0,
            'Web Scrapping': 0, 'Server': 0, 'Blockchain': 0, 'English': 0, 'French': 0,
            'Postman': 0, 'Websphere': 0, 'Conception': 0, 'Documentation': 0, 'Teach': 0,
            'Debug': 0, 'Test': 0, 'Redux': 0, 'JQuery': 0, 'Maintenance': 0, 'Microservices': 0}

    studylevel = request.form.getlist('gridRadioEtude')[0]
    explevel = request.form.getlist('gridRadioExp')[0]
    pays = request.form.getlist('gridRadiosPays')[0]
    skills = request.form.getlist('skills')

    for skill in skills:
        test[skill] = 1

    test[metier] = 1
    test[studylevel] = 1
    test[explevel] = 1
    test[pays] = 1

    int_features = [int(x) for x in list(test.values())]
    final_features = [np.array(int_features)]


    prediction = model.predict(final_features)[0]

    if pays == "France":
        devise = '€'
    else:
        devise = '$'

    return render_template('predict.html', prediction_text = "Vous devez proposez un salaire compris entre " + prediction + ' ' + devise + " par an")


if __name__ == '__main__':
    app.run(debug=True, port=5000)