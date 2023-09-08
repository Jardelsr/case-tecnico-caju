# case tecnico caju
Uma transação é composta pelos seguintes dados:
● id - Um identificador único para esta transação.
● accountId - Um identificador para a conta.
● amount - O valor a ser debitado de um saldo.
● merchant - O nome do estabelecimento.
● mcc - Um código numérico de 4 dígitos que classifica os estabelecimentos
comerciais de acordo com o tipo de produto vendido ou serviço prestado.
O `MCC` contém a classificação do estabelecimento. Baseado no seu valor, deve-se
decidir qual o saldo será utilizado (na totalidade do valor da transação). Por
simplicidade, vamos usar a seguinte regra:
- Se o `mcc` for `"5411" ou "5412"`, deve-se utilizar o saldo de `FOOD`.
- Se o `mcc` for `"5811" ou "5812"`, deve-se utilizar o saldo de `MEAL`.
- Para quaisquer outros valores do `mcc`, deve-se utilizar o saldo de `CASH`.
Considere que uma conta possua 3 saldos distintos, sendo eles: FOOD, MEAL e
CASH, e um identificador único para a conta.
Parte 1.1
💡 Considere que o sistema deve guardar os resultados de cada execução de
transação, se foram aprovadas ou rejeitadas (e a causa), e permitir a busca de
todos os resultados por conta.
Parte 1.2
💡 Considere agora que o sistema deve permitir a busca de resultados por nome do
estabelecimento.
Enunciado: Implemente a lógica de autorização de transações, considerando um
sistema que gerencie múltiplas contas. Atualize o saldo após o débito da transação
(não é necessário uma interface gráfica para execução do teste).
Casos de teste para validação da solução:
1. Uma transação aprovada em FOOD e MEAL com valor igual ao saldo
2. Uma transação recusada
3. Uma transação aprovada em CASH
4. Duas compras consecutivas em qualquer categoria, uma compra aprovada e
uma recusada
