from flask import Flask, request, jsonify
from db_init import getAccountBalanceByMCC, setAccountBalance

app = Flask(__name__)

# Mapeamento MCC para saldo
mcc_to_balance = {
    5411: 'food',
    5412: 'food',
    5811: 'meal',
    5812: 'meal',
}

# Rota para lidar com solicitações POST
@app.route('/api/transaction', methods=['POST'])
def endpoint_post():
    # Obtenha os dados JSON da solicitação POST
    data = request.get_json()

    # Verifica se todos os campos necessários estão presentes
    required_fields = ['id', 'accountId', 'amount', 'merchant', 'mcc']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'all fields required'}), 400

    # Verificar qual saldo usar com base no MCC
    balance = mcc_to_balance.get(int(data['mcc']), 'cash')
    accountBalanceAmount = getAccountBalanceByMCC(data['id'], balance)
    amount = data['amount']

    # Verificar se a transação pode ser efetuada, com base no saldo da conta
    if amount <= accountBalanceAmount: 
        setAccountBalance(data['id'], balance, accountBalanceAmount - amount)
        return jsonify({'transaction': 'approved'}), 200
    else :
        return jsonify({'transaction': 'denied'}), 401

if __name__ == '__main__':
    app.run()