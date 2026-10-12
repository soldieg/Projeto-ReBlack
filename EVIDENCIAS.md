# Evidências resumidas

Este arquivo registra conclusões curtas e suas limitações. Os relatórios completos permanecem no diretório local de resultados do projeto; esta cópia não inclui binários do jogo, memória bruta ou código derivado.

## Execução #502 — comparação REA/Ghidra/fluxo combinado

- Mesmo executável ELF/MIPS e mesma cadeia técnica da #500.
- REA 6.4.0 reconheceu o formato ELF/MIPS, mas o provedor Ghidra no Windows recusou o alvo com `target_format_unsupported`; não houve pseudocódigo ou xrefs independentes do REA.
- Ghidra em modo somente leitura repetiu as consultas de quatro funções e chamadores; saída terminou com código 0.
- Recontagem independente confirmou hashes e tamanhos de 42/42 arquivos Unit e os números da amostra #500.
- O fluxo combinado melhora a triagem e o registro, mas não encontrou funções novas nessa execução.
- Relatório local: `04 - RESULTADOS/PCSX2/EXECUCOES/2026-10-11_502-rea-vs-ghidra-comparison/RELATORIO-COMPARACAO-REA-GHIDRA-502.md`.

## Execução #500 — slots Unit e tabelas aninhadas

- Escopo contado: 292 slots da amostra analisada.
- 152 C0 não nulos; 138 alvos fora dos arquivos extraídos e 14 dentro.
- Entre os 14 internos: 11 descritores com limites plausíveis e 3 casos ainda com limites inválidos.
- Integridade: hashes e tamanhos de 42/42 arquivos Unit foram rechecados.
- Esses números descrevem somente o conjunto amostrado; não estimam o executável todo.
- Relatório local: `04 - RESULTADOS/PCSX2/EXECUCOES/2026-10-04_500-unit-tail-nested-table-audit/`.

## Outras frentes registradas no status local

- IOP: 25 módulos ELF do mapa inicial importados e analisados no projeto separado.
- VU/DVP: 88 variantes catalogadas, 151.472 bytes em 28 grupos de origem; as listas e relatórios do lote estão no projeto local. A identificação independente de linguagem VU1 no Ghidra segue pendente.
- Reconstrução: há uma região de 36 bytes com correspondência exata documentada e perfil de compilação candidato. Isso não comprova a toolchain original.

## Convenção de evidência

- **Observado:** saída direta de ferramenta ou leitura runtime registrada.
- **Reproduzido:** mesma operação repetida com resultado consistente.
- **Confirmado:** evidência independente sustenta a afirmação no escopo declarado.
- **Hipótese:** explicação plausível que ainda precisa de teste discriminativo.
- **Pendente:** evidência insuficiente ou limite conhecido.

Cada número deve apontar para um escopo contado e preservar casos sem resolução. Não contar identificadores de execução (#500, #502 etc.) como funções concluídas.
