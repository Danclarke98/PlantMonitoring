import paho.mqtt.client as mqtt  # import the client1
import time
import json as json
import pymysql


conn = pymysql.connect(
    host='{hostname}',
    user='{user}',
    passwd='{pswd}',
    db='{db}',
    autocommit=True
)

with conn:

    cur = conn.cursor();

    try:
        cur.execute("SELECT id FROM sensor_data LIMIT 1;")
    except pymysql.ProgrammingError as e:
        print e


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))

    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

    m_decode = str(message.payload.decode("utf-8", "ignore"))
    print("data Received type", type(m_decode))
    print("data Received", m_decode)
    json.loads(m_decode)
    print("Converting from Json to Object")
    jsondata = json.loads(m_decode)  # decode json data
    jsonbackup(jsondata)
    print ("done")


def jsonbackup(jsondata):
    sqlstatement = ''
    for json in jsondata:
        keylist = "("
        valuelist = "("
        firstPair = True
        for key, value in json.items():
            if not firstPair:
                keylist += ", "
                valuelist += ", "
            firstPair = False
            keylist += key
            if type(value) in (str, unicode):
                valuelist += "'" + value + "'"
            else:
                valuelist += str(value)
        keylist += ")"
        valuelist += ")"

        sqlstatement += "INSERT INTO " + "sensor_data" + " " + keylist + " VALUES " + valuelist + "\n"
        print (sqlstatement)
        cur.execute(sqlstatement)
        print ("Data Inserted")

    print(sqlstatement)


broker_address = "{MQTTBROKER IP ADDRESS}"
print("creating new instance")
client = mqtt.Client("P1")  # create new instance
client.on_message = on_message  # attach function to callback
print("connecting to broker")
client.username_pw_set("sqlbroker", "{Password}")
client.connect(broker_address)  # connect to broker
print("Subscribing to sensor topics")
client.subscribe("sensor/#")
time.sleep(4)  # wait
client.loop_forever()
