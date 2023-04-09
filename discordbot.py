from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
import datetime
load_dotenv()

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

client = discord.Client()

# 보스 이름을 리스트에 저장합니다.
boss_list = [
    "투르",
    "나딘",
    "룬드레드",
    "울리케",
    "리안",
    "보모",
    "캄투드",
    "나스로",
    "로드리고",
    "프랜신",
    "루바란",
    "볼테트",
    "라크다르",
    "이올라",
    "기드온",
    "호쏜",
    "분쇄자",
    "다비드",
    "암몬",
    "아르노슈트"
]

# 보스 목록과 예상 출현 시간을 저장하는 딕셔너리입니다.
boss_timers = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == f'{PREFIX}call':
        await message.channel.send("callback!")

    if message.content.startswith(f'{PREFIX}hello'):
        await message.channel.send('Hello!')

    # "보스" 라는 명령어가 입력되면 보스 리스트와 해당 보스의 예상 출현 시간을 출력합니다.
    elif message.content == '보스':
        # 예상 출현 시간이 빠른 순서대로 보스 목록을 정렬합니다.
        boss_timers_sorted = sorted(boss_timers.items(), key=lambda x: x[1]['time'] if x[1] else datetime.datetime.max)
        boss_list_sorted = [x[0] for x in boss_timers_sorted] + [x for x in boss_list if x not in boss_timers]
        # 보스 리스트와 예상 출현 시간을 문자열로 변환합니다.
        boss_str = '\n'.join([f"[{boss}] 출현 예상 : {boss_timers[boss]['time'].strftime('%H:%M:%S')}" if boss in boss_timers else f"[{boss}] 출현 예상 : " for boss in boss_list_sorted])
        await message.channel.send(f"```{boss_str}```")

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
``
