import discord
from discord import app_commands
from discord.ext import commands
import socket
import requests
import whois
import ssl
import json

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
TOKEN = "BOT_TOKENİNİ_BURAYA_YAZ"

# Slash komut
class DomainQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="domainsorgu", description="Bir domain hakkında bilgi al")
    @app_commands.describe(domain="Sorgulanacak domain (örn: roblox.com)")
    async def domainsorgu(self, interaction: discord.Interaction, domain: str):
        await interaction.response.defer()

        url = f"https://{domain}"

        def get_ip(domain):
            try:
                return socket.gethostbyname(domain)
            except:
                return "IP alınamadı"

        def get_whois(domain):
            try:
                w = whois.whois(domain)
                return str(w.domain_name)
            except:
                return "Whois alınamadı"

        def get_headers(url):
            try:
                headers = requests.get(url, timeout=5).headers
                return dict(headers)
            except:
                return {}

        def get_ssl_info(domain):
            try:
                context = ssl.create_default_context()
                conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
                conn.settimeout(5)
                conn.connect((domain, 443))
                cert = conn.getpeercert()
                return cert['issuer'][0][0][1]
            except:
                return "SSL alınamadı"

        def get_robots(url):
            try:
                response = requests.get(url + "/robots.txt", timeout=5)
                return response.text[:1000] if response.status_code == 200 else "robots.txt yok"
            except:
                return "robots.txt alınamadı"

        ip = get_ip(domain)
        whois_data = get_whois(domain)
        ssl_info = get_ssl_info(domain)
        headers = get_headers(url)
        robots = get_robots(url)

        embed = discord.Embed(title=f"🌐 {domain} Bilgileri", color=0x00ff00)
        embed.add_field(name="IP Adresi", value=ip, inline=False)
        embed.add_field(name="Whois Domain Adı", value=whois_data, inline=False)
        embed.add_field(name="SSL Sertifika Sahibi", value=ssl_info, inline=False)
        embed.add_field(name="User-Agent Başlığı", value=headers.get("User-Agent", "Yok"), inline=False)
        embed.add_field(name="Robots.txt", value=robots or "Yok", inline=False)

        await interaction.followup.send(embed=embed)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Giriş yapıldı: {bot.user}")

bot.add_cog(DomainQuery(bot))
bot.run(TOKEN)
