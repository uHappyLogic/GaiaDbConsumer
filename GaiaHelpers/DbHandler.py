import psycopg2
from GaiaHelpers.LocalConfig import LocalConfig


class DbHandler:

    def __init__(self):
        self.conn = None

    def get_connection(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                user=LocalConfig.get_db_user(),
                password=LocalConfig.get_db_password(),
                host=LocalConfig.get_db_host(),
                port=LocalConfig.get_db_port(),
                database=LocalConfig.get_db_name())
            self.conn.autocommit = False

        return self.conn

    def get_cursor(self):
        return self.get_connection().cursor()

    def drop_tables(self):
        try:
            with self.get_cursor() as cursor:
                cursor.execute("drop table stars")
                cursor.execute("drop table done")
                self.get_connection().commit()
            print("Tables dropped")
        except:
            print("Initialising tables")

    def create_tables(self):
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""CREATE TABLE stars(
                    source_id BIGINT,
                    color CHAR(7),
                    x float,
                    y float,
                    z float
                    )""")
                cursor.execute("""CREATE TABLE done(
                    filename VARCHAR(255)
                    )""")
                cursor.execute("""CREATE INDEX done__filename on done(filename)""")
                self.get_connection().commit()
                print("Tables created")
        except Exception as e:
            print(e)

    def check_if_done(self, file):
        with self.get_cursor() as cursor:
            cursor.execute("select 1 from done d where d.filename = '{}'".format(file))
            return cursor.fetchone() is not None

    def mark_as_done(self, file):
        with self.get_cursor() as cursor:
            cursor.execute("insert into done values ('{}')".format(file))
            self.get_connection().commit()

    def bulk_save_to_db(self, queue):
        try:
            command = "insert into stars values "

            for s_id, hex_color, x, y, z in queue:
                command += "({}, '{}', {}, {}, {}),".format(s_id, hex_color, x, y, z)

            command = command[:-1]

            with self.get_cursor() as cursor:
                cursor.execute(command)
                self.get_connection().commit()
        except (Exception, psycopg2.Error) as ex:
            print("Error happen during save")
            print(ex)

    def check_values(self, amount):
        with self.get_cursor() as cursor:
            print("first {} rows from stars:".format(amount))
            cursor.execute("select s.* from stars s limit{}".format(amount))
            for row in cursor:
                print(row)
