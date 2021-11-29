from flask.scaffold import F
from owlready2 import *

onto = get_ontology("tea.owl").load()  # Change the path of the ontology

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def page_entry():
    html = """<html><body>
<h3>Entrez les caractéristiques du Thé:</h3>
<form action="/result">
    Method :<br/>
    <input type="radio" name="method" value="Oxidised"/> Oxi<br/>
    <input type="radio" name="method" value="Dried"/> Dry<br/>
    <br/>
     <input type="radio" name="flavour" value="Spicy"/>Spicy<br/>
    <input type="radio" name="flavour" value="Bitter"/>Bitter<br/>
    <br/>
    
      <br/>
     <input type="checkbox" name="hasI" value="Jasmin"/> Jasmin<br/>
     <input type="checkbox" name="hasI" value="Bergamote"/> Bergamote<br/>
    <br/>
   
    <input type="submit"/>
</form>  
</body></html>"""
    return html


ONTO_ID = 0


@app.route("/result")
def page_result():
    global ONTO_ID
    ONTO_ID = ONTO_ID + 1

    onto_tmp = get_ontology("http://tmp.org/onto_%s.owl#" % ONTO_ID)

    method = request.args.get("method", "")
    flavour = request.args.get("flavour", "")
    ingredients = request.args.getlist("hasI")
    print(method, flavour, onto.Tea, ingredients)

    with onto_tmp:
        new_tea = onto.Tea()

        if method:
            method = onto[method]
            new_tea.has_method = method()

        if flavour:
            flavour = onto[flavour]
            new_tea.has_taste = flavour()

        for ingredient in ingredients:
            ingredi = onto[ingredient]
            new_tea.has_ingredient.append(ingredi())

        close_world(new_tea)

        sync_reasoner([onto, onto_tmp])

    noms_des_classes = []
    for classe in new_tea.is_a:
        print(classe)
        if isinstance(classe, ThingClass):
            noms_des_classes.append(classe.name)
    html = """<html><body><h4>Result :%s Tea</h4></body></html>""" % noms_des_classes
    onto_tmp.destroy()
    return html


import werkzeug.serving

werkzeug.serving.run_simple("localhost", 5000, app)
