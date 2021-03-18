from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_common

ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
questions_file = 'sample_data/question.csv'
answers_file = 'sample_data/answer.csv'


@database_common.connection_handler
def get_questions(cursor: RealDictCursor, criteria: str = None, direction: str = None) -> list:
    query = f"""
        SELECT id, submission_time, view_number, vote_number, title, image, message
        FROM question
        ORDER BY {criteria} {direction}
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_questions_by_time(cursor: RealDictCursor) -> list:
    query = """
    SELECT id, submission_time, view_number, vote_number, title, image, message
    FROM question 
    ORDER BY submission_time DESC 
    """
    cursor.execute(query)
    return cursor.fetchmany(5)


@database_common.connection_handler
def get_individual_question(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        SELECT id, submission_time, view_number, vote_number, title, image, message, user_id
        FROM question
        WHERE id = %(i)s
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answers(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        SELECT id, submission_time, vote_number, question_id, message, image, accepted
        FROM answer
        WHERE question_id = %(i)s
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_by_id(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        SELECT id, submission_time, vote_number, question_id, message, image, user_id
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
def save_answer(cursor: RealDictCursor, submission_time: int, vote_number: int, question_id: str, message: str,
                image: str, user_id: str) -> list:
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
        VALUES (%(s_t)s, %(vote_n)s, %(q)s, %(m)s, %(im)s, %(u)s)
        RETURNING *
        """
    cursor.execute(query, {'s_t': submission_time, 'vote_n': vote_number, 'q': question_id, 'm': message,
                           'im': image, 'u': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def save_question(cursor: RealDictCursor, submission_time: int, view_number: int, vote_number: str, title: str, message: str, image: str, user_id) -> list:
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
        VALUES (%(s_t)s, %(view_n)s, %(vote_n)s, %(t)s, %(m)s, %(im)s, %(u)s)
        RETURNING *
        """
    cursor.execute(query, {'s_t': submission_time, 'view_n': view_number, 'vote_n': vote_number, 't': title,
                           'm': message, 'im': image, 'u': user_id})
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


@database_common.connection_handler
def search_in_questions(cursor: RealDictCursor, search_input: str) -> list:
    query = """
        SELECT title, message, image
        FROM question
        WHERE title LIKE %(s)s OR message like %(s)s
        """
    cursor.execute(query, {'s': search_input})
    return cursor.fetchall()


@database_common.connection_handler
def search_in_answers(cursor: RealDictCursor, search_input: str) -> list:
    query = """
        SELECT message, image
        FROM answer
        WHERE message like %(s)s
        """
    cursor.execute(query, {'s': search_input})
    return cursor.fetchall()


@database_common.connection_handler
def increase_view_count(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id(cursor: RealDictCursor, title: str) -> list:
    query = """
        SELECT id
        FROM question 
        WHERE title = %(s)s
        """
    cursor.execute(query, {'s': title})
    return cursor.fetchall()


@database_common.connection_handler
def save_comment(cursor: RealDictCursor, submission_time: int, question_id: int, answer_id: int, edited_count: int,
                 message: str, user_id: str) -> list:
    query = """
        INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id)
        VALUES (%(q_i)s, %(a_i)s, %(m)s, %(s_t)s, %(e_c)s, %(u)s)
        RETURNING *
        """
    cursor.execute(query,
                   {'q_i': question_id, 'a_i': answer_id, 'm': message, 's_t': submission_time, 'e_c': edited_count,
                    'u': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def save_comment_no_user(cursor: RealDictCursor, submission_time: int, question_id: int, answer_id: int, edited_count: int,
                 message: str) -> list:
    query = """
        INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
        VALUES (%(q_i)s, %(a_i)s, %(m)s, %(s_t)s, %(e_c)s)
        RETURNING *
        """
    cursor.execute(query,
                   {'q_i': question_id, 'a_i': answer_id, 'm': message, 's_t': submission_time, 'e_c': edited_count,
                    })
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_id(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        SELECT id, question_id, answer_id, message, submission_time, edited_count, user_id
        FROM comment
        WHERE id = %(i)s
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_individual_comment(cursor: RealDictCursor, used_id: int) -> list:
    query = """
        SELECT id, question_id, answer_id, message, submission_time, edited_count, user_id
        FROM comment
        WHERE question_id = %(i)s
        """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def update_comment(cursor: RealDictCursor, used_id: int, message_input: str, edited_count: int, time_used: int) -> list:
    query = """
        UPDATE comment
        SET message = %(m)s, submission_time = %(ti)s, edited_count = %(e_t)s
        WHERE id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': used_id, 'm': message_input, 'ti': time_used, 'e_t': edited_count})
    return cursor.fetchall()


@database_common.connection_handler
def delete_comment(cursor: RealDictCursor, used_id: int) -> list:
    query = """
            DELETE FROM comment
            WHERE id = %(i)s
            RETURNING *
            """
    cursor.execute(query, {'i': used_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id_by_answer_id(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
        SELECT question_id
        FROM answer
        WHERE id = %(i)s
        """
    cursor.execute(query, {'i': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_by_answer_id(cursor: RealDictCursor, answer_id: int) -> list:
    query = """
        SELECT id, question_id, answer_id, message, submission_time, edited_count
        FROM comment
        WHERE answer_id = %(i)s
        """
    cursor.execute(query, {'i': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_answers_by_question_id(cursor: RealDictCursor, question_id: str) -> list:
    query = """
            DELETE FROM answer
            WHERE question_id = %(q)s
            RETURNING *
            """
    cursor.execute(query, {'q': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_comments_by_question_id(cursor: RealDictCursor, question_id: str) -> list:
    query = """
            DELETE FROM comment
            WHERE question_id = %(q)s
            RETURNING *
            """
    cursor.execute(query, {'q': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def delete_tags_by_question_id(cursor: RealDictCursor, question_id: str) -> list:
    query = """
            DELETE FROM question_tag
            WHERE question_id = %(q)s
            RETURNING *
            """
    cursor.execute(query, {'q': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_all_users(cursor: RealDictCursor) -> list:
    query = """
        SELECT username, password, user_id, username, submission_time, reputation
        FROM users
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def add_user(cursor: RealDictCursor, username: str, password: str, submission_time: str) -> list:
    query = """
        INSERT INTO users (username, password, submission_time)
        VALUES (%(u)s, %(p)s, %(s_t)s)
        RETURNING *
        """
    cursor.execute(query, {'u': username, 'p': password, 's_t': submission_time})
    return cursor.fetchall()


@database_common.connection_handler
def get_tags(cursor: RealDictCursor) -> list:
    query = """
            SELECT COUNT(question_tag.tag_id), tag.name FROM question_tag
	        RIGHT JOIN tag ON question_tag.tag_id = tag.id
	        GROUP BY tag_id, tag.name
	        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_user_credentials(cursor: RealDictCursor, username_input: str) -> list:
    query = """
        SELECT username, password, user_id
        FROM users
        WHERE username = %(u)s
        """
    cursor.execute(query, {'u': username_input})
    return cursor.fetchall()


@database_common.connection_handler
def get_user_id(cursor: RealDictCursor, username: str) -> list:
    query = """
    SELECT user_id
    FROM users
    WHERE username = %(u)s
    """
    cursor.execute(query, {'u': username})
    return cursor.fetchone()


@database_common.connection_handler
def increase_user_rep_by_question(cursor: RealDictCursor, user_id: int) -> list:
    query = """
        UPDATE users
        SET reputation = reputation + 5
        WHERE user_id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def increase_user_rep_by_answer(cursor: RealDictCursor, user_id: int) -> list:
    query = """
        UPDATE users
        SET reputation = reputation + 10
        WHERE user_id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def decrease_user_reputation(cursor: RealDictCursor, user_id: int) -> list:
    query = """
        UPDATE users
        SET reputation = reputation - 2
        WHERE user_id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def accept_answer(cursor: RealDictCursor, answer_id: int):
    query = """
        UPDATE answer
        SET accepted = 'true' 
        WHERE id = %(i)s
    """
    cursor.execute(query, {'i': answer_id})


@database_common.connection_handler
def increase_rep_accepted_answer(cursor: RealDictCursor, user_id: int) -> list:
    query = """
        UPDATE users
        SET reputation = reputation + 15
        WHERE user_id = %(i)s
        RETURNING *
        """
    cursor.execute(query, {'i': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comment_userid(cursor: RealDictCursor, comment_id: str) -> list:
    query = """
        SELECT user_id
        FROM comment 
        WHERE id = %(id)s
        """
    cursor.execute(query, {'id': comment_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_userid(cursor: RealDictCursor, answer_id: str) -> list:
    query = """
        SELECT user_id
        FROM answer 
        WHERE id = %(id)s
        """
    cursor.execute(query, {'id': answer_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_by_user_id(cursor: RealDictCursor, user_id: str) -> list:
    query = """
        SELECT id, question_id, answer_id, message, submission_time, edited_count, user_id
        FROM comment
        WHERE user_id = %(i)s
        """
    cursor.execute(query, {'i': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_user_id(cursor: RealDictCursor, user_id: str) -> list:
    query = """
        SELECT id, submission_time, vote_number, image, message, user_id, question_id, accepted
        FROM answer
        WHERE user_id = %(i)s
        """
    cursor.execute(query, {'i': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_questions_by_user_id(cursor: RealDictCursor, user_id: str) -> list:
    query = """
        SELECT id, submission_time, view_number, vote_number, title, image, message, user_id
        FROM question
        WHERE user_id = %(i)s
        """
    cursor.execute(query, {'i': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_user_by_id(cursor: RealDictCursor, user_id: str) -> list:
    query = """
        SELECT username, user_id, submission_time, reputation
        FROM users
        WHERE user_id = %(i)s
        """
    cursor.execute(query, {'i': user_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_user_by_id(cursor: RealDictCursor, user_id: str) -> list:
    query = """
        SELECT username, user_id, submission_time, reputation
        FROM users
        WHERE user_id = %(i)s
        """
    cursor.execute(query, {'i': user_id})
    return cursor.fetchone()


