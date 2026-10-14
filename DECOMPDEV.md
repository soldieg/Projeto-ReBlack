# Integração com decomp.dev

**Estado em 14/10/2026: ainda não sincronizado.** O decomp.dev publica relatórios de progresso de decompilações matching; não é um espelho deste painel de pesquisa.

## O que a wiki exige

O [guia oficial](https://decomp.wiki/tools/decomp-dev) descreve este fluxo:

1. Preparar objetos-alvo que representem a versão matching e objetos-base compilados das fontes reconstruídas.
2. Gerar `objdiff.json` com todas as unidades ligadas ao executável, caminhos de alvo/base e `base_path: null` quando ainda não existir fonte.
3. Gerar `build/report.json` com `objdiff-cli report generate`.
4. Publicar o arquivo em GitHub Actions como artefato chamado `<versão>_report` — para este projeto, a versão proposta é `SLUS_213.76_report`.
5. Depois que houver relatórios no branch padrão, um administrador do repositório pode cadastrar o projeto em `https://decomp.dev/manage/new`.
6. Opcionalmente instalar o app do decomp.dev no repositório para receber eventos de conclusão de workflows e configurar comentários em PRs.

## Situação verificada neste repositório

- A branch `main` contém documentação do projeto e o mapa SVG; não contém pipeline de build, `objdiff.json`, objetos-alvo/base ou workflow de GitHub Actions.
- O status do projeto ainda declara pendente o inventário completo de funções únicas do EE, IOP e VU. Sem esse denominador, não há relatório global reproduzível.
- As evidências #507–#508 são observações do jogo original no PCSX2. Elas não podem ser contadas como unidades matching no `objdiff`.
- O README registra o repositório como privado. A página de progresso do decomp.dev é pública; antes do cadastro e da instalação do app, é necessário conferir que informações do projeto e do commit ficarão visíveis e quais permissões o app solicitará.
- O conector GitHub do Codex não tem conta conectada nesta sessão. A leitura do clone foi possível pelo Git local; a área de gerenciamento do decomp.dev redirecionou para autenticação do GitHub e ainda não foi aberta como sessão autenticada.

## Próximos passos

1. Concluir a contagem de unidades por módulo, preservando aliases e proveniência, como previsto na issue #4.
2. Selecionar uma estratégia de objetos-alvo/base que corresponda ao estado real do código. Não inferir objetos comparáveis a partir de mapas Ghidra, dumps ou listas de endereços.
3. Gerar e conferir localmente `objdiff.json` e `report.json`; verificar se as unidades não reconstruídas ficam explicitamente sem base e se desmontagem inline não infla a porcentagem.
4. Criar workflow para gerar o relatório e publicá-lo como artefato `SLUS_213.76_report` no branch padrão.
5. Revisar visibilidade e permissões necessárias. Então cadastrar o projeto em decomp.dev e, se aprovado, instalar o GitHub App e validar a atualização automática com um run real.

Até esses passos serem concluídos, mostrar `0%` no decomp.dev seria enganoso: a cobertura global ainda não foi contada.
