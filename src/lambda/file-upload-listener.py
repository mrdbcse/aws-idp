import os
from datetime import datetime as dt
from urllib.parse import unquote_plus
from zoneinfo import ZoneInfo

import boto3

dynamo_db = boto3.resource("dynamodb")
table = dynamo_db.Table(os.getenv("DOCS_TABLE_NAME"))
IST = ZoneInfo("Asia/Kolkata")


def lambda_handler(event, context):
    print(event)

    for record in event["Record"]:
        key = unquote_plus(record["s3"]["object"]["key"])
        size = record["s3"]["object"]["size"]
        etag = record["s3"]["object"]["eTag"]

        parts = key.split("/")
        user_id, doc_id = parts[0], parts[1]
        now = dt.now(tz=IST).isoformat()

        table.update_item(
            Key={"user_id": user_id, "doc_id": doc_id},
            UpdateExpression="SET #s = :s, uploaded_at = :t, file_size = :fs, etag = :e",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":s": "UPLOADED",
                ":t": now,
                ":fs": size,
                ":e": etag,
            },
        )
