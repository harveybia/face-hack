import pickle

def saveUserDict(dct):
    pickle.dump(dct, open('user.db', 'wb'))

def loadUserDict():
    return pickle.load(open('user.db', 'wb'))
