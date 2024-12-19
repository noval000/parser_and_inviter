from telethon import TelegramClient, events
import pandas as pd
import os
import asyncio

# Вставьте свои данные
api_id = '29702282'
api_hash = '8b6330a9ec56f9e7641046169ee590b5'
bot_token = '7734519840:AAEMbZ1EmVjO523AOmzTA13CTmoF8iVAd1o'
group_username = 'gynechat'  # Юзернейм группы, например, 'testgroup'

# Инициализация клиента
client = TelegramClient('bot_session', api_id, api_hash)

# Путь к CSV файлу
csv_file = 'group_members.csv'

# Функция для загрузки существующих пользователей из CSV
def load_existing_users():
    try:
        return pd.read_csv(csv_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=["user_id", "username", "first_name", "last_name"])

# Функция для добавления нового пользователя в CSV
def append_new_user_to_csv(new_user):
    existing_users = load_existing_users()

    # Проверяем, если пользователь уже есть в списке, не добавляем
    if new_user['user_id'] not in existing_users['user_id'].values:
        # Добавляем нового пользователя в конец файла
        new_user_df = pd.DataFrame([new_user])
        new_user_df.to_csv(csv_file, mode='a', header=not existing_users.empty, index=False)
        print(f"Пользователь {new_user['user_id']} добавлен в таблицу.")
    else:
        print(f"Пользователь {new_user['user_id']} уже существует в таблице.")

# Обработчик события нового пользователя
@client.on(events.ChatAction())
async def handler(event):
    if event.user_added or event.user_joined:
        user = await client.get_entity(event.user_id)
        new_user = {
            "user_id": user.id,
            "username": user.username if user.username else "",
            "first_name": user.first_name if user.first_name else "",
            "last_name": user.last_name if user.last_name else "",
        }
        append_new_user_to_csv(new_user)

# Основная функция
async def main():
    print("Бот запущен и ожидает новых пользователей...")
    await client.start(bot_token=bot_token)  # Запускаем с бот-токеном
    await client.run_until_disconnected()

# Запуск программы
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"Ошибка выполнения: {e}")
