# coding: utf8

import pymssql
import psycopg2
import fdb

__author__ = "karlosss"

# Class to establish database connection and execute queries
# Reads from ../connections.pwd file
# Syntax rules inside the file
#
#
#
# USAGE:
#
# sample_connection = Connection("connection name")
# sample_connection.execute("SQL query")
#
# if using the SELECT statement:
# selected_data = sample_connection.execute("SQL SELECT query")
#
# TODO: exceptions

class Connection:

    def __init__(self, target):

        f = open('connections.pwd')

        content = []

        # preparing the config for being parsed
        for line in f:
            # remove right and left-side spaces from each line
            line = line.strip()
            # remove blank lines
            if line == "":
                continue
            # remove comments
            if line[0] != "#":
                content.append(line)

        parsed_content = []

        # parsing the content, grouping it to lists by connections
        for line in content:

            # create a new connection
            if line == "[Connection]":
                parsed_content.append({})

            # append a feature of an existing connection
            else:
                parsed_content[len(parsed_content)-1][line.split(":")[0].strip()] = line.split(":")[1].strip()

        connection_data = {}

        # finding the desired connection
        for data in parsed_content:

            # searches for the desired connection
            if data["name"] == target:
                for line in data:
                    connection_data[line] = data[line]

                # handling optional argument, port
                if "port" not in connection_data:
                    connection_data["port"] = ""
                else:
                    if connection_data["type"] == "MSSQL":
                        connection_data["port"] = ":" + connection_data["port"]

                if "charset" not in data:
                    connection_data["charset"] = ""

        # connects to the desired connection
        if connection_data["type"] == "MSSQL":
            self.connection = pymssql.connect(
                host=connection_data["ip"] + connection_data["port"],
                user=connection_data["user"],
                password=connection_data["password"],
                database=connection_data["database"],
                charset=connection_data["charset"],
            )

        elif connection_data["type"] == "PostgreSQL":
            self.connection = psycopg2.connect(
                host=connection_data["ip"],
                port=connection_data["port"],
                user=connection_data["user"],
                password=connection_data["password"],
                dbname=connection_data["database"],
                client_encoding=connection_data["charset"],
            )

        elif connection_data["type"] == "Firebird":
            self.connection = fdb.connect(
                host=connection_data["ip"],
                database=connection_data["database"],
                user=connection_data["user"],
                password=connection_data["password"],
                port=connection_data["port"]
            )

        # prepares the cursor
        self.cursor = self.connection.cursor()
        self.type = connection_data["type"]

    def execute(self, query, protected=True):
        if self.type == "Firebird":
            self.cursor.execute("execute procedure relog_user(1)")
            self.connection.commit()

        # escape the following statements in queries if protected
        if "INSERT " not in query.upper() and \
           "DELETE " not in query.upper() and \
           "UPDATE " not in query.upper() and \
           "DROP " not in query.upper() and \
           "CREATE " not in query.upper() and \
           ";" not in query:
                self.cursor.execute(query)
                if "SELECT " not in query.upper():
                    self.connection.commit()

        else:
            if protected:
                raise Exception("YOU SHALL NOT PASS!!!")
            else:
                self.cursor.execute(query)
                if "SELECT " not in query.upper():
                    self.connection.commit()
        try:
            return self.cursor.fetchall()
        except:
            pass

