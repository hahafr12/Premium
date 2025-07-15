import os
import subprocess

def clear():
    os.system('clear')

def banner():
    print("  _____              _ _      ")
    print(" |  __ \\            ( ) |     ")
    print(" | |  | | ___  _ __ |/| |_    ")
    print(" | |  | |/ _ \\| '_ \\  | __|   ")
    print(" | |__| | (_) | | | | | |_    ")
    print(" |_____/ \\___/|_| |_|  \\__|   ")
    print()
    print("  ____                                ")
    print(" |  _ \\                               ")
    print(" | |_) | ___     ______     _ _       ")
    print(" |  _ < / _ \\   |  ____|   (_) |      ")
    print(" | |_) |  __/   | |____   ___| |      ")
    print(" |____/ \\___|   |  __\\ \\ / / | |      ")
    print("                | |___\\ V /| | |      ")
    print("                |______\\_/ |_|_|      ")
    print()

def main_menu():
    input("Bu aracı sadece eğitim amaçlı kullanın. Devam etmek için Enter'a basın.")
    clear()
    print("   1. Boot2Root    ")
    print("   2. JustRoot     ")
    print()
    print("Sürüm 1.1")
    choice = input("Seçiminizi girin (1 veya 2): ")
    return choice

def install_packages():
    subprocess.run(["apt", "update", "-y"])
    subprocess.run(["apt", "upgrade", "-y"])
    for pkg in ["wget", "openssl-tool", "proot", "bash", "nano", "neofetch"]:
        subprocess.run(["apt", "install", pkg, "-y"])
    os.system("termux-setup-storage")

def setup_kali():
    etc_dir = "/data/data/com.termux/files/usr/etc"
    root_dir = os.path.join(etc_dir, "Root")
    os.makedirs(root_dir, exist_ok=True)

    os.chdir(root_dir)
    subprocess.run([
        "wget",
        "https://raw.githubusercontent.com/EXALAB/AnLinux-Resources/master/Scripts/Installer/Kali/kali.sh"
    ])
    subprocess.run(["bash", "kali.sh"])

def apply_choice(choice):
    bashrc = "/data/data/com.termux/files/usr/etc/bash.bashrc"
    root_script = "bash /data/data/com.termux/files/usr/etc/Root/start-kali.sh"

    if choice == "1":
        with open(bashrc, "a") as f:
            f.write(f"\n{root_script}\n")
        print("\nTermux'u yeniden başlatın, root olarak açılacaktır.")
    elif choice == "2":
        with open(bashrc, "a") as f:
            f.write(f"\nalias rootme='{root_script}'\n")
        os.system(f"source {bashrc}")
        print("\nTermux'u yeniden başlatın ve root olmak için herhangi bir yerde 'rootme' yazın.")
    else:
        print("""
   ___   ___  _ __  ___  
  / _ \\ / _ \\| '_ \\/ __| 
 | (_) | (_) | |_) \\__ \\ 
  \\___/ \\___/| .__/|___/ 
             | |         
             |_|         
Beklenmeyen bir hata oluştu. Lütfen doğru bir seçim yapın ve tekrar deneyin.
""")
        exit()

def credit_info():
    print("\nRoot işlemi AnLinux tarafından sağlanmıştır.")
    print("Araç geliştirici: Ajay")
    print("\nİletişim:")
    print("Telegram  : Tamilhackz (public group)")
    print("Instagram : tamilhackz_ ")
    print("Twitter   : TamilHackz ")
    print("\nYouTube bilgileri kaldırılmıştır.\n")

if __name__ == "__main__":
    clear()
    banner()
    choice = main_menu()
    install_packages()
    os.chdir("/data/data/com.termux/files/usr/etc/")
    os.system("cp bash.bashrc bash.bashrc.bak")
    setup_kali()
    clear()
    os.system("neofetch")
    apply_choice(choice)
    credit_info()