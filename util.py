from datetime import datetime


def unix_date_converter(row):
    value = row.get('submission_time')
    if type(value) == int:
        row['submission_time'] = datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
        return row


def sort_data(data, sort_criteria, order):
    if order == 'desc':
        sorted_data = sorted(data, key=lambda k: k[sort_criteria], reverse=True)
    else:
        sorted_data = sorted(data, key=lambda k: k[sort_criteria])
    return sorted_data


def single_value_dateconverter(value):
    result = datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
    return result