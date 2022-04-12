from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.domain.patch_retention_rule import PatchRetentionRule

url = "http://localhost:8086"
bucket = "openwisp2"
org = "openwisp"
token = "openwisp"

client = InfluxDBClient(url=url, org=org, token=token)

# there are two APIs, one used for writing data and the other for reading
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

# bucket is already created in the docker container

#creating a point to write data to the bucket

# specifying the measurement (metric) adding tags and values, optionally adding time
point = Point("test_load_short").tag("host", "test_host").tag("region", "India").field("value", 0.1).time('2022-04-10T23:00:00Z')

#writing data
write_api.write(bucket=bucket, record=point)

# query api
query = '''from(bucket:"openwisp2") |> range(start: 0, stop: now()) |> filter(fn: (r) => r._measurement == "test_load_short")'''
records = query_api.query_stream(query)
# records is a 'generator object and needs to be modified if rpresentation is desired in the form of a dictionary or a json object'

# get the object for bucket with it's name
bucket = client.buckets_api().find_bucket_by_name("openwisp2")

#retention rules
retention_rules = bucket.retention_rules

#PatchRetentionRule for more precise control over each retention rule
