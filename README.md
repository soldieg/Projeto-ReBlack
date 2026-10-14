# ReBlack-PS2 — BLACK para PlayStation 2

O ReBlack-PS2 acompanha a engenharia reversa e a decompilação de *BLACK* para **PlayStation 2**. O escopo é a arquitetura do console: Emotion Engine (EE/R5900), IOP e unidades vetoriais VU. Nenhuma outra versão ou plataforma faz parte deste projeto.

Este repositório publica documentação e progresso. Ele não distribui a imagem do jogo, executáveis, arquivos extraídos, dumps de memória ou código derivado do jogo.

## Current Status

- **Cobertura global:** ainda sem percentual confiável. O inventário completo de funções únicas do EE, IOP e VU e seu denominador ainda não foram fechados.
- **Piloto de decomp.dev:** o relatório cobre uma função EE, `FUN_001ABEB8`, com 40/40 bytes e 1/1 função correspondentes. Os 100% são apenas dessa unidade de piloto, não do executável nem do jogo.
- **IOP:** 25/25 módulos ELF do inventário inicial foram importados e analisados no projeto IOP separado; a cobertura de funções ainda não foi medida.
- **VU/DVP:** 88/88 arquivos do lote inicial foram desmontados com o vudis. Isso é inventário de instruções, não contagem de funções decompiladas.
- **PCSX2:** execuções documentadas observaram gameplay e a tela `LOADING` no jogo original; são evidências de runtime, não de cobertura de código.
- **decomp.dev:** o GitHub Actions gera o artefato do relatório piloto. O cadastro do repositório e a leitura do relatório no painel ainda precisam ser confirmados.

## Project Documents

- [Project status](STATUS.md) — estado, medidas verificáveis e limitações de cada frente PS2.
- [Evidence](EVIDENCIAS.md) — resultados resumidos de análise estática e observação no PCSX2.
- [Roadmap](ROADMAP.md) — próximos passos rastreáveis para EE, IOP, VU e runtime.
- [Updates](ATUALIZACOES.md) — histórico dos marcos e mudanças do projeto.
- [decomp.dev integration](DECOMPDEV.md) — formato do relatório, evidência do piloto e situação da sincronização.

## Reference and Tools

- [Ghidra](https://github.com/NationalSecurityAgency/ghidra) — análise estática de executáveis e módulos PlayStation 2, incluindo EE/R5900.
- [PCSX2](https://github.com/PCSX2/pcsx2) — execução do jogo original e observação dinâmica em runtime.
- **vudis** — desmontagem inicial de dados VU/DVP; seus arquivos e contagens não são tratados como funções decompiladas.
- [objdiff](https://github.com/encounter/objdiff) — comparação do piloto de uma função; o relatório publicado é limitado a esse escopo.
- **GitHub Actions** — valida os dados e gera o relatório Report v2 para a integração de progresso.
- [decomp.dev](https://decomp.dev/) e [decomp.wiki](https://decomp.wiki/tools/decomp-dev) — destino do painel de progresso e documentação do fluxo de integração.
- [REA](https://github.com/morluto/rea) — avaliado no fluxo PS2; o provedor disponível recusou o alvo ELF/MIPS nesta execução, então não há resultado independente do REA contado como decompilação.

## AI Assistance

- [OpenAI Codex](https://openai.com/codex/) — apoio à organização das evidências, análise técnica e documentação, com resultados sujeitos à verificação registrada no projeto.
