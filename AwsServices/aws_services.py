from services.storage_service import StorageService
from services.translation_service import TranslationService
from services.voice_over import VoiceOver
import dotenv
import os

dotenv.load_dotenv()

aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

class AWSServices:
    def __init__(self):
        self.bucket_name = 'telecord-storage'
        self.storage_service = StorageService(self.bucket_name, aws_access_key, aws_secret_access_key)
        if(not self.storage_service.bucket_exists(self.bucket_name)):
            print('Bucket does not exist, creating a new one')
            self.storage_service.create_bucket(self.bucket_name)
            print("Bucket created successfully")
        else:
            print("Bucket already exists")

        self.translation = TranslationService(aws_access_key, aws_secret_access_key)
        self.voice_over = VoiceOver(aws_access_key, aws_secret_access_key)

    def translate_text(self, text, source_language, target_language):
        return self.translation.translate_text(text, source_language, target_language)
    
    def upload_file(self, file_bytes, file_name):
        return self.storage_service.upload_file(file_bytes, file_name)
    
    def audio(self, text):
        return self.voice_over.voice_over(text)