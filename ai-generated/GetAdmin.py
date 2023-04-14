import os
import sys
import win32com.shell.shell as shell

def is_admin():
    try:
        return shell.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([os.path.abspath(p) for p in sys.argv[1:]])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters='{} {}'.format(script, params))
        sys.exit(0)

if __name__ == '__main__':
    run_as_admin()
