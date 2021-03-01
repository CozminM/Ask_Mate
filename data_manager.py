import csv
import util
import os

from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common


ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
questions_file = 'sample_data/question.csv'
answers_file = 'sample_data/answer.csv'


@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT id, submission_time, view_number, vote_number, title, image, message
        FROM question
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_individual_question(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        SELECT id, submission_time, view_number, vote_number, title, image, message
        FROM question
        WHERE id = %(i)s
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_individual_answer(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE question_id = %(i)s
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()

def append_to_csv(data_row, header, filename):
    with open(filename, 'a+') as file:
        csv_dict_writer = csv.DictWriter(file, fieldnames=header)
        csv_dict_writer.writerow(data_row)


def get_question_or_answer(matching_id, filename, used_id):#functie privata si o transformam in 2 functii
    list_of_items = []
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row[matching_id] == used_id:
                list_of_items.append(row)
    return list_of_items


def delete_from_csv(question_id, data, header, filename):
    with open(filename, 'w') as file:
        csv_dict_writer = csv.DictWriter(file, fieldnames=header, delimiter=',')
        csv_dict_writer.writeheader()
        for row in data:
            if row['id'] == question_id:
                data.remove(row)
        for row in data:
            csv_dict_writer.writerow(row)


def delete_image(filename, question_id):
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['id'] == str(question_id):
                os.remove('static/images/' + row['image'])


def vote_questions(filename, question_id, action):
    questions = read_from_csv(filename)
    for row in questions:
        if row['id'] == question_id:
            if action == 'up':
                row['vote_number'] = str(int(row['vote_number']) + 1)
            else:
                row['vote_number'] = str(int(row['vote_number']) - 1)
    with open(filename, "w") as csv_file:
        fieldnames = QUESTION_HEADER
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in questions:
            writer.writerow(row)


def vote_answer(filename, answer_id, action):
    answers = read_from_csv(filename)
    for row in answers:
        if row['id'] == answer_id:
            if action == 'up':
                row['vote_number'] = str(int(row['vote_number']) + 1)
            elif action == 'down':
                row['vote_number'] = str(int(row['vote_number']) - 1)
    with open(filename, "w") as csv_file:
        fieldnames = ANSWER_HEADER
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in answers:
            writer.writerow(row)


def update_question(question_id, data, header, filename, title_input, message_input, time_input):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header, delimiter=',')
        writer.writeheader()
        for row in data:
            if row['id'] == question_id:
                #row.update(question_arg)
                row['title'] = title_input
                row['message'] = message_input
                row['submission_time'] = time_input
            writer.writerow(row)