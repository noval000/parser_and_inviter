import csv
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest

# Данные для подключения
api_id = '29702282'  # Замените на ваш API ID
api_hash = '8b6330a9ec56f9e7641046169ee590b5'  # Замените на ваш API Hash
phone_number = '+79266216444'  # Замените на ваш номер телефона

# Создаем клиент для реального аккаунта
client = TelegramClient('user_session', api_id, api_hash)

# Юзернейм группы, в которую будем добавлять участников
destination_group_username = 'pro_gynecolog'  # Замените на юзернейм вашей целевой группы

# Путь к CSV файлу с участниками
input_file = 'group_members.csv'

# Функция для добавления пользователя в группу
async def add_user_to_group(username):
    try:
        # Получаем объект пользователя по username
        user = await client.get_entity(username)

        # Получаем объект группы по юзернейму
        destination_group = await client.get_entity(destination_group_username)

        # Добавляем пользователя в группу
        await client(InviteToChannelRequest(destination_group, [user]))
        print(f"Пользователь {username} добавлен в группу {destination_group_username}.")
    except Exception as e:
        print(f"Не удалось добавить пользователя {username}: {str(e)}")

# Функция для чтения пользователей из CSV и добавления их в группу с задержкой 1 час
async def process_users_from_csv():
    while True:
        with open(input_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Читаем все строки в список

            if len(rows) <= 1:
                print("CSV файл пуст или не содержит пользователей.")
                break

            # Пропускаем заголовок
            headers = rows.pop(0)

            # Чтение пользователей по одному
            for row in rows:
                username = row[1]  # Предположим, что username находится во второй колонке
                print(f"Добавляем пользователя {username}...")
                await add_user_to_group(username)

                # После добавления удаляем пользователя из списка
                rows.remove(row)

                # Сохраняем обновленный список обратно в файл
                with open(input_file, mode='w', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)  # Записываем заголовки
                    writer.writerows(rows)  # Записываем обновленные данные

                await asyncio.sleep(3600)  # Задержка 1 час (3600 секунд)

async def main():
    # Запускаем парсинг
    print(f"Бот запущен. Добавляем участников в группу {destination_group_username}...")
    await client.start(phone_number)  # Используем start для подключения с номером телефона
    await process_users_from_csv()  # Читаем и добавляем участников
    await client.disconnect()  # Отключаем клиента

if __name__ == '__main__':
    # Обеспечиваем правильную работу asyncio и запускаем основной цикл
    import asyncio
    asyncio.run(main())
