import asyncio
import datetime
import json
import random
import re
from re import L
from typing import Union

from bs4 import BeautifulSoup
import discord
from discord.ext import commands

import CONFIG
from utils.embed import Embed
from utils.http import HTTP
from utils.invoke import Invoke, need_chunk, with_typing
from utils.logs import Logs


class Chatting(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.logger = Logs.create_logger(self)

    async def cog_after_invoke(self, ctx):
        await Invoke.after_invoke(ctx, self.logger)

    def _html_to_str(self, tag: str) -> str:
        return BeautifulSoup(tag, "lxml").text

    def _lxml_string(self, soup: BeautifulSoup, tag: str) -> str:
        try:
            find = soup.find(tag).string
            if find is None or find == "":
                return "정보 없음"
            return find
        except:
            return "정보 없음"

    def _checkpm10(self, n: int) -> str:
        try:
            n = int(n)
            if n >= 0 and n < 31:
                return "좋음"
            elif n >= 31 and n < 81:
                return "보통"
            elif n >= 80 and n < 151:
                return "`나쁨`"
            elif n >= 151:
                return "**`매우 나쁨`**"
            return ""
        except:
            return ""

    def _checkpm25(self, n: int) -> str:
        try:
            n = int(n)
            if n >= 0 and n < 16:
                return "좋음"
            elif n >= 16 and n < 36:
                return "보통"
            elif n >= 36 and n < 76:
                return "`나쁨`"
            elif n >= 76:
                return "**`매우 나쁨`**"
            return ""
        except:
            return ""

    def _handle_pm(self, soup: BeautifulSoup) -> dict:
        misae_datatime = self._lxml_string(soup, "dataTime")
        seoul = self._lxml_string(soup, "seoul")
        busan = self._lxml_string(soup, "busan")
        daegu = self._lxml_string(soup, "daegu")
        incheon = self._lxml_string(soup, "incheon")
        gwangju = self._lxml_string(soup, "gwangju")
        daejon = self._lxml_string(soup, "daejeon")
        ulsan = self._lxml_string(soup, "ulsan")
        gyeonggi = self._lxml_string(soup, "gyeonggi")
        gangwon = self._lxml_string(soup, "gangwon")
        chungbuk = self._lxml_string(soup, "chungbuk")
        chungnam = self._lxml_string(soup, "chungnam")
        jeonbuk = self._lxml_string(soup, "jeonbuk")
        jeonnam = self._lxml_string(soup, "jeonnam")
        gyeongbuk = self._lxml_string(soup, "gyeongbuk")
        gyeongnam = self._lxml_string(soup, "gyeongnam")
        jeju = self._lxml_string(soup, "jeju")
        sejong = self._lxml_string(soup, "sejong")
        misae_sido = {
            "sido": {
                "서울": seoul,
                "부산": busan,
                "대구": daegu,
                "인천": incheon,
                "광주": gwangju,
                "대전": daejon,
                "울산": ulsan,
                "경기": gyeonggi,
                "강원": gangwon,
                "충북": chungbuk,
                "충남": chungnam,
                "전북": jeonbuk,
                "전남": jeonnam,
                "경북": gyeongbuk,
                "경남": gyeongnam,
                "제주": jeju,
                "세종": sejong,
            },
            "date": misae_datatime,
        }
        return misae_sido

    async def _nmt(self, source: str, target: str, text: str) -> str:
        headers = {
            "X-Naver-Client-Id": CONFIG.PAPAGO_NMT_ID,
            "X-Naver-Client-Secret": CONFIG.PAPAGO_NMT_SECRET,
        }
        data = {"source": source, "target": target, "text": text}

        r = await HTTP.post(
            "https://openapi.naver.com/v1/papago/n2mt",
            data=data,
            headers=headers,
            json=True,
            status=200,
        )

        assert isinstance(r, dict)
        translated = r["message"]["result"]["translatedText"]
        return translated

    async def _smt(self, source: str, target: str, text: str) -> str:
        headers = {
            "X-Naver-Client-Id": CONFIG.PAPAGO_SMT_ID,
            "X-Naver-Client-Secret": CONFIG.PAPAGO_SMT_SECRET,
        }
        data = {"source": source, "target": target, "text": text}

        r = await HTTP.post(
            "https://openapi.naver.com/v1/language/translate",
            data=data,
            headers=headers,
            json=True,
            status=200,
        )
        assert isinstance(r, dict)

        translated = r["message"]["result"]["translatedText"]
        return translated

    @commands.command(name="안녕", aliases=["ㅎㅇ", "gd", "gdgd", "안냥", "잘가"])
    async def hello(self, ctx):
        bot_profile = self.bot.user.avatar_url_as(size=4096)
        embed = discord.Embed(
            title="👋 안녕하세요!",
            description="**봇을 사용해 주셔서 고마워요!**\n봇 / BOT은 BGM#0970이 개발중인 디스코드 봇이에요.\n\n자세한 내용은 `봇 도움` 명령어를 사용해서 볼 수 있어요.",
            color=0x237CCD,
        )
        embed.set_thumbnail(url=bot_profile)
        await ctx.send(embed=embed)

    @commands.command(name="코로나", aliases=["코로나바이러스"])
    async def ncov2019(self, ctx):
        r = await HTTP.get(
            "http://ncov.mohw.go.kr/index_main.jsp", trust_env=True
        )
        soup = BeautifulSoup(r, "lxml")
        boardList = soup.select("ul.liveNum > li > span")
        newstNews = soup.select(".m_news > ul > li > a")[0]

        boardList = [x.text for x in boardList]
        embed = discord.Embed(
            title="🦠 코로나바이러스감염증-19 국내 현황",
            description="[예방수칙](http://ncov.mohw.go.kr/baroView4.do?brdId=4&brdGubun=44)",
            color=0xD8EF56,
        )
        embed.add_field(name="확진환자", value="\n".join(boardList[0:2]))
        embed.add_field(name="완치", value=" ".join(boardList[2:4]))
        embed.add_field(name="사망", value=" ".join(boardList[6:8]), inline=True)

        embed.add_field(
            name="질병관리청 최신 브리핑",
            value="[{}](http://ncov.mohw.go.kr{})".format(
                newstNews.text, newstNews.get("href")
            ),
            inline=False,
        )
        embed.set_footer(text="질병관리청")
        await ctx.send(embed=embed)

    @commands.command(name="따라해")
    async def repeat(self, ctx, *, args):
        if args == "":
            raise commands.BadArgument()

        try:
            await ctx.delete()
        except:
            pass

        await ctx.send(
            args,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, roles=False
            ),
        )

    @commands.command(name="거꾸로", aliases=["뒤집어"])
    async def reverse(self, ctx, *, args):
        if args == "":
            raise commands.BadArgument()

        try:
            await ctx.delete()
        except:
            pass
        await ctx.send(
            args[::-1],
            allowed_mentions=discord.AllowedMentions(
                everyone=False, roles=False
            ),
        )

    @commands.command(name="샤드")
    @commands.guild_only()
    async def guild_shard(self, ctx):
        embed = discord.Embed(
            title="🖥 샤드",
            description=f"이 서버는 샤드 {ctx.guild.shard_id}번에 있어요!",
            color=0x237CCD,
        )
        await ctx.send(embed=embed)

    @commands.command(name="초대", aliases=["초대링크"])
    async def invite_link(self, ctx):
        embed = discord.Embed(
            title="❔ 봇 초대",
            description="저를 초대하고 싶으신가요?\n[여기를 클릭해주세요!](https://discordapp.com/oauth2/authorize?client_id=351733476141170688&scope=bot&permissions=268463166)",
            color=0x1DC73A,
        )
        await ctx.send(embed=embed)

    @commands.command(name="시간계산")
    async def time_calc(self, ctx, *, args):
        try:
            strped_time = datetime.datetime.strptime(args, "%Y-%m-%d")
        except:
            embed = Embed.error("시간 파싱 오류", "yyyy-mm-dd 형식으로 입력해주세요!")
            await ctx.send(embed=embed)
            return

        now = datetime.datetime.now()
        dap = strped_time - now

        days = dap.days
        hours, remainder = divmod(dap.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        seconds += dap.microseconds / 1e6

        embed = discord.Embed(
            title="⏲ 시간 계산",
            description=f"{days}일 {hours}시간 {minutes}분 {round(seconds)}초 {'남았어요.' if days >= 0 else '전이에요.'} ",
            color=0x237CCD,
        )

        await ctx.send(embed=embed)

    @commands.command(name="핑", aliases=["퐁"])
    async def ping(self, ctx):
        ping = str(int(self.bot.latency * 1000))
        embed = discord.Embed(
            title=f"🏓 퐁! {ping}ms",
            description="Discord WebSocket 프로토콜의 레이턴시에요.",
            color=0x237CCD,
        )
        await ctx.send(embed=embed)

    @commands.command(name="리마인더")
    async def reminder(self, ctx, *, args):
        rmd_pat = r"(\d{1,2}h)?\s?(\d{1,2}m)?\s?(\d*s)?"
        hms = re.search(rmd_pat, args)
        hms_group = hms.groups()
        if hms_group == (None, None, None):
            # Embed.warn(
            #     "주의",
            #     "시간 파싱에 실패했어요. 아래 예시를 참고해주세요.\n\n`봇 리마인더 3h` (3시간)\n`봇 리마인더 1h 30m` (1시간 30분)\n`봇 리마인더 20s` (20초)",
            # )
            raise commands.BadArgument()
        reason = args.replace(hms.group(0), "")
        hour = (
            int(hms_group[0].split("h")[0]) if hms_group[0] is not None else 0
        )
        minute = (
            int(hms_group[1].split("m")[0]) if hms_group[1] is not None else 0
        )
        seconds = (
            int(hms_group[2].split("s")[0]) if hms_group[2] is not None else 0
        )

        total_seconds = hour * 3600 + minute * 60 + seconds

        n_hour = total_seconds // 3600
        n_minutes = total_seconds % 3600 // 60
        n_seconds = total_seconds % 3600 % 60
        embed = Embed.check(
            "리마인더", f"{n_hour}시간 {n_minutes}분 {n_seconds}초 후에 알려드릴께요!"
        )
        print(reason)
        if not reason == "":
            embed.add_field(name="사유", value=reason)
        embed.set_footer(text="봇이 종료되면 울리지 않아요!")
        await ctx.send(embed=embed)
        await asyncio.sleep(total_seconds)
        await ctx.send(ctx.author.mention)
        embed = discord.Embed(
            title="⏰ 알림", description="시간이 다 되었어요!", color=0x1DC73A
        )
        if not reason == "":
            embed.add_field(name="사유", value=reason)
        await ctx.send(embed=embed)

    @commands.command(name="조의", aliases=["joy"])
    async def joy(self, ctx):
        emojis = ["❌", "✖", "🇽", "🇯", "🇴", "🇾"]
        for i in emojis:
            await ctx.message.add_reaction(i)

    @commands.command(name="강아지", aliases=["멍멍이", "댕댕이"])
    async def random_dog(self, ctx):
        data = await HTTP.get("http://random.dog/woof.json", json=True)

        assert isinstance(data, dict)
        embed = discord.Embed(title=" ", color=0xF2E820)
        embed.set_image(url=data["url"])
        embed.set_footer(text="http://random.dog")
        await ctx.send(embed=embed)

    @commands.command(name="고양이", aliases=["냥이", "냥냥이"])
    async def random_cat(self, ctx):
        data = await HTTP.get("http://aws.random.cat/meow", json=True)

        assert isinstance(data, dict)
        embed = discord.Embed(title=" ", color=0xF2E820)
        embed.set_image(url=data["file"])
        embed.set_footer(text="http://random.cat")
        await ctx.send(embed=embed)

    @commands.command(name="지진")
    @with_typing
    async def get_earthquake(self, ctx):
        c = await HTTP.get("https://m.kma.go.kr/m/eqk/eqk.jsp?type=korea")
        soup = BeautifulSoup(c, "lxml")

        table = [
            x.text.strip()
            for x in soup.select(".sub-bd2 > table")[0].select("tr > td")
        ]

        img = soup.select(".img-center > a > img")[0]["src"]

        date = table[1]
        mag = table[3]
        max_mag = table[5]
        location = table[7]
        depth = table[9]
        detail = table[10]

        embed = discord.Embed(title="지진 정보", description=date, color=0x62BF42)
        embed.add_field(name="규모 (불확도)", value=mag)
        embed.add_field(name="발생위치", value=location)
        embed.add_field(name="발생긾이", value=depth)
        embed.add_field(name="최대진도", value=max_mag)
        embed.add_field(name="참고사항", value=detail)
        embed.set_footer(text="기상청")
        embed.set_image(url=None or f"http://m.kma.go.kr{img}")

        await ctx.send(embed=embed)

    @commands.command(name="골라", aliases=["선택"])
    async def choice(self, ctx, *, args):
        content = args.strip()
        choice_list = content.split(",")
        embed = discord.Embed(
            title="❔ 봇의 선택",
            description=random.choice(choice_list),
            color=0x1DC73A,
        )
        await ctx.send(embed=embed)

    @commands.command(name="미세먼지", aliases=["초미세먼지"])
    @with_typing
    async def fine_dust(self, ctx, *, args=None):
        params = {
            "serviceKey": CONFIG.MISAE,
            "numOfRows": 1,
            "pageSize": 1,
            "pageNo": 1,
            "startPage": 1,
            "itemCode": "PM10",
            "dataGubun": "HOUR",
        }

        misae_c = await HTTP.get(
            url="http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst",
            params=params,
        )
        soup = BeautifulSoup(misae_c, "lxml-xml")
        misae_sido = self._handle_pm(soup)

        params["itemCode"] = "PM25"
        chomisae_c = await HTTP.get(
            url="http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureLIst",
            params=params,
        )
        soup = BeautifulSoup(chomisae_c, "lxml-xml")
        chomisae_sido = self._handle_pm(soup)

        embed = discord.Embed(
            title="💨 미세먼지",
            desciption="<미세먼지>\n<초미세먼지> 로 알려드려요.",
            color=0x1DC73A,
        )
        embed.set_footer(text=f"에어코리아 | {misae_sido['date']}")

        if args is None:
            for i in misae_sido["sido"].keys():
                embed.add_field(
                    name=i,
                    value=f"{misae_sido['sido'][i]}㎍/m³ |  {self._checkpm10(misae_sido['sido'][i])}\n{chomisae_sido['sido'][i]}㎍/m³ |  {self._checkpm25(chomisae_sido['sido'][i])}",
                    inline=True,
                )
            await ctx.send(embed=embed)
        else:
            if args in misae_sido["sido"].keys():
                embed.add_field(
                    name=args,
                    value=f"{misae_sido['sido'][args]}㎍/m³ |  {self._checkpm10(misae_sido['sido'][args])}\n{chomisae_sido['sido'][args]}㎍/m³ |  {self._checkpm25(chomisae_sido['sido'][args])}",
                    inline=True,
                )
                await ctx.send(embed=embed)
            else:
                embed = Embed.warn(
                    title="주의",
                    description="선택하신 지역 이름을 찾을 수 없어요.\n`봇 미세먼지` 로 전체 지역을 볼 수 있어요.",
                )
                await ctx.send(embed=embed)

    @commands.command(name="프사", aliases=["프로필", "프로필사진"])
    @commands.guild_only()
    @need_chunk
    async def profile_emoji(
        self, ctx, *, user: Union[discord.Member, int, str] = None
    ):
        if user is None:
            user = ctx.author
        elif isinstance(user, int):
            user = ctx.guild.get_member(user)
        elif isinstance(user, str):
            user = ctx.guild.get_member_named(user)
            if user is None:
                raise commands.BadArgument()

        avatar_url = user.avatar_url
        embed = discord.Embed(
            title="🖼️ 프로필 사진",
            description="[원본 보기]({})".format(avatar_url),
            color=0x62BF42,
        )

        embed.set_image(url=avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="한강")
    @with_typing
    async def hangang(self, ctx):
        data = await HTTP.get("http://hangang.dkserver.wo.tc/")

        assert isinstance(data, str)
        data = json.loads(data)

        if data["result"] == "true":
            temp = data["temp"]
            chk_time = data["time"]

            embed = discord.Embed(
                title="🌡 한강 현재수온", description=f"{temp} °C", color=0x62BF42
            )
            embed.set_footer(text=f"퐁당! / {chk_time}")
        else:
            embed = Embed.error(title="오류", description="API에서 정보를 받지 못했어요!")
        await ctx.send(embed=embed)

    @commands.command(name="영한번역")
    @with_typing
    async def en_to_ko(self, ctx, *, args):
        a = args.lstrip()
        trans = await self._nmt("en", "ko", a)
        if trans is None:
            embed = discord.Embed(
                title="❌ 오류 발생", description="번역에 오류가 발생하였어요.", color=0xFF0909,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="✅ 한국어 번역", description=trans, color=0x1DC73A
            )
            await ctx.send(embed=embed)

    @commands.command(name="한영번역")
    @with_typing
    async def ko_to_en(self, ctx, *, args):
        a = args.strip()
        trans = await self._nmt("ko", "en", a)
        if trans is None:
            embed = discord.Embed(
                title="❌ 오류 발생", description="번역에 오류가 발생하였어요.", color=0xFF0909,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="✅ 영어 번역", description=trans, color=0x1DC73A
            )
            await ctx.send(embed=embed)

    @commands.command(name="한일번역")
    @with_typing
    async def ko_to_ja(self, ctx, *, args):
        a = args.strip()
        trans = await self._nmt("ko", "ja", a)
        if trans is None:
            embed = discord.Embed(
                title="❌ 오류 발생", description="번역에 오류가 발생하였어요.", color=0xFF0909,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="✅ 일본어 번역", description=trans, color=0x1DC73A
            )
            await ctx.send(embed=embed)

    @commands.command(name="일한번역")
    @with_typing
    async def ja_to_ko(self, ctx, *, args):
        a = args.strip()
        trans = await self._nmt("ja", "ko", a)
        if trans is None:
            embed = discord.Embed(
                title="❌ 오류 발생", description="번역에 오류가 발생하였어요.", color=0xFF0909,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="✅ 한글 번역", description=trans, color=0x1DC73A
            )
            await ctx.send(embed=embed)

    @commands.command(name="자동번역", aliases=["번역"])
    @with_typing
    async def translate(self, ctx, *, args):
        a = args.strip()
        headers = {
            "X-Naver-Client-Id": CONFIG.PAPAGO_DETECT_ID,
            "X-Naver-Client-Secret": CONFIG.PAPAGO_DETECT_SECRET,
        }
        data = {"query": a}

        r = await HTTP.post(
            "https://openapi.naver.com/v1/papago/detectLangs",
            data=data,
            headers=headers,
            json=True,
        )
        assert isinstance(r, dict)
        langcode = r["langCode"]
        langcode = langcode.replace("zh-cn", "zh-CN")
        langcode = langcode.replace("zh-tw", "zh-TW")

        trans = None
        if langcode == "ko":
            trans = await self._nmt("ko", "en", a)

        else:
            trans = await self._nmt(langcode, "ko", a)

        if trans is None:
            embed = discord.Embed(
                title="❌ 오류 발생",
                description="언어 감지 중 오류가 발생했어요.",
                color=0xFF0909,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="✅ 자동 번역", description=trans, color=0x1DC73A,
            )
            embed.set_footer(text=langcode)
            await ctx.send(embed=embed)

    @commands.command(name="사전", aliases=["백과사전"])
    @with_typing
    async def dictionary(self, ctx, *, args):
        a = args.strip()
        headers = {
            "X-Naver-Client-Id": CONFIG.SEARCH_ID,
            "X-Naver-Client-Secret": CONFIG.SEARCH_SECRET,
        }

        data = await HTTP.get(
            "https://openapi.naver.com/v1/search/encyc.json",
            params={"query": a},
            headers=headers,
            json=True,
        )
        assert isinstance(data, dict)
        data = data["items"][0]
        title = self._html_to_str(data["title"])
        link = data["link"]
        thumbnail = data["thumbnail"]
        description = self._html_to_str(data["description"])

        embed = discord.Embed(
            title="🔖 백과사전",
            description=f"**{title}**에 대한 검색결과에요.",
            color=0x237CCD,
        )
        embed.add_field(
            name="내용", value=f"{description[:500]}\n\n[더 읽기]({link})"
        )
        embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)

    @commands.command(name="서버정보", aliases=["서정"])
    @commands.guild_only()
    @need_chunk
    async def guild_chunk(self, ctx):
        now = datetime.datetime.now()
        creeated_at = ctx.guild.created_at
        now = datetime.datetime.now()
        created_at = ctx.guild.created_at + datetime.timedelta(hours=9)
        dap = now - created_at
        created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")

        members = ctx.guild.members
        bot_count = len([x for x in members if x.bot])
        members_count = len(members)

        txt_ch_cnt = len(ctx.guild.text_channels)
        voi_ch_cnt = len(ctx.guild.voice_channels)

        embed = discord.Embed(
            title="📝 서버 정보",
            description="이 서버에 대한 정보를 불러왔어요.​　　　　　​",
            color=0x1DC73A,
        )
        embed.add_field(name="이름", value=ctx.guild.name, inline=False)
        embed.add_field(name="서버 ID", value=ctx.guild.id, inline=False)
        embed.add_field(
            name="서버 인원",
            value=f"{members_count}명\n(유저 {members_count- bot_count}명, 봇 {bot_count}개)　　​",
            inline=True,
        )
        embed.add_field(
            name="서버 채널",
            value=f"{txt_ch_cnt + voi_ch_cnt}개\n(텍스트 {txt_ch_cnt}개, 음성 {voi_ch_cnt}개)",
            inline=True,
        )

        embed.add_field(name="음성 서버 위치", value=ctx.guild.region, inline=False)
        embed.add_field(name="서버 오너", value=ctx.guild.owner, inline=True)
        embed.add_field(
            name="서버 생성일", value=f"{created_at}\n({dap.days}일 전)", inline=True,
        )

        embed.add_field(
            name="서버 부스트", value=f"{ctx.guild.premium_tier}단계", inline=True,
        )

        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="유저정보", aliases=["유저", "유정"])
    @commands.guild_only()
    @need_chunk
    async def user_info(
        self, ctx, *, user: Union[discord.Member, int, str] = None
    ):
        try:
            if user is None:
                user = ctx.author
            elif isinstance(user, int):
                user = ctx.guild.get_member(user)
            elif isinstance(user, str):
                user = ctx.guild.get_member_named(user)
                if user is None:
                    raise commands.BadArgument()
            now = datetime.datetime.now()
            created_at = user.created_at + datetime.timedelta(hours=9)
            dap_created = now - created_at
            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")

            joined_at = user.joined_at + datetime.timedelta(hours=9)
            dap_joined = now - joined_at
            joined_at = joined_at.strftime("%Y-%m-%d %H:%M:%S")

            avatar_url = user.avatar_url

            embed = discord.Embed(
                title="👥 유저 정보",
                description="선택하신 유저에 대한 정보를 불러왔어요.　　　​",
                color=0x1DC73A,
            )
            embed.add_field(name="이름", value=user.name, inline=False)
            embed.add_field(name="유저 ID", value=user.id, inline=False)
            embed.add_field(
                name="계정 생성일",
                value=f"{created_at}\n({dap_created.days}일 전)",
                inline=True,
            )
            embed.add_field(
                name="서버 가입일",
                value=f"{joined_at}\n({dap_joined.days}일 전)",
                inline=True,
            )
            embed.set_thumbnail(url=avatar_url)
            await ctx.send(embed=embed)
        except:
            embed = Embed.warn(
                "주의", "`봇 유저정보 (멘션 or ID or 이름)` 으로 사용해주세요.\n유저를 불러오지 못했어요.",
            )
            embed.set_footer(text="이 서버에 있는 유저가 아니면 검색이 불가해요.")
            await ctx.send(embed=embed)

    @commands.command(name="질문")
    async def question(self, ctx):
        response = [
            "아니요?",
            "아뇨?",
            "어...음...네",
            "흐음...아뇨?",
            "모르겠어요",
            "네",
            "맞아요",
            "흐음...몰라요",
        ]
        a = random.choice(response)
        await ctx.send(a)

    @commands.command(name="확률")
    async def perpu(self, ctx, *, args):
        a = args.strip()
        per = random.randint(0, 100)
        await ctx.send(f"{a} 확률은 **{per}%** 입니다.")


# TODO : 도움, 문의


def setup(bot) -> None:
    bot.add_cog(Chatting(bot))

