# Integração com decomp.dev

**Estado:** workflow e artefato do piloto ativos no branch padrão; cadastro e leitura pelo painel do decomp.dev ainda não confirmados.

Este projeto acompanha a pesquisa de decompilação do BLACK para PS2. A cobertura global do EE, IOP e VU segue **sem percentual confiável**, porque o inventário completo de unidades e o denominador ainda não foram fechados.

## Piloto atual

O primeiro relatório cobre somente EE/FUN_001ABEB8: uma função de 40 bytes, comparada pelo objdiff-cli 3.8.2, com 40/40 bytes e 1/1 função correspondentes. O escopo está rotulado como “EE single-function pilot; not global project coverage” tanto nos dados quanto no relatório.

### Evidência e limites

- O objeto-base foi compilado da reconstrução C com SN Systems ProDG EE GCC 2.95.3-EE (SN BUILD 1.36), -O2 -G8 -fomit-frame-pointer.
- O objeto-alvo foi reconstruído localmente a partir da disassembly verificada; a relocação da chamada foi restaurada e corroborada contra o objeto-base.
- Ambos os objetos foram ligados no endereço original. A janela resultante de 40 bytes dos dois lados coincide com a referência original registrada pelo SHA-256 b072a1104192ced915e82243dedc5fc3547bd3e62d6b174ef97254d07d2e9182.
- O alvo relocável é uma divisão reconstruída, não o objeto pré-link original. Essa incerteza está declarada nos metadados do progresso.
- O runtime dessa função curta não foi confirmado.
- Nenhum objeto, ELF, assembly, dump ou byte do jogo é incluído no repositório ou no artefato do workflow. Os dados publicados são métricas, nomes, método e hash da janela de referência.

O relatório do piloto pode mostrar 100% **dessa única unidade**. Não é percentual do executável nem do jogo. Não somar os conjuntos de módulos IOP, arquivos VU/DVP, funções EE, capturas de emulador ou sessões de análise sem inventário e regra de denominador comuns.

## Como o relatório é gerado

O fluxo segue o padrão usado pelo [BFM-decomp](https://github.com/Druthulu/BFM-decomp): métricas auditadas ficam em um JSON versionado e um conversor gera o formato Report v2 que o decomp.dev consome. A Action não recompila o jogo e não precisa acessar os objetos locais.

- Fonte dos dados: docs/decompdev/progress.json.
- Conversor: tools/decompdev_report.py.
- Workflow: .github/workflows/decompdev-report.yml.
- Artefato publicado pelo GitHub Actions: SLUS_213.76_report, com o arquivo report.json gerado localmente em build/report.json.
- O workflow roda quando os dados, conversor ou teste mudam no branch padrão, ou por acionamento manual.

Reproduza localmente:

~~~sh
python -m unittest tools.test_decompdev_report -v
python tools/decompdev_report.py --in docs/decompdev/progress.json --out build/report.json
~~~

O relatório Report v2 é derivado das contagens da prova local; a prova completa e seus objetos permanecem no acervo privado de pesquisa. Atualizações futuras entram no painel por mudança auditada em progress.json, acompanhada de evidência equivalente.

## Cadastro e sincronização

1. O workflow já foi integrado ao branch padrão main no PR #7.
2. A execução do workflow no branch padrão concluiu com sucesso e publicou o artefato SLUS_213.76_report.
3. Cadastrar o repositório em [decomp.dev/manage/new](https://decomp.dev/manage/new), com descrição que identifique explicitamente o escopo do piloto.
4. Conferir no painel que versão, unidade e métricas correspondem ao relatório; a linha de função deve permitir o detalhamento da unidade.
5. Registrar a URL e a data da sincronização neste documento e no README depois de comprovar a leitura no painel.

O projeto ainda não está cadastrado nem há prova de leitura do relatório pelo painel. A instalação opcional do GitHub App do decomp.dev deve ser limitada a este repositório caso o serviço realmente a exija; não conceder acesso a todos os repositórios da conta.

## Próximo trabalho de progresso global

Concluir o inventário de funções únicas e estados de reconstrução do EE, IOP e VU, preservando aliases, limites e proveniência. Cada nova unidade precisa de evidência de compilação/comparação apropriada à arquitetura e versão. O denominador global só será publicado depois de essa reconciliação e validação.
