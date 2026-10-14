# Atualizações do painel

## 14/10/2026 — marcos PCSX2 #507 e #508

- A execução #507 registrou visualmente uma cena de gameplay do jogo original, com HUD e arma.
- A execução #508 confirmou a solicitação `Loading_screen` por registradores e capturou a tela animada `LOADING` após retomar a mesma VM.
- A correlação exata do record APT e dos pacotes GS segue pendente; os marcos não medem percentual de decompilação.
- O decomp.dev foi avaliado conforme a wiki oficial. A sincronização automática depende de relatório `objdiff`, artefato de GitHub Actions e cadastro do projeto. A base local ainda não tem objetos de referência/base nem inventário completo para gerar um relatório fiel; veja [DECOMPDEV.md](DECOMPDEV.md).

## 11/10/2026 — criação do acompanhamento privado

- Criado o repositório privado [soldieg/Projeto-ReBlack](https://github.com/soldieg/Projeto-ReBlack).
- Adicionado painel inicial, roteiro, resumo de evidências, orientação para piloto no decomp.me e estas regras de atualização.
- O percentual global ficou pendente até existir inventário completo de funções únicas. Percentuais de conjuntos delimitados permanecem identificados como locais àquele conjunto.
- Criadas quatro tarefas no GitHub: inventário global (#4), validação da amostra Unit no PCSX2 (#3), trilha StUnit/Unit (#2) e viabilidade do decomp.me (#1).
- Base documental: status local da decompilação até a execução #502.
