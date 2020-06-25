

#string = "[Nice photo][Damn follow me please][Heeey][nice pic][DAMN SON]"



def filterComment(stringComment):
    start = 0
    end = 0

    list_comment = []

    for m in range(len(stringComment)):
        if (stringComment[m] == "["):
            start = m + 1
        elif (stringComment[m] == "]"):
            end = m
            list_comment.append(stringComment[start:end])
            start = 0
            end = 0

    return list_comment

