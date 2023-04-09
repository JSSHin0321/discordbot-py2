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


    # '컷'이 들어간 메시지에 대한 처리입니다.
    elif message.content.endswith('컷'):
        # 보스 이름을 추출합니다.
        boss_name = message.content[:-1].strip()

        # 보스 이름이 존재하지 않는 경우, 에러 메시지를 전송합니다.
        if boss_name not in boss_list:
            await message.channel.send(f"{boss_name} 보스는 존재하지 않는 보스입니다.")
        else:
            # 보스 이름이 존재하는 경우, 보스 타이머를 초기화하고 3시간 후에 다시 출현한다는 메시지를 전송합니다.
            # 보스 타이머를 UTC 기준으로 계산합니다.
            boss_timers[boss_name] = {
                'time': datetime.datetime.utcnow() + datetime.timedelta(hours=3),
                'author': message.author.id
            }
            # 한국 시간으로 변환합니다.
            boss_timers[boss_name]['time'] += datetime.timedelta(hours=9)
            # 예상 시간을 한국 시간으로 표기합니다.
            expected_time_str = boss_timers[boss_name]['time'].strftime('%H:%M:%S')
            # 작성자 아이디를 가져와 메시지를 전송합니다.
            author_name = message.author.name
            await message.channel.send(f"{boss_name} 보스 타이머가 초기화되었고, {expected_time_str} 에 다시 출현합니다. / {author_name}")

    # "보스이름 시간" 형태의 메시지에 대한 처리입니다.
    elif len(message.content.split()) == 2:
        args = message.content.split()
        if args[0] in boss_list:
            # 입력된 시간을 파싱합니다.
            try:
                expected_time_kst = datetime.datetime.strptime(args[1], '%H%M')
            except ValueError:
                await message.channel.send('잘못된 시간 형식입니다. (HHMM)')
                return

            # 보스 타이머를 초기화하고 예상 출현 시간을 계산합니다.
            # 보스 타이머를 UTC 기준으로 계산합니다.
            now = datetime.datetime.utcnow()
            expected_time_utc = datetime.datetime(now.year, now.month, now.day, expected_time_kst.hour, expected_time_kst.minute, 0) + datetime.timedelta(hours=3)
            # 입력된 시간이 현재 시간보다 이전인 경우, 날짜를 하루 추가합니다.
            if expected_time_utc < now:
                expected_time_utc += datetime.timedelta(days=1)
            boss_timers[args[0]] = {
                'time': expected_time_utc,
                'author': message.author.id
            }
            # 예상 시간을 한국 시간으로 표기합니다.
            expected_time_str = expected_time_utc.strftime('%H:%M:%S')
            # 작성자 아이디를 가져와 메시지를 전송합니다.
            author_name = message.author.name
            await message.channel.send(f"{args[0]} 보스 출현 시간이 변경되었습니다. / {author_name}")


    # "보스 초기화" 형태의 메시지에 대한 처리입니다.
    elif len(message.content.split()) == 2 and message.content.split()[1] == '초기화':
        boss_name = message.content.split()[0]
        if boss_name in boss_timers:
            del boss_timers[boss_name]
            await message.channel.send(f"{boss_name} 보스 타이머가 초기화되었습니다.")
        else:
            await message.channel.send(f"{boss_name} 보스 타이머가 존재하지 않습니다.")



try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
