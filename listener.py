from web3 import Web3
import json
import time

# Установите соединение с Ethereum-провайдером
# Замените URL на ваш провайдер (например, Ganache, Infura и т.д.)
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/api'))

# Проверьте соединение
if not w3.is_connected():
    print("Не удалось подключиться к Ethereum-провайдеру")
    exit()

# ABI контракта (сгенерировано из предоставленного кода контракта)
abi = json.loads("""
[
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
                "internalType": "uint8",
                "name": "move",
                "type": "uint8"
            }
        ],
        "name": "PlayerRevealed",
        "type": "event"
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
                "internalType": "uint8",
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
                "internalType": "uint8",
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
]
""")

# Адрес контракта (замените на реальный адрес вашего развернутого контракта)
contract_address = '0x05E93A255b66DA7635760A97011F2eDb31036AdE'

# Создайте объект контракта
contract = w3.eth.contract(address=contract_address, abi=abi)

# Функция для обработки события GameStarted
def handle_game_started(event):
    args = event['args']
    player1 = args['player1']
    player2 = args['player2']
    bet_amount = args['betAmount']
    print(f"Событие GameStarted:")
    print(f"  Игрок 1: {player1}")
    print(f"  Игрок 2: {player2}")
    print(f"  Сумма ставки: {bet_amount} wei\n")

# Функция для обработки события PlayerCommitted
def handle_player_committed(event):
    args = event['args']
    player = args['player']
    print(f"Событие PlayerCommitted:")
    print(f"  Игрок: {player} совершил коммит своего хода.\n")

# Функция для обработки события PlayerRevealed
def handle_player_revealed(event):
    args = event['args']
    player = args['player']
    move = args['move']
    move_name = {1: 'Rock', 2: 'Paper', 3: 'Scissors'}.get(move, 'None')
    print(f"Событие PlayerRevealed:")
    print(f"  Игрок: {player} раскрыл свой ход: {move_name}.\n")

# Функция для обработки события GameResult
def handle_game_result(event):
    args = event['args']
    winner = args['winner']
    loser = args['loser']
    result = args['result']
    print(f"Событие GameResult:")
    print(f"  Игрок 1: {winner}")
    print(f"  Игрок 2: {loser}")
    print(f"  Результат: {result}\n")

# Получаем хеши сигнатур событий
import hashlib

def event_signature(event_name, param_types):
    signature = f"{event_name}({','.join(param_types)})"
    return w3.keccak(text=signature).hex()

# Сигнатуры событий в соответствии с ABI
event_signatures = {
    'GameStarted': event_signature('GameStarted', ['address', 'address', 'uint256']),
    'PlayerCommitted': event_signature('PlayerCommitted', ['address']),
    'PlayerRevealed': event_signature('PlayerRevealed', ['address', 'uint8']),
    'GameResult': event_signature('GameResult', ['address', 'address', 'string']),
}

# Словарь соответствия сигнатур событий и обработчиков (с постоянными значениями)
event_handler_map = {
    event_signatures['GameStarted']: handle_game_started,
    event_signatures['PlayerCommitted']: handle_player_committed,
    event_signatures['PlayerRevealed']: handle_player_revealed,
    event_signatures['GameResult']: handle_game_result,
}

# Функция для обработки события общего вида
def handle_event(event):
    # Определяем сигнатуру события
    event_signature = event['topics'][0].hex()
    # Получаем соответствующий обработчик
    handler = event_handler_map.get(event_signature, None)
    if handler:
        # Получаем ABI события по сигнатуре
        for event_abi in abi:
            if event_abi.get('type') == 'event':
                signature = event_signature_from_abi(event_abi)
                if signature == event_signature:
                    # Декодируем событие
                    decoded_event = contract.events[event_abi['name']]().process_log(event)
                    # Вызываем обработчик
                    handler(decoded_event)
                    break
    else:
        print("Получено неизвестное событие")
        

# Вспомогательная функция для получения сигнатуры события из ABI
def event_signature_from_abi(event_abi):
    inputs = event_abi['inputs']
    types = [input['type'] for input in inputs]
    signature = f"{event_abi['name']}({','.join(types)})"
    return w3.keccak(text=signature).hex()

# Создаем фильтр для отслеживания событий контракта
event_filter = w3.eth.filter({
    'fromBlock': 'latest',
    'address': contract_address
})

print("Начинаем прослушивание событий...")

# Бесконечный цикл для прослушивания событий
try:
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(2)  # Задержка между проверками
except KeyboardInterrupt:
    print("Остановлено пользователем")
