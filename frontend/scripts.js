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

// Carregar feed ao abrir a página
window.onload = carregarFeed;
