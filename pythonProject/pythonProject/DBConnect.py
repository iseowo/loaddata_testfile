import io
import os
from datetime import datetime
import DBConfig
from ansible.module_utils.postgres import psycopg2


class DbConnection:
    db_parm = DBConfig.db_name
    username_parm = DBConfig.db_username
    host_parm = DBConfig.db_endpoint
    pw_parm = DBConfig.pw_tile

    # def db_connect(self, db_parm, username_parm, host_parm, pw_parm):
    def db_connect(self):

        # Parse in connection information
        credentials = {'host': self.host_parm, 'database': self.db_parm, 'user': self.username_parm,
                       'password': self.pw_parm}

        conn = psycopg2.connect(**credentials)
        conn.autocommit = True  # auto-commit each entry to the database
        cur = conn.cursor()
        print("Connected Successfully to DB: " + str(self.db_parm) + "@" + str(self.host_parm))
        return conn, cur

    def copy_from_stringio(self, conn, df, table):

        print("copy_from_StringIO() start")
        """
        Here we are going save the dataframe in memory 
        and use copy_from() to copy it to the table
        """
        # save dataframe to an in memory buffer
        buffer = io.StringIO()

        df.to_csv(buffer, sep="|", index=False, header=False)

        buffer.seek(0)

        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM " + table + ";")
            cur.copy_from(buffer, table, sep="|")
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            # os.remove(tmp_df)
            print("Error: %s" % error)
            conn.rollback()
            cur.close()
            return 1
        print("copy_from_stringio() done")
        end = datetime.now().strftime("%Y%m%d%H%M%S")
        print('end', end)
        cur.close()
