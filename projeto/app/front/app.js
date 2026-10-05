const API_URL = "http://127.0.0.1:8000";


// ==========================================================
// CARREGAR TAREFAS
// ==========================================================

async function carregarTarefas() {

    const status =
        document.getElementById("filtroStatus").value;

    const prioridade =
        document.getElementById("filtroPrioridade").value;

    const responsavel =
        document.getElementById("filtroResponsavel").value;


    const params = new URLSearchParams();


    if (status) {
        params.append("status", status);
    }


    if (prioridade) {
        params.append("prioridade", prioridade);
    }


    if (responsavel) {
        params.append("responsavel", responsavel);
    }


    let url = `${API_URL}/tarefas/`;

    if (params.toString()) {
        url += `?${params.toString()}`;
    }


    try {

        const resposta = await fetch(url);

        const tarefas = await resposta.json();

        mostrarTarefas(tarefas);

    } catch (erro) {

        console.error("Erro ao carregar tarefas:", erro);

        alert("Não foi possível conectar com a API.");

    }
}


// ==========================================================
// MOSTRAR TAREFAS
// ==========================================================

function mostrarTarefas(tarefas) {

    const lista =
        document.getElementById("listaTarefas");


    lista.innerHTML = "";


    tarefas.forEach(tarefa => {

        const card =
            document.createElement("div");

        card.className = "card";


        // ==============================
        // STATUS
        // ==============================

        let classeStatus =
            tarefa.status
                .replaceAll(" ", "-")
                .replace("í", "i");


        // ==============================
        // TAGS
        // ==============================

        const tagsHTML =
            tarefa.tags && tarefa.tags.length > 0

                ? tarefa.tags
                    .map(tag =>
                        `<span class="tag-badge">${tag}</span>`
                    )
                    .join("")

                : "";


        // ==============================
        // BOTÃO CONCLUIR
        // ==============================

        let botaoConcluir = "";


        if (
            tarefa.status !== "concluída" &&
            tarefa.status !== "cancelada"
        ) {

            botaoConcluir = `
                <button
                    class="btn-concluir"
                    onclick="concluirTarefa(${tarefa.id})"
                >
                    Concluir
                </button>
            `;

        }


        // ==============================
        // CARD
        // ==============================

        card.innerHTML = `

            <h3>
                ${tarefa.titulo}
            </h3>


            <div class="informacoes">

                <span class="status ${classeStatus}">
                    ${tarefa.status}
                </span>

                <span>
                    ${tarefa.prioridade}
                </span>

                <span>
                    ${tarefa.responsavel}
                </span>

            </div>


            <div class="tags">
                ${tagsHTML}
            </div>


            <div class="acoes">

                ${botaoConcluir}

                <button
                    class="btn-remover"
                    onclick="removerTarefa(${tarefa.id})"
                >
                    Remover
                </button>

            </div>

        `;


        lista.appendChild(card);

    });


    atualizarEstatisticas();

}


// ==========================================================
// ESTATÍSTICAS
// ==========================================================

async function atualizarEstatisticas() {

    try {

        const resposta =
            await fetch(
                `${API_URL}/tarefas/estatisticas`
            );

        const dados =
            await resposta.json();


        document.getElementById(
            "estatisticas"
        ).innerText =

            `Total: ${dados.total} | ` +
            `Pendentes: ${dados.pendentes} | ` +
            `Em andamento: ${dados.em_andamento} | ` +
            `Concluídas: ${dados.concluidas}`;

    } catch (erro) {

        console.error(erro);

    }
}


// ==========================================================
// CONCLUIR TAREFA
// ==========================================================

async function concluirTarefa(id) {

    try {

        const resposta =
            await fetch(
                `${API_URL}/tarefas/${id}/status`,
                {
                    method: "PATCH",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        status: "concluída"
                    })
                }
            );


        if (!resposta.ok) {

            const erro =
                await resposta.json();

            alert(erro.detail);

            return;
        }


        carregarTarefas();

    } catch (erro) {

        console.error(erro);

        alert("Erro ao concluir tarefa.");

    }
}


// ==========================================================
// REMOVER TAREFA
// ==========================================================

async function removerTarefa(id) {

    const confirmar =
        confirm(
            "Deseja realmente remover esta tarefa?"
        );


    if (!confirmar) {
        return;
    }


    try {

        const resposta =
            await fetch(
                `${API_URL}/tarefas/${id}`,
                {
                    method: "DELETE"
                }
            );


        if (!resposta.ok) {

            alert("Erro ao remover tarefa.");

            return;
        }


        carregarTarefas();

    } catch (erro) {

        console.error(erro);

        alert("Erro ao remover tarefa.");

    }
}


// ==========================================================
// ABRIR FORMULÁRIO
// ==========================================================

function abrirFormulario() {

    document
        .getElementById("formulario")
        .classList.remove("escondido");
}


// ==========================================================
// FECHAR FORMULÁRIO
// ==========================================================

function fecharFormulario() {

    document
        .getElementById("formulario")
        .classList.add("escondido");
}


// ==========================================================
// CRIAR TAREFA
// ==========================================================

async function criarTarefa() {

    const titulo =
        document.getElementById("titulo").value;

    const descricao =
        document.getElementById("descricao").value;

    const responsavel =
        document.getElementById("responsavel").value;

    const prioridade =
        document.getElementById("prioridade").value;

    const tagsTexto =
        document.getElementById("tags").value;


    const tags =
        tagsTexto
            .split(",")
            .map(tag => tag.trim())
            .filter(tag => tag.length > 0);


    if (!titulo || !descricao || !responsavel) {

        alert(
            "Preencha título, descrição e responsável."
        );

        return;
    }


    const novaTarefa = {

        titulo: titulo,

        descricao: descricao,

        responsavel: responsavel,

        prioridade: prioridade,

        status: "pendente",

        tags: tags

    };


    try {

        const resposta =
            await fetch(
                `${API_URL}/tarefas/`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(novaTarefa)
                }
            );


        if (!resposta.ok) {

            const erro =
                await resposta.json();

            alert(
                erro.detail ||
                "Erro ao criar tarefa."
            );

            return;
        }


        document.getElementById("titulo").value = "";

        document.getElementById("descricao").value = "";

        document.getElementById("responsavel").value = "";

        document.getElementById("tags").value = "";


        fecharFormulario();

        carregarTarefas();

    } catch (erro) {

        console.error(erro);

        alert("Erro ao conectar com a API.");

    }
}


// ==========================================================
// INICIAR
// ==========================================================

carregarTarefas();