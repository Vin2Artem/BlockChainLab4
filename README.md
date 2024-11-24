# Лабораторная работа № 4

Цель работы: получить практические навыки взаимодействия со смарт-контрактами из внешних информационных систем.

---

## Описание файлов

1. **test.py**  
   Скрипт для взаимодействия со смарт-контрактом "Камень-ножницы-бумага". Содержит функции:
   - Регистрация игроков.
   - Коммит хода игрока с хэшированием.
   - Раскрытие хода после коммита.

2. **listener.py**  
   Скрипт для обработки событий, создаваемых смарт-контрактом. Реализовано:
   - Обработка событий:
     - `GameStarted` — начало игры.
     - `PlayerCommitted` — коммит хода игрока.
     - `PlayerRevealed` — раскрытие хода игрока.
     - `GameResult` — результат игры.
   - Постоянное отслеживание событий через Ethereum-провайдер
