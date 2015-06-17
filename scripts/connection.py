# coding: utf8

from os.path import dirname
import pymssql
import psycopg2

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

        f = open(dirname(__file__) + '/../connections.pwd')

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

        data = {}

        # finding the desired connection
        for data in parsed_content:

            # searches for the desired connection
            if data["name"] == target:
                for line in data:
                    data[line] = data[line]

                # handling optional argument, port
                if "port" not in data:
                    data["port"] = ""
                else:
                    if data["type"] == "MSSQL":
                        data["port"] = ":" + data["port"]

                if "charset" not in data:
                    data["charset"] = ""

        # connects to the desired connection
        if data["type"] == "MSSQL":
            connection = pymssql.connect(
                host=data["ip"] + data["port"],
                user=data["user"],
                password=data["password"],
                database=data["database"],
                charset=data["charset"],
            )

        elif data["type"] == "PostgreSQL":
            connection = psycopg2.connect(
                host=data["ip"],
                port=data["port"],
                user=data["user"],
                password=data["password"],
                dbname=data["database"],
                client_encoding=data["charset"],
            )

        # prepares the cursor
        self.cursor = connection.cursor()

    def execute(self, query):

        # escape the following statements in queries
        if "INSERT" not in query and \
           "DELETE" not in query and \
           "UPDATE" not in query and \
           "DROP" not in query and \
           "CREATE" not in query and \
           ";" not in query:
                self.cursor.execute(query)
        else:
                raise Exception("YOU SHALL NOT PASS!!!")

        return self.cursor.fetchall()

