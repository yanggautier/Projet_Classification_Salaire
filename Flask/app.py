import oyaml as yaml
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    websitedata = yaml.load(open('Flask/_config.yaml', encoding='utf-8'))

    return render_template('index.html', data=websitedata)


if __name__ == '__main__':
    app.run(debug=True, port=5000)