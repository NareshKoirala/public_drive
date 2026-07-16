import os
from dotenv import load_dotenv

load_dotenv()


VAULT_NAME = os.environ.get("VAULTNAME")
VAULT_ROOT = os.environ.get("VAULTROOT")


def createVault():
    if not os.path.exists(VAULT_NAME):
        os.makedirs(VAULT_NAME)


def getRoot():
    return os.getcwd()


def updateRoot(cus_path):
    new_path = VAULT_ROOT + cus_path
    if os.path.exists(new_path):
        os.chdir(new_path)
        return "OK"
    return "ERR"


def listItems(path):
    path = VAULT_ROOT + path
    if os.path.exists(path):
        return os.listdir(path)
    return "ERR"


def renameItem(l_name, n_name):
    if l_name in listItems(getRoot()):
        os.rename(l_name, n_name)
        return "OK"
    return "ERR"


def removeItem(name):
    if name in listItems(getRoot()):
        if os.path.isdir(name):
            try:
                os.rmdir(name)
                return "OK"
            except OSError:
                return "NEM"
        try:
            os.remove(name)
        except OSError:
            return "ERR"

    return "ERR"


def createDir(name):
    if not name or len(name.encode()) > 255 or not name.isalnum():
        return "ERR"

    try:
        os.mkdir(name)
        return "OK"
    except ValueError:
        return "NUL"
    except FileExistsError:
        return "EXS"
    except OSError:
        return "OSE"
