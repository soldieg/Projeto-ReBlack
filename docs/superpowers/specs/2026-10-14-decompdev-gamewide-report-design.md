# Relatório de cobertura do BLACK PS2 no decomp.dev

## Objetivo

O relatório do projeto deve permitir identificar o progresso confirmado por função, sem que uma amostra isolada pareça representar o executável inteiro. O workflow do GitHub deve gerar e publicar o artefato a partir de dados versionados e revisáveis. A porcentagem global só pode ser chamada de cobertura do jogo quando o inventário de código do EE, IOP e VU estiver reconciliado.

## Estado atual e limites conhecidos

- O relatório publicado atualmente representa apenas `EE/FUN_001ABEB8`, 40 bytes e uma função. Seu 100% é local à amostra.
- O inventário candidato do decomp.wtf tem 11.774 entradas EE, 2.690.948 bytes somados e 11.774 estados `open` no CSV disponível.
- O catálogo local revisado tem 9.842 funções e 141 rótulos executáveis. A comparação entre catálogos registra 9.524 inícios e tamanhos iguais, 398 inícios com tamanho divergente, 61 entradas locais sem início correspondente e 1.852 entradas só no catálogo do decomp.wtf.
- Foram registradas quatro compilações locais byte a byte exatas em seis funções examinadas, mas essas evidências não são automaticamente matches aceitos pelo pipeline do decomp.dev. A função piloto de 40 bytes tem o fluxo de evidência publicado mais completo.
- O inventário funcional dos 25 módulos IOP e dos programas VU/DVP ainda não foi reconciliado com o inventário EE. Não há denominador global do jogo aprovado.

Essas contagens devem ser tratadas como fontes com proveniência e divergências, não somadas ou promovidas a um total definitivo sem reconciliação.

## Modelo do relatório

1. Manter um inventário canônico versionado com identidade do alvo, arquitetura/módulo, endereço, tamanho, nome, classe da entrada, estado de reconstrução, estado de comparação e referência da evidência.
2. Distinguir pelo menos: função catalogada sem reconstrução verificada; reconstrução existente sem comparação byte a byte confirmada; correspondência parcial medida; correspondência integral confirmada; e limite/identidade pendente.
3. Preservar aliases, rótulos, thunks, funções sobrepostas e limites incertos como classes distintas. Não contar rótulos como funções nem resolver discrepâncias somente por proximidade de endereço.
4. Produzir o Report v2 suportado pelo objdiff/decomp.dev a partir do inventário validado. As medidas agregadas devem usar a soma dos corpos de código únicos e as funções únicas; itens sem correspondência confirmada não podem herdar progresso da unidade piloto.
5. Mostrar os itens por unidades e categorias que correspondam às arquiteturas/módulos reais. O percentual de match deve se referir à comparação binária medida; evidência de execução no emulador fica separada.
6. A interface Report v2 não contém um campo textual livre por função para todos os estados de pesquisa. Portanto, o relatório humano de proveniência/estado continua no repositório; o painel deve usar os percentuais e rótulos suportados pelo schema e declarar o limite de que “sem match” significa “sem correspondência confirmada”, não prova de ausência de código-fonte.

## Fluxo no GitHub

- Um gerador determinístico lê somente dados de cobertura versionados; não requer ELF, ISO, dumps, objetos privados, segredos ou acesso a arquivos do jogo no runner.
- A Action valida identidades, duplicatas, limites, soma de tamanhos, classes de entradas, evidências e coerência entre estado e percentual.
- Pull requests validam o dataset e geram uma prévia não consumida como relatório global pelo decomp.dev.
- O artefato com o nome consumido pelo decomp.dev só é publicado quando a cobertura do escopo que ele declara estiver validada. Dados EE provisórios não devem ser rotulados como total de EE+IOP+VU.
- O relatório deve continuar reproduzível localmente e ter um caminho explícito para atualização manual/CI no branch padrão.

## Critérios para declarar cobertura global

- Fixar uma versão exata do jogo por identidade/hash sem publicar o binário.
- Reconciliar os catálogos EE e resolver/explicar cada entrada exclusiva ou divergente, sem eliminar evidência de fonte.
- Inventariar os corpos únicos de código dos módulos IOP relevantes e as unidades VU/DVP do jogo; registrar módulos/overlays incluídos e excluídos e justificar exclusões.
- Deduplicar intervalos compartilhados e aliases sem duplicar bytes ou funções.
- Garantir que cada unidade do denominador tenha tamanho de código e classificação auditáveis.
- Associar todo valor de match acima de zero a comparação reproduzível de bytes e evidência identificável; não converter “importado/analisado no Ghidra” em decompilado.
- Somente então publicar um percentual com rótulo de cobertura do jogo.

## Decisões de implementação propostas

- Evoluir o gerador atual de relatório de um formato rígido de uma função para um formato versionado de inventário com múltiplas funções e categorias.
- Manter o piloto como evidência histórica da função e preservá-lo no registro de progresso, sem deixá-lo definir o denominador geral.
- Introduzir validação que bloqueie o artefato global quando inventário, reconciliação ou evidência ainda estiverem incompletos.
- Enquanto EE/IOP/VU não estiverem fechados, gerar uma prévia explicitamente provisória para revisão no GitHub, sem permitir que o decomp.dev a interprete como cobertura total do jogo.

## Riscos e limites

- O relatório do decomp.dev mede matching/completion no schema objdiff; não mede sozinho compreensão semântica, comportamento em runtime ou qualidade da reconstrução.
- O inventário EE atualmente disponível tem diferenças materiais entre fontes. Escolher silenciosamente um catálogo como verdade poderia aumentar ou diminuir o denominador de forma enganosa.
- VU/DVP e módulos IOP podem demandar unidades de comparação/toolchains distintas das funções R5900; cada arquitetura deve preservar sua própria proveniência e regra de match.
- Um relatório parcial com nome/versão de jogo pode continuar parecendo global no cabeçalho do site. O artefato consumido deve ser bloqueado até que o rótulo de escopo esteja tecnicamente claro no painel.

## Resultado esperado

O decomp.dev deixa de mostrar 100% do jogo a partir da função piloto. O GitHub mostra o inventário, os estados confirmados e as pendências com validação automática. O relatório global só é publicado quando seu denominador representa os alvos e unidades declarados; até lá, o estado provisório fica evidente e não se apresenta como progresso do jogo inteiro.
