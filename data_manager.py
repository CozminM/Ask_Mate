import csv
import util
import os


ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
questions_file = '/home/bogdan/Desktop/web projects/ask-mate-1-python-bogdaniordan/sample_data/question.csv'
answers_file = '/home/bogdan/Desktop/web projects/ask-mate-1-python-bogdaniordan/sample_data/answer.csv'


def read_from_csv(filename):
    list_of_questions = []
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            util.unix_date_converter(row)
            list_of_questions.append(row)
    return list_of_questions


def append_to_csv(data_row, header, filename):
    with open(filename, 'a+', newline='') as file:
        csv_dict_writer = csv.DictWriter(file, fieldnames=header)
        csv_dict_writer.writerow(data_row)
        

def get_question_or_answer(matching_id, filename, used_id):
    list_of_items = []
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row[matching_id] == used_id:
                util.unix_date_converter(row)
                list_of_items.append(row)
    return list_of_items