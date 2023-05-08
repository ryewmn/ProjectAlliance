import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_components import DiscordComponents, Button, ButtonStyle

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)
queue = []


@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')


@bot.event
async def on_button_click(res):
    global queue
    if res.component.custom_id == 'join_queue':
        if len(queue) >= 10:
            await res.respond(content='Queue is full, please wait.')
        elif res.user.id not in queue:
            queue.append(res.user.id)
            await res.respond(content='You have joined the queue.')
        else:
            await res.respond(content='You are already in the queue.')
    elif res.component.custom_id == 'leave_queue':
        if res.user.id in queue:
            queue.remove(res.user.id)
            await res.respond(content='You have left the queue.')
        else:
            await res.respond(content='You are not in the queue.')


@slash.slash(name="queue_status", description="Check the current queue status.")
async def _queue_status(ctx: SlashContext):
    if not queue:
        await ctx.send('The queue is empty.')
    else:
        queue_list = [f'<@{user_id}>' for user_id in queue]
        await ctx.send(f'Current queue ({len(queue)}): {", ".join(queue_list)}')


@slash.slash(name="prompt_buttons", description="Prompt the join and leave queue buttons.")
async def _prompt_buttons(ctx: SlashContext):
    buttons = [
        Button(style=ButtonStyle.green, label='Join Queue', custom_id='join_queue'),
        Button(style=ButtonStyle.red, label='Leave Queue', custom_id='leave_queue')
    ]
    await ctx.send(content='Choose an action:', components=[buttons])


bot.run('your_bot_token')
