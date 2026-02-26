let usuarioLogado = 1; // por enquanto fixo, depois podemos integrar login

// Carregar perfil
async function carregarPerfil() {
    if (!usuarioLogado) return;
    const resposta = await fetch(`http://127.0.0.1:5000/usuario/${usuarioLogado}`);
    const perfil = await resposta.json();
    const container = document.getElementById("perfil-container");
    container.innerHTML = `
        <img src="${perfil.foto}" alt="Foto de perfil" width="100">
        <p><strong>${perfil.nome}</strong></p>
        <p>Email: ${perfil.email}</p>
        <p>Pontos: ${perfil.pontos}</p>
        <p>Comunidades: ${perfil.comunidades.join(", ")}</p>
    `;
}

// Carregar comunidades
async function carregarComunidades() {
    const resposta = await fetch("http://127.0.0.1:5000/comunidades");
    const comunidades = await resposta.json();
    const container = document.getElementById("comunidades-container");
    container.innerHTML = "";
    comunidades.forEach(c => {
        const div = document.createElement("div");
        div.className = "comunidade";
        div.innerHTML = `
            <h3>${c.nome}</h3>
            <p>${c.descricao}</p>
            <button onclick="entrarComunidade(${c.id})">Entrar 🌸</button>
        `;
        container.appendChild(div);
    });
}

// Entrar em comunidade
async function entrarComunidade(comunidadeId) {
    if (!usuarioLogado) {
        alert("Você precisa estar logado!");
        return;
    }
    await fetch(`http://127.0.0.1:5000/comunidade/${comunidadeId}/entrar`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({usuario_id: usuarioLogado})
    });
    carregarPerfil();
}

// Scraps
document.getElementById("scrap-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const mensagem = document.getElementById("scrap-msg").value;
    await fetch("http://127.0.0.1:5000/scrap", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({autor_id: usuarioLogado, destino_id: usuarioLogado, mensagem})
    });
    document.getElementById("scrap-msg").value = "";
    carregarScraps();
});

async function carregarScraps() {
    if (!usuarioLogado) return;
    const resposta = await fetch(`http://127.0.0.1:5000/scraps/${usuarioLogado}`);
    const scraps = await resposta.json();
    const container = document.getElementById("scraps-container");
    container.innerHTML = "";
    scraps.forEach(s => {
        const div = document.createElement("div");
        div.className = "scrap";
        div.innerHTML = `<p>${s.mensagem}</p>`;
        container.appendChild(div);
    });
}

// Inicialização
window.onload = () => {
    carregarPerfil();
    carregarComunidades();
    carregarScraps();
};
