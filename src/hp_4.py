# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    reformatted_dates = []
    for date in dates:
        datetime_obj = datetime.strptime(date, '%Y-%m-%d')
        reformatted_date = datetime.strftime(datetime_obj, '%d %b %Y')
        reformatted_dates.append(reformatted_date)
    return reformatted_dates


def date_range(start, n):
    if not isinstance(start, str):
        raise TypeError("start must be a string in 'yyyy-mm-dd' format")
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
        
    start_date = datetime.strptime(start, '%Y-%m-%d')
    date_list = [start_date + timedelta(days=i) for i in range(n)]
    return date_list


def add_date_range(values, start_date):
    date_list = date_range(start_date, len(values))
    result = [(date_list[i], values[i]) for i in range(len(values))]
    return result


def fees_report(infile, outfile):
    late_fees = defaultdict(float)

    with open(infile, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%y')
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            if date_returned > date_due:
                days_late = (date_returned - date_due).days
                late_fee = 0.25 * days_late
                patron_id = row['patron_id']
                late_fees[patron_id] += late_fee

    with open(outfile, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['patron_id', 'late_fees'])
        for patron_id, fees in late_fees.items():
            writer.writerow([patron_id, f'{fees:.2f}'])


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        # Ensure csv module is available
        import csv
        
        # Construct full file paths
        data_dir = '/Users/sairaghavendra/Desktop/homework-project-4-sairaghavendra9/data'
        BOOK_RETURNS_SHORT_PATH = f'{data_dir}/book_returns_short.csv'
        OUTFILE = f'{data_dir}/book_fees.csv'

        # Call fees_report function
        fees_report(BOOK_RETURNS_SHORT_PATH, OUTFILE)
        
        print(f"Late fees report generated at: {OUTFILE}")
    except FileNotFoundError:
        print("Error: Input file not found. Please check the file path.")
    except Exception as e:
        print(f"Error occurred: {e}")
