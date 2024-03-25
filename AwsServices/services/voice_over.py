import boto3


class VoiceOver(object):
    """
    This class is used to convert text to speech using AWS Polly
    """

    def __init__(self):
        self.client = boto3.client('polly', aws_access_key_id='AKIA4MTWGWVBKGMRIBZA',
                                   aws_secret_access_key='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')

    def voice_over(self, text, voice_id='Joanna', output_format='mp3'):
        """
        It is converting the text to speech using AWS Polly
        :param text:
        :param voice_id:
        :param output_format:
        :return:
        """
        response = self.client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id
        )
        audio_stream = response['AudioStream'].read()
        return audio_stream
