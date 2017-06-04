from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, utils
import re

input_path = 'incoming_wa.txt'
input_file = open(input_path, 'r+')
out_file = open('commands.sh', 'w+')
error_file = open('error_records.txt', 'w+')
es = Elasticsearch(
    'https://127.0.0.1:8084',
    ca_certs='/opt/evive/pkgs/elasticsearch-5.2.2/config/keys/ca.pem',
    http_auth=('admin', 'changeme'),
    timeout=120
)


def parse_date(str_date):
    """
    Sample input :: 07/03/17, 10:42 PM
    :param str_date: 
    :return: return datetime
    """
    pass

def get_record_details(line):
    """
    Sample input : 07/03/17, 10:42 PM - Jay Vora: Parakh, parth, kishan, hdk 110/5 to Jv roti
    :param line: 
    :return: 
    """
    if 'M -' in line:
        record_string = line.split('M -')[1]
        return record_string
    return None


def get_who_made_entry_and_entry(record_line):
    if ':' in record_line:
        record_user, record_line = record_line.split(':')
        return record_user, record_line

    return None

def ultimate_tokenizer(record_data):
    return re.findall(r"[\w\.\-']+", record_data)


def record_data_to_token(record_data):
    split = record_data.split('to')
    if len(split) > 1:
        return split
    split = record_data.split(']')
    if len(split) > 0:
        return split


def digits_only(str_amt):
    return re.findall(r"\d", str_amt)

def get_amount_from_record_string(record_data_from):
    return record_data_from.split(' ')[-1]


def integration_test(data):
    step1 = get_record_details(
        data
    )

    print(step1)

    step2 = get_who_made_entry_and_entry(
        step1
    )

    print(step2)

    step3 = record_data_to_token(
        step2[1]
    )

    step3[0] = step3[0].rstrip(' ')

    print(step3)

    amount_value = ultimate_tokenizer(get_amount_from_record_string(step3[0]))

    to_user = list(check_user_in_db(ultimate_tokenizer(step3[1])[0]))[0]

    if 'all' not in step3[0].lower():
        from_user_list = check_user_in_db(step3[0])
    else:
        try:
            from_user_list = check_user_in_db(step3[0])
            from_user_list = from_user_list - set([to_user])
            if '-' in step3[0]:
                removables =  check_user_in_db(step3[0].lower().replace('all', ''))
                from_user_list = from_user_list - removables
        except ValueError as ve:
            raise


    comment_string = ' '.join(ultimate_tokenizer(step3[1].lstrip(' '))[1:])

    operation_str = "split" if '/' in get_amount_from_record_string(step3[0]) else "group"

    print("from : ",  from_user_list)
    print("amount : ", amount_value )
    print("to : ", to_user)
    print("comment : ", comment_string)
    print("operation : ", operation_str)



    out_file.write('./exec {} {} {} {} {}\n'.format(
        operation_str,
        ','.join(from_user_list),
        amount_value[0],
        to_user,
        comment_string
    ))


def populate_es():
    users = ["jd" , "jv", "hardik", "kishan", "parth", "jayb", "jigar", "gautm", "harshil", "parakh"]
    fuzzy = [ ("all", [ "parakh", "jd",  "jv",  "hardik", "kishan", "parth", "jigar" ]) ]
    for user in fuzzy:
        es.index(
            index="expense_manager",
            doc_type="user",
            body={
                "username": user[0],
                "actual_username": user[1]
            }
        )


def check_user_in_db(user):
    search_q = Search(using=es, index='expense_manager', doc_type='user') \
        .query('match', username=user)

    result = search_q.scan()
    res = []
    for user_found in result:
        if isinstance(user_found.actual_username, utils.AttrList):
            res.extend(user_found.actual_username)
        else:
            res.append(user_found.actual_username)
    print(res)
    return set(res)

# populate_es()
#check_user_in_db("Parag 22")
#integration_test("20/03/17, 10:13 PM - Jay Vora: jv kishan [9.4] to jd for perk")

for line in input_file:
    try:
        integration_test(line)
    except Exception as e:
        print(e)
        error_file.write(line)

out_file.close()
error_file.close()