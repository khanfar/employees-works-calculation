import csv
from datetime import datetime
import re

def read_csv(filename, start_date, end_date):
    mechanics_work = {}
    cash_amount = 0
    with open(filename, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['تقرير نهائي'] and 'شيكل' in row['تقرير نهائي']:
                try:
                    entry_date = datetime.strptime(row['تاريخ الدخول'], '%d.%m.%Y')
                except ValueError:
                    print(f"Error parsing date for row: {row}")
                    continue

                if start_date <= entry_date <= end_date:
                    mechanic = row['اسم الميكانيكي']
                    if mechanic in mechanics_work:
                        mechanics_work[mechanic]['job_count'] += 1
                        amount_str = row['تقرير نهائي']
                        amount = re.findall(r'(\d+(\.\d+)?) شيكل', amount_str)
                        if amount:
                            mechanics_work[mechanic]['total_money'] += float(amount[0][0])
                    else:
                        mechanics_work[mechanic] = {'job_count': 1, 'total_money': 0}
                        amount_str = row['تقرير نهائي']
                        amount = re.findall(r'(\d+(\.\d+)?) شيكل', amount_str)
                        if amount:
                            mechanics_work[mechanic]['total_money'] = float(amount[0][0])
                    
                    # Check if رقم المركبة and نوع المركبه are both "كاش"
                    if row['رقم المركبة'].strip() == 'كاش' and row['نوع المركبه'].strip() == 'كاش':
                        cash_amount += float(re.findall(r'(\d+(\.\d+)?) شيكل', row['تقرير نهائي'])[0][0])
    return mechanics_work, cash_amount

def get_work_by_date_range(filename, start_date, end_date):
    mechanics_work, _ = read_csv(filename, start_date, end_date)
    total_amount = sum(info['total_money'] for info in mechanics_work.values())
    return mechanics_work, total_amount

def write_to_text_file(data, total_amount, cash_amount, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'Total Amount: {total_amount} شيكل (Total Jobs: {sum(info["job_count"] for info in data.values())})\n')
        for mechanic, info in data.items():
            file.write(f'{mechanic}: {info["total_money"]} شيكل (Total Jobs: {info["job_count"]})\n')
        file.write(f'Cash Amount: {cash_amount} شيكل\n')

start_date_str = input("Enter the start date (format: dd.mm.yyyy): ")
end_date_str = input("Enter the end date (format: dd.mm.yyyy): ")

start_date = datetime.strptime(start_date_str, '%d.%m.%Y')
end_date = datetime.strptime(end_date_str, '%d.%m.%Y')

csv_filename = 'your_data.csv'  # Replace 'your_data.csv' with the actual filename
output_filename = 'employee_works.txt'

work_by_date_range, total_amount = get_work_by_date_range(csv_filename, start_date, end_date)
_, cash_amount = read_csv(csv_filename, start_date, end_date)
write_to_text_file(work_by_date_range, total_amount, cash_amount, output_filename)
