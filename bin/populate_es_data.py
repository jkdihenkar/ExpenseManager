from elasticsearch import Elasticsearch
import elasticsearch_dsl

from ESBasedParser import check_user_in_db

es = Elasticsearch(
    'http://127.0.0.1:9200',
    timeout=120
)


def populate_es():
    users = ["jd", "jv", "hardik", "kishan", "parth",
             "jayb", "jigar", "gautm", "harshil", "parakh"]
    fuzzy = [("all", ["parakh", "jd",  "jv",  "hardik", "kishan", "parth", "jigar"])]
    for user in fuzzy:
        es.index(
            index="expense_manager",
            doc_type="user",
            id=user[0],
            body={
                "username": user[0],
                "actual_username": user[1]
            }
        )
    for user in users:
        es.index(
            index="expense_manager",
            doc_type="user",
            id=user,
            body={
                "username": user,
                "actual_username": user
            }
        )
    mappings_name = {
        'hdk': 'hardik',
        'parag': 'parakh',
        'paado': 'parth',
        'pado': 'parth',
        'chotyo': 'hardik',
        'chotiyo': 'hardik',
        '6otiyo': 'hardik',
        '6otyo': 'hardik',
        'tidde': 'hardik'
    }
    for usrname, actusername in mappings_name.items():
        es.index(
            index="expense_manager",
            doc_type="user",
            id=usrname,
            body={
                "username": usrname,
                "actual_username": actusername
            }
        )

if __name__ == "__main__":
    populate_es()
    check_user_in_db(es, "Parag 22")
    check_user_in_db(es, "6otyo 22")
    check_user_in_db(es, "Pado 22")
    check_user_in_db(es, "Paado 22")
