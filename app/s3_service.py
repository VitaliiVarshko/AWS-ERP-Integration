import boto3

BUCKET_NAME = "erp-integration-documents-2026-vv"

s3_client = boto3.client("s3")


def upload_document(
    content: str,
    object_key: str
):
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=object_key,
        Body=content.encode("utf-8"),
        ContentType="application/json"
    )
