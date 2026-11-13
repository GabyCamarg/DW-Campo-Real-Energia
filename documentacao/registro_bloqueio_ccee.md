# Registro de tentativa de extração — CCEE

## 1. Fonte de dados
- Instituição: Câmara de Comercialização de Energia Elétrica (CCEE).
- Conjunto: PLD_HORARIO.
- Endereço: https://dadosabertos.ccee.org.br/dataset/pld_horario
- Dados pretendidos: Preço de Liquidação das Diferenças (PLD) horário.
- Períodos: 2025 e 2026.

## 2. Procedimento realizado
Foi realizada uma consulta ao catálogo da CCEE pelo navegador e por meio de Python, utilizando a biblioteca Requests.

O catálogo apresentou resposta de sucesso no navegador, identificando o conjunto PLD_HORARIO e seus recursos.

Também foram realizadas tentativas de consulta à API CKAN e de download dos dados por meio do Python.

## 3. Resultado
As requisições realizadas pelo Python retornaram HTTP 403 (Forbidden).

Na tentativa de download, o servidor retornou uma página HTML informando que o acesso foi bloqueado por políticas de segurança da CCEE.

## 4. Tratamento da ocorrência
A ocorrência foi registrada como falha de acesso à fonte externa.

Os dados de PLD não foram considerados extraídos nem carregados no banco de dados.

Nenhum dado fictício foi criado para substituir os valores indisponíveis.

Será necessária uma nova tentativa após orientação ou liberação de acesso pela CCEE.

## 5. Evidências
- prints/01_catalogo_ccee.png
- prints/02_bloqueio_ccee_403.png

## 6. Situação
Pendente de resolução do acesso à fonte CCEE.
