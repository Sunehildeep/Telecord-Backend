import boto3
from chalice import Response


class TranslationService:
    def __init__(self, aws_access_key, aws_secret_access_key):
        self.client = boto3.client('translate', aws_access_key_id=aws_access_key,
                                   aws_secret_access_key=aws_secret_access_key)

    def translate_text(self, chats, source_language='auto', target_language='en'):
        """
        It is translating the text from the source language to the target language
        Using Boto3
        Using translate_text method of translate (boto3) client
        passing text, lanhuage, and target language
        """
        translatedChats = []
        for chat in chats:
            response = self.client.translate_text(
                Text=chat["Message"],
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language
            )

            if 'TranslatedText' not in response:
                return Response(body={'error': 'Translation failed'}, status_code=400)

            # taking in the response and returning the translatedText, sourceLanguage and targetLanguage
            translation = {
                'translatedText': response['TranslatedText'],
                'sourceLanguage': response['SourceLanguageCode'],
                'targetLanguage': response['TargetLanguageCode']
            }

            # Copy chat and update the message with the translated text
            translatedChat = chat.copy()
            translatedChat['Message'] = translation['translatedText']

            # Append the translated chat to the list of translated chats
            translatedChats.append(translatedChat)

        return Response(body=translatedChats, status_code=200)
