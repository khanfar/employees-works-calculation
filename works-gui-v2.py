import csv
from datetime import datetime
import re
import tkinter as tk
from tkinter import filedialog
import os

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
                    mechanic = row['اسم الميكانيكي'].strip()  # Remove trailing spaces
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

def write_to_text_file(data, total_amount, filename, start_date, end_date):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'    ARAFAR JOB Calc. from date ({start_date.strftime("%d.%m.%Y")}) to date ({end_date.strftime("%d.%m.%Y")})\n')
        file.write('#' * 70 + '\n')
        file.write('-' * 50 + '\n')
        file.write(f'Total Amount: {total_amount} شيكل (Total Jobs: {sum(info["job_count"] for info in data.values())})\n')
        file.write('-' * 50 + '\n')
        for mechanic, info in data.items():
            file.write(f'{mechanic}: {info["total_money"]} شيكل (Total Jobs: {info["job_count"]})\n')
            file.write('-' * 50 + '\n')



def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_filename.delete(0, tk.END)
    entry_filename.insert(0, filename)

def find_csv_in_directory():
    directory = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            entry_filename.delete(0, tk.END)
            entry_filename.insert(0, os.path.join(directory, file))
            break

def start_processing():
    start_date_str = entry_start_date.get()
    end_date_str = entry_end_date.get()

    start_date = datetime.strptime(start_date_str, '%d.%m.%Y')
    end_date = datetime.strptime(end_date_str, '%d.%m.%Y')

    csv_filename = entry_filename.get()
    output_filename = 'employee_works.txt'

    work_by_date_range, total_amount = get_work_by_date_range(csv_filename, start_date, end_date)
    write_to_text_file(work_by_date_range, total_amount, output_filename, start_date, end_date)


# GUI setup
root = tk.Tk()
root.title("حاسبة العمل والموظفين")
root.geometry("400x250")

label_start_date = tk.Label(root, text="من يوم (dd.mm.yyyy):")
label_start_date.grid(row=0, column=0)

entry_start_date = tk.Entry(root)
entry_start_date.grid(row=0, column=1)

label_end_date = tk.Label(root, text="الى يوم (dd.mm.yyyy):")
label_end_date.grid(row=1, column=0)

entry_end_date = tk.Entry(root)
entry_end_date.grid(row=1, column=1)

label_filename = tk.Label(root, text="CSV اسم ملف:")
label_filename.grid(row=2, column=0)

entry_filename = tk.Entry(root)
entry_filename.grid(row=2, column=1)

button_browse = tk.Button(root, text="استكشاف", command=browse_file)
button_browse.grid(row=2, column=2)

button_find_csv = tk.Button(root, text="قاعدة البيانات", command=find_csv_in_directory)
button_find_csv.grid(row=3, columnspan=3)

button_start = tk.Button(root, text="ابدأ الحساب", command=start_processing)
button_start.grid(row=4, columnspan=3)

root.mainloop()
