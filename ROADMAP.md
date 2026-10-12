# Roteiro de trabalho

A ordem abaixo reduz repetição e cria uma medida real de cobertura antes de prometer um percentual global. As tarefas abertas podem ser acompanhadas pelos links.

## 1. Medir o universo analisável — [Issue #4](https://github.com/soldieg/Projeto-ReBlack/issues/4)

- Inventariar funções únicas nos módulos EE, IOP e VU.
- Remover duplicatas de overlays e aliases sem apagar a procedência.
- Classificar cada função com um estado e uma evidência.
- Publicar totais por módulo. A partir daí, calcular percentuais com denominador explícito.

**Condição de saída:** cada módulo tem total contado, quantidade por estado e origem reproduzível.

## 2. Fechar a validação runtime da amostra Unit — [Issue #3](https://github.com/soldieg/Projeto-ReBlack/issues/3)

- Escolher um slot C0 não nulo que possa ser inspecionado sem avançar o save.
- Em um checkpoint controlado do PCSX2, conferir o endereço relocacionado contra a RAM.
- Inspecionar os campos vizinhos e a tabela aninhada; registrar limites válidos e falhas.
- Marcar cada resultado como observado, hipótese ou ainda sem evidência.

**Condição de saída:** os casos da amostra #500 têm explicação ou permanecem explicitamente pendentes.

## 3. Continuar a trilha StUnit/Unit — [Issue #2](https://github.com/soldieg/Projeto-ReBlack/issues/2)

Reusar as análises #409–#413. Seguir a origem das chaves e a escrita/leitura da lista de objetos filhos; manter a investigação dos campos-raiz +0x40/+0x48 separada até existir ligação de dados demonstrada.

**Condição de saída:** cada ligação afirmada tem produtor, consumidor e evidência binária ou runtime compatível.

## 4. Validar reconstruções pontuais

- Selecionar funções pequenas e com bytes de referência preservados.
- Documentar endereço, tamanho, compilador, flags e método de comparação.
- Marcar “correspondência exata” somente quando a comparação reproduzir todos os bytes do escopo.
- Não extrapolar uma função exata para a toolchain original ou para o jogo inteiro sem evidência.

## 5. Fazer um piloto controlado no decomp.me — [Issue #1](https://github.com/soldieg/Projeto-ReBlack/issues/1)

- Conferir se há preset ou compilador compatível com EE/R5900 e com a versão/flags relevantes.
- Revisar a visibilidade e o tratamento do conteúdo enviado.
- Registrar no GitHub o scratch, preset, tamanho do alvo, resultado de correspondência e decisão.
- Não tratar um bom match como validação runtime.

**Condição de saída:** um scratch reproduzível ajuda numa função PS2 específica sem confundir o resultado com cobertura global.

## 6. Atualizar o painel

Em cada avanço importante, atualizar [STATUS.md](STATUS.md), registrar os dados e limites em [EVIDENCIAS.md](EVIDENCIAS.md) e incluir uma entrada em [ATUALIZACOES.md](ATUALIZACOES.md). Um número só entra como percentual quando numerador e denominador estiverem definidos.
