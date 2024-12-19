import csv
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# Данные для подключения
api_id = '29702282'  # Замените на ваш API ID
api_hash = '8b6330a9ec56f9e7641046169ee590b5'  # Замените на ваш API Hash
bot_token = '7734519840:AAEMbZ1EmVjO523AOmzTA13CTmoF8iVAd1o'  # Замените на ваш токен бота

# Создаем клиент для бота
client = TelegramClient('bot_session', api_id, api_hash)

# Юзернейм группы, из которой будем парсить участников
group_username = 'gynechat'  # Замените на юзернейм вашей группы

# Путь к файлу, в котором будем хранить информацию о пользователях
output_file = 'group_members.csv'


async def parse_group_members():
    # Получаем объект группы по юзернейму
    group = await client.get_entity(group_username)

    # Параметры для получения участников
    offset = 0
    limit = 200  # Количество участников, которое будет загружено за раз
    all_participants = []

    while True:
        participants = await client(GetParticipantsRequest(
            group, ChannelParticipantsSearch(''), offset, limit, hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    # Открываем CSV файл для записи
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Записываем заголовок
        writer.writerow(['User ID', 'Username', 'First Name', 'Last Name'])

        # Записываем информацию о каждом пользователе
        for participant in all_participants:
            writer.writerow([participant.id, participant.username, participant.first_name, participant.last_name])

    print(f'Парсинг завершен! Все участники сохранены в {output_file}')


async def main():
    # Запускаем парсинг
    print(f"Бот запущен. Парсим участников группы {group_username}...")
    await client.start(bot_token=bot_token)  # Используем start для подключения с токеном бота
    await parse_group_members()
    await client.disconnect()


if __name__ == '__main__':
    # Обеспечиваем правильную работу asyncio и запускаем основной цикл
    asyncio.run(main())
