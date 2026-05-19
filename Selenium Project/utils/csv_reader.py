import csv

class CSVReader:
    @staticmethod
    def read_csv(file_path):
        """Reads a CSV file and returns a list of dictionaries mapped by headers."""
        data_list = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Strip spaces from keys and values to protect against typos
                clean_row = {str(k).strip(): str(v).strip() for k, v in row.items()}
                data_list.append(clean_row)
        return data_list