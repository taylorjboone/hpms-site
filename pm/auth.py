import win32security
import win32api
import win32net

def finduser(user):
    try:
        user_info = win32net.NetUserGetInfo(win32net.NetGetAnyDCName(), user, 2)
        full_name = user_info
        return True
    except:
        return False

def validateUser(ENO,PW):
    auth=False
    try:
        token= win32security.LogonUser(ENO,'executive',PW,win32security.LOGON32_LOGON_NETWORK,win32security.LOGON32_PROVIDER_DEFAULT)
        auth = bool(token)
    except:
        pass
    return auth