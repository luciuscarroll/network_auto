import csv

with open ('networkauto/actions/usernames.csv', newline='') as csvfile:
    usernamereader = csv.reader(csvfile, delimiter=',')
    usernames = []
    for row in usernamereader:
        usernames.append
        print()