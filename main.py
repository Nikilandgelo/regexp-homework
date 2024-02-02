import csv
import re

def read_csv(filename):
    with open(filename, "r", encoding='UTF-8') as csv_file: 
        return list(csv.reader(csv_file))

def correct_data(csv_data):
    correct_csv_data = []
    for item in csv_data:
        corrected_fio = " ".join(item[:3]).split(" ")
        indexes_empty = [index for index, value in enumerate(corrected_fio) if value == '']
        for index, empty in enumerate(indexes_empty):
            empty -= index
            del corrected_fio[empty]
        while len(corrected_fio) < 3:
            corrected_fio.append("")
     
        corrected_phone = re.sub(r"(\+7|8)\s*\(*(\d{3,3})\)*\s*\-*(\d{3,3})\-*(\d{2,2})\-*(\d{2,2}) *\(*(доб.)* *(\d+)*\)*", r"+7(\2)\3-\4-\5 \6\7", item[5]).rstrip()
        item[5] = corrected_phone
        corrected_fio.extend(item[3:7])

        for correct_item in correct_csv_data:
            if corrected_fio[0] == correct_item[0] and corrected_fio[1] == correct_item[1]:
                missing_items = [index for index, item in enumerate(correct_item) if item == '']
                for index_item in missing_items:
                    if corrected_fio[index_item] != '':
                        correct_item[index_item] = corrected_fio[index_item]
                break
        else:
            correct_csv_data.append(corrected_fio)

    return correct_csv_data

def write_csv(list_data):
    with open("phonebook.csv", "w", encoding='UTF-8', newline="") as csv_file: 
        csv.writer(csv_file).writerows(list_data)

if __name__ == "__main__":
    source_list = read_csv("phonebook_raw.csv")
    write_csv(correct_data(source_list))