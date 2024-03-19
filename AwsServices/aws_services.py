from services.storage_service import StorageService
from services.translation_service import TranslationService
from services.voice_over import VoiceOver

class AWSServices:
    def __init__(self):
        self.bucket_name = 'telecord-storage'
        self.storage_service = StorageService(self.bucket_name)
        if(not self.storage_service.bucket_exists(self.bucket_name)):
            print('Bucket does not exist, creating a new one')
            self.storage_service.create_bucket(self.bucket_name)
            print("Bucket created successfully")
        else:
            print("Bucket already exists")

        self.translation = TranslationService()
        self.voice_over = VoiceOver()