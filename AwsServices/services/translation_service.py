import boto3


class TranslationService:
    def __init__(self):
        self.client = boto3.client('translate', aws_access_key_id='AKIA4MTWGWVBKGMRIBZA',
                                   aws_secret_access_key='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')

    def translate_text(self, text, source_language='auto', target_language='en'):
        """
        It is translating the text from the source language to the target language
        Using Boto3
        Using translate_text method of translate (boto3) client
        passing text, lanhuage, and target language
        """

        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )

        # taking in the response and returning the translatedText, sourceLanguage and targetLanguage
        translation = {
            'translatedText': response['TranslatedText'],
            'sourceLanguage': response['SourceLanguageCode'],
            'targetLanguage': response['TargetLanguageCode']
        }

        return translation
