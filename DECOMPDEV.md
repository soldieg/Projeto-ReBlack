# Integração com decomp.dev

**Escopo atual do relatório:** catálogo provisório de funções EE/R5900 de `SLUS_213.76`. Este recorte não representa a cobertura completa do BLACK para PS2: IOP e VU/DVP estão fora do denominador.

## O que o painel deve mostrar

O catálogo Ghidra usado pela fila contém 9.842 funções, 2.584.776 bytes de corpo e 141 rótulos sintéticos excluídos. Não há intervalos de função sobrepostos na fila.

| Medida EE/R5900 | Resultado | Como interpretar |
|---|---:|---|
| Funções do catálogo provisório | 9.842 | Universo EE da fila Ghidra; limites ainda sujeitos à reconciliação final |
| Correspondências exatas | 31 funções / 376 bytes | 31/9.842 funções e 376/2.584.776 bytes |
| Correspondência parcial | 2 funções / 65 bytes | Registros locais de 10/128 e 55/336 bytes; não são matches exatos |
| Bytes com alguma correspondência | 441/2.584.776 — 0,0171% | 376 exatos + 65 parciais |
| Bytes totalmente exatos | 376/2.584.776 — 0,0145% | Só funções cujo corpo inteiro recompilado bateu |

Os 100% exibidos anteriormente não eram o progresso do jogo: o relatório histórico continha apenas `EE/FUN_001ABEB8` (40 bytes). O painel foi sincronizado em 14/10/2026 e agora mostra o commit `e1d6e10`: **0,02% decompilado**, **0,01% totalmente ligado** e **2,58 MB** de código. O projeto usa o nome `Black PS2 — EE/R5900 (catálogo provisório)` e comentários automáticos de PR estão desligados. O link direto funciona; o site só inclui o projeto em listagens depois do limite mínimo de 0,5% de código correspondido.

## Proveniência e limites

- A fonte é a fila EE produzida pela exportação local do Ghidra em modo somente leitura: `EE-FILA-DEPENDENCIAS-2026-10-14.csv`.
- O relatório preserva a ordem da fila e publica apenas nome, endereço, tamanho e medida de comparação de cada função. Chamadores, pseudocódigo, objetos, ELF, ISO e dumps não são incluídos.
- Os 31 matches exatos incluem 27 reconstruções novas e quatro históricas; os dois casos divergentes contribuem somente com seus bytes parciais medidos.
- Os 141 rótulos sintéticos não entram na contagem de funções. Os 25 módulos IOP ainda não têm total consolidado de funções. As 88 entradas VU/DVP são fluxos, não funções confirmadas.
- Por isso, o título e a categoria do painel precisam dizer **EE/R5900 provisório**. Não chamar esses percentuais de cobertura global do PS2.
- A reconstrução exata mede igualdade estática no escopo registrado; não confirma semântica completa ou comportamento no PCSX2.
- decomp.wtf não é fonte nem etapa deste processo.

## Fonte de dados e workflow

- Dados sanitizados e revisáveis: `docs/decompdev/progress.json`.
- Gerador Report v2: `tools/decompdev_report.py`.
- Workflow: `.github/workflows/decompdev-report.yml`.
- Artefato consumido pelo decomp.dev: `SLUS_213.76_report`, contendo `build/report.json`.
- O JSON de progresso registra o SHA-256 da fila de origem (`49fcf49980da8d045273a9b6a47431fbad9869c507ee7936a18d231462d2c1c3`). Nenhum binário ou código do jogo é usado pelo runner.

Reprodução local, a partir da raiz do repositório:

~~~sh
python -m unittest tools.test_decompdev_report -v
python -m unittest tools.test_record_validated_functions -v
python tools/decompdev_report.py --in docs/decompdev/progress.json --out build/report.json
~~~

O gerador bloqueia versão ou escopo diferentes, contagens divergentes, endereços duplicados, tamanhos inconsistentes e funções marcadas exatas sem correspondência do corpo inteiro.

## Registrar uma função validada

Use `tools/record_validated_functions.py` depois que a comparação local comprovar o match exato. Para funções cuja validação depende uma da outra, inclua todas no mesmo registro: o lote só é aceito por inteiro.

1. Crie um JSON local com ID/método da evidência e as funções (`name`, `address`, `size`).
2. Aponte para o arquivo local da evidência. O script calcula o SHA-256; o arquivo e seu caminho não são enviados.
3. Execute `python tools/record_validated_functions.py --record <registro.json> --evidence-file <evidencia-local>`.
4. O script busca `origin/main`, confere nome/endereço/tamanho, executa as validações e envia uma branch contendo apenas `docs/decompdev/progress.json`.
5. GitHub Actions abre um PR e valida o relatório. Revise o resultado e faça merge; o workflow de `main` publica o artefato `SLUS_213.76_report`, que atualiza o painel.

Modelo do registro local:

~~~json
{
  "schema": 1,
  "validated_at": "AAAA-MM-DD",
  "evidence": {"id": "ID-DA-EVIDENCIA", "method": "comparação integral de bytes"},
  "functions": [
    {"name": "FUN_XXXXXXXX", "address": "0xXXXXXXXX", "size": 8}
  ]
}
~~~

O progresso só aceita correspondência exata de corpo inteiro. Evidência incompleta ou dependência pendente continua na fila local; não deve ser promovida ao painel como função completa.

## Sincronização do painel

O projeto está configurado como PlayStation 2, versão padrão `SLUS_213.76`, workflow `decompdev-report.yml` e ativo. A sincronização foi confirmada em [decomp.dev](https://decomp.dev/soldieg/ReBlack-PS2), commit `e1d6e10`, após o workflow `decomp.dev progress report` concluir com sucesso. A página mostra 9.842 unidades, 31 funções exatas, 376 bytes exatos e 441 bytes fuzzy, com escopo EE/R5900 provisório. Comentários automáticos em PR estão desativados.

Só ampliar o escopo para IOP/VU/DVP depois de inventariar unidades e tamanhos únicos e reconciliar aliases, limites e sobreposições. Até lá, a porcentagem do painel é exclusivamente do catálogo EE provisório.
