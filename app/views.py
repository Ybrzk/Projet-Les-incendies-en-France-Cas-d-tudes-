
from app import app

# importer les autres éléments déclarés 
# dans /app/__init__py selon les besoins
# from app import db, babel
# importer les modèles pour accéder aux données

from app.models import *
from flask import render_template, request
from app.config import create_plot1, create_plot2



@app.route('/', methods = ['GET', 'POST'])
def index():
  return render_template('index.html')

  
@app.route('/dashbord', methods = ['GET', 'POST'])
def dashbord(): #Fonction permettant d'afficher le dashbord avec ses paramètres et attribut
  annee = request.form['annee'] # Assignation d'une variable annee avec la méthode de la bibliothèque request avec la méthode form qui a comme attribut le name annee de l'html
  categorie = request.form['categorie'] 

   
  plot1 = create_plot1(annee, categorie) #Création d'une variable, pour la valeur de create_plot qui est graphJSON
  plot2 = create_plot2() #Création d'une variable, pour la valeur de create_plot2 qui est graphJSON


  return render_template('graph.html', plot1 = plot1, plot2 = plot2, annee = annee, categorie = categorie) # Transcrire la valeur du paramètre de la méthode dans le render_template pour avoir un rendu visuel

  #return render_template ou rendu template, retourne la page html

  #Le fichier views.py réunit le config et les input html pour avoir la vue sur le navigateur