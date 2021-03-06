from flask import Flask, request, render_template
from . import config
from . import utils

app = Flask(__name__)
elastic = utils.ElasticsearchDB()

# Config options - Make sure you created a 'config.py' file.
app.config.from_object(config)

@app.route('/', methods=['GET','POST'])
def accueil():
    #Appel elasticsearch avec les données du form remplie par l'utilisateur
    if request.method == 'POST':
        sub = request.form.get("substance").lower()
        exc = request.form.get("excipient").lower()
        #Vérification si la donnée excipient est présente
        if exc=="":
            exc=False
        substance  = elastic.search_insubstance(sub)
        medicament = utils.reshape_to_3_columns(elastic.search_inmedicament(sub, exc))

        return render_template('real-app.html', substance = substance, medicament = medicament)
    #Si l'appel est GET
    return render_template('real-app.html')


#Root de test
@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return "Vous avez envoyé un message..."
    return '<form action="" method="post"><input type="text" name="msg" /><input type="submit" value="Envoyer" /></form>'

if __name__ == "__main__":
    app.run()
