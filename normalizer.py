import csv

list_elevation = []
list_aspect = []
list_horizontal_distance_to_roadways = []
with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            list_elevation.append(int(row[0]))
            list_aspect.append(int(row[1]))
            list_horizontal_distance_to_roadways.append(int(row[5]))
        line_count += 1

max_elevation = max(list_elevation)
max_aspect = max(list_aspect)
max_horizontal = max(list_horizontal_distance_to_roadways)

min_elevation = min(list_elevation)
min_aspect = min(list_aspect)
min_horizontal = min(list_horizontal_distance_to_roadways)

list_normalize_elevation = []
list_normalize_aspect = []
list_normalize_horizontal = []

for x in range(len(list_aspect)):
    normalize_elevation = (list_elevation[x] - min_elevation) / (max_elevation - min_elevation)
    normalize_aspect = (list_aspect[x] - min_aspect) / (max_aspect - min_aspect)
    normalize_horizontal = (list_horizontal_distance_to_roadways[x] - min_horizontal) / (max_horizontal - min_horizontal)

    list_normalize_elevation.append(normalize_elevation)
    list_normalize_aspect.append(normalize_aspect)
    list_normalize_horizontal.append(normalize_horizontal)

# print(list_normalize_elevation[0])
# print(list_normalize_aspect[0])
# print(list_normalize_horizontal[0])

fieldnames=['elevation', 'aspect', 'horizontal_distance_to_roadways']
with open('normalized_fc.csv', 'wt', newline='', encoding='utf-8') as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(list_elevation)):
        writer.writerow({
            'elevation': list_normalize_elevation[i],
            'aspect': list_normalize_aspect[i],
            'horizontal_distance_to_roadways': list_normalize_horizontal[i]
        })
print("DONE...")