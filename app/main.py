from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>🚀 Funcionou! Página carregada.</h1>"

@app.route("/tradesmen")
def view_tradesmen():
    tradesmen = [
        {"name": "João", "trade": "Eletricista"},
        {"name": "Carlos", "trade": "Pintor"},
        {"name": "Ricardo", "trade": "Pedreiro"},
        {"name": "Eduardo", "trade": "Marceneiro"},
        {"name": "Felipe", "trade": "Serralheiro"}
    ]
    return render_template("view_tradesmen.html", tradesmen=tradesmen)

if __name__ == "__main__":
    app.run(debug=True)