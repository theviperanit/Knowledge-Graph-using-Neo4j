from flask import Flask, render_template, request, jsonify, Response, redirect
import requests as r
import spacy
from spacy import displacy
import en_ner_bc5cdr_md

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('search_term')
    url = "https://www.ncbi.nlm.nih.gov/research/litsense-api/api/?format=json&query=" + query + "&rerank=true"
    res = r.get(url)
    json_data = res.json()
    lis = []
    nlp = spacy.load("en_ner_bc5cdr_md")
    for i in json_data:
        doc=nlp(i['text'])
        lis.append(doc)
    col_dict = {}
    seven_colours = ['#e6194B', '#3cb44b', '#ffe119', '#ffd8b1', '#f58231', '#f032e6', '#42d4f4']
    for label, colour in zip(nlp.pipe_labels['ner'], seven_colours):
        col_dict[label] = colour   

    options = {'ents': nlp.pipe_labels['ner'], 'colors':col_dict}
    html = displacy.render(lis, style='ent', page=True,options=options)
    return render_template('new.html',data=str(html))

    

    

if __name__ == '__main__':
    app.run(port=5002)

