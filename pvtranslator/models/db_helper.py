import os


def gen_connection_string():

    sql_user = os.environ.get('CLOUDSQL_USER', 'root')
    sql_pass = os.environ.get('CLOUDSQL_PASSWORD', '')
    sql_db = os.environ.get('CLOUDSQL_DATABASE')

    # if not on Google then use local MySQL
    if not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        conn_template = 'mysql+mysqldb://%s:%s@127.0.0.1:3306/%s'
        return conn_template % (sql_user, sql_pass, sql_db)

    else:
        conn_name = os.environ.get('CLOUDSQL_CONNECTION_NAME' '')
        conn_template = 'mysql+mysqldb://%s:%s@/%s?unix_socket=/cloudsql/%s'
        return conn_template % (sql_user, sql_pass, sql_db, conn_name)