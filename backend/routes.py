from flask import request, jsonify
from models import db, Usuario, Favor

def init_routes(app):
    @app.route("/")
    def home():
        return "Bem-vindo ao Altruz!"

    @app.route("/cadastro", methods=["POST"])
    def cadastro():
        data = request.json
        nome = data.get("nome")
        email = data.get("email")
        novo_usuario = Usuario(nome=nome, email=email)
        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({"mensagem": f"Usuário {nome} cadastrado com sucesso!"})

    @app.route("/favor", methods=["POST"])
    def favor():
        data = request.json
        descricao = data.get("descricao")
        usuario_id = data.get("usuario_id")
        novo_favor = Favor(descricao=descricao, usuario_id=usuario_id)
        db.session.add(novo_favor)
        db.session.commit()
        return jsonify({"mensagem": f"Favor registrado: {descricao}"})

    @app.route("/pontos/<int:usuario_id>", methods=["GET"])
    def pontos(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            return jsonify({"usuario": usuario.nome, "pontos": usuario.pontos})
        else:
            return jsonify({"erro": "Usuário não encontrado"}), 404

    # 🔹 Novo: listar feed de favores
    @app.route("/feed", methods=["GET"])
    def feed():
        favores = Favor.query.all()
        lista = [
            {"id": f.id, "descricao": f.descricao, "status": f.status, "usuario": f.usuario.nome}
            for f in favores
        ]
        return jsonify(lista)
