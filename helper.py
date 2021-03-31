import os

def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

def pwd():
    """Returns the current working directory"""
    cwd = os.getcwd()
    return cwd

def data_path():
    data_dir = os.path.dirname(os.path.abspath(__file__)) + "\\MarginTest\\bin\\Debug\\netcoreapp3.1\\data\\"
    return data_dir
