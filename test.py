from web3 import Web3
import hashlib

# Подключение к Infura
infura_url = "https://sepolia.infura.io/v3/api"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Проверка подключения
if web3.is_connected():
    print("Успешное подключение к Ethereum узлу")
else:
    print("Ошибка подключения")

# Адрес контракта и ABI
contract_address = "0x05E93A255b66DA7635760A97011F2eDb31036AdE"
contract_abi = """[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_betAmount",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "winner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "loser",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "result",
				"type": "string"
			}
		],
		"name": "GameResult",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "player1",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "player2",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "betAmount",
				"type": "uint256"
			}
		],
		"name": "GameStarted",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "player",
				"type": "address"
			}
		],
		"name": "PlayerCommitted",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "player",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "enum RockPaperScissors.Move",
				"name": "move",
				"type": "uint8"
			}
		],
		"name": "PlayerRevealed",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "betAmount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_commitment",
				"type": "bytes32"
			}
		],
		"name": "commitMove",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "playerAddresses",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "players",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "commitment",
				"type": "bytes32"
			},
			{
				"internalType": "enum RockPaperScissors.Move",
				"name": "move",
				"type": "uint8"
			},
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "register",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "enum RockPaperScissors.Move",
				"name": "_move",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "_secret",
				"type": "string"
			}
		],
		"name": "revealMove",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]"""

# Создание объекта контракта
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def get_updated_gas_price(web3):
    """
    Получает обновленную цену газа на основе состояния сети.

    :param web3: объект Web3
    :return: обновленная цена газа в wei
    """
    try:
        # Получаем текущую базовую цену газа
        current_gas_price = web3.eth.gas_price
        
        # Увеличиваем базовую цену газа на 20%
        adjusted_gas_price = int(current_gas_price * 1.2)
        print(f"Текущая цена газа: {current_gas_price} wei, Увеличенная цена: {adjusted_gas_price} wei")
        
        return adjusted_gas_price
    except Exception as e:
        print(f"Ошибка при обновлении цены газа: {e}")
        return web3.toWei('20', 'gwei')  # Возвращаем дефолтное значение, если произошла ошибка

# Пример работы с контрактом
def register_player(player_private_key, bet_amount):
    """Регистрация игрока"""
    account = web3.eth.account.from_key(player_private_key)
    #estgas = contract.functions.register().estimate_gas({'from': account.address})
    transaction = contract.functions.register().build_transaction({
        'from': account.address,
        'value': bet_amount,
        'gas': 2000000,
        'nonce': web3.eth.get_transaction_count(account.address)
    })
    signed_tx = web3.eth.account.sign_transaction(transaction, private_key=player_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Регистрация отправлена, хэш транзакции: {tx_hash.hex()}")

    # Ожидание подтверждения транзакции
    print("Ожидание подтверждения транзакции...")
    try:
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # Тайм-аут 120 секунд
        print(f"Транзакция подтверждена: {receipt}")
    except Exception as e:
        print(f"Ошибка ожидания транзакции: {e}")
        return None

    return receipt

def commit_move(player_private_key, move, secret):
    """Отправка хэша хода"""
    print("Sending")
    account = web3.eth.account.from_key(player_private_key)
    move_hash = web3.solidity_keccak(['uint8', 'string'], [move, secret])
    updated_gas_price = get_updated_gas_price(web3)
    print("updated_gas =", updated_gas_price)
    updated_gas_price = int(updated_gas_price * 2)
    print("updated_gas1 =", updated_gas_price)

    transaction = contract.functions.commitMove(move_hash).build_transaction({
        'from': account.address,
        'gas': 2000000,
        'gasPrice': updated_gas_price,
        'nonce': web3.eth.get_transaction_count(account.address)
    })
    signed_tx = web3.eth.account.sign_transaction(transaction, private_key=player_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Коммит хода отправлен, хэш транзакции: {tx_hash.hex()}")
    
    # Ожидание подтверждения транзакции
    print("Ожидание подтверждения транзакции...")
    try:
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # Тайм-аут 120 секунд
        print(f"Транзакция подтверждена: {receipt}")
    except Exception as e:
        print(f"Ошибка ожидания транзакции: {e}")
        return None

    return receipt

def reveal_move(player_private_key, move, secret):
    """Раскрытие хода"""
    print("Revealing")
    account = web3.eth.account.from_key(player_private_key)
    updated_gas_price = get_updated_gas_price(web3)
    print("updated_gas =", updated_gas_price)
    updated_gas_price = int(updated_gas_price * 2.5)
    print("updated_gas1 =", updated_gas_price)
    transaction = contract.functions.revealMove(move, secret).build_transaction({
        'from': account.address,
        'gas': 2000000,
        'gasPrice': updated_gas_price,
        'nonce': web3.eth.get_transaction_count(account.address)
    })
    signed_tx = web3.eth.account.sign_transaction(transaction, private_key=player_private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Раскрытие хода отправлено, хэш транзакции: {tx_hash.hex()}")
    
    # Ожидание подтверждения транзакции
    print("Ожидание подтверждения транзакции...")
    try:
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  # Тайм-аут 120 секунд
        print(f"Транзакция подтверждена: {receipt}")
    except Exception as e:
        print(f"Ошибка ожидания транзакции: {e}")
        return None

    return receipt

# Секретные ключи игроков
player_private_key1 = "player_private_key1"
player_private_key2 = "player_private_key2"

# Вызов функции-геттера для betAmount
bet_amount = contract.functions.betAmount().call()

print("bet = ", bet_amount)

# Регистрация игроков
register_player(player_private_key1, bet_amount=bet_amount)
register_player(player_private_key2, bet_amount=bet_amount)

# Ход игрока 1
move1 = 1
secret1 = "mysecret1"

# Коммит хода
commit_move(player_private_key1, move1, secret1)


# Ход игрока 2
move2 = 2
secret2 = "mysecret2"

# Коммит хода
commit_move(player_private_key2, move2, secret2)

# Раскрытие хода
reveal_move(player_private_key1, move1, secret1)
# Раскрытие хода
reveal_move(player_private_key2, move2, secret2)
