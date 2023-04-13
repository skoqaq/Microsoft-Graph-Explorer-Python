import os
import uuid
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox
import msal
import winreg

# 加载环境配置
load_dotenv()

# 获取应用程序参数
CLIENT_ID = os.getenv("APP_CLIENT_ID")
AUTHORITY = os.getenv("APP_AUTHORITY")
SCOPE = [os.getenv("APP_SCOPE")]
REDIRECT_URI = os.getenv("APP_REDIRECT_URI")

# 创建MSAL应用程序对象
app = msal.PublicClientApplication(
    client_id=CLIENT_ID,
    authority=AUTHORITY,
    redirect_uri=REDIRECT_URI
)

# 创建一个窗口
window = tk.Tk()
window.title("Python MS Graph")

# 创建标签和输入框
tk.Label(window, text="Email:").grid(row=0)
email_entry = tk.Entry(window)
email_entry.grid(row=0, column=1)

tk.Label(window, text="Password:").grid(row=1)
password_entry = tk.Entry(window, show="*")
password_entry.grid(row=1, column=1)

# 为每个账户分配一个唯一的uuid
def generate_uuid():
    return str(uuid.uuid4())

# 创建一个添加按钮
def add_account():
    email = email_entry.get()
    password = password_entry.get()
    result = app.acquire_token_by_username_password(email, password, scopes=SCOPE)
    if "access_token" in result:
        # 为账户分配一个uuid，并将其保存到配置文件中
        uuid_str = generate_uuid()
        with open(".env", "a") as f:
            f.write("\\\\n{0}_EMAIL={1}\\\\n{0}_TOKEN={2}".format(uuid_str, email, result["access_token"]))
        messagebox.showinfo("Success", "Account added successfully. UUID: {}".format(uuid_str))
    else:
        messagebox.showerror("Error", "Failed to add account.")

add_button = tk.Button(window, text="Add Account", command=add_account)
add_button.grid(row=2, columnspan=2)

# 创建一个删除按钮
def delete_account():
    uuid_str = uuid_entry.get()
    # 从配置文件中删除账户信息
    with open(".env", "r") as f:
        lines = f.readlines()
    with open(".env", "w") as f:
        for line in lines:
            if not line.startswith(uuid_str):
                f.write(line)
    messagebox.showinfo("Success", "Account deleted successfully. UUID: {}".format(uuid_str))

tk.Label(window, text="UUID:").grid(row=3)
uuid_entry = tk.Entry(window)
uuid_entry.grid(row=3, column=1)

delete_button = tk.Button(window, text="Delete Account", command=delete_account)
delete_button.grid(row=4, columnspan=2)

# 创建一个定时调用按钮
class ScheduleWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Schedule")
        self.window.geometry("300x200")

        # 创建标签和下拉框
        tk.Label(self.window, text="Frequency:").grid(row=0)
        self.frequency_box = ttk.Combobox(self.window, values=["Daily", "Weekly", "Monthly"])
        self.frequency_box.grid(row=0, column=1)

        tk.Label(self.window, text="Time:").grid(row=1)
        self.hour_box = ttk.Spinbox(self.window, from_=0, to=23, width=2)
        self.hour_box.grid(row=1, column=1)
        tk.Label(self.window, text=":").grid(row=1, column=2)
        self.minute_box = ttk.Spinbox(self.window, from_=0, to=59, width=2)
        self.minute_box.grid(row=1, column=3)

        # 创建确定和取消按钮
        tk.Button(self.window, text="OK", command=self.ok).grid(row=2, column=0)
        tk.Button(self.window, text="Cancel", command=self.cancel).grid(row=2, column=1)

    def show(self):
        self.window.mainloop()

    def ok(self):
        frequency = self.frequency_box.get()
        hour = self.hour_box.get()
        minute = self.minute_box.get()

        # 在此处添加定时调用Graph API的代码

        self.window.destroy()

    def cancel(self):
        self.window.destroy()

def schedule():
    schedule_window = ScheduleWindow()
    schedule_window.show()

schedule_button = tk.Button(window, text="Schedule", command=schedule)
schedule_button.grid(row=5, columnspan=2)

# 创建一个开机自动启动按钮
def autostart():
    autostart_button.config(state=tk.DISABLED) # 禁用按钮
    autostart_enabled = winreg.QueryValueEx(winreg.HKEY_CURRENT_USER, "Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run", "Python MS Graph")[0] == sys.argv[0]
    if autostart_enabled:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "Python MS Graph")
        winreg.CloseKey(key)
        messagebox.showinfo("Success", "Autostart disabled.")
    else:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Python MS Graph", 0, winreg.REG_SZ, sys.argv[0])
        winreg.CloseKey(key)
        messagebox.showinfo("Success", "Autostart enabled.")
    autostart_button.config(state=tk.NORMAL) # 启用按钮

autostart_button = tk.Button(window, text="Autostart", command=autostart)
autostart_button.grid(row=6, columnspan=2)

window.mainloop()
