# import datetime
import math

###########################################
# DETERMINES THE DATE BASED ON PUSH DAYS  #
###########################################

def pushDate(userDate, dateToday, push):
    # USER's following time
    month = userDate[3:5] # MONTH
    date = userDate[:2] # DATE
    year = userDate[6:] # YEAR

    month_pushed = 0 # NEW MONTH
    day_pushed = 0 # NEW DATE
    year_pushed = 0 # NEW YEAR

    yearsFEB = []

    for x in range(4, 100, 4):
        yearsFEB.append(2020 + x)

    # ALL MONTHS with their dates
    dictMonths = {"01": 31, "02": 29 if year in yearsFEB else 28, "03": 31, "04": 30, "05": 31, "06": 30, "07": 31, "08": 31, "09": 30,
                    "10": 31, "11": 30, "12": 31}

    # DAYS TO PUSH
    day_push = push
    while_val = True

    while(while_val):

        dictMonths["02"] = 29 if year in yearsFEB else 28

        for months in dictMonths.keys():

            if (int(months) >= int(month)):

                if(int(date) + day_push > dictMonths.get(months)):
                    day_push -= dictMonths.get(months)
                    month_pushed += 1

                    if(month_pushed + int(month) > 12):
                        month_pushed = 0
                        month = 1
                        year = int(year) + 1

                else:
                    while_val = False
                    break

    day_pushed = int(date) + day_push
    month_pushed += int(month)
    year_pushed = int(year)

    if(day_pushed < 10):
        day_pushed = "0{}".format(day_pushed)
    if(month_pushed < 10):
        month_pushed = "0{}".format(month_pushed)

    date_result = "{}/{}/{}".format(day_pushed,month_pushed,year_pushed)

   # print("TODAY DATE:",dateToday)
   # print("TIME FOLLOWED:",userDate)
   # print("TIME TO UNFOLLOW:",date_result)


    day_user = int(date_result[:2])
    month_user = int(date_result[3:5])
    year_user = int(date_result[6:])

    conf = year_user < int(dateToday[6:]) or year_user <= int(dateToday[6:]) and month_user < int(dateToday[3:5]) or \
           day_user <= int(dateToday[:2]) and month_user == int(dateToday[3:5])

    if (conf):
        return True

    else:
        return False

# date_today = datetime.datetime.today()
#
# day_today = date_today.day
# month_today = date_today.month
# year_today = date_today.year
#
# if(day_today < 10):
#     day_today = "0{}".format(day_today)
#
# if(month_today < 10):
#     month_today = "0{}".format(month_today)
#
# date_today = "{}/{}/{}".format(day_today,month_today,year_today)
# user_date = "30/06/2020"
#
# print(pushDate(user_date, date_today, 5))
###########################################
###########################################
# DETERMINES THE time BASED ON PUSH hour/minute  #
###########################################
def pushTime(date_today, time_Now, push):
    # DATE
    month = date_today[3:5]  # MONTH
    day = date_today[:2]  # DATE
    year = date_today[6:]  # YEAR

    day_e = day
    month_e = month
    year_e = year

    # TIME
    hour = time_Now[:2]  # HOUR
    minute = time_Now[3:]  # MINUTE


    # NEW VALUES
    year_pushed = 0
    month_pushed = 0
    day_pushed = 0
    hour_pushed = 0

    day_pushed = math.floor(push/24)

    hours_pushed = push % 24
    hours_pushed += int(hour)

    if(hours_pushed >= 24):
        day_pushed += 1
        hours_pushed %= 24

    yearsFEB = []

    # Leap year
    for x in range(4,100,4):
        yearsFEB.append(2020+x)

    # ALL MONTHS with their dates
    dictMonths = {"01": 31, "02": 29 if year in yearsFEB else 28, "03": 31, "04": 30, "05": 31, "06": 30, "07": 31, "08": 31, "09": 30,
                    "10": 31, "11": 30, "12": 31}

    jf = True
    while(jf):

        dictMonths["02"] = 29 if year in yearsFEB else 28

        for months in dictMonths.keys():

            if (int(months) >= int(month)):

                if(day_pushed + int(day) > dictMonths.get(months)):
                    day_pushed = day_pushed + int(day)
                    day = 0
                    day_pushed -= dictMonths.get(months)
                    month_pushed += 1

                    if (month_pushed + int(month) > 12):
                        month_pushed = 0
                        month = 1
                        year = int(year) + 1

                else:
                    day_pushed += int(day)
                    jf = False
                    break

    month_pushed += int(month)

    if (day_pushed < 10):
        day_pushed = "0{}".format(day_pushed)

    if (month_pushed < 10):
        month_pushed = "0{}".format(month_pushed)

    if(hours_pushed < 10):
        hours_pushed = "0{}".format(hours_pushed)

