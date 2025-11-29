from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class GeneraicAPIResponse(BaseModel):
    status_code: List[int] = Field(example=[200, 400, 404])
    message: str = Field(example="File uploaded successfully")


class FileUploadRequest(BaseModel):
    user_id: str = Field(example="user_123")
    filename: str = Field(example="invoice.pdf")
    content_type: str = Field(example="application/pdf")


class FileUploadResponse(BaseModel):
    doc_id: str = Field(example="doc_123")
    upload_url: str = Field(example="https://s3.amazonaws.com/...")
    s3_key: str = Field(example="user_123/doc_123/invoice.pdf")
