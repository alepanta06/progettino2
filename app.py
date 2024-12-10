from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurazione del database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lista_spesa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inizializza SQLAlchemy
db = SQLAlchemy(app)

# Modello per la tabella ListaSpesa
class ListaSpesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID univoco
    elemento = db.Column(db.String(100), nullable=False)  # Nome dell'elemento

# Crea il database
with app.app_context():
    db.create_all()

# Rotte
@app.route('/')
def home():
    # Recupera tutti gli elementi dal database
    lista_spesa = ListaSpesa.query.all()
    return render_template('index.html', lista=lista_spesa)

@app.route('/aggiungi', methods=['POST'])
def aggiungi():
    elemento = request.form['elemento']
    if elemento:
        nuovo_elemento = ListaSpesa(elemento=elemento)  # Crea un nuovo record
        db.session.add(nuovo_elemento)  # Aggiunge al database
        db.session.commit()  # Salva i cambiamenti
    return redirect(url_for('home'))

@app.route('/rimuovi/<int:indice>', methods=['POST'])
def rimuovi(indice):
    elemento = ListaSpesa.query.get_or_404(indice)  # Trova l'elemento
    db.session.delete(elemento)  # Rimuove l'elemento
    db.session.commit()  # Salva i cambiamenti
    return redirect(url_for('home'))

@app.route('/svuota', methods=['POST'])
def svuota():
    ListaSpesa.query.delete()  # Cancella tutti i record
    db.session.commit()  # Salva i cambiamenti
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
