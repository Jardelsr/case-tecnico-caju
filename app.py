from flask import Flask, request, jsonify
from db_init import (
    getAccountBalanceByMCC,
    setAccountBalance,
    createTransaction,
    getTransactionsByAccount,
    getTransactionsByMerchant,
)
app = Flask(__name__)

# Mapeamento MCC para saldo
mcc_to_balance = {
    5411: 'food',
    5412: 'food',
    5811: 'meal',
    5812: 'meal',
}

# Rota para efetuar as transções
@app.route('/api/transaction', methods=['POST'])
def endpoint_post():
    # Obtenha os dados JSON da solicitação POST
    data = request.get_json()

    # Verifica se todos os campos necessários estão presentes
    required_fields = ['accountId', 'amount', 'merchant', 'mcc']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'all fields required'}), 400

    # Verificar qual saldo usar com base no MCC
    balance = mcc_to_balance.get(int(data['mcc']), 'cash')
    accountBalanceAmount = getAccountBalanceByMCC(data['accountId'], balance)
    amount = data['amount']

    # Verificar se a transação pode ser efetuada, com base no saldo da conta
    if amount <= accountBalanceAmount: 
        setAccountBalance(data['accountId'], balance, accountBalanceAmount - amount)
        createTransaction(data['accountId'], amount, data['merchant'], data['mcc'], 'approved')
        return jsonify({'transaction': 'approved'}), 200
    else :
        reason = 'Insufficient balance to proceed with the transaction.'
        createTransaction(data['accountId'], amount, data['merchant'], data['mcc'], 'denied', reason)
        return jsonify({'transaction': 'denied'}), 401
    
# rota para buscar as transações de uma conta
@app.route('/api/<int:id>/transactions', methods=['GET'])
def getTransactions(id):
    return getTransactionsByAccount(id)

# rota para buscar as transações de um estabelecimento
@app.route('/api/search', methods=['GET'])
def search():
    merchant = request.args.get('merchant', type=str)
    return getTransactionsByMerchant(merchant)

if __name__ == '__main__':
    app.run()