import csv
import random
import string

def generateRandomINDData(records, dimension, file_name):
    records = int(records)
    list_time_in = []
    for i in range(0, records):
        list_time_in.append(random.randint(0, 1000))

    list_time_out = []
    for i in range(0, records):
        lower_bound = list_time_in[i] + 1
        list_time_out.append(random.randint( lower_bound, 2000))
    
    if dimension == '2':
        fieldnames=['name', 'x', 'y','time_in', 'time_out']
        with open(file_name, 'wt', newline='', encoding='utf-8') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, records):
                ran = ''.join(random.choices(string.ascii_lowercase, k = 8))
                writer.writerow({
                    'name': ran,
                    'x': round(random.uniform(0.0, 1.0), 3),
                    'y': round(random.uniform(0.0, 1.0), 3),
                    'time_in': list_time_in[i],
                    'time_out': list_time_out[i]
                })

    elif dimension == '3':
        fieldnames=['name', 'x', 'y', 'z','time_in', 'time_out']
        with open(file_name, 'wt', newline='', encoding='utf-8') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, records):
                ran = ''.join(random.choices(string.ascii_lowercase, k = 8)) 
                writer.writerow({
                    'name': ran,
                    'x': round(random.uniform(0.0, 1.0), 3),
                    'y': round(random.uniform(0.0, 1.0), 3),
                    'z': round(random.uniform(0.0, 1.0), 3),
                    'time_in': list_time_in[i],
                    'time_out': list_time_out[i]
                })
    else:
        print("Dimensi tidak valid")

def generateRandomANTData(records, dimension, file_name):
    records = int(records)
    list_time_in = []
    for i in range(0, records):
        list_time_in.append(random.randint(0, 1000))

    list_time_out = []
    for i in range(0, records):
        lower_bound = list_time_in[i] + 1
        list_time_out.append(random.randint( lower_bound, 2000))
    
    if dimension == '2':
        fieldnames=['name', 'x', 'y','time_in', 'time_out']
        with open(file_name, 'wt', newline='', encoding='utf-8') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, records):
                enum = ['x', 'y']
                x_value = None
                y_value = None
                pole = random.choice(enum)
                if pole == 'x':
                    x_value = round(random.uniform(0.0, 1.0), 3)
                    range_enum = [-0.15, 0.15]
                    y_value = 1.0 - x_value + random.choice(range_enum)
                    if y_value < 0:
                        y_value = 0
                    elif y_value > 1:
                        y_value = 1.0
                else:
                    y_value = round(random.uniform(0.0, 1.0), 3)
                    range_enum = [-0.15, 0.15]
                    x_value = 1.0 - y_value + random.choice(range_enum)
                    if x_value < 0:
                        x_value = 0
                    elif x_value > 1:
                        x_value = 1.0

                ran = ''.join(random.choices(string.ascii_lowercase, k = 8))
                writer.writerow({
                    'name': ran,
                    'x': x_value,
                    'y': y_value,
                    'time_in': list_time_in[i],
                    'time_out': list_time_out[i]
                })
    elif dimension == '3':
        fieldnames=['name', 'x', 'y', 'z', 'time_in', 'time_out']
        with open(file_name, 'wt', newline='', encoding='utf-8') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, records):
                enum = ['x', 'y', 'z']
                range_enum = [-0.15, 0.15]
                x_value = None
                y_value = None
                z_value = None
                pole = random.choice(enum)
                if pole == 'x':
                    x_value = round(random.uniform(0.0, 1.0), 3)
                    
                    y_value = 1.0 - x_value + random.choice(range_enum)
                    if y_value < 0:
                        y_value = 0
                    elif y_value > 1:
                        y_value = 1.0
                    
                    z_value = 1.0 - x_value + random.choice(range_enum)
                    if z_value < 0:
                        z_value = 0
                    elif z_value > 1:
                        z_value = 1
                elif pole == 'y' :
                    y_value = round(random.uniform(0.0, 1.0), 3)

                    x_value = 1.0 - y_value + random.choice(range_enum)
                    if x_value < 0:
                        x_value = 0
                    elif x_value > 1:
                        x_value = 1.0
                    
                    z_value = 1.0 - y_value + random.choice(range_enum)
                    if z_value < 0:
                        z_value = 0
                    elif z_value > 1:
                        z_value = 1.0
                else:
                    z_value = round(random.uniform(0.0, 1.0), 3)

                    x_value = 1.0 - z_value + random.choice(range_enum)
                    if x_value < 0:
                        x_value = 0
                    elif x_value > 1:
                        x_value = 1.0
                    
                    y_value = 1.0 - z_value + random.choice(range_enum)
                    if y_value < 0:
                        y_value = 0
                    elif y_value > 1:
                        y_value = 1.0

                ran = ''.join(random.choices(string.ascii_lowercase, k = 8))
                writer.writerow({
                    'name': ran,
                    'x': x_value,
                    'y': y_value,
                    'z': z_value,
                    'time_in': list_time_in[i],
                    'time_out': list_time_out[i]
                })
    else:
        print("Dimensi tidak valid")

def generateRandomFCData(records, dimension, file_name):
    records = int(records)
    list_time_in = []
    for i in range(0, records):
        list_time_in.append(random.randint(0, 1000))

    list_time_out = []
    for i in range(0, records):
        lower_bound = list_time_in[i] + 1
        list_time_out.append(random.randint( lower_bound, 2000))

    list_elevation = []
    list_aspect = []
    list_horizontal_distance_to_roadways = []
    with open('normalized_fc.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                list_elevation.append(float(row[0]))
                list_aspect.append(float(row[1]))
                list_horizontal_distance_to_roadways.append(float(row[2]))
            line_count += 1
    
    if dimension == '2':
        fieldnames=['name', 'elevation', 'aspect', 'time_in', 'time_out']
        with open(file_name, 'wt', newline='', encoding='utf-8') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, records):
                ran = ''.join(random.choices(string.ascii_lowercase, k = 8))
                writer.writerow({
                    'name': ran,
                    'elevation': round(list_elevation[i], 3),
                    'aspect': round(list_aspect[i], 3),
                    'time_in': list_time_in[i],
                    'time_out': list_time_out[i]
                })
    elif dimension == '3':
        fieldnames=['name', 'elevation', 'aspect', 'horizontal_distance_to_roadways' , 'time_in', 'time_out']
        with open(file_name, 'wt', newline='', encoding='utf-8') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, records):
                ran = ''.join(random.choices(string.ascii_lowercase, k = 8))
                writer.writerow({
                    'name': ran,
                    'elevation': round(list_elevation[i], 3),
                    'aspect': round(list_aspect[i], 3),
                    'horizontal_distance_to_roadways': round(list_horizontal_distance_to_roadways[i], 3),
                    'time_in': list_time_in[i],
                    'time_out': list_time_out[i]
                })



    
if __name__ == "__main__":
    print("Generate Random Data")
    print("1. IND")
    print("2. ANT")
    print("3. FC")
    data_type = input("Pilih Tipe Data (Dalam Angka):")
    if data_type == '1':
        records = input("Jumlah Data (10k, 30k, 50k, 100k, 200k, 300k):")
        dimension = input("Dimensi data:")
        print("Generate random {} records with {} dimensions of IND Data" .format(records, dimension))
        file_name = "random_{}_{}d_ind.csv" .format(records, dimension)
        generateRandomINDData(records, dimension, file_name)
    elif data_type == '2':
        records = input("Jumlah Data (10k, 30k, 50k, 100k, 200k):")
        dimension = input("Dimensi data:")
        print("Generate random {} records with {} dimensions of ANT Data" .format(records, dimension))
        file_name = "random_{}_{}d_ant.csv" .format(records, dimension)
        generateRandomANTData(records, dimension, file_name)
    elif data_type == '3':
        records = input("Jumlah Data (10k, 30k, 50k, 100k, 200k):")
        dimension = input("Dimensi data:")
        print("Generate random {} records with {} dimensions of FC Data" .format(records, dimension))
        file_name = "random_{}_{}d_fc.csv" .format(records, dimension)
        generateRandomFCData(records, dimension, file_name)