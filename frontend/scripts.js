// Função para carregar feed
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

// Registro de favor
document.getElementById("favor-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const usuario_id = document.getElementById("usuario_id").value;
    const descricao = document.getElementById("descricao").value;

    try {
        const resposta = await fetch("http://127.0.0.1:5000/favor", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({usuario_id, descricao})
        });
        const resultado = await resposta.json();
        document.getElementById("favor-msg").innerText = resultado.mensagem;
        carregarFeed();
    } catch (erro) {
        console.error("Erro ao registrar favor:", erro);
    }
});

// Carregar feed ao abrir página
window.onload = carregarFeed;
