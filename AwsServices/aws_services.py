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

    def translate_text(self, text, source_language, target_language):
        return self.translation.translate_text(text, source_language, target_language)
    
    def upload_file(self, file_bytes, file_name):
        return self.storage_service.upload_file(file_bytes, file_name)
    
    def audio(self, text):
        return self.voice_over.voice_over(text)