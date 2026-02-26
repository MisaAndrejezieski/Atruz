from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes import init_routes

app = Flask(__name__)

# Configuração do banco SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/altruz.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
init_routes(app)

# Criar tabelas automaticamente
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
