# Status do Projeto ReBlack

**Atualizado:** 14/10/2026
**Plataforma deste projeto:** PlayStation 2 (Emotion Engine/R5900, IOP e VU).  
**Estado geral:** investigação técnica em andamento; recuperação integral do código-fonte ainda não alcançada.

## Visão rápida

| Frente | Avanço verificável | Estado | O que falta |
|---|---:|---|---|
| Cobertura global do executável | **Sem percentual confiável** | Base de contagem pendente | Inventariar funções únicas do EE, IOP e VU e classificar cada uma. |
| Módulos IOP do mapa inicial | **25/25 — 100% desse conjunto** | Análise inicial pronta para consulta | Medir cobertura de funções e confirmar o que exige aprofundamento. |
| Overlays VU/DVP do lote catalogado | **88/88 — 100% do mapeamento inicial** | Catálogo e desmontagem inicial concluídos | Análise independente da VU1 no Ghidra e interpretação semântica. |
| Amostra de slots Unit da execução #500 | **292/292 — 100% da amostra** | Processamento concluído; alguns casos sem resolução | Validar alvos em RAM e explicar os 3 casos com limites inválidos. |
| Integridade dos arquivos Unit da #500 | **42/42 — 100% desse conjunto** | Hashes e tamanhos conferidos | Nenhum passo pendente para essa conferência específica. |
| Reconstrução comparada | **1 região exata de 36 bytes documentada** | Prova técnica pontual | Confirmar a toolchain original e ampliar por funções selecionadas. |
| REA no fluxo PS2 | **Avaliação comparativa concluída (#502)** | Resultado documentado; sem análise PS2 independente no ambiente testado | Reavaliar somente se houver suporte compatível com ELF/MIPS EE. |
| Captura e análise runtime | **Várias observações documentadas** | Útil para hipóteses específicas; cobertura do jogo não medida | Fazer captura discriminativa para validar endereços e estruturas pendentes. |
| Piloto decomp.me | **0% iniciado** | Planejado, ainda não pronto para uso no BLACK | Verificar compilador EE/R5900 e exposição dos dados antes de criar scratch. |
| Execuções PCSX2 #507–#508 | **Gameplay e tela `LOADING` observados** | Marcos visuais do jogo original documentados | Seguir o record APT até a submissão GS; isso não mede cobertura de código. |

### Como ler os percentuais

- “100%” significa que o conjunto explicitamente contado naquela linha foi concluído. Não significa que 100% do jogo foi decompilado.
- A amostra #500 contém 152 ponteiros C0 não nulos: 138 (90,8%) apontam para fora dos arquivos extraídos e 14 (9,2%) ficam dentro. Dos 14, 11 têm descritores limitados; 3 ainda apresentam limites inválidos.
- **Sem percentual global não significa 0%.** Significa que ainda não foi contado o total de funções que servirá de denominador.
- “Pronto para consulta” descreve os dados documentados; não certifica reconstrução do módulo inteiro nem equivalência de gameplay.

## Próximas ações rastreáveis

1. [#4 — Inventariar funções únicas do EE, IOP e VU](https://github.com/soldieg/Projeto-ReBlack/issues/4). Essa contagem permitirá publicar percentuais por módulo e global.
2. [#3 — Validar os C0 pendentes da amostra Unit #500 no PCSX2](https://github.com/soldieg/Projeto-ReBlack/issues/3).
3. [#2 — Fechar o fluxo de chaves e lista de objetos StUnit/Unit](https://github.com/soldieg/Projeto-ReBlack/issues/2), reusando #409–#413.
4. [#1 — Verificar o suporte EE/R5900 e preparar piloto seguro no decomp.me](https://github.com/soldieg/Projeto-ReBlack/issues/1).

## Últimos marcos

A execução #502 comparou REA, Ghidra e o fluxo combinado no mesmo ELF. O Ghidra repetiu as consultas com sucesso e os dados da amostra #500 foram conferidos novamente. O REA detectou ELF/MIPS, mas o provedor Ghidra no Windows rejeitou o alvo antes da análise. Não foram encontradas funções novas nessa execução.

Na execução #507, uma captura nativa do PCSX2 mostrou gameplay em primeira pessoa, com cenário 3D, HUD e arma. Na #508, a VM foi parada na solicitação `Loading_screen` (`PC=0x0020B678`, `a1=0x003FA5A0`, `a2=5`); após retomar o mesmo processo, os quadros 03–05 mostraram a tela animada `LOADING`. A correlação exata entre o record de `Loading.bin`, os pacotes GS e cada quadro ainda não foi demonstrada. Veja [EVIDENCIAS.md](EVIDENCIAS.md).

Esses marcos pertencem ao jogo original no PCSX2. Eles não confirmam uma recompilação para PC, nem alteram o estado de cobertura global: o denominador de funções únicas segue pendente.
