import discord
from discord.ext import commands
import json

with open("config.json") as file:
    CONFIG = json.load(file)
TOKEN = CONFIG["token"]


class Bot(commands.Bot):
    async def on_ready(self):
        print(f"Плеер дурак зашёл под {self.user}")


intents = discord.Intents.default()
intents.messages = True

bot = Bot(command_prefix="!", intents=intents)


@bot.command(name="послать")
@commands.has_permissions(administrator=True)
async def send(ctx: commands.Context):
    with open("message.txt", "r") as f:
        message = await ctx.send(f"```{f.read()}```")
    with open("emoji.json", "r") as f:
        dictionary = json.load(f)
    for key, value in dictionary.items():
        await message.add_reaction(key)


@bot.command(name="изменить_послание")
@commands.has_permissions(administrator=True)
async def edit_message(ctx: commands.Context, *, message):
    with open("message.txt", "w") as f:
        f.write(message)
    await ctx.send(f"Посланіе измѣнено на:```\n{message}```")


@bot.command(name="посмотреть_реакции")
@commands.has_permissions(administrator=True)
async def load_reactions(ctx: commands.Context):
    with open("emoji.json", "r") as f:
        dictionary = json.load(f)
    await ctx.send(output_dictionary(dictionary))


@bot.command(name="изменить_реакции")
@commands.has_permissions(administrator=True)
async def edit_reactions(ctx: commands.Context, *args):
    print(*args)
    with open("emoji.json", "r") as f:
        dictionary = json.load(f)
        print(dictionary)
        for i in range(len(args)):
            if i % 2 == 1:
                dictionary[args[i - 1]] = args[i]
        print(dictionary)
    with open("emoji.json", "w") as f:
        f.write(json.dumps(dictionary))
        output = output_dictionary(dictionary)
        await ctx.send(f"РЕАКЦИИ ИЗМЕНЕНЫ, ТОВАРИЩ ПРАПОРЩИК!\n{output}")


@bot.command(name="удалить_реакцию")
@commands.has_permissions(administrator=True)
async def delete_reaction(ctx: commands.Context, *, emoji):
    dictionary = load_emoji()
    del dictionary[emoji]
    with open("emoji.json", "w") as f:
        f.write(json.dumps(dictionary))
    await ctx.send(output_dictionary(dictionary))


def output_dictionary(dictionary: dict) -> str:
    print(dictionary)
    output = ""
    for key, value in dictionary.items():
        output += f"{key}: {value}\n"
    return output


def load_emoji():
    with open("emoji.json", "r") as f:
        return json.load(f)


bot.run(TOKEN)
