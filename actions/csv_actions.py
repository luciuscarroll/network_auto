import csv
import os

current_directory = os.getcwd()
def get_usernames():
    usernames = []
    with open(f"{current_directory}/actions/usernames.csv", newline='') as csvfile:
        usernamereader = csv.reader(csvfile, delimiter=',')
        is_first = True
        for row in usernamereader:
            if is_first:
                is_first = False
            else:
                usernames.append(row[0])
    return usernames
