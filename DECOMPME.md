# Uso do decomp.me neste projeto

## Papel esperado

O decomp.me pode ajudar na comparação iterativa de uma função C com sua montagem-alvo, desde que a plataforma/compilador e as opções correspondam ao alvo. É uma bancada por função; não decompila automaticamente o ELF inteiro, não faz a análise runtime do PCSX2 e não sincroniza este painel do GitHub.

## Verificações antes do primeiro scratch

1. Confirmar se o preset ou compilador disponível representa o EE/R5900, incluindo versão e flags necessárias.
2. Escolher uma função pequena cuja origem, endereço e bytes tenham sido verificados.
3. Revisar a visibilidade e o tratamento do conteúdo enviado. A política do serviço diz que dados salvos ficam associados à sessão e que exportações públicas podem conter dados já públicos no próprio site.
4. Não enviar ISO, módulos completos, dumps, strings extensas nem pseudocódigo derivado sem a autorização e revisão apropriadas.
5. Registrar neste projeto o scratch, preset/flags, escopo em bytes/instruções, match e limites.

## Estado

**Ainda não iniciado.** A execução #502 avaliou o REA junto do Ghidra; ela não foi um teste do decomp.me. O primeiro passo é validar o suporte à toolchain PS2/EE e o escopo seguro para um piloto.

## Referências

- [decomp.me](https://decomp.me/)
- [Código-fonte do decomp.me](https://github.com/decompme/decomp.me)
- [Documento de compiladores do decomp.me](https://github.com/decompme/decomp.me/blob/main/docs/COMPILER.md)
- [Política de privacidade do decomp.me](https://www.decomp.me/privacy)
