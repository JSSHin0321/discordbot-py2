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

# 파티 정보를 저장하는 변수입니다.
party = None

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

    if message.content == '보스맵 1':
        await message.channel.send('https://dszw1qtcnsa5e.cloudfront.net/community/20230404/274c4eee-66f5-4a35-81d4-4b187667f333/40%EB%B3%B4%EC%8A%A4.png?data-size=5309107')

    if message.content == '보스맵 2':
        await message.channel.send('https://dszw1qtcnsa5e.cloudfront.net/community/20230404/716418d7-2576-43c3-9580-3d2bf2d77e58/45%EB%B3%B4%EC%8A%A4.png?data-size=5332128')

    if message.content == '보스맵 3':
        await message.channel.send('https://dszw1qtcnsa5e.cloudfront.net/community/20230404/29c555d6-eb4b-4674-8955-eae7d94b48d1/50%EB%B3%B4%EC%8A%A4.png?data-size=5311083')

    # 파티 모집
    elif message.content == '파티 모집':
        global party
        if party:
            await message.channel.send('이미 진행 중인 파티 모집이 있습니다.')
            return

        party = {'leader': message.author, 'members': []}
        await message.channel.send(f'{message.author.mention}님이 파티 모집을 시작했습니다. 참가하시려면 !참가 를 입력해주세요.')

    # 참가 신청
    elif message.content == '참가':
        global party
        if not party:
            await message.channel.send('진행 중인 파티 모집이 없습니다.')
            return

        if len(party['members']) >= 5:
            await message.channel.send('파티 인원이 꽉 찼습니다.')
            return

        if message.author in party['members']:
            await message.channel.send('이미 참가한 상태입니다.')
            return

        party['members'].append(message.author)
        await message.channel.send(f'{message.author.mention}님이 파티에 참가했습니다. ({len(party["members"])} / 5)')

    # 파티 해산
    elif message.content == f'{PREFIX}파티 해산':
        global party
        if not party:
            await message.channel.send('진행 중인 파티 모집이 없습니다.')
            return

        if message.author != party['leader']:
            await message.channel.send('파티 리더만 파티를 해산할 수 있습니다.')
            return

        members_str = ', '.join([member.mention for member in party['members']])
        await message.channel.send(f'파티가 해산되었습니다. {members_str}')
        party = None
    
    # "보스" 형태의 메시지에 대한 처리입니다.
    elif message.content == '보스':
        # 예상 출현 시간이 빠른 순서대로 보스 목록을 정렬합니다.
        boss_timers_sorted = sorted(boss_timers.items(), key=lambda x: x[1]['time'] if x[1] else datetime.datetime.max)
        boss_list_sorted = [x[0] for x in boss_timers_sorted] + [x for x in boss_list if x not in boss_timers]
        # 보스 리스트와 예상 출현 시간을 문자열로 변환합니다.
        author_name = message.author.display_name
        boss_str = '\n'.join([f"[{boss}] 출현 예상 : {boss_timers[boss]['time'].strftime('%H:%M:%S')} ({author_name})" if boss in boss_timers else f"[{boss}] 출현 예상 : " for boss in boss_list_sorted])
        await message.channel.send(f"```{boss_str}```")


    # "보스 초기화" 형태의 메시지에 대한 처리입니다.
    elif len(message.content.split()) == 2 and message.content.split()[1] == '초기화':
        boss_name = message.content.split()[0]
        if boss_name in boss_timers:
            del boss_timers[boss_name]
            await message.channel.send(f"{boss_name} 보스 타이머가 초기화되었습니다.")
        else:
            await message.channel.send(f"{boss_name} 보스 타이머가 존재하지 않습니다.")


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
            author_name = message.author.display_name
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
            author_name = message.author.display_name
            await message.channel.send(f"{args[0]} 보스 출현 시간이 변경되었습니다. / {author_name}")

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
