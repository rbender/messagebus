import mysql.connector

import sys
import uuid
import json
import logging
import messagebus.util.log_utils
import messagebus.util.date_time_utils as date_time_utils

from messagebus import Message

INSERT_MESSAGE_SQL = ("INSERT INTO messages "
                      "(message_uuid, message_uuid_text, message_source, message_type, message_json, message_timestamp, message_received) "
                      "VALUES (%(message_uuid)s, %(message_uuid_text)s, %(message_source)s, "
                      "%(message_type)s, %(message_json)s, %(message_timestamp)s, %(message_received)s)")

class MySqlMessageStore(object):

    def __init__(self, username, password, host, database):
        self.username = username
        self.password = password
        self.host = host
        self.database = database
        self.logger = logging.getLogger("MySqlMessageStore")

    def insert_message(self, message):

        message_uuid = uuid.UUID(message.id)
        timestamp = date_time_utils.unix_timestamp_to_datetime(message.timestamp)
        received = date_time_utils.unix_timestamp_to_datetime(message.received_timestamp)

        values = {
            "message_uuid" : message_uuid.bytes,
            "message_uuid_text" : message.id,
            "message_source" : message.source,
            "message_type" : message.type,
            "message_json" : json.dumps(message.data),
            "message_timestamp" : timestamp,
            "message_received" : received
        }

        self.logger.debug(values)

        connection = mysql.connector.connect(user=self.username, password=self.password, host=self.host, database=self.database)

        cursor = connection.cursor()
        cursor.execute(INSERT_MESSAGE_SQL, values)

        connection.commit()

        cursor.close()

        connection.close()

if __name__ == "__main__":

    messagebus.util.log_utils.init()

    mysql_store = MySqlMessageStore(username='root', password=sys.argv[1], host="127.0.0.1", database="messagebus")

    message_uuid = uuid.uuid4()
    now = date_time_utils.timestamp()

    id = str(uuid.uuid4())
    message = Message(id=id, type="event.test", source="foo.bar", data={"hello" : "world"}, timestamp=now, received_timestamp=now)

    mysql_store.insert_message(message)

    print "Done"

