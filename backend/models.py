from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabela de Usuários
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pontos = db.Column(db.Integer, default=0)

    favores = db.relationship("Favor", backref="usuario", lazy=True)

# Tabela de Favores
class Favor(db.Model):
    __tablename__ = "favores"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="pendente")  # pendente, aceito, concluído
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

# Histórico de transações de pontos
class Transacao(db.Model):
    __tablename__ = "transacoes"

    id = db.Column(db.Integer, primary_key=True)
    usuario_origem = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    usuario_destino = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    pontos = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(200))
