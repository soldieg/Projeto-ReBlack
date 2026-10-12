# Projeto ReBlack

Acompanhamento privado da engenharia reversa e decompilação da versão PlayStation 2 de BLACK.

> Este repositório é um painel de progresso e documentação. Ele não contém a ISO, arquivos extraídos do jogo, executáveis, dumps de memória ou pseudocódigo derivado do jogo.

## Mapa de arquivos

![Treemap dos 88 arquivos assembly VU1 desmontados](MAPA-PROGRESSO.svg)

Cada retângulo corresponde a um arquivo assembly gerado pelo vudis. A área acompanha o tamanho em bytes; os tons agrupam arquivos pela origem. Passe o cursor sobre um bloco para ver nome, seção de origem, endereço, tamanho e estado. O mapa representa a desmontagem VU1 documentada, não o progresso de decompilação de todo o jogo.

## Situação do projeto

- **Progresso global:** ainda sem percentual confiável. Falta inventariar todas as funções únicas do executável e classificá-las; os números abaixo são escopos específicos.
- **Módulos IOP:** 25/25 módulos ELF do mapa inicial importados e analisados no projeto IOP separado. A cobertura de funções ainda precisa ser medida.
- **VU1 / DVP:** 88/88 arquivos desmontados, 151.472 bytes, 18.934 pares, 222 pares com flag I e 83 com flag E; 0 instruções desconhecidas e 0 falhas no relatório do vudis. A identificação de linguagem VU1 no Ghidra e a interpretação semântica continuam pendentes.
- **Amostra Unit #500/#502:** 292 slots analisados. Foram encontrados 152 ponteiros C0 não nulos: 138 apontam para fora dos arquivos extraídos e 14 para dentro. Entre os 14 internos, 11 tabelas têm limites plausíveis e 3 casos seguem com limites inválidos. A validação desses alvos na RAM do PCSX2 está pendente.
- **Integridade da amostra Unit:** hashes e tamanhos de 42/42 arquivos conferidos.
- **Reconstrução comparada:** uma região de 36 bytes tem correspondência exata documentada. Isso ainda não confirma a toolchain original.
- **Comparação REA/Ghidra (#502):** a comparação e a repetição das consultas Ghidra foram registradas; o provedor REA no Windows recusou o alvo antes da análise independente. Nenhuma função nova foi confirmada nessa execução.

## Próximas etapas

1. Inventariar as funções únicas do EE, IOP e VU e atribuir estado e evidência a cada uma.
2. Validar em RAM do PCSX2 os alvos C0 pendentes da amostra Unit.
3. Confirmar uma toolchain compatível e ampliar a reconstrução comparada para funções selecionadas.
4. Reavaliar o piloto de decomp.me quando o compilador EE/R5900 e as condições de exposição dos dados estiverem confirmados.

Os relatórios completos permanecem na pasta local privada de resultados. Para critérios, evidências resumidas e atualizações, consulte [STATUS.md](STATUS.md), [EVIDENCIAS.md](EVIDENCIAS.md), [ROADMAP.md](ROADMAP.md) e [ATUALIZACOES.md](ATUALIZACOES.md).
