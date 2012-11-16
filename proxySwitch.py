# -*- coding:windows-1251 -*-
# 
# This tiny script is for autoswitch proxy servers depending on
# specific network location.
#
# Specific locations is detected by "specific host" - unique host 
# and port combination that available only in one location.
#
# 2012, Michel Beloshitsky <mbeloshitsky@gmail.com>
#
import _winreg
import socket

# Proxy list. Each entry has following format
#    (
#       (<locationSpecificHost>, <locationSpecificPort>), 
#       <locationProxy>
#    )
proxies = [
    (
        ('mylocspec.host', 80),
         'mylocpro.xy:3128'
    ),
]

Registry      = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
proxySettings = _winreg.OpenKey(Registry, 
                                r'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\', 
                                0, _winreg.KEY_WRITE)

# Forever loop, that monitors network.
while True:
    proxyFound = False
    for test, proxy in proxies:
        try:
            socket.create_connection(test, 3)
            # If connection to location specific host successful so we are there
            # and need to enable location specific proxy
            proxyFound = True
            _winreg.SetValueEx(proxySettings, "ProxyEnable", 0, _winreg.REG_DWORD, 1)
            _winreg.SetValueEx(proxySettings, "ProxyServer", 0, _winreg.REG_SZ, proxy)
            break
        except:
            pass
    # No known proxified locations found. Disabling proxy so.
    if not proxyFound:
        _winreg.SetValueEx(proxySettings, "ProxyEnable", 0, 4, 0)