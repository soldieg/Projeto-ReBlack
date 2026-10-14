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

## Execução #507 — primeiro quadro de gameplay

- Captura nativa do PCSX2 mostrou o jogo em uma cena 3D, com HUD e arma na tela, depois da sequência de abertura.
- A imagem é posterior à tela de loading; não prova visualmente o quadro de loading.
- A sessão documenta o jogo original no PCSX2, não um runner recompilado nem um port para PC.

## Execução #508 — primeira tela de loading

- No mesmo processo, o breakpoint temporário em `0x0020B678` foi atingido. A leitura de registradores identificou `a1=0x003FA5A0` (`Loading_screen`) e `a2=5`; a condição configurada não ficou ativa.
- Após retomar a VM, capturas nativas mostraram `LOADING` nos quadros 03–05. O quadro 04 também exibe indicadores de progresso.
- SHA-256 do hit de registradores: `2d9624af8eb4cf41483add5f6170ae2929d11cff2c06b491053780821238894c`.
- SHA-256 das capturas: quadro 03 `f5b7c1618021eb798079ebdd9e2de757db7794a9a5053f51f8ad7631f7dc7ba2`; quadro 04 `13d38d4456cc73ca1648ef9345355b4dc247e44f36a35826a3063b0340e766be`; quadro 05 `d2b2ff732e782cf60180f419a74536f4157b4f04f27fea3d2f4b1f5a5f76f271`.
- `Loading_01` é um forte candidato estático pelo conteúdo e animação, mas ainda não foi provado qual record forneceu `Loading_screen` em runtime. Também falta sincronizar um pacote GS específico com o ciclo de cada captura.
- O relato e os artefatos completos permanecem no acervo privado local; nenhum jogo, dump ou captura foi copiado para este repositório.
