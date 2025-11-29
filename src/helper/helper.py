import os
from datetime import datetime as dt

import boto3
import pytz
from dotenv import load_dotenv

load_dotenv()
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.getenv("DOCS_TABLE_NAME")
IST = pytz.timezone("Asia/Kolkata")


def store_document_metadata(
    user_id: str,
    doc_id: str,
    s3_key: str,
    filename: str,
    content_type: str,
    status: str = "PENDING_UPLOAD",
) -> None:

    try:

        if not TABLE_NAME:
            raise RuntimeError("DOCS_TABLE_NAME environment variable is not set")

        table = dynamodb.Table(TABLE_NAME)

        item = {
            "user_id": user_id,
            "doc_id": doc_id,
            "s3_key": s3_key,
            "filename": filename,
            "content_type": content_type,
            "status": status,
            "created_at": dt.now(tz=IST).isoformat(),
            "updated_at": dt.now(tz=IST).isoformat(),
        }

        table.put_item(Item=item)

    except Exception as e:
        print(f"Dynamo DB insert failed: {e}")
