from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista della spesa
lista_spesa = []

@app.route('/')
def home():
    return render_template('index.html', lista=lista_spesa)

@app.route('/aggiungi', methods=['POST'])
def aggiungi():
    elemento = request.form.get('elemento')
    if elemento:
        lista_spesa.append(elemento)
    return redirect(url_for('home'))

@app.route('/rimuovi/<int:indice>', methods=['POST'])
def rimuovi(indice):
    if 0 <= indice < len(lista_spesa):
        lista_spesa.pop(indice)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
