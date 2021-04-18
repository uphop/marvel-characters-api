import os
from dotenv import load_dotenv
import boto3
import logging

load_dotenv()
logger = logging.getLogger(__name__)

'''
Wrapper for AWS Translate API.
'''
class AwsTranslateApiClient:
    def __init__(self):
        self.aws_region = os.environ.get('AWS_REGION', 'eu-west-1')

    '''
    Translates text between source / target languages.
    '''
    def translate(self, source_language_code, target_language_code, text):
        logger.debug(f'Translating text: {text}')
 
        translate = boto3.client(service_name='translate', region_name=self.aws_region, use_ssl=True)
        result = translate.translate_text(
            Text=text, 
            SourceLanguageCode=source_language_code, 
            TargetLanguageCode=target_language_code)
        
        return result.get('TranslatedText', '')
   