from time import sleep
import threading


followed = 0
liked = 0

follow = True
like = True

def likePhoto(activate):
    global  liked

    if(activate):
        liked += 1
        print("L",liked)

def followUser(activate):
    global followed

    if (activate):
        followed += 1
        print("F",followed)

def activateAction(actionName):
    global like
    global liked

    global follow
    global followed
    sec = 0

    for _ in range(10):
        sleep(1)
        sec += 1
        text = "** SEC: {} ->  ({}) **".format(sec, actionName)
        print(text)

        if(sec == 10):
            print("** ACTION ACTIVATED AGAIN -> {} **".format(actionName))

            if (actionName == "like"):
                like = True
                liked = 0
            else:
                follow = True
                followed = 0

likeMax = 10
followMax = 5

for _ in range(0,100):
    sleep(1)

    if(liked < likeMax and like == True):
        likePhoto(like)

    else:
        if(like == True):
            like = False
            print("PAUSE **LIKE**")
            print("")
            t1 = threading.Thread(target=activateAction, args=("like",))
            t1.start()

    print(" ")

    if(followed < followMax and follow == True):
        followUser(follow)

    else:
        if(follow == True):
            follow = False
            print("PAUSE **FOLLOW**")
            print("")
            t2 = threading.Thread(target=activateAction, args=("follow",))
            t2.start()

    print(" ")

