from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Usuários
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pontos = db.Column(db.Integer, default=0)
    foto = db.Column(db.String(200), default="default.png")  # foto de perfil

    favores = db.relationship("Favor", backref="usuario", lazy=True)
    scraps = db.relationship("Scrap", backref="destino", lazy=True)

# Favores
class Favor(db.Model):
    __tablename__ = "favores"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="pendente")
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

# Comunidades
class Comunidade(db.Model):
    __tablename__ = "comunidades"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))

    membros = db.relationship("Usuario", secondary="membros_comunidade", backref="comunidades")

# Associação usuário ↔ comunidade
membros_comunidade = db.Table("membros_comunidade",
    db.Column("usuario_id", db.Integer, db.ForeignKey("usuarios.id"), primary_key=True),
    db.Column("comunidade_id", db.Integer, db.ForeignKey("comunidades.id"), primary_key=True)
)

# Scraps (recados no perfil)
class Scrap(db.Model):
    __tablename__ = "scraps"

    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.String(300), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    destino_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
