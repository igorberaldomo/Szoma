import  os, json
import pandas as pd
import sqlalchemy
from flask import Flask, request
DATABASE_URL = os.getenv("DATABASE_URL")
engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
def select_names(nome):
    search_string = f"SELECT * FROM suvinil WHERE nome = '{nome}' or pantone_name = '{nome}' "
    resultset  = pd.read_sql(search_string, engine)
    print(resultset)
    return resultset


def primary_select(red,green,blue):
    distancia = 36
    maxred = red + distancia
    minred = red - distancia
    maxgreen = green + distancia
    mingreen = green - distancia
    maxblue = blue + distancia
    minblue = blue - distancia
    if maxred > 255:
        maxred = 255
    if minred < 0:
        minred = 0
    if maxgreen > 255:
        maxgreen = 255
    if mingreen < 0:
        mingreen = 0
    if maxblue > 255:
        maxblue = 255
    if minblue < 0:
        minblue = 0
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
    search_string = f"SELECT * FROM suvinil WHERE red >= {minred} AND  red <= {maxred} AND green >= {mingreen} AND green <= {maxgreen} AND blue >= {minblue} AND blue <= {maxblue} "
    resultset  = pd.read_sql(search_string, engine)

    return resultset
    

app = Flask(__name__)
lastQuery = list()

@app.route('/', methods = ['GET'])
def infopage():
    return ('<h1>Colors API</h1><p>This api will request a picture or RGB, and will return a product (paint, tiles, fabrics) </p> '
)

@app.route('/suvinil/', methods =['GET','POST'])
def getsuvinilColors():
    if request.method == 'POST':
        rgb = request.get_json()
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        temp = primary_select(red,green,blue)
        response = temp.to_dict(orient='records')
        c = 0
        while c < len(response):
            lastQuery.append(response[c])
            c+=1
        with open ('response.json', 'w+') as file:
            json.dump(lastQuery, file)
            lastQuery.clear()
        return response
    if request.method == 'GET':
        with open ('response.json', 'r') as file:
            response = json.load(file)
            return response

@app.route('/names/', methods =['POST'])
def getNames():
    if request.method == 'POST':
        nomecor = request.get_json()
        print(nomecor['nome'])
        nome = nomecor['nome']
        response = select_names(nome)
        response = response.to_dict(orient='records')
        with open ('response.json', 'w+') as file:
            json.dump(response, file)
        return data
    
@app.route('/procura/', methods =['POST'])
def getProcura():
    if request.method == 'POST':
        codigo_cor = request.get_json()
        #  para buscar o nome da cor no futuro
        
         
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)