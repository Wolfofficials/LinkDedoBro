import os
import asyncio
import random
import time
from pyrogram import Client

groups_file = 'groups.txt'
texts_file = 'texts.txt'

async def join_groups(client):
    groups = read_groups_file()
    joined_groups = []

    for group in groups:
        try:
            await client.join_chat(group)
            joined_groups.append(group)
            print(f"Joined group: {group}")
            await asyncio.sleep(10)  # Delay of 10 seconds before joining the next group
        except Exception as e:
            print(f"Failed to join group: {group}")
            print(f"Error: {str(e)}")
            remove_group(group)

    print(f"Joined {len(joined_groups)} groups.")

    return joined_groups

async def send_message(client, joined_groups):
    if len(joined_groups) == 0:
        print("No groups joined. Skipping message sending.")
        return

    message = get_random_message()
    group = random.choice(joined_groups)

    try:
        await client.send_message(group, message)
        print(f"Sent message in group: {group}")
    except Exception as e:
        print(f"Failed to send message in group: {group}")
        print(f"Error: {str(e)}")

async def main():
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')

    session_string = os.getenv('SESSION_STRING')

    client = Client(session_name=session_name, api_id=api_id, api_hash=api_hash, session_string=session_string)
    await client.start()

    while True:
        joined_groups = await join_groups(client)
        await send_message(client, joined_groups)
        await asyncio.sleep(10)  # Delay of 10 seconds before sending the next message

    await client.stop()

def read_groups_file():
    with open(groups_file, 'r') as file:
        groups = file.read().splitlines()
    return groups

def get_random_message():
    with open(texts_file, 'r') as file:
        messages = file.read().splitlines()
    return random.choice(messages)

def remove_group(group):
    with open(groups_file, 'r') as file:
        lines = file.readlines()
    with open(groups_file, 'w') as file:
        for line in lines:
            if line.strip() != group:
                file.write(line)

if __name__ == '__main__':
    asyncio.run(main())
