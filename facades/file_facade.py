import os

from fastapi import UploadFile, HTTPException, status
from aiobotocore.session import get_session
from dotenv import load_dotenv

load_dotenv()


class FileManager:
    def __init__(self):
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key_id = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.endpoint_url = os.getenv('ENDPOINT_URL')
        self.region_name = os.getenv('REGION_NAME')

    async def save_file(self, file: UploadFile, file_path: str):
        session = get_session()
        async with session.create_client(
            's3',
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_key_id
        ) as client:
            try:
                data = await file.read()
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=file_path,
                    Body=data
                )
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Cannot save file(')


FILE_MANAGER = FileManager()
