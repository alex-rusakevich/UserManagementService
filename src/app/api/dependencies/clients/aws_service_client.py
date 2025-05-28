from app.infra.database_conntection import get_aws_client
from app.infra.services.s3 import S3Service
from app.infra.services.ses import SESService
from app.config import get_settings


def get_s3_client_service() -> S3Service:
    s3_client = S3Service(get_aws_client, config=get_settings().aws)
    return s3_client


def get_ses_client_service() -> SESService:
    ses_client = SESService(get_aws_client, config=get_settings().aws)
    return ses_client
