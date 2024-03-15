import boto3


class RecognitionService:
    def __init__(self, storage_service):
        self.client = boto3.client('rekognition')
        self.bucket_name = storage_service.get_storage_location()

    def detect_text(self, file_name):
        """
        It is detecting the text from the image using boto3 and saving the response in the lines array
        """

        response = self.client.detect_text(
            # using the detect_text method from boto3 and passing the file_name to detecting the text
            Image={
                'S3Object': {
                    'Bucket': self.bucket_name,
                    'Name': file_name
                }
            }
        )

        lines = []
        for detection in response['TextDetections']:
            # checking if it is a line then appending it on the lines array, saving confidence and boundingBox as well
            if detection['Type'] == 'LINE':
                lines.append({
                    # only taking the text from the response not using confidence
                    'text': detection['DetectedText'],
                })

        return lines