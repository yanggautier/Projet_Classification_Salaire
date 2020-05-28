# import oyaml as yaml
from flask import Flask, render_template

app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    # website_data = yaml.load(open('_config.yaml', encoding="utf-8"))
    return render_template('templates/index.html')
    # return render_template('index.html', data=website_data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)