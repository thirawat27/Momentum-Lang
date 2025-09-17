import sys
import os
import asyncio

try:
    import colorama
    from colorama import Fore, Style, init
    colorama_enabled = True
except ImportError:
    colorama_enabled = False

# Import ฟังก์ชันและตัวแปรที่จำเป็นจาก intp.py
from intp import run_momentum, run_repl, MomentumError, MomentumExit, GFX_GLOBALS, gfx_wait

# โลโก้ ASCII Art ของ Momentum
MOMENTUM_LOGO = r"""
 ███▄ ▄███▓ ▒█████   ███▄ ▄███▓▓█████  ███▄    █ ▄▄▄█████▓ █    ██  ███▄ ▄███▓
▓██▒▀█▀ ██▒▒██▒  ██▒▓██▒▀█▀ ██▒▓█   ▀  ██ ▀█   █ ▓  ██▒ ▓▒ ██  ▓██▒▓██▒▀█▀ ██▒
▓██    ▓██░▒██░  ██▒▓██    ▓██░▒███   ▓██  ▀█ ██▒▒ ▓██░ ▒░▓██  ▒██░▓██    ▓██░
▒██    ▒██ ▒██   ██░▒██    ▒██ ▒▓█  ▄ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▓▓█  ░██░▒██    ▒██ 
▒██▒   ░██▒░ ████▓▒░▒██▒   ░██▒░▒████▒▒██░   ▓██░  ▒██▒ ░ ▒▒█████▓ ▒██▒   ░██▒
░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒░   ░  ░░░ ▒░ ░░ ▒░   ▒ ▒   ▒ ░░   ░▒▓▒ ▒ ▒ ░ ▒░   ░  ░
░  ░      ░  ░ ▒ ▒░ ░  ░      ░ ░ ░  ░░ ░░   ░ ▒░    ░    ░░▒░ ░ ░ ░  ░      ░
░      ░   ░ ░ ░ ▒  ░      ░      ░      ░   ░ ░   ░       ░░░ ░ ░ ░      ░   
       ░       ░ ░         ░      ░  ░         ░             ░            ░   
"""

def main():
    """Main function: process arguments, run the interpreter asynchronously, and handle program exit."""
    if colorama_enabled:
        init(autoreset=True)

    exit_code = 0
    try:
        if len(sys.argv) > 1:
            # --- โหมดรันไฟล์ ---
            filename = sys.argv[1]
            if not os.path.exists(filename):
                print(Fore.MAGENTA + Style.BRIGHT + f"❌ Error: File '{filename}' not found")
                exit_code = 1
            else:
                # ใช้สีม่วง (MAGENTA) เป็นธีมหลัก
                header = Fore.MAGENTA + "🚀 Running file: " + Style.BRIGHT + Fore.WHITE + os.path.basename(filename)
                print(header)
                print(Fore.MAGENTA + "-" * (len(os.path.basename(filename)) + 18))
                
                asyncio.run(run_momentum(filename))

                print(Fore.MAGENTA + "-" * (len(os.path.basename(filename)) + 18))
                print(Fore.GREEN + Style.BRIGHT + "✅ Program completed successfully")
        else:
            # --- โหมด REPL ---
            print(Style.BRIGHT + Fore.MAGENTA + MOMENTUM_LOGO)
            print(Style.BRIGHT + Fore.WHITE + "Momentum Language")
            print(Fore.MAGENTA + "---------------------------------------------------\n")
            
            asyncio.run(run_repl())
            
    except MomentumExit as e:
        # ดักจับเมื่อผู้ใช้เรียก exit() ในโค้ด
        print(Fore.YELLOW + f"\nProgram exited with code {e.code}.")
        exit_code = e.code
    except (MomentumError, Exception):
        # ดักจับข้อผิดพลาดจาก Interpreter และข้อผิดพลาดอื่นๆ
        print(Fore.MAGENTA + Style.BRIGHT + "\n❌ Program terminated due to an error.")
        exit_code = 1
        
    finally:
        # ส่วนนี้จะทำงานเสมอ
        if GFX_GLOBALS.get("window"):
            print(Fore.YELLOW + "\nGraphic window is running, close the window to finish...")
            gfx_wait()
        
        # รอให้ผู้ใช้กด Enter ก่อนปิดหน้าต่าง
        if sys.stdout.isatty():
             input(Style.DIM + "\nPress Enter to exit...")
        
        sys.exit(exit_code)

if __name__ == "__main__":
    main()