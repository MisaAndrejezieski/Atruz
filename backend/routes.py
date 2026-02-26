from flask import request, jsonify
from models import db, Usuario, Favor

def init_routes(app):
    # Rota inicial
    @app.route("/")
    def home():
        return "Bem-vindo ao Altruz!"

    # Cadastro de usuário
    @app.route("/cadastro", methods=["POST"])
    def cadastro():
        data = request.json
        nome = data.get("nome")
        email = data.get("email")

        # Criar usuário
        novo_usuario = Usuario(nome=nome, email=email)
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({"mensagem": f"Usuário {nome} cadastrado com sucesso!"})

    # Registrar favor
    @app.route("/favor", methods=["POST"])
    def favor():
        data = request.json
        descricao = data.get("descricao")
        usuario_id = data.get("usuario_id")

        # Criar favor
        novo_favor = Favor(descricao=descricao, usuario_id=usuario_id)
        db.session.add(novo_favor)
        db.session.commit()

        return jsonify({"mensagem": f"Favor registrado: {descricao}"})

    # Consultar pontos
    @app.route("/pontos/<int:usuario_id>", methods=["GET"])
    def pontos(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            return jsonify({"usuario": usuario.nome, "pontos": usuario.pontos})
        else:
            return jsonify({"erro": "Usuário não encontrado"}), 404
