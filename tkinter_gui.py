from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import *

# IMPORTS MAIN FILE
import index

# VARIABLES
backgroundColor_HEX = "#FFFFFF"
rectColorHEX = "#b5b7ba"
loginSucces = False
username_value = None
list_langauge = []
tuplesWithCountries = ("None","All","English","Danish","Spanish","German","Swedish","French","Russian","Italian","Chinese","Portuguese")
show_warning = True

# Calling on the class object from index file
bot = index.bot()


#### FILTER FOR STRING COMING FROM THE TEXTINPUT (HASHTAGS)
def filterTextInput(stringText):

    string = stringText.replace(" ", "")
    start = 0
    end = 0
    listHashtags = []
    dicts = {}

    for n in range(len(string)):
        if (string[n] == "["):
            start = n + 1

        elif (string[n] == ":"):
            end = n
            hashtag = string[start:end]
            listHashtags.append(hashtag)

        if (string[n] == ":"):
            start = n + 1

        elif (string[n] == "]"):
            end = n
            weight = string[start:end]
            listHashtags.append(weight)

    try:
        dicts = {listHashtags[i]: int(listHashtags[i + 1]) for i in range(0, len(listHashtags), 2)}
    except:
        dicts = "WRONG"
        messagebox.showerror("ERROR","Something went wrong with selecting hashtag \nTry Again")
    finally:
        return dicts

########################

## RUNS WHEN LOGIN BUTTON IS CLICKED
def login_function():
    print("LOADING...")
    print("-----")
    password_value = None
    username_value =  None

    if(show_warning == True):
        messagebox.showwarning("","Use of this software is at your own risk")

    try:
        username_value = str(Entry.get(username))
        password_value = str(Entry.get(password))
    except ValueError:
        messagebox.showerror("","Something went wrong\n try again")

    windowVal = valVisibleWindow.get()
    login_function.usernameVal = username_value

    ch_number = False

    if (len(password_value) < 6 or len(username_value) < 3):
        messagebox.showerror("","Username must be greater than 3 characters\n"
                        "Password must be greater than 6 characters\nTry again")
    else:
        ch_number = True

    if(ch_number == True):
        root.withdraw()
        bot.login(username_value, password_value, windowVal)
        if(bot.error_login == True):
            messagebox.showerror("","Login failed\n try again")
            root.deiconify()
        elif(bot.login_success == True):
            print("Successful login")
            root.destroy()

# CALLED WHEN LAUNCH BUTTON IS CLICKED
def settings_function():
    list_langauge = []
    ### LIKE OR FOLLOW ###
    likeActivated = likePhotosVal.get()
    followActivated = followVal.get()
    ###  GENDER PICK ###
    girlActiaved = girlVal.get()
    boyActiaved = boyVal.get()
    #### LANGUAGE PICK ####
    lang_1 = lang_1_Val.get()
    lang_2 = lang_2_Val.get()
    lang_3 = lang_3_Val.get()
    lang_4 = lang_4_Val.get()

    #### CHECK FOR DUPLICATED LANGUAGES AND INSERT VALUES INSIDE A LIST ####
    for x in [lang_1, lang_2, lang_3, lang_4]:
        if(x == "All"):
            list_langauge = []
            for p in list(tuplesWithCountries):
                if(p is not "None" and p is not "All"):
                    list_langauge.append(p)
            break

        elif(x == "None"):
            continue

        elif(x not in list_langauge):
                list_langauge.append(x)

    inputValue=texthastags.get("1.0",'end-1c')
    textDict = filterTextInput(inputValue)

    # GOES TO BOT FUNCTION tagFinfder
    if(textDict != "WRONG"):
        bot.tagFinder(textDict, followActivated, likeActivated, list_langauge, girlActiaved, boyActiaved,setting)
        bot.send_own_data_csv()
        bot.save_information_csv()
        bot.unfollower()
    else:
        pass
###############################################

#### LOGIN WINDOW
root = Tk()
root.title("Instagram bot")

root.config(height=270, width=480)
root.geometry('+%d+%d'%(500,250))

root.resizable(0,0)
root['bg'] = backgroundColor_HEX
Canvas(root, bg="red").create_rectangle(1,4,20,400)

rect = Canvas(root,width=450,height=200,background=rectColorHEX, highlightbackground="grey")
rect.place(x=15,y=0)

Label(root, text="Bot for Instagram automation", bg=rectColorHEX, fg="black", font=("Comic Sans MS",20,"bold")).place(x=20, y=2)
Label(root, text="Login Instagram", bg=rectColorHEX, fg="black", font=("Comic Sans MS",15,"")).place(x=20, y=45)

Label(root, text="Username", bg=backgroundColor_HEX, fg="black",background=rectColorHEX,font=("Comic Sans MS",19,"")).place(x=20, y=90)
Label(root, text="Password", bg=backgroundColor_HEX, fg="black",background=rectColorHEX, font=("Comic Sans MS",19,"")).place(x=20, y=145)
# USERNAME INPUT
username = Entry(root, font=("",20,"bold"), borderwidth = 3,relief = SUNKEN)
username.insert(0, "skopidoo2")
username.place(x=155,y=90, width=275,height=42)
# PASSWORD INPUT
password = Entry(root, font=("",20,"bold"), borderwidth = 3, show="*")
password.insert(0, "Tyggegummi123123")
password.place(x=155,y=147, width=275,height=42)
Label(root, text="This software is made by Mohammad",bg=backgroundColor_HEX, fg="black",highlightcolor="red", font=("Comic Sans MS",10,"bold")).place(x=20, y=210)
Label(root, text="from Aarhus Gymnasium ©",bg=backgroundColor_HEX,fg="black", font=("Comic Sans MS",10,"bold")).place(x=20, y=230)

valVisibleWindow = BooleanVar()
windowVisible = Checkbutton(root, text="invisible browser", bg=backgroundColor_HEX, font=("",8,""), variable=valVisibleWindow).place(x=280, y=230)

if(root.winfo_exists() == 0):
    login_page_open = False

username_value = Entry.get(username)
login_button = Button(root,text="Login", width=9, height=2, command=login_function).place(x=395,y=210)
root.mainloop()

# CHECKING OWN FOLLOWERS AND FOLLOWING
bot.send_own_data_csv()
######################################################
 #### SETTING WINDOW ####
setting = Tk()
setting.title("Instagram bot")
setting.geometry("500x550")
setting.resizable(0,0)
setting['bg'] = backgroundColor_HEX
rect1 = Canvas(setting,width=483,height=47,background=rectColorHEX, highlightbackground="grey")
rect1.place(x=6,y=3)

rect1 = Canvas(setting,width=483,height=80,background=rectColorHEX, highlightbackground="grey")
rect1.place(x=6,y=58)

rect1 = Canvas(setting,width=483,height=400,background=rectColorHEX, highlightbackground="grey")
rect1.place(x=6,y=146)

### DATA AREA
text_welcome = "Account: {}".format(username_value)
Label(setting, text=text_welcome,bg=rectColorHEX, fg="black",highlightcolor="red", font=("Comic Sans MS",15,"bold")).place(x=15, y=7)

Label(setting, text="Account data",bg=rectColorHEX, fg="black",highlightcolor="red", font=("Comic Sans MS",15,"bold")).place(x=15, y=60)

text_followers = "Followers: {}".format(len(bot.followers_list))
text_following = "Following: {}".format(len(bot.following_list))
Label(setting, text=text_followers,bg=rectColorHEX, fg="black",highlightcolor="red", font=("Comic Sans MS",12,"bold")).place(x=15, y=100)
Label(setting, text=text_following,bg=rectColorHEX, fg="black",highlightcolor="red", font=("Comic Sans MS",12,"bold")).place(x=150, y=100)

#### SETTINGS AREA #####

Label(setting, text="Bot settings",bg=rectColorHEX, fg="black",highlightcolor="red", font=("Comic Sans MS",15,"bold")).place(x=15, y=150)

likePhotosVal = IntVar()
followVal = IntVar()

likePhotos = Checkbutton(setting, text="Like (The bot will like photos based on your preferences)", bg=rectColorHEX, variable=likePhotosVal).place(x=15, y=190)
followpeople = Checkbutton(setting, text="Follow (The bot will follow users based on your preferences)",bg=rectColorHEX, variable=followVal).place(x=15, y=223)

Label(setting, text="Which kind of gender do want to follow?",bg=rectColorHEX, fg="black",highlightcolor="red", font=("Comic Sans MS",12,"bold")).place(x=15, y=255)

boyVal = IntVar()
girlVal = IntVar()

pref_boys = Checkbutton(setting, text="Boys)", bg=rectColorHEX, variable=boyVal).place(x=15, y=290)
pref_girls = Checkbutton(setting, text="Girls)", bg=rectColorHEX, variable=girlVal).place(x=80, y=290)

    # LANGUAGE TO PICK

lang_1_Val = StringVar()
lang_2_Val = StringVar()
lang_3_Val = StringVar()
lang_4_Val = StringVar()

Label(setting, text="Pick language the user most speak before liking or following them",bg=rectColorHEX, fg="black",highlightcolor="red", font=("Comic Sans MS",10,"bold")).place(x=15, y=320)
language_1 = Spinbox(setting, values=tuplesWithCountries, width=7, state="readonly",textvariable=lang_1_Val, font=('Helvetica', 12, '')).place(x=15, y=350)
language_2 = Spinbox(setting, values=tuplesWithCountries, width=7,textvariable=lang_2_Val, font=('Helvetica', 12, '')).place(x=100, y=350)
language_3 = Spinbox(setting, values=tuplesWithCountries, width=7,textvariable=lang_3_Val, font=('Helvetica', 12, '')).place(x=185, y=350)
language_4 = Spinbox(setting, values=tuplesWithCountries, width=7,textvariable=lang_4_Val,font=('Helvetica', 12, '')).place(x=270, y=350)

## SELECT HASHTAG

Label(setting, text="Select which hashtags where you want to find the users",bg=rectColorHEX, fg="black",highlightcolor="red", font=("Comic Sans MS",9,"bold")).place(x=15, y=380)
Label(setting, text="You can select the hashtag as follows ->[hashtag_Name:weight(integer)] e.g.",bg=rectColorHEX, fg="black",highlightcolor="red", font=("Comic Sans MS",8,"")).place(x=15, y=400)
Label(setting, text="[like4like:14][like4follow:100]",bg=rectColorHEX, fg="black",highlightcolor="red", font=("Comic Sans MS",8,"")).place(x=15, y=420)

texthastags = Text(setting, height=5,width=50, borderwidth=5)
texthastags.insert(INSERT,"[danmark:50][aarhus:100]")
texthastags.place(x=15,y=450)

buttonLaunch = Button(setting, text="LAUNCH", width=7, height=2, command=settings_function).place(x=430, y=500)
root.mainloop()



