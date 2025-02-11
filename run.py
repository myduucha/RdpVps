import os
import subprocess
import shutil
import random
import string

# طلب كود المصادقة من المستخدم
CRD_SSH_Code = input("Google CRD SSH Code: ").strip()
if not CRD_SSH_Code:
    print("❌ خطأ: يجب إدخال كود المصادقة.")
    exit(1)

# إنشاء اسم مستخدم عشوائي (لتجنب الحسابات الثابتة)
username = "user_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

# إنشاء كلمة مرور قوية وعشوائية
password = "".join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()", k=16))

# إنشاء رقم PIN عشوائي (6 أرقام)
pin = "".join(random.choices(string.digits, k=6))

print(f"🔹 إنشاء مستخدم جديد: {username}")
os.system(f"useradd -m {username}")
os.system(f"echo '{username}:{password}' | sudo chpasswd")
os.system(f"adduser {username} sudo")  # الإبقاء على صلاحيات sudo

# إعداد CRD
class CRDSetup:
    def __init__(self, user):
        os.system("apt update -y")
        self.installCRD()
        self.installDesktopEnvironment()
        self.installGoogleChrome()
        self.installTelegram()
        self.installQbit()
        self.finish(user)

    @staticmethod
    def installCRD():
        url = "https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb"
        file_name = "chrome-remote-desktop.deb"
        subprocess.run(['wget', '-q', '-O', file_name, url], check=True)
        subprocess.run(['dpkg', '--install', file_name])
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'])
        print("✅ تم تثبيت Chrome Remote Desktop")

    @staticmethod
    def installDesktopEnvironment():
        os.system("export DEBIAN_FRONTEND=noninteractive")
        os.system("apt install -y xfce4 xfce4-goodies xfce4-terminal")
        with open("/etc/chrome-remote-desktop-session", "w") as f:
            f.write("exec /etc/X11/Xsession /usr/bin/xfce4-session\n")
        os.system("apt remove -y gnome-terminal")
        os.system("apt install -y xscreensaver")
        os.system("systemctl disable lightdm.service")
        print("✅ تم تثبيت بيئة سطح المكتب XFCE4")

    @staticmethod
    def installGoogleChrome():
        url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
        file_name = "google-chrome.deb"
        subprocess.run(["wget", "-q", "-O", file_name, url], check=True)
        subprocess.run(["dpkg", "--install", file_name])
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'])
        print("✅ تم تثبيت Google Chrome")

    @staticmethod
    def installTelegram():
        subprocess.run(["apt", "install", "--assume-yes", "telegram-desktop"])
        print("✅ تم تثبيت Telegram")

    @staticmethod
    def installQbit():
        subprocess.run(["apt", "install", "-y", "qbittorrent"])
        print("✅ تم تثبيت qBittorrent")

    @staticmethod
    def finish(user):
        os.system(f"adduser {user} chrome-remote-desktop")
        command = f"{CRD_SSH_Code} --pin={pin}"
        os.system(f"su - {user} -c '{command}'")
        os.system("service chrome-remote-desktop start")
        
        print("\n🚀 **تم الإعداد بنجاح!** 🚀")
        print(f"🔹 اسم المستخدم: {user}")
        print(f"🔹 كلمة المرور: {password}")
        print(f"🔹 رقم PIN للاتصال: {pin}")
        print("\n💡 استخدم هذه المعلومات لتسجيل الدخول.")

try:
    CRDSetup(username)
except Exception as e:
    print(f"❌ خطأ أثناء الإعداد: {e}")
