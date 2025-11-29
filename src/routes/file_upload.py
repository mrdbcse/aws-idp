import os
import uuid

import boto3
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from src.helper.helper import store_document_metadata
from src.schema.schema import FileUploadRequest, FileUploadResponse

load_dotenv()
router = APIRouter()
s3 = boto3.client("s3")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
EXPIRES_IN = 3600


@router.post("/file-upload", response_model=FileUploadResponse)
def generate_upload_url(req: FileUploadRequest):
    document_id = f"doc_{uuid.uuid4().hex[:12]}"
    print(f"{document_id=}")

    s3_key = f"{req.user_id}/{document_id}/{req.filename}"
    print(f"{s3_key=}")

    try:
        upload_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": s3_key,
                "ContentType": req.content_type,
            },
            ExpiresIn=EXPIRES_IN,
        )

        store_document_metadata(
            user_id=req.user_id,
            doc_id=document_id,
            s3_key=s3_key,
            filename=req.filename,
            content_type=req.content_type,
            status="PENDING_UPLOAD",
        )

        print(f"{upload_url=}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate upload URL: {e}"
        )

    return FileUploadResponse(doc_id=document_id, s3_key=s3_key, upload_url=upload_url)
