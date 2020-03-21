
import pyautogui


# count = 0
# while count < 100:
#     pyautogui.mouseDown()
#     print("yes", count)
#     count += 1


import pandas as pd

record = {
  'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka', 'Priya', 'Shaurya' ],
  'Age': [21, 19, 20, 18, 17, 21],
  'Stream': ['Math', 'Commerce', 'Science', 'Math', 'Math', 'Science'],
  'Percentage': [88, 92, 95, 70, 65, 78]}

# create a dataframe
dataframe = pd.DataFrame(record, columns = ['Name', 'Age', 'Stream', 'Percentage'])

print(dataframe)
print("--------------------------------------------------")

newsales = dataframe[dataframe['Percentage'] <= 80]
print(newsales)
print("--------------------------------------------------")

f = dataframe['Percentage'] <= 80 ; newsales = dataframe[f]
print(newsales)
print("--------------------------------------------------")

newsales = dataframe.loc[[300],['Percentage']]
print(newsales)
