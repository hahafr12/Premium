import os
import platform
import subprocess
import time
from colorama import init, Fore

init(autoreset=True)

current_dir = os.getcwd()

def banner():
    print(Fore.RED + """
┌──(root㉿kali)-[~]
└─# Kali Linux Terminal Emulator
""")

def run_command(cmd):
    global current_dir
    if cmd.startswith("git clone"):
        repo = cmd.split("git clone")[1].strip()
        print(f"[*] Reposu kopyalanıyor: {repo}")
        subprocess.call(["git", "clone", repo])
    
    elif cmd.startswith("ping "):
        host = cmd.split("ping ")[1]
        os.system(f"ping -c 4 {host}")

    elif cmd.startswith("nmap "):
        target = cmd.split("nmap ")[1]
        os.system(f"nmap {target}")

    elif cmd.startswith("whois "):
        target = cmd.split("whois ")[1]
        os.system(f"whois {target}")

    elif cmd.startswith("curl "):
        url = cmd.split("curl ")[1]
        os.system(f"curl {url}")

    elif cmd == "neofetch":
        print(Fore.CYAN + "root@kali\n-----------")
        print("OS: Kali GNU/Linux Rolling")
        print("Host: Custom Emulator")
        print("Kernel: 6.0.0-kali-amd64")
        print("Shell: Bash")
        print("Terminal: Simulated")
        print("CPU: Intel i7")
        print("Memory: 8GB")

    elif cmd == "clear":
        os.system("clear" if platform.system() != "Windows" else "cls")

    elif cmd.startswith("echo "):
        print(cmd.split("echo ", 1)[1])

    elif cmd.startswith("touch "):
        file = cmd.split("touch ")[1]
        open(os.path.join(current_dir, file), 'a').close()
        print(f"{file} oluşturuldu.")

    elif cmd.startswith("rm "):
        file = cmd.split("rm ")[1]
        try:
            os.remove(os.path.join(current_dir, file))
            print(f"{file} silindi.")
        except:
            print("Dosya silinemedi.")

    elif cmd.startswith("mkdir "):
        folder = cmd.split("mkdir ")[1]
        os.makedirs(os.path.join(current_dir, folder), exist_ok=True)
        print(f"{folder} klasörü oluşturuldu.")

    elif cmd == "pwd":
        print(current_dir)

    elif cmd.startswith("cd "):
        target = cmd.split("cd ")[1]
        try:
            os.chdir(os.path.join(current_dir, target))
            current_dir = os.getcwd()
        except:
            print("Klasör bulunamadı.")

    elif cmd == "ls":
        try:
            files = os.listdir(current_dir)
            for f in files:
                print(f)
        except:
            print("Dizin listelenemedi.")

    elif cmd.startswith("cat "):
        file = cmd.split("cat ")[1]
        try:
            with open(os.path.join(current_dir, file), "r") as f:
                print(f.read())
        except:
            print("Dosya okunamadı.")

    elif cmd == "ifconfig":
        print("eth0: inet 192.168.1.10 netmask 255.255.255.0")
        print("wlan0: inet 192.168.1.15 netmask 255.255.255.0")

    elif cmd == "netstat":
        print("Proto Recv-Q Send-Q Local Address           Foreign Address         State")
        print("tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN")
        print("tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN")

    elif cmd == "help":
        print(Fore.YELLOW + """
Kullanabileceğin komutlar:
- git clone <repo>
- ping <host>
- nmap <host>
- whois <domain>
- curl <url>
- neofetch
- ifconfig
- netstat
- echo <text>
- touch <file>
- rm <file>
- mkdir <folder>
- ls
- cd <folder>
- pwd
- cat <file>
- clear
- exit
""")

    elif cmd == "exit":
        print("Çıkılıyor...")
        exit()

    else:
        print(Fore.RED + f"Komut bulunamadı: {cmd}")

def terminal():
    banner()
    while True:
        try:
            cmd = input(Fore.GREEN + f"┌──(root㉿kali)-[{current_dir}]\n└─# ").strip()
            run_command(cmd)
        except KeyboardInterrupt:
            print("\n[!] Çıkmak için 'exit' yazın.")

if __name__ == "__main__":
    terminal()
