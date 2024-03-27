import boto3
from chalice import Response


class VoiceOver(object):
    """
    This class is used to convert text to speech using AWS Polly
    """

    def __init__(self, aws_access_key, aws_secret_access_key):
        self.client = boto3.client('polly', aws_access_key_id=aws_access_key,
                                   aws_secret_access_key=aws_secret_access_key)

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
        return Response(body=audio_stream, headers={'Content-Type': 'audio/mpeg'},
                        status_code=200)
