# Integração com decomp.dev

**Estado em 14/10/2026: ainda não sincronizado; piloto bloqueado pela ausência de objeto-alvo relocável e entrada segura para o workflow.** O decomp.dev publica relatórios de progresso de decompilações matching; não é um espelho deste painel de pesquisa.

## O que a wiki exige

O [guia oficial](https://decomp.wiki/tools/decomp-dev) descreve este fluxo:

1. Preparar objetos-alvo que representem a versão matching e objetos-base compilados das fontes reconstruídas.
2. Gerar `objdiff.json` com todas as unidades ligadas ao executável, caminhos de alvo/base e `base_path: null` quando ainda não existir fonte.
3. Gerar `build/report.json` com `objdiff-cli report generate`.
4. Publicar o arquivo em GitHub Actions como artefato chamado `<versão>_report` — para este projeto, a versão proposta é `SLUS_213.76_report`.
5. Depois que houver relatórios no branch padrão, um administrador do repositório pode cadastrar o projeto em `https://decomp.dev/manage/new`.
6. Opcionalmente instalar o app do decomp.dev no repositório para receber eventos de conclusão de workflows e configurar comentários em PRs.

## Situação verificada neste repositório

- A branch `main` contém documentação do projeto; o mapa SVG foi removido do estado atual no PR #5. Ainda não contém pipeline de build, `objdiff.json`, objetos-alvo/base ou workflow de GitHub Actions.
- Como o histórico do Git não foi reescrito, o SVG removido ainda pode ser recuperado pelo commit histórico `248931b`, agora visível no repositório público.
- O status do projeto ainda declara pendente o inventário completo de funções únicas do EE, IOP e VU. Sem esse denominador, não há relatório global reproduzível.
- As evidências #507–#508 são observações do jogo original no PCSX2. Elas não podem ser contadas como unidades matching no `objdiff`.
- O repositório GitHub foi tornado público em 14/10/2026. O painel decomp.dev ainda não foi cadastrado e não há relatório de progresso para publicar.
- Antes da mudança de visibilidade, o formulário `decomp.dev/manage/new` não listava este repositório e indicava a instalação do GitHub App para acesso a repositórios privados. A elegibilidade do repositório público no formulário ainda precisa ser conferida depois que existir um artefato de relatório válido.
- A tela de instalação oferece `All repositories` como padrão. Essa opção cobre todos os repositórios atuais e futuros da conta; também existe `Only select repositories`. As permissões mostradas pelo GitHub são leitura de Actions, código e metadados, mais leitura e escrita em issues e pull requests.
- A instalação do GitHub App não foi confirmada nem aplicada. A página do decomp.dev publica relatórios de progresso; o app recebe eventos de workflows e pode comentar em PRs. Como o repositório agora é público, a instalação permanece opcional e pode ser avaliada depois de um workflow de relatório real.

## Pré-flight do piloto decomp.dev — 14/10/2026

**Estado: bloqueado antes da geração do relatório.** Há uma amostra com matching estático exato, `FUN_001ABEB8`: 40/40 bytes no intervalo original `SLUS_213.76` do offset `0xACEB8`, com SHA-256 `b072a1104192ced915e82243dedc5fc3547bd3e62d6b174ef97254d07d2e9182`. A fonte foi compilada com SN Systems ProDG EE GCC 2.95.3-EE (SN BUILD 1.36), `-O2 -G8 -fomit-frame-pointer`; o objeto candidato `FUN_001ABEB8.o` tem SHA-256 `e0e60e4745799ad9b3a25fe0549fd39db9f3a337b99eb38ffd3010bb62b07b3c`. A comparação e o comando estão documentados no material local `03 - RESULTADOS E EVIDENCIAS/INVENTARIO DE FUNCOES/SNPRODG-2.95.3-CONTROLLED-SAMPLES-2026-10-11/FUN_001ABEB8/`.

O material da amostra contém o `.o` candidato e um `function.bin` extraído da seção `.text` do ELF candidato com `ee-objcopy`; a comparação registrada confirma que os 40 bytes coincidem com a janela original do alvo. O objeto-alvo relocável está ausente. O objdiff compara objetos relocáveis (`.o`), conforme a [documentação oficial do objdiff](https://github.com/encounter/objdiff#usage); portanto, o binário de 40 bytes não pode ser apontado como `target_path`. Também não foi identificado um caminho seguro e reproduzível para disponibilizar os objetos privados ao runner do GitHub Actions sem publicá-los como artefatos.

**Decisão do pré-flight:** não criar `objdiff.json`, relatório, workflow ou percentual de piloto até que exista um objeto-alvo relocável comprovado e um método seguro para o runner acessar as entradas. O matching estático de 40 bytes permanece evidência local de uma função, não uma sincronização decomp.dev.
## Próximos passos

1. Concluir a contagem de unidades por módulo, preservando aliases e proveniência, como previsto na issue #4.
2. Selecionar uma estratégia de objetos-alvo/base que corresponda ao estado real do código. Não inferir objetos comparáveis a partir de mapas Ghidra, dumps ou listas de endereços.
3. Gerar e conferir localmente `objdiff.json` e `report.json`; verificar se as unidades não reconstruídas ficam explicitamente sem base e se desmontagem inline não infla a porcentagem.
4. Criar workflow para gerar o relatório e publicá-lo como artefato `SLUS_213.76_report` no branch padrão.
5. Revisar visibilidade e permissões necessárias. Então cadastrar o projeto em decomp.dev e, se aprovado, instalar o GitHub App e validar a atualização automática com um run real.

Até esses passos serem concluídos, mostrar `0%` no decomp.dev seria enganoso: a cobertura global ainda não foi contada.
