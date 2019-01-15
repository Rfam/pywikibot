import pymysql.cursors

# Connect to the database


connection = pymysql.connect(host='mysql-rfam-public.ebi.ac.uk',
                             user='rfamro',
                             db='Rfam',
                             port=4497,
                             cursorclass=pymysql.cursors.DictCursor)


def get_rfam_wiki_pages():
    pages = []
    try:
        with connection.cursor() as cursor:
            sql = """SELECT DISTINCT title
                     FROM wikitext, family
                     WHERE
                     wikitext.auto_wiki = family.auto_wiki"""
            cursor.execute(sql)
            for result in cursor.fetchall():
                pages.append(result['title'].decode('utf-8'))
    finally:
        connection.close()
    return pages
