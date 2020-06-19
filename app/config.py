
import pandas as pd # procès de données, CSV file I/O (e.g. pd.read_csv)
import numpy as np
from plotly.offline import init_notebook_mode, iplot, plot
import plotly
import plotly.graph_objs as go
import json
from flask import render_template
from sqlalchemy import create_engine
from urllib.request import urlopen
import plotly.express as px

#Établir la connection entre Python et MySQL
engine = create_engine("mysql+pymysql://yacine-fil-rouge:yacine13@localhost/interventions_incendie_et_secours")




def create_plot1(annee, categorie):
    """Traitements des requêtes et création de figure"""


    query1 = pd.read_sql_query("""SELECT annee, interventions_2016.departement, categorie, incendies
    FROM interventions_2016
    JOIN temperature_quotidienne_regionale ON interventions_2016.region = temperature_quotidienne_regionale.region AND annee = %s AND categorie = '%s'
    GROUP BY annee, categorie, incendies, departement

    UNION

    SELECT annee, interventions_2017.departement, categorie, incendies
    FROM interventions_2017
    JOIN temperature_quotidienne_regionale ON interventions_2017.region = temperature_quotidienne_regionale.region AND annee = %s AND  categorie = '%s'
    GROUP BY annee, categorie, incendies, departement

    UNION

    SELECT annee, interventions_2018.departement, categorie, incendies
    FROM interventions_2018
    JOIN temperature_quotidienne_regionale ON interventions_2018.region = temperature_quotidienne_regionale.region AND annee = %s AND categorie = '%s'
    GROUP BY annee, categorie, incendies, departement
    ORDER BY incendies, categorie;""" %(annee, categorie, annee, categorie, annee, categorie), con = engine)



    #query1 = pd.read_csv('/home/yacine/Bureau/interventions2016.csv', encoding ='latin-1', sep = ';')
    query1['incendies'] = query1["incendies"].str.strip()
    query1['incendies'] = query1['incendies'].str.replace(" ","")


    query1["incendies"] = pd.to_numeric(query1["incendies"])
  





    





# Création de la trame 1
    """trace1 = go.Scatter(
                        x = query1.moyenne_temperature,
                        y = query1.nb_incendies,
                        mode = "markers",
                        name = "Nombre d'incendies en fonction des moyennes des température",
                        marker = dict(color = 'rgba(2, 102, 35, 0.5)')
                        #text = query1.
                        )

    data = [trace1]

    layout = dict(title = "Nombre d'incendies en fonction des températures moyenne dans l'hexagone",
                xaxis = dict(title = "Moyenne des températures",ticklen = 5,zeroline = True),
                yaxis = dict(title = "Nombre d'incendies",ticklen = 5,zeroline = True)
                )
    fig = go.Figure(data = data, layout = layout)"""

    trace1 = go.Bar(
                x = query1["departement"],
                y = query1["incendies"],
                name = "Nombre de feux en fonction des départements",
                marker = dict(color = 'rgba(2, 102, 35, 0.5)',
                             line = dict(color ='rgb(2, 102, 35)',width =1.5))
                ,text = query1['departement']
                )
    data = [trace1]

    layout = go.Layout(barmode = "group")
    fig = go.Figure(data = data, layout = layout)


    
    graphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)

    return graphJSON



def create_plot2():
    query2 = pd.read_sql_query("""SELECT SUM(incendies) as nb_incendies, departement, numero
    FROM interventions_2016
    GROUP BY departement, numero

    UNION

    SELECT SUM(incendies) as nb_incendies, departement, numero
    FROM interventions_2017
    GROUP BY departement, numero

    UNION

    SELECT SUM(incendies) as nb_incendies, departement, numero
    FROM interventions_2018
    GROUP BY departement, numero""", con = engine)

    query2.nb_incendies.astype(int)

    with urlopen('https://france-geojson.gregoiredavid.fr/repo/departements.geojson') as response:
        geojson = json.load(response)
        
    fig = px.choropleth_mapbox(query2,geojson= geojson
                          ,color = "nb_incendies"
                         ,locations = "numero"
                         ,featureidkey = "properties.code"
                           ,hover_name = 'departement'
                           #, color_continuous_scale = [(0,"purple"), (1,"red")]
                           #,color_continuous_midpoint = 2
                          ,range_color = (0, 5000) 
                           ,center={"lat": 46.3223, "lon": 1.2549}
                           ,mapbox_style="carto-positron", zoom=4.5)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})    

    graphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON

"""def create_plot3():
    query3 = pd.read_sql_query(SELECT annee, interventions_2016.region as region, interventions_2016.departement, numero, categorie,
    incendies as nb_incendies, placettes_foret_2016.couverture_du_sol
    FROM interventions_2016
    JOIN placettes_foret_2016 ON interventions_2016.numero = placettes_foret_2016.departement
    GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region

    UNION

    SELECT annee, interventions_2017.region as region, interventions_2017.departement, numero, categorie,
    incendies as nb_incendies, placettes_foret_2017.couverture_du_sol
    FROM interventions_2017
    JOIN placettes_foret_2017 ON interventions_2017.numero = placettes_foret_2017.departement
    GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region


    UNION

    SELECT annee, interventions_2018.region as region, interventions_2018.departement, numero, categorie,
    incendies as nb_incendies, placettes_foret_2018.couverture_du_sol
    FROM interventions_2018
    JOIN placettes_foret_2018 ON interventions_2018.numero = placettes_foret_2018.departement
    GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region
    ORDER BY annee, region, departement, numero, categorie, nb_incendies, couverture_du_sol;, con = engine)

    fig = {
    "data": [
        {
        "values": query3.nb_incendies,
        "labels": query3.couverture_du_sol,
        "domain": {"x": [0, .5]},
        "name": "Nombres d'incendies en fonction du type de fôret",
        "hoverinfo":"label+percent+name",
        "hole": .5,
        "type": "pie"
        },],
    "layout": {
            "title":"Nombres d'incendies en fonction du type de fôret",
            "annotations": [
                { "font": { "size": 15},
                "showarrow": False,
                "text": "Nombre d'étudiants",
                    "x": 0.20,
                    "y": 1
                },
            ]
        }
    }

    graphJSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON"""











    

""" def create_plot2(annee, departement, categorie, couverture_du_sol):
     query = pd.read_sql_query("                                                                                                                                SELECT annee, interventions_2010.region as region, interventions_2010.departement, numero, categorie,                                                       incendies as nb_incendies, placettes_foret_2010.couverture_du_sol                                                                                                                                           FROM interventions_2010                                                                                                                                     JOIN placettes_foret_2010 ON interventions_2010.numero = placettes_foret_2010.departement, annee = '%s' AND departement = '%s' AND numero = '%s' AND categorie = '%s' AND nb_incendies = '%s' AND couverture_du_sol = s%                                                                                                                                                        GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region                                                                                                                                                                                                                                                                                                                                     UNION                                                                                                                                                                                                                                                                                                                SELECT annee, interventions_2011.region as region, interventions_2011.departement, numero, categorie,                                                      incendies as nb_incendies, placettes_foret_2011.couverture_du_sol                                                                                                                                            FROM interventions_20                                                                                                                                          JOIN placettes_foret_2011 ON interventions_2011.numero = placettes_foret_2011.departement, annee = '%s' AND departement = '%s' AND numero = '%s' AND categorie = '%s' AND nb_incendies = '%s' AND couverture_du_sol = '%s'                                                                                        GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol                region                                                                                                                                                                                                                   UNION                                                                                                                                                                                                                                                                                                                     SELECT annee, interventions_2012.region as region, interventions_2012.departement, numero, categorie,                                                     incendies as nb_incendies, placettes_foret_2012.couverture_du_sol                                                                                           FROM interventions_2012                                                                                                                                         JOIN placettes_foret_2012 ON interventions_2012.numero = placettes_foret_2012.departement, annee = '%s' AND departement = '%s' AND numero = '%s' AND categorie = '%s' AND nb_incendies = '%s' AND couverture_du_sol = '%s'                                                                                   GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region                                                                                                                                                                                                                                                                                                                 UNION                                                                                                                                                                                                                                                                                                                   SELECT annee, interventions_2013.region as region, interventions_2013.departement, numero, categorie,                                                       incendies as nb_incendies, placettes_foret_2013.couverture_du_sol                                                                                           FROM interventions_2013                                                                                                                                     JOIN placettes_foret_2013 ON interventions_2013.numero = placettes_foret_2013.departement, annee = '%s' AND departement = '%s' AND numero = '%s' AND categorie = '%s' AND nb_incendies = '%s' AND couverture_du_sol = '%s'                                                                                                                                                    GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region                                                                                                                                                                                                                                                                                                                 UNION                                                                                                                                                                                                                                                                                                                    SELECT annee, interventions_2014.region as region, interventions_2014.departement, numero, categorie,                                                      incendies as nb_incendies, placettes_foret_2014.couverture_du_sol                                                                                        FROM  interventions_2014                                                                                                                                     JOIN placettes_foret_2014 ON interventions_2014.numero = placettes_foret_2014.departement, annee = '%s' AND departement = '%s' AND numero = '%s' AND categorie = '%s' AND nb_incendies = '%s' AND couverture_du_sol = '%s'                                                                                                                                                         GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region                                                                                                                                                                                                                                                                                                                    UNION                                                                                                                                                                                                                                                                                                                SELECT annee, interventions_2015.region as region, interventions_2015.departement, numero, categorie,                                                   incendies as nb_incendies, placettes_foret_2015.couverture_du_sol                                                                                                                                            FROM interventions_2015                                                                                                                                    JOIN placettes_foret_2015 ON interventions_2015.numero = placettes_foret_2015.departement, annee = '%s' AND departement = '%s' AND numero = '%s' AND categorie = '%s' AND nb_incendies = '%s' AND couverture_du_sol = '%s'                                                                                                                                                     GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region                                                                                                                                                                                                                                                                                                                 UNION                                                                                                                                                                                                                                                                                                               SELECT annee, interventions_2016.region as region, interventions_2016.departement, numero, categorie,                                                       incendies as nb_incendies, placettes_foret_2016.couverture_du_sol                                                                                                                                            FROM interventions_2016                                                                                                                                     JOIN placettes_foret_2016 ON interventions_2016.numero = placettes_foret_2016.departement, annee = '%s' AND departement = '%s' AND numero = '%s' AND categorie = '%s' AND nb_incendies = '%s' AND couverture_du_sol = '%s'                                                                                                                                                     GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region                                                                                                                                                                                                                                                                                                                   UNION                                                                                                                                                                                                                                                                                                                 SELECT annee, interventions_2017.region as region, interventions_2017.departement, numero, categorie,                                                       incendies as nb_incendies, placettes_foret_2017.couverture_du_sol                                                                                           FROM interventions_2017                                                                                                                                         JOIN placettes_foret_2017 ON interventions_2017.numero = placettes_foret_2017.departement, annee = '%s' AND departement = '%s' AND numero = '%s' AND categorie = '%s' AND nb_incendies = '%s' AND couverture_du_sol = '%s'                                                                                                                                                         GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region                                                                                                                                                                                                                                                                                                                    UNION                                                                                                                                                    SELECT annee, interventions_2018.region as region, interventions_2018.departement, numero, categorie,                                                       incendies as nb_incendies, placettes_foret_2018.couverture_du_sol                                                                                           FROM interventions_2018                                                                                                                                    JOIN placettes_foret_2018 ON interventions_2018.numero = placettes_foret_2018.departement, annee = '%s' AND departement = '%s' AND numero = '%s' AND categorie = '%s' AND nb_incendies = '%s' AND couverture_du_sol = '%s'                                                                                                                                                      GROUP BY numero, annee, categorie, nb_incendies, departement, couverture_du_sol, region                                                                     ORDER BY annee, region, departement, numero, categorie, nb_incendies, couverture_du_sol;", %(annee, departement, numero, categorie, nb_incendies,couverture_du_sol, annee, departement, numero, categorie, nb_incendies,couverture_du_sol, annee, departement, numero, categorie, nb_incendies,couverture_du_sol, annee, departement, numero, categorie, nb_incendies,couverture_du_sol, annee, departement, numero, categorie, nb_incendies,couverture_du_sol, annee, departement, numero, categorie, nb_incendies,couverture_du_sol, annee, departement, numero, categorie, nb_incendies,couverture_du_sol, annee, departement, numero, categorie, nb_incendies,couverture_du_sol, annee, departement, numero, categorie, nb_incendies,couverture_du_sol), con = engine)


#Création de la trame 3
    trace3 = go.Scatter(
                        x = query.nb_incendies,
                        y = query.couverture_du_sol,
                        mode = "markers",
                        name = "Nombre d'incendies en fonction de la couverture du sol",
                        marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                        #text = query1.
                        )
    # Création de la trame 4
    trace4 = go.Scatter(
                        x = query.categorie,
                        y = query.couverture_du_sol,
                        mode = "markers",
                        name = "Catégorie d'incendies en fonction de la couverture du sol",
                        marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                        #text = query1.
                        )

    data = [trace3, trace4]
    layout = dict(title = "Catégorie et nombre d'incendies en fonction de la couverture du sol",
                xaxis = dict(title = '',ticklen = 5,zeroline = True)
                )
    fig = dict(data = data, layout = layout)
    
    graphJSON = json.dumps (fig, cls = plotly.utils.PlotlyJSONEncoder) 
    
    return graphJSON """






































        

