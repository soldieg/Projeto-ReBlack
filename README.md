# ReBlack-PS2 — BLACK de PlayStation 2 para PC

O ReBlack-PS2 acompanha a engenharia reversa e a decompilação de *BLACK* para **PlayStation 2**. O escopo é a arquitetura do console: Emotion Engine (EE/R5900), IOP e unidades vetoriais VU. Nenhuma outra versão ou plataforma faz parte deste projeto.

Este repositório publica documentação e progresso. Ele não distribui a imagem do jogo, executáveis, arquivos extraídos, dumps de memória ou código derivado do jogo.

## Current Status

- **Cobertura global:** ainda sem percentual confiável. O inventário completo de funções únicas do EE, IOP e VU e seu denominador ainda não foram fechados.
- **decomp.dev — EE/R5900 provisório:** o catálogo Ghidra reúne 9.842 funções e 2.584.776 bytes de corpo. Há 31 funções exatas (376 bytes) e 2 resultados parciais (65 bytes); os 441 bytes fuzzy equivalem a 0,0171% deste catálogo provisório. IOP e VU/DVP não entram nessa medida; ela não é cobertura global do PS2. O painel está sincronizado no commit `e1d6e10`, exibe 0,02% decompilado e 0,01% totalmente ligado, e fica fora das listagens até alcançar o limite de 0,5%; veja [estado, método e sincronização](DECOMPDEV.md).
- **IOP:** 25/25 módulos ELF do inventário inicial foram importados e analisados no projeto IOP separado; a cobertura de funções ainda não foi medida.
- **VU/DVP:** 88/88 arquivos do lote inicial foram desmontados com o vudis. Isso é inventário de instruções, não contagem de funções decompiladas.
- **PCSX2:** execuções documentadas observaram gameplay e a tela `LOADING` no jogo original; são evidências de runtime, não de cobertura de código.
- **decomp.dev:** o workflow gera o Report v2 a partir de dados sanitizados e publica no `main`; a página direta está sincronizada no commit `e1d6e10`.

## Project Documents

- [Project status](STATUS.md) — estado, medidas verificáveis e limitações de cada frente PS2.
- [Evidence](EVIDENCIAS.md) — resultados resumidos de análise estática e observação no PCSX2.
- [Roadmap](ROADMAP.md) — próximos passos rastreáveis para EE, IOP, VU e runtime.
- [Updates](ATUALIZACOES.md) — histórico dos marcos e mudanças do projeto.
- [decomp.dev integration](DECOMPDEV.md) — catálogo EE provisório, métricas, limites e sincronização do painel.

## Reference and Tools

- [Ghidra](https://github.com/NationalSecurityAgency/ghidra) — análise estática de executáveis e módulos PlayStation 2, incluindo EE/R5900.
- [PCSX2](https://github.com/PCSX2/pcsx2) — execução do jogo original e observação dinâmica em runtime.
- **vudis** — desmontagem inicial de dados VU/DVP; seus arquivos e contagens não são tratados como funções decompiladas.
- [objdiff](https://github.com/encounter/objdiff) — formato do relatório de progresso por função.
- **GitHub Actions** — valida os dados e gera o relatório Report v2 para a integração de progresso.
- **Registro de função validada** — `tools/record_validated_functions.py` cria uma alteração só de metadados; Actions valida o PR e, após merge, atualiza o artefato consumido pelo painel. Veja [passo a passo e modelo](DECOMPDEV.md#registrar-uma-função-validada).
- [decomp.dev](https://decomp.dev/) e [decomp.wiki](https://decomp.wiki/tools/decomp-dev) — destino do painel de progresso e documentação do fluxo de integração.
- [REA](https://github.com/morluto/rea) — avaliado no fluxo PS2; o provedor disponível recusou o alvo ELF/MIPS nesta execução, então não há resultado independente do REA contado como decompilação.

## AI Assistance

- [OpenAI Codex](https://openai.com/codex/) — apoio à organização das evidências, análise técnica e documentação, com resultados sujeitos à verificação registrada no projeto.
