from typing import cast
from types_aiobotocore_s3 import S3Client
from types_aiobotocore_s3.literals import BucketLocationConstraintType
from app.config import AwsConfig


class S3Service:
    def __init__(self, client, config: AwsConfig):
        self.client: S3Client = client("s3")
        self.bucket_name = config.aws_bucket_name
        self.region = config.aws_region

    async def service_list_buckets(self):
        async with self.client as client:
            response = await client.list_buckets()
            buckets = response["Buckets"]

            for bucket in buckets:
                bucket_name = bucket["name"]  # type: ignore[typeddict-item]
                print(bucket_name)

    async def service_create_bucket(self):
        location_constraint = cast(BucketLocationConstraintType, self.region)

        async with self.client as client:
            await client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={"LocationConstraint": location_constraint},
            )

    async def upload_file(self, file: bytes, key: str):
        async with self.client as client:
            await client.put_object(Bucket=self.bucket_name, Body=file, Key=key)

    async def get_file(self, key: str):
        async with self.client as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=key)
            return await response["Body"].read()

    async def delete_file(self, key: str):
        async with self.client as client:
            await client.delete_object(Bucket=self.bucket_name, Key=key)
