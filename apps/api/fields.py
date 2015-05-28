from rest_framework import serializers
from time import mktime
from arrow.arrow import Arrow
import dateutil.parser


class StdImageField(serializers.ImageField):
    def __init__(self, *args, **kwargs):
        super(StdImageField, self).__init__(*args, **kwargs)
        self.variation_names = []
        self.include_attributes = ['width', 'height', 'url', 'size']

    def set_variation_names(self, stdimage):
        """
        Get all available variations from stdimagefield
        Ex: ['large', 'thumbnail']
        """
        self.variation_names = stdimage.field.variations.keys()

    def extract_image_files(self, stdimage):
        """
        Extract image file objects according to variations available
        """

        # Initialize image dict
        images = {}

        # Check all available variations in the object
        for variation in self.variation_names:
            # Check if variation is inside the object
            if hasattr(stdimage, variation):
                images[variation] = getattr(stdimage, variation)
        return images

    def serialize_image(self, image):
        """
        Serialize single image file
        """

        # Initialize image dict
        serialized_image = {}

        # We need to only check for specific attributes to include
        for attr in self.include_attributes:
            if hasattr(image, attr):
                serialized_image[attr] = getattr(image, attr)
        return serialized_image

    def serialize_images(self, images):
        """
        Serialize all available variations inside the image files
        """

        # Initialize images dict
        serialized_images = {}

        # Add all variations to the images dict
        for variation, image in images.iteritems():
            serialized_images[variation] = self.serialize_image(image)
        return serialized_images

    def get_variations(self, stdimage):
        """
        Performs image extraction and serialization from stdimage object
        """

        # Set all available variation names
        self.set_variation_names(stdimage)

        # Extract image files from stdimage object
        images = self.extract_image_files(stdimage)

        return self.serialize_images(images)

    def to_representation(self, value):
        variations = self.get_variations(value)
        return variations

    def to_internal_value(self, data):
        return super(StdImageField, self).to_internal_value(data)


class EpochTimeReadOnlyField(serializers.ReadOnlyField):

    def to_representation(self, value):
        epoch_utc = int(mktime(value.timetuple()))
        return epoch_utc
