import matplotlib.pyplot as plt

# list holding time records and number of drones
num_drones = []
gen_group_key_time = []
re_key_time = []

# read a csv file
# import its content into lists
CSV_file = '../time_records/existing_drones_varies.csv'
with open(CSV_file, 'r', encoding='utf-8') as csv_file:
    for line in csv_file.readlines()[1:]:
        drones, gen_group_key, re_key = list(map(float, line.split(',')))
        num_drones.append(drones)
        gen_group_key_time.append(gen_group_key)
        re_key_time.append(re_key)

# plotting a line graph
plt.rcParams.update({'font.size': 14})
plt.figure()
plt.plot(num_drones, gen_group_key_time, '-bo', label='GenGroupKey')
plt.plot(num_drones, re_key_time, '-ro', label='Re-Key')
plt.xlim((0,2000))
plt.ylim((0,60))

plt.xlabel('Number of Edge Drones')
plt.ylabel('Time (s)')
plt.xticks([0,500,1000,1500,2000])
# plt.title('Performance of Team Leader')
plt.legend(prop={'size': 16})
plt.grid(axis='y')

plt.show()