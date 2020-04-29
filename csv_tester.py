import csv


with open("myFollowers.csv", mode="w") as myFollowers_file:
    myFollowers_file_writer = csv.writer(myFollowers_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    myFollowers_file_writer.writerow(["hello","friend"])
    myFollowers_file.sa