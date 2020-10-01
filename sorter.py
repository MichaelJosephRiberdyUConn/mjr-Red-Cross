import sys, os, pandas, csv, re, math

target = [1,2]

names = ["Eric Niedomys", "Tyler Dietelbaum", "Charles Taylor", "Chloe Ho", "Gigi Shugrue", "Joe Riberdy", "Megan Russell", "Mich Gagliardi", "Nicole Melilo", "Nicole Nyzio", "Samantha Feliciano", "Sylvester Jung"]

blood_types = ["O +", "O -", "A +", "A -", "B +", "B -", "AB +", "AB -"]

initial_data = pandas.read_csv("data.csv", header=None)
number_of_rows = initial_data.shape[0]

first_row_indices = []
for row_num in range(number_of_rows):
  if(initial_data.iloc[row_num, 5] in blood_types):
    first_row_indices.append(row_num)

entry_list = []
for entry_num in range(len(first_row_indices) - 1):
  entry_list.append(initial_data[first_row_indices[entry_num]:first_row_indices[entry_num + 1]])

with open('towns.csv', 'r') as f:
    reader = csv.reader(f)
    towns = list(reader)

essential_info = []
for row_num in range(len(entry_list)):
  #print(entry_list[row_num])
  relevant_info = []
  num_of_rows = entry_list[row_num].shape[0]
  do_not_call_count = 0
  for row_num_two in range(num_of_rows):
    if(entry_list[row_num].iloc[row_num_two].str.contains('Do Not Call').any()):
      do_not_call_count += 1
  #print(do_not_call_count)
  if(do_not_call_count == 0):
    town_count = 0
    for row_num_two in range(num_of_rows):
      for town in range(len(towns)):
        if(entry_list[row_num].iloc[row_num_two].str.contains(towns[town][0], case=False).any()):
          town_count += 1
    #print(town_count)
    if(town_count > 0):
      for row_num_two in range(num_of_rows):
        local_list = re.compile("\d\d\d-\d\d\d-\d\d\d\d").findall(entry_list[row_num].iloc[row_num_two].str.cat())
        #print("row_num_two = " + str(row_num_two))
        #print("local_list:")
        #print(local_list)
        if local_list:
          relevant_info += local_list
      if relevant_info:
        essential_info.append([entry_list[row_num].iloc[0,2], entry_list[row_num].iloc[0,3], relevant_info[0]])
        print("row = "+str(row_num))
        print(essential_info[-1])

if 1 in target:
  for name_index in range(len(names)):
    name = names[name_index]
    with open("./output_by_name/"+name+".csv", 'w') as eboard_file:
      eboard_writer = csv.writer(eboard_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      quotient = math.floor(len(essential_info)/len(names))
      eboard_writer.writerow(["First Name", "Last Name", "Phone Number"])
      for entry in range(quotient):
        eboard_writer.writerow(essential_info[name_index * quotient + entry])

if 2 in target:
  with open("./output_by_name/master.csv", 'w') as master_file:
    master_writer = csv.writer(master_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    master_writer.writerow(["First Name", "Last Name", "Phone Number"])
    for entry in range(len(essential_info)):
      master_writer.writerow(essential_info[entry])
