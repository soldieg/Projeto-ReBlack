# Piloto de progresso do Projeto ReBlack no decomp.dev

**Data:** 2026-10-14
**Estado:** proposta para revisão
**Repositório:** `soldieg/Projeto-ReBlack`

## Objetivo

Substituir o mapa estático que conta arquivos assembly VU1 por uma prova de conceito do painel nativo do decomp.dev, alimentado por relatórios do objdiff. A visualização deve representar unidades realmente reconstruídas e comparadas com o jogo, e não arquivos desmontados.

O piloto valida o fluxo de dados de ponta a ponta para um escopo pequeno e claramente identificado. Não deve ser apresentado como percentual de decompilação global.

## Contexto confirmado

- O README atual descreve um SVG estático de 88 arquivos VU1 e registra que todos passaram pela etapa de desmontagem. Isso não é medida de reconstrução matching.
- Este repositório contém documentação, mas ainda não contém `objdiff.json`, objetos-alvo/base, relatório objdiff ou workflow de GitHub Actions.
- O inventário global de funções/unidades ainda está incompleto. Os totais existentes pertencem a escopos e ferramentas diferentes e não formam um denominador global confiável.
- A integração do decomp.dev consome relatórios objdiff publicados pelo GitHub Actions. O cadastro privado pode exigir a instalação do GitHub App e permissões no repositório.

## Abordagens consideradas

1. **Painel nativo do decomp.dev (selecionado):** gerar relatórios objdiff no GitHub Actions e usar o painel do serviço. Mantém uma única interface de progresso e evita duplicar a visualização.
2. **Aplicativo próprio no GitHub Pages:** permitiria controlar o mapa, mas criaria uma interface e sincronização adicionais.
3. **SVG gerado no GitHub:** seria simples de atualizar, mas continuaria sendo uma imagem incorporada e não daria a navegação do painel nativo.

## Desenho

### Fonte e unidade de progresso

O objdiff será a fonte de estado matching. Cada unidade incluída precisa ter um objeto-alvo correspondente à versão do jogo e um objeto-base produzido a partir da reconstrução. Unidades ainda sem fonte ou sem comparação válida devem permanecer sem base no relatório, em vez de receber estado de conclusão.

O piloto usará somente um conjunto de unidades que tenha proveniência e pares de objetos verificáveis. O escopo, a versão e as limitações desse conjunto deverão aparecer na documentação e no nome/descrição do projeto no decomp.dev. A escolha do conjunto depende de confirmar quais objetos e fontes compatíveis realmente existem; não se presume que os arquivos já encontrados localmente formem um conjunto matching.

O progresso global só poderá ser calculado quando o inventário completo de unidades e seu denominador forem definidos. Dados de EE, IOP e VU não serão somados entre si sem uma regra explícita de unidade e cobertura.

### Fluxo de publicação

1. Preparar e revisar `objdiff.json` para o piloto, com unidades, caminhos de alvo/base e unidades sem base representadas corretamente.
2. Gerar `build/report.json` com `objdiff-cli report generate` e inspecionar o resultado localmente.
3. Adicionar GitHub Actions para gerar o relatório no branch padrão e publicá-lo como artefato no padrão esperado pelo decomp.dev (`<versão>_report`).
4. Confirmar que o artefato publicado pode ser lido pelo decomp.dev; cadastrar o projeto quando os pré-requisitos do serviço estiverem atendidos.
5. Validar uma atualização real do painel usando uma execução concluída do workflow.

### README e documentação

Remover do README o mapa VU1 como indicador de progresso de decompilação. Até que o painel esteja disponível, substituí-lo por um estado textual honesto com o escopo do piloto, a ausência de percentual global e um link para o painel quando cadastrado. Manter os dados de desmontagem VU1 apenas na seção técnica que descreve essa etapa.

Atualizar `DECOMPDEV.md` com o escopo escolhido, os comandos/configuração confirmados, o estado do workflow e evidências da primeira sincronização. Não declarar sincronização concluída antes de verificar o relatório no painel.

### Acesso e privacidade

O repositório continuará privado durante preparação e validação. Se o cadastro privado exigir o GitHub App, a instalação será avaliada com acesso limitado a este repositório e às permissões necessárias; não escolher acesso a todos os repositórios da conta. Alterar a visibilidade para público é uma etapa posterior e separada, após revisão do conteúdo e confirmação explícita no momento da mudança.

## Fora de escopo

- Afirmar ou estimar percentual global antes de fechar o inventário e denominador.
- Tratar desmontagem, importação no Ghidra, análise de RAM, screenshots ou execução no emulador como unidades matching.
- Criar um frontend próprio ou manter simultaneamente um segundo mapa interativo.
- Instalar automaticamente o GitHub App, conceder acesso a todos os repositórios ou tornar o repositório público como parte do piloto.
- Incluir ISO, arquivos extraídos do jogo, dumps de memória ou pseudocódigo derivado no repositório.

## Critérios de aceitação

- O README não apresenta o SVG estático VU1 como mapa de decompilação.
- A documentação distingue claramente o progresso do piloto da cobertura global.
- O relatório objdiff do piloto pode ser regenerado e contém somente unidades com escopo e caminhos de objeto revisados; unidades não reconstruídas não aparecem como matching.
- O workflow no branch padrão publica o artefato de relatório com o nome esperado pelo serviço.
- O painel nativo do decomp.dev mostra o relatório após a sincronização ser validada, e a documentação registra evidência dessa validação.
- O estado de privacidade do repositório permanece privado até uma decisão separada.

## Dependências e riscos

O trabalho de integração depende da existência ou preparação de objetos-alvo e objetos-base compatíveis para o piloto. Se esses objetos não puderem ser identificados com proveniência suficiente, a implementação deve parar antes de gerar métricas e registrar a lacuna; não deve fabricar um relatório de progresso.

O cadastro privado e a sincronização podem depender de permissões do GitHub App do decomp.dev. Essas permissões e a visibilidade pública do repositório não são aprovadas por esta especificação.
