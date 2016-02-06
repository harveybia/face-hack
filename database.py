import pickle
import webbrowser

def saveUserDict(dct):
    pickle.dump(dct, open('user.db', 'wb'))

def loadUserDict():
    return pickle.load(open('user.db', 'wb'))

def newBrowserTab(url):
    webbrowser.open(url)

if __name__ == "__main__":
    webbrowser.open('http://www.google.com', new=1)
