import os
import platform
import psutil
import socket
import getpass
import time

def get_system_info():
    user = getpass.getuser()
    hostname = socket.gethostname()
    
    # ОС
    os_name = f"{platform.system()} {platform.release()}"
    os_version = f"(Build {platform.version().split('.')[2]})" if '.' in platform.version() else ""
    
    # Аптайм
    uptime_seconds = time.time() - psutil.boot_time()
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    
    # CPU (Безопасный метод без внешних библиотек)
    cpu_brand = platform.processor()
    # Обрезаем лишнее, если строка слишком длинная
    if len(cpu_brand) > 40:
        cpu_brand = cpu_brand[:40] + "..."
    
    # Память
    ram = psutil.virtual_memory()
    ram_total = round(ram.total / (1024 ** 3), 1)
    ram_used = round(ram.used / (1024 ** 3), 1)
    ram_percent = ram.percent

    # Диск C:
    disk = psutil.disk_usage('C:\\')
    disk_total = round(disk.total / (1024 ** 3), 1)
    disk_used = round(disk.used / (1024 ** 3), 1)
    disk_percent = disk.percent

    # IP-адрес (с таймаутом, чтобы не висло, если нет сети)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1.0) # Ждем максимум 1 секунду
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    # Разрешение экрана
    try:
        import ctypes
        user32 = ctypes.windll.user32
        resolution = f"{user32.GetSystemMetrics(0)}x{user32.GetSystemMetrics(1)}"
    except:
        resolution = "Unknown"

    # Тема (читаем аккуратно)
    theme = "Dark" # По умолчанию ставим темную
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        theme_val, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        theme = "Light" if theme_val == 1 else "Dark"
        winreg.CloseKey(key)
    except Exception:
        pass # Если не получилось прочитать, оставляем "Dark"

    info = [
        ("", f"{user}@{hostname}"),
        ("", "─" * 25),
        ("OS", f"{os_name} {os_version}".strip()),
        ("Host", platform.machine()),
        ("Uptime", f"{hours} hours, {minutes} mins"),
        ("Shell", "PowerShell / CMD"),
        ("Resolution", resolution),
        ("Theme", theme),
        ("CPU", cpu_brand),
        ("Memory", f"{ram_used} GiB / {ram_total} GiB ({ram_percent}%)"),
        ("Disk (C:)", f"{disk_used} GiB / {disk_total} GiB ({disk_percent}%)"),
        ("Local IP", local_ip),
    ]
    return info

def get_accent_color_ansi():
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM")
        color_val, _ = winreg.QueryValueEx(key, "ColorizationColor")
        winreg.CloseKey(key)
        b = (color_val >> 16) & 0xFF
        g = (color_val >> 8) & 0xFF
        r = color_val & 0xFF
        return f"\033[38;2;{r};{g};{b}m"
    except Exception:
        return "\033[94m" # Синий по умолчанию

def print_fetch():
    # Твой логотип
    logo = [
        ".----------------.",
        "|          _       |",
        "|      _.-'|'-._   |",
        "| .__.|    |    |  |",
        "|     |_.-'|'-._|  |",
        "| '--'|    |    |  |",
        "| '--'|_.-'`'-._|  |",
        "| '--'          `  |",
        "'----------------'",
    ]

    info = get_system_info()
    max_len = max(len(logo), len(info))

    C_ACCENT = get_accent_color_ansi()
    C_VALUE = "\033[97m"
    C_RESET = "\033[0m"   

    logo_width = max(len(line) for line in logo) + 2

    for i in range(max_len):
        if i < len(logo):
            left = logo[i].ljust(logo_width)
        else:
            left = " " * logo_width

        if i < len(info):
            title, value = info[i]
            if title == "":
                right = f"{C_ACCENT}{value}{C_RESET}"
            else:
                right = f"{C_ACCENT}{title}:{C_RESET} {C_VALUE}{value}{C_RESET}"
        else:
            right = ""

        print(f"{C_ACCENT}{left}{C_RESET} {right}")

if __name__ == "__main__":
    print_fetch()