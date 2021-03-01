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


@database_common.connection_handler
def get_answer_by_id(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        SELECT id, submission_time, vote_number, question_id, message, image
        FROM answer
        WHERE id = %(i)s
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_question(cursor: RealDictCursor, used_id: str) -> list:
    query = """
        SELECT id, submission_time, vote_number, image, message
        FROM answer
        WHERE question_id = %(i)s
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def save_answer(cursor: RealDictCursor, submission_time: int, vote_number: int, question_id: str, message: str, image: str) -> list:
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (%(s_t)s, %(vote_n)s, %(q)s, %(m)s, %(im)s)
        RETURNING *
        """
    cursor.execute(query, {'s_t': submission_time, 'vote_n': vote_number, 'q': question_id, 'm': message, 'im': image})
    return cursor.fetchall()


@database_common.connection_handler
def save_question(cursor: RealDictCursor, submission_time: int, view_number: int, vote_number: str, title: str, message: str, image: str) -> list:
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES (%(s_t)s, %(view_n)s, %(vote_n)s, %(t)s, %(m)s, %(im)s)
        RETURNING *
        """
    cursor.execute(query, {'s_t': submission_time, 'view_n': view_number, 'vote_n': vote_number, 't': title, 'm': message, 'im': image})
    return cursor.fetchall()


@database_common.connection_handler
def update_question(cursor: RealDictCursor, used_id: int, title_input: str, message_input: str, time_used: str) -> list:
    query = """
        UPDATE question
        SET title = %(t)s, message = %(m)s, submission_time = %(ti)s
        WHERE id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': used_id, 't': title_input, 'm': message_input, 'ti': time_used})
    return cursor.fetchall()


@database_common.connection_handler
def update_answer(cursor: RealDictCursor, used_id: int, message_input: str, time_used: str) -> list:
    query = """
        UPDATE answer
        SET message = %(m)s, submission_time = %(ti)s
        WHERE id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': used_id, 'm': message_input, 'ti': time_used})
    return cursor.fetchall()


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, used_id: int) -> list:
    query = """
            DELETE FROM answer
            WHERE id = %(i)s
            RETURNING *
            """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, used_id: int) -> list:
    query = """
            DELETE FROM question
            WHERE id = %(i)s
            RETURNING *
            """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def increment_question_vote_number(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def decrement_question_vote_number(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def increment_answer_vote_number(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def decrement_answer_vote_number(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def insert_tag(cursor: RealDictCursor, tag_name: str) -> list:
    query = """
        INSERT INTO tag (name)
        VALUES (%(t_n)s)
        RETURNING *
        """
    cursor.execute(query, {'t_n': tag_name})
    return cursor.fetchall()


@database_common.connection_handler
def get_existing_tags(cursor: RealDictCursor) -> list:
    query = """
        SELECT id, name
        FROM tag
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def insert_questions_tag(cursor: RealDictCursor, question_id: str, tag_id: str) -> list:
    query = """
        INSERT INTO question_tag (question_id, tag_id)
        VALUES (%(q)s, %(t)s)
        RETURNING *
        """
    cursor.execute(query, {'q': question_id, 't': tag_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_tags(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT question.id, tag.name, tag.id FROM question INNER JOIN question_tag 
        ON question.id=question_tag.question_id 
        INNER JOIN tag ON question_tag.tag_id=tag.id WHERE question.id=%(i)s;
        """
    cursor.execute(query, {'i': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_tag(cursor: RealDictCursor, question_id: str, tag_id: str) -> list:
    query = """
            DELETE FROM question_tag
            WHERE tag_id = %(t)s and question_id = %(q)s
            RETURNING *
            """
    cursor.execute(query, {'q': question_id, 't': tag_id})
    return cursor.fetchall()