import base64
from binascii import Error as BinASCIIError

from django.core.files.base import ContentFile

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ImageField


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        """
        It checks for the type of the data and either decodes it from
        base64 or directly saves the file.
        """

        data_name = data['name']
        data_content = data['content']
        if isinstance(data_content, str):
            try:
                decoded_file = base64.b64decode(data_content)
            except BinASCIIError:
                raise ValidationError('Corrupted file data, please try again.')
            data_content = ContentFile(decoded_file, name=f'{data_name}')
        else:
            raise ValidationError(
                '%(value)s is not a valid file format' % type(data_content),
                code='invalid',
            )
        return super().to_internal_value(data_content)
