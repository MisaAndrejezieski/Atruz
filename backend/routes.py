from flask import request, jsonify

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
        return jsonify({"mensagem": f"Usuário {nome} cadastrado com sucesso!"})

    # Registrar favor
    @app.route("/favor", methods=["POST"])
    def favor():
        data = request.json
        descricao = data.get("descricao")
        return jsonify({"mensagem": f"Favor registrado: {descricao}"})

    # Consultar pontos
    @app.route("/pontos/<usuario>", methods=["GET"])
    def pontos(usuario):
        # Por enquanto, valor fixo (vamos ligar ao banco depois)
        return jsonify({"usuario": usuario, "pontos": 10})
