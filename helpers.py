import psycopg2

def connect_to_database(host, dbname, username, pw):
    conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

    try:
        conn = psycopg2.connect(conn_string)
    except psycopg2.OperationalError as e:
        print('Connection failed!')
        print('Error message:', e)
        exit()

    cursor = conn.cursor()

    return cursor, conn