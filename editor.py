import csv

x_new = []
y_new = []

with open("./data_points/spaceship_119P4H1V0.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        x = int(row[0])
        y = int(row[1])
        x_new.append(x + 100)
        y_new.append(y)


with open("./data_points/spaceship_119P4H1V0_better.csv", "w", newline='') as f:
    writer = csv.writer(f)
    for x_i, y_i in zip(x_new, y_new):
        writer.writerow([x_i, y_i])
