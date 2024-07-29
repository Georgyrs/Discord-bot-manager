import discord
from discord.ext import commands
import json
import os
import datetime

bot = commands.Bot(command_prefix='Q', intents=discord.Intents.all())

# Load or initialize user data
if os.path.exists('user_data.json'):
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
else:
    user_data = {}

level_thresholds = [0, 10, 50, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500,
                    1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100,
                    3200, 3300, 3400, 3500, 3600, 3700]

@bot.event
async def on_ready():
    print("The bot is now online!")

def get_level(exp):
    for i, threshold in enumerate(level_thresholds):
        if exp < threshold:
            return i
    return len(level_thresholds)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    if user_id not in user_data:
        user_data[user_id] = {"exp": 0, "level": 0, "punishments": 0, "joined_at": str(message.author.joined_at), "last_message": "", "voice_time": 0}

    user_data[user_id]["exp"] += 1
    user_data[user_id]["last_message"] = message.content
    new_level = get_level(user_data[user_id]["exp"])

    if new_level > user_data[user_id]["level"]:
        user_data[user_id]["level"] = new_level
        await message.channel.send(f"{message.author.mention} достиг {new_level} уровня!")
        await assign_role(message.author, new_level)

    save_user_data()
    await bot.process_commands(message)

async def assign_role(member, level):
    guild = member.guild
    roles = {
        1: "Level 1",
        5: "Level 5",
        10: "Level 10",
        15: "Level 15",
        20: "Level 20",
        25: "Level 25",
        30: "Level 30",
        35: "Level 35",
        40: "Level 40"
    }

    for lvl, role_name in roles.items():
        role = discord.utils.get(guild.roles, name=role_name)
        if level >= lvl:
            if role not in member.roles:
                await member.add_roles(role)
        else:
            if role in member.roles:
                await member.remove_roles(role)

def save_user_data():
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

@bot.command()
async def leaderboard(ctx):
    leaderboard = sorted(user_data.items(), key=lambda item: item[1].get("exp", 0), reverse=True)
    embed = discord.Embed(title="Leaderboard")
    for i, (user_id, data) in enumerate(leaderboard):
        user = await bot.fetch_user(int(user_id))
        if user:
            embed.add_field(name=f"{i + 1}. {user.name}",
                            value=f"Уровень: {data.get('level', 0)}, Сообщения: {data.get('exp', 0)}", inline=False)
    await ctx.send(embed=embed)

# Moderation commands
@bot.command()
async def hello(ctx):
    username = ctx.message.author.mention
    await ctx.send("Приветствую, " + username)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def ban(ctx, member: discord.Member, *, reason=None):
    user_id = str(member.id)
    if user_id in user_data:
        user_data[user_id]["punishments"] += 1
    else:
        user_data[user_id] = {"exp": 0, "level": 0, "punishments": 1, "joined_at": str(member.joined_at)}

    save_user_data()

    if reason is None:
        reason = "Пользователь забанен " + ctx.message.author.name
    await member.ban(reason=reason)
    await ctx.send(f"Пользователь {member.mention} был забанен по причине: {reason}")
  #  await member.send(f"Вы были забанены на сервере {ctx.guild.name} по причине: {reason}")

    channel = discord.utils.get(ctx.guild.channels, name='ml')
    if channel:
        embed = discord.Embed(
            title="Пользователь забанен",
            description=f"{member.mention} был забанен.",
            color=discord.Color.red()
        )
        embed.add_field(name="Причина", value=reason, inline=False)
        embed.add_field(name="Модератор", value=ctx.message.author.mention, inline=False)
        await channel.send(embed=embed)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def kick(ctx, member: discord.Member, *, reason=None):
    user_id = str(member.id)
    if user_id in user_data:
        user_data[user_id]["punishments"] += 1
    else:
        user_data[user_id] = {"exp": 0, "level": 0, "punishments": 1, "joined_at": str(member.joined_at)}

    save_user_data()

    if reason is None:
        reason = "Пользователь был кикнут " + ctx.message.author.name
    await member.kick(reason=reason)
    await ctx.send(f"Пользователь {member.mention} был кикнут по причине: {reason}")
   # await member.send(f"Вы были кикнуты с сервера {ctx.guild.name} по причине: {reason}")

    channel = discord.utils.get(ctx.guild.channels, name='ml')
    if channel:
        embed = discord.Embed(
            title="Пользователь кикнут",
            description=f"{member.mention} был кикнут.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Причина", value=reason, inline=False)
        embed.add_field(name="Модератор", value=ctx.message.author.mention, inline=False)
        await channel.send(embed=embed)

@bot.command()
async def mute(ctx, member: discord.Member, timelimit: str, *, reason=None):
    user_id = str(member.id)
    if user_id in user_data:
        user_data[user_id]["punishments"] += 1
    else:
        user_data[user_id] = {"exp": 0, "level": 0, "punishments": 1, "joined_at": str(member.joined_at)}

    save_user_data()

    if reason is None:
        reason = "Пользователь замучен " + ctx.message.author.name
    if "s" in timelimit:
        gettime = timelimit.strip("s")
        if int(gettime) > 2419200:
            await ctx.send("The mute time amount cannot be bigger than 28 days")
        else:
            newtime = datetime.timedelta(seconds=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
            await ctx.send(f"Пользователь {member.mention} был замучен на {gettime} секунд по причине: {reason}")
            await member.send(f"Вы были замучены на сервере {ctx.guild.name} на {gettime} секунд по причине: {reason}")
    elif "m" in timelimit:
        gettime = timelimit.strip("m")
        if int(gettime) > 40320:
            await ctx.send("The mute time amount cannot be bigger than 28 days")
        else:
            newtime = datetime.timedelta(minutes=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
            await ctx.send(f"Пользователь {member.mention} был замучен на {gettime} минут по причине: {reason}")
            await member.send(f"Вы были замучены на сервере {ctx.guild.name} на {gettime} минут по причине: {reason}")
    elif "h" in timelimit:
        gettime = timelimit.strip("h")
        if int(gettime) > 672:
            await ctx.send("The mute time amount cannot be bigger than 28 days")
        else:
            newtime = datetime.timedelta(hours=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
            await ctx.send(f"Пользователь {member.mention} был замучен на {gettime} часов по причине: {reason}")
            await member.send(f"Вы были замучены на сервере {ctx.guild.name} на {gettime} часов по причине: {reason}")
    elif "d" in timelimit:
        gettime = timelimit.strip("d")
        if int(gettime) > 28:
            await ctx.send("The mute time amount cannot be bigger than 28 days")
        else:
            newtime = datetime.timedelta(days=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
            await ctx.send(f"Пользователь {member.mention} был замучен на {gettime} дней по причине: {reason}")
            await member.send(f"Вы были замучены на сервере {ctx.guild.name} на {gettime} дней по причине: {reason}")
    else:
        await ctx.send("Неверный формат. Используйте s - секунды, m - минуты, h - часы...")

    channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
    if channel:
        embed = discord.Embed(
            title="Пользователь замучен",
            description=f"{member.mention} был замучен на {timelimit}.",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Причина", value=reason, inline=False)
        embed.add_field(name="Модератор", value=ctx.message.author.mention, inline=False)
        await channel.send(embed=embed)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def unmute(ctx, member: discord.Member):
    await member.edit(timed_out_until=None)
    await ctx.send(f"Пользователь {member.mention} был размучен.")
    await member.send(f"Вы были размучены на сервере {ctx.guild.name}.")

    channel = discord.utils.get(ctx.guild.channels, name='moderation-logs')
    if channel:
        embed = discord.Embed(
            title="Пользователь размучен",
            description=f"{member.mention} был размучен.",
            color=discord.Color.green()
        )
        embed.add_field(name="Модератор", value=ctx.message.author.mention, inline=False)
        await channel.send(embed=embed)

@bot.command()
@commands.has_any_role("Owner", "Administrator", "Helper")
async def user(ctx, member: discord.Member):
    user_id = str(member.id)
    if user_id in user_data:
        user_info = user_data[user_id]
        joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
        level = user_info.get("level", 0)
        exp = user_info.get("exp", 0)
        punishments = user_info.get("punishments", 0)
        last_message = user_info.get("last_message", "No message yet")
        voice_time = user_info.get("voice_time", 0)
        embed = discord.Embed(title=f"Информация о пользователе {member.name}")
        embed.add_field(name="Дата присоединения", value=joined_at, inline=False)
        embed.add_field(name="Уровень", value=level, inline=False)
        embed.add_field(name="Опыт", value=exp, inline=False)
        embed.add_field(name="Количество наказаний", value=punishments, inline=False)
        embed.add_field(name="Последнее сообщение", value=last_message, inline=False)
        embed.add_field(name="Время в голосовом чате (в секундах)", value=voice_time, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Нет данных для пользователя {member.name}.")

# Event for logging member join
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='enterleave-logs')
    if channel:
        created_at = member.created_at.strftime("%Y-%m-%d %H:%M:%S")
        embed = discord.Embed(
            title="Новый участник!",
            description=f"{member.mention} присоединился к сообществу.",
            color=discord.Color.green()
        )
        embed.add_field(name="Дата создания аккаунта", value=created_at, inline=False)
        await channel.send(embed=embed)

# Event for logging member leave
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name='enterleave-logs')
    if channel:
        created_at = member.created_at.strftime("%Y-%m-%d %H:%M:%S")
        embed = discord.Embed(
            title="Пока пока!",
            description=f"{member.mention} покинул сообщество.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Дата создания аккаунта", value=created_at, inline=False)
        await channel.send(embed=embed)

# Track voice state updates
@bot.event
async def on_voice_state_update(member, before, after):
    user_id = str(member.id)
    if user_id not in user_data:
        user_data[user_id] = {"exp": 0, "level": 0, "punishments": 0, "joined_at": str(member.joined_at), "last_message": "", "voice_time": 0}

    now = datetime.datetime.utcnow()
    if before.channel is None and after.channel is not None:
        user_data[user_id]["voice_join_time"] = now
    elif before.channel is not None and after.channel is None:
        if "voice_join_time" in user_data[user_id]:
            join_time = user_data[user_id]["voice_join_time"]
            voice_time = (now - join_time).total_seconds()
            user_data[user_id]["voice_time"] += voice_time
            del user_data[user_id]["voice_join_time"]

    save_user_data()

# Log message edits
@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return

    channel = discord.utils.get(before.guild.channels, name='msglogs')
    if channel:
        embed = discord.Embed(
            title="Сообщение изменено",
            description=f"Сообщение от {before.author.mention} было изменено.",
            color=discord.Color.blue()
        )
        embed.add_field(name="До", value=before.content, inline=False)
        embed.add_field(name="После", value=after.content, inline=False)
        embed.add_field(name="Канал", value=before.channel.mention, inline=False)
        await channel.send(embed=embed)

# Log message deletions
@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    channel = discord.utils.get(message.guild.channels, name='msglogs')
    if channel:
        embed = discord.Embed(
            title="Сообщение удалено",
            description=f"Сообщение от {message.author.mention} было удалено.",
            color=discord.Color.red()
        )
        embed.add_field(name="Содержание", value=message.content, inline=False)
        embed.add_field(name="Канал", value=message.channel.mention, inline=False)
        await channel.send(embed=embed)


# Log role creation
@bot.event
async def on_guild_role_create(role):
    channel = discord.utils.get(role.guild.channels, name='serverlogs')
    if channel:
        embed = discord.Embed(
            title="Роль создана",
            description=f"Роль {role.name} была создана.",
            color=discord.Color.green()
        )
        await channel.send(embed=embed)

# Log role deletion
@bot.event
async def on_guild_role_delete(role):
    channel = discord.utils.get(role.guild.channels, name='serverlogs')
    if channel:
        embed = discord.Embed(
            title="Роль удалена",
            description=f"Роль {role.name} была удалена.",
            color=discord.Color.red()
        )
        await channel.send(embed=embed)

# Log permission updates
@bot.event
async def on_guild_update(before, after):
    channel = discord.utils.get(before.guild.channels, name='serverlogs')
    if channel:
        embed = discord.Embed(
            title="Права изменены",
            description=f"Права на сервере {before.name} были изменены.",
            color=discord.Color.orange()
        )
        await channel.send(embed=embed)
bot.run('YOUR TOKEN HERE')
