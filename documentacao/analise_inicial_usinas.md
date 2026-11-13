# Análise inicial de qualidade – Cadastro de usinas

## Quantidade de registros

Foram identificados 10 registros na tabela campo_real_energia.usina.
O cenário prevê 9 usinas de referência.

## Inconsistências identificadas

1. CRE-UFV-004:
   - Latitude cadastrada como 15.803.
   - Valor de referência no script original: -15.803.

2. CRE-BIO-005:
   - UF cadastrada como PE.
   - Valor de referência no script original: SP.

3. CRE-EOL-07:
   - Código diferente do padrão CRE-EOL-007.
   - Município não informado.
   - Nome com espaço extra no final.
   - Coordenadas coincidem com CRE-EOL-007.
   - Indício de registro duplicado.

## Decisão inicial

Os dados originais serão preservados para permitir a análise de qualidade.
As inconsistências serão documentadas e tratadas em uma etapa específica,
sem alterações silenciosas na base de origem.

