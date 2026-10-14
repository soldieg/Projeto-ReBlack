# ReBlack-PS2 — BLACK para PlayStation 2

Projeto de engenharia reversa e decompilação de **BLACK para PlayStation 2**. O escopo técnico é o Emotion Engine (EE/R5900), o IOP e as unidades vetoriais VU; o projeto não acompanha outra plataforma.

> Este repositório é um painel de progresso e documentação. Ele não contém a ISO, arquivos extraídos do jogo, executáveis, dumps de memória ou pseudocódigo derivado do jogo.

## Progresso da decompilação

- **Piloto do decomp.dev:** uma unidade EE, FUN_001ABEB8, com 40/40 bytes correspondentes no relatório piloto. O workflow do branch padrão já gera o artefato `SLUS_213.76_report`; o cadastro e a leitura no painel ainda precisam ser confirmados. O alvo foi reconstruído localmente e ligado contra a referência; objetos e bytes do jogo não são enviados. Esse 100% se aplica somente à unidade do piloto e não mede a cobertura do jogo. Veja [evidências, método e limites](DECOMPDEV.md).
- **Cobertura global:** ainda sem percentual confiável. Falta inventariar todas as funções únicas do executável e definir um denominador completo; os números abaixo pertencem a escopos específicos.

## Situação do projeto

- **Módulos IOP:** 25/25 módulos ELF do inventário inicial importados e analisados no projeto IOP separado. A cobertura de funções ainda precisa ser medida.
- **VU1 / DVP:** 88/88 arquivos desmontados, 151.472 bytes, 18.934 pares, 222 pares com flag I e 83 com flag E; 0 instruções desconhecidas e 0 falhas no relatório do vudis. A identificação de linguagem VU1 no Ghidra e a interpretação semântica continuam pendentes.
- **Amostra Unit #500/#502:** 292 slots analisados. Foram encontrados 152 ponteiros C0 não nulos: 138 apontam para fora dos arquivos extraídos e 14 para dentro. Entre os 14 internos, 11 tabelas têm limites plausíveis e 3 casos seguem com limites inválidos. A validação desses alvos na RAM do PCSX2 está pendente.
- **Integridade da amostra Unit:** hashes e tamanhos de 42/42 arquivos conferidos.
- **Reconstrução comparada:** uma região de 36 bytes tem correspondência exata documentada. Isso ainda não confirma a toolchain original.
- **Comparação REA/Ghidra (#502):** a comparação e a repetição das consultas Ghidra foram registradas; o provedor REA no Windows recusou o alvo antes da análise independente. Nenhuma função nova foi confirmada nessa execução.
- **Execuções #507–#508:** capturas do PCSX2 confirmam uma cena em primeira pessoa com HUD e, depois, a própria tela animada `LOADING`. Isso documenta o jogo original rodando no emulador; não é um port para PC nem um percentual de decompilação.

O relatório piloto do objdiff é gerado a partir de métricas auditadas em `docs/decompdev/progress.json`. O workflow do GitHub Actions está ativo no branch padrão e publica o artefato `SLUS_213.76_report`; falta conferir o cadastro e a sincronização do painel. O inventário completo de unidades ainda não existe, portanto a cobertura global continua sem percentual. Consulte [DECOMPDEV.md](DECOMPDEV.md) para os requisitos e o estado da sincronização.

## Próximas etapas

1. Inventariar as funções únicas do EE, IOP e VU e atribuir estado e evidência a cada uma.
2. Validar em RAM do PCSX2 os alvos C0 pendentes da amostra Unit.
3. Confirmar uma toolchain compatível e ampliar a reconstrução comparada para funções selecionadas.
4. Reavaliar o piloto de decomp.me quando o compilador EE/R5900 e as condições de exposição dos dados estiverem confirmados.

Os relatórios completos permanecem na pasta local privada de resultados. Para critérios, evidências resumidas e atualizações, consulte [STATUS.md](STATUS.md), [EVIDENCIAS.md](EVIDENCIAS.md), [ROADMAP.md](ROADMAP.md) e [ATUALIZACOES.md](ATUALIZACOES.md).

## Project Documents

- [Status do projeto](STATUS.md) — avanço verificável, limites e próximos passos por frente PS2.
- [Evidências](EVIDENCIAS.md) — resultados de Ghidra e PCSX2, com escopo e limitações.
- [Roteiro de trabalho](ROADMAP.md) — tarefas rastreáveis para EE, IOP, VU e validação runtime.
- [Atualizações](ATUALIZACOES.md) — histórico resumido das mudanças e marcos do projeto.
- [Integração com decomp.dev](DECOMPDEV.md) — relatório objdiff, piloto e estado da sincronização.
- [Avaliação do decomp.me](DECOMPME.md) — compatibilidade e condições para um piloto seguro no EE/R5900.

## Reference and Tools

- **Ghidra 12.1.3** — análise estática dos executáveis e módulos PS2, incluindo EE/R5900.
- **PCSX2** — observação dinâmica do jogo original e validação de hipóteses em runtime.
- **objdiff-cli 3.8.2** — comparação pontual de objetos reconstruídos; o resultado atual cobre somente a função piloto listada em `DECOMPDEV.md`.
- **GitHub Actions** — validação do relatório e geração do artefato Report v2 usado na integração de progresso.
- **decomp.dev** — destino planejado para exibir o progresso decompilado; o cadastro e a leitura do relatório ainda precisam ser confirmados.
- **vudis** — inventário e desmontagem inicial dos dados VU/DVP; esses resultados não são contados como funções decompiladas.

As referências e ferramentas listadas aqui correspondem ao fluxo de PlayStation 2 documentado neste repositório. Resultados de desmontagem, capturas do emulador e métricas de conjuntos isolados não representam, por si só, cobertura global de decompilação.
