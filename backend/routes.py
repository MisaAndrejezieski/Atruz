from flask import request, jsonify
from models import db, Usuario, Favor, Transacao

def init_routes(app):
    @app.route("/")
    def home():
        return "Bem-vindo ao Altruz!"

    # Cadastro de usuário
    @app.route("/cadastro", methods=["POST"])
    def cadastro():
        data = request.json
        nome = data.get("nome")
        email = data.get("email")

        novo_usuario = Usuario(nome=nome, email=email)
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({"mensagem": f"Usuário {nome} cadastrado com sucesso!"})

    # Login simples
    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        email = data.get("email")

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            return jsonify({"mensagem": "Login realizado com sucesso!", "usuario_id": usuario.id, "nome": usuario.nome})
        else:
            return jsonify({"erro": "Usuário não encontrado"}), 404

    # Registrar favor
    @app.route("/favor", methods=["POST"])
    def favor():
        data = request.json
        descricao = data.get("descricao")
        usuario_id = data.get("usuario_id")

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

    # Listar feed de favores
    @app.route("/feed", methods=["GET"])
    def feed():
        favores = Favor.query.all()
        lista = [
            {"id": f.id, "descricao": f.descricao, "status": f.status, "usuario": f.usuario.nome}
            for f in favores
        ]
        return jsonify(lista)

    # Aceitar favor
    @app.route("/aceitar_favor", methods=["POST"])
    def aceitar_favor():
        data = request.json
        favor_id = data.get("favor_id")
        usuario_id = data.get("usuario_id")  # quem está aceitando

        favor = Favor.query.get(favor_id)
        usuario = Usuario.query.get(usuario_id)

        if not favor or not usuario:
            return jsonify({"erro": "Favor ou usuário não encontrado"}), 404

        # Atualiza status
        favor.status = "aceito"

        # Movimenta pontos (exemplo: quem ajuda ganha 5 pontos)
        usuario.pontos += 5

        # Registra transação
        transacao = Transacao(
            usuario_origem=favor.usuario_id,
            usuario_destino=usuario_id,
            pontos=5,
            descricao=f"Aceitou favor: {favor.descricao}"
        )
        db.session.add(transacao)
        db.session.commit()

        return jsonify({"mensagem": f"Favor {favor_id} aceito por {usuario.nome}. Pontos adicionados!"})
