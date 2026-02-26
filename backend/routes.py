from flask import request, jsonify
from models import db, Usuario, Favor, Comunidade, Scrap

def init_routes(app):
    @app.route("/")
    def home():
        return "Bem-vindo ao Altruz estilo Orkut!"

    # Perfil de usuário
    @app.route("/usuario/<int:usuario_id>", methods=["GET"])
    def perfil(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "pontos": usuario.pontos,
            "foto": usuario.foto,
            "comunidades": [c.nome for c in usuario.comunidades]
        })

    # Criar comunidade
    @app.route("/comunidade", methods=["POST"])
    def criar_comunidade():
        data = request.json
        nome = data.get("nome")
        descricao = data.get("descricao")
        nova = Comunidade(nome=nome, descricao=descricao)
        db.session.add(nova)
        db.session.commit()
        return jsonify({"mensagem": f"Comunidade {nome} criada com sucesso!"})

    # Listar comunidades
    @app.route("/comunidades", methods=["GET"])
    def listar_comunidades():
        comunidades = Comunidade.query.all()
        lista = [{"id": c.id, "nome": c.nome, "descricao": c.descricao} for c in comunidades]
        return jsonify(lista)

    # Entrar em comunidade
    @app.route("/comunidade/<int:comunidade_id>/entrar", methods=["POST"])
    def entrar_comunidade(comunidade_id):
        data = request.json
        usuario_id = data.get("usuario_id")
        usuario = Usuario.query.get(usuario_id)
        comunidade = Comunidade.query.get(comunidade_id)
        if not usuario or not comunidade:
            return jsonify({"erro": "Usuário ou comunidade não encontrado"}), 404
        comunidade.membros.append(usuario)
        db.session.commit()
        return jsonify({"mensagem": f"{usuario.nome} entrou na comunidade {comunidade.nome}!"})

    # Enviar scrap (recado)
    @app.route("/scrap", methods=["POST"])
    def enviar_scrap():
        data = request.json
        autor_id = data.get("autor_id")
        destino_id = data.get("destino_id")
        mensagem = data.get("mensagem")

        scrap = Scrap(mensagem=mensagem, autor_id=autor_id, destino_id=destino_id)
        db.session.add(scrap)
        db.session.commit()
        return jsonify({"mensagem": "Scrap enviado com sucesso!"})

    # Listar scraps de um usuário
    @app.route("/scraps/<int:usuario_id>", methods=["GET"])
    def listar_scraps(usuario_id):
        scraps = Scrap.query.filter_by(destino_id=usuario_id).all()
        lista = [{"autor_id": s.autor_id, "mensagem": s.mensagem} for s in scraps]
        return jsonify(lista)
