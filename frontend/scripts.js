let usuarioLogado = null;

// Carregar feed
async function carregarFeed() {
    try {
        const resposta = await fetch("http://127.0.0.1:5000/feed");
        const favores = await resposta.json();

        const container = document.getElementById("feed-container");
        container.innerHTML = "";

        favores.forEach(favor => {
            const card = document.createElement("div");
            card.className = "post";
            card.innerHTML = `
                <h3>@${favor.usuario}</h3>
                <p>${favor.descricao}</p>
                <p>Status: ${favor.status}</p>
                <button>Participar 🤝</button>
            `;
            container.appendChild(card);
        });
    } catch (erro) {
        console.error("Erro ao carregar feed:", erro);
    }
}

// Cadastro de usuário
document.getElementById("cadastro-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;

    try {
        const resposta = await fetch("http://127.0.0.1:5000/cadastro", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({nome, email})
        });
        const resultado = await resposta.json();
        document.getElementById("cadastro-msg").innerText = resultado.mensagem;
        carregarFeed();
    } catch (erro) {
        console.error("Erro no cadastro:", erro);
    }
});

// Login
document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("login-email").value;

    try {
        const resposta = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({email})
        });
        const resultado = await resposta.json();

        if (resultado.usuario_id) {
            usuarioLogado = resultado.usuario_id;
            document.getElementById("login-msg").innerText = `Bem-vindo, ${resultado.nome}!`;
        } else {
            document.getElementById("login-msg").innerText = resultado.erro;
        }
    } catch (erro) {
        console.error("Erro no login:", erro);
    }
});

// Registrar favor
document.getElementById("favor-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const descricao = document.getElementById("descricao").value;

    if (!usuarioLogado) {
        document.getElementById("favor-msg").innerText = "Você precisa estar logado para registrar um favor.";
        return;
    }

    try {
        const resposta = await fetch("http://127.0.0