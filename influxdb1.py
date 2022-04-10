from influxdb import InfluxDBClient

host = "localhost"
port = "8086"
user = "openwisp"
password = "openwisp"
db = "openwisp2"

client = InfluxDBClient(host, port, user, password, db)

#creating a database
database = client.create_database("openwisp")

#writing data to the created database
points = []
point = {
  "measurement": "test_load_short",
  "tags": {
    "host": "test_host",
    "region": "India"
  },
  "time": "2022-04-10T23:00:00Z",
  "fields": {
    "value": 0.1
  }
}

points.append(point)
client.write_points(points)

#making a query
query = "select value from test_load_short"
# query clause, precision, response code, database
query_result = client.query(query, epoch='s', expected_response_code=200, database=database)
query_points = query_result.get_points()
# expected result set: ResultSet({'('test_load_short', None)': [{'time': '2022-04-10T23:00:00Z', 'value': 0.1}]})

#retention policies
retention_policies = client.get_list_retention_policies()
# retention_policies is a list of retention_policy objects

#create a new retention policy
client.create_retention_policy(name="test_policy", duration='1h', replication=1)

#alter an existing retention policy
client.alter_retention_policy(name="test_policy", duration='2h', replication=1)

#deleting data from a 'metric' basically data related to a specific set of events happening at regular intervals
""" tags
{'host': 'test_host'}
key
'test_load_short' """
client.delete_series(measurement=key, tags=tags)

#delete a database
client.drop_database(db)
