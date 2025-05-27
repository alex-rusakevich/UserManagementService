from types_aiobotocore_ses import SESClient
from app.app_layer.errors.exceptions.services_exceptions import SESException
from app.app_layer.errors.strings import SES_SEND, SES_VERIFY
from app.config import AwsConfig


class SESService:
    def __init__(self, client, config: AwsConfig):
        self.client: SESClient = client("ses")
        self.sender_email = config.aws_sender_email

    async def verify_email(self):
        try:
            async with self.client as client:
                await client.verify_email_identity(EmailAddress=self.sender_email)
        except Exception:
            raise SESException(SES_VERIFY)

    async def send_email(self, recipient: str, msg: str):
        try:
            async with self.client as client:
                await client.send_email(
                    Source=self.sender_email,
                    Destination={"ToAddresses": [recipient]},
                    Message={
                        "Subject": {"Data": "ACME User Management Service"},
                        "Body": {"Text": {"Data": msg}},
                    },
                )
        except Exception:
            raise SESException(SES_SEND)
