import csv
import os

current_directory = os.getcwd()
with open(f"{current_directory}/actions/usernames.csv", newline='') as csvfile:
    usernamereader = csv.reader(csvfile, delimiter=',')
    usernames = []
    for row in usernamereader:
        usernames.append
        print()