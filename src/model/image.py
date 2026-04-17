import base64
import uuid
from bson import Regex
from pathlib import Path
from src.common.database import Database
from PIL import Image as PImage
from io import BytesIO

__author__ = 'smok'

MAX_IMAGE_SIZE = 200

#TODO: this is image class for Mongo only, doesn't work with SQLite
class Image(object):

    def __init__(self, user_id, image, _id=None):
        self.user_id = user_id
        self.image_filename = image.filename
        self.image_data = image.read()
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "id": self._id,
            "userId": self.user_id,
            "imageFilename": self.image_filename
        }

    def save_user_image(self):
        fs = Database.get_db_fs()
        stored = fs.put(self.image_data, filename=self.image_filename, user_id=self.user_id, _id=self._id)
        print('image saved under id: '+stored)

    @staticmethod
    def get_file_by_name(filename):
        fs = Database.get_db_fs()
        for f in fs.find({'filename': Regex(filename)}):  # {'filename': Regex(r'.*\.(png|jpg)')} - all images
            image_data = f.read()
            print(image_data)

    @staticmethod
    def delete_file_by_name(filename):
        fs = Database.get_db_fs()
        files = fs.find({'filename': Regex(filename)})
        for f in files:
            fs.delete(f._id)

    @staticmethod
    def delete_file_by_id(_id):
        fs = Database.get_db_fs()
        fs.delete(_id)

    @staticmethod
    def get_user_image(user_id):
        fs = Database.get_db_fs()
        image_data = fs.find_one({'user_id': user_id})
        if image_data is not None:
            return image_data  # Image.fit_image_to_frame(image_data)
        else:
            return None

    @staticmethod
    def replace_user_image(user_id, image):
        fs = Database.get_db_fs()
        image_data = fs.find_one({'user_id': user_id})
        image_filename = image_data.filename
        Image.delete_file_by_id(image_data._id)
        stored = fs.put(image, filename=image_filename, user_id=user_id, _id=uuid.uuid4().hex)
        print('image replaced, new id: ' + stored)

    @staticmethod
    def delete_user_image(user_id):
        fs = Database.get_db_fs()
        image_data = fs.find_one({'user_id': user_id})
        Image.delete_file_by_id(image_data._id)
        print('user image removed')

    @staticmethod
    def get_user_image_uri(user_id):
        image_uri = None
        fs = Database.get_db_fs()
        image_data = fs.find_one({'user_id': user_id})
        if image_data is not None:
            fitted_image = Image.fit_image_to_frame(image_data)
            if fitted_image is not None:
                ext = Path(image_data.filename).suffix
                image_uri = "data:image/%s;base64,%s" % (ext, base64.b64encode(fitted_image).decode('utf-8').replace('\n', ''))

        return image_uri

    @staticmethod
    def get_original_image_uri(user_id):
        image_uri = None
        fs = Database.get_db_fs()
        image_data = fs.find_one({'user_id': user_id})
        if image_data is not None:
            ext = Path(image_data.filename).suffix
            image_uri = "data:image/%s;base64,%s" % (ext, base64.b64encode(image_data.read()).decode('utf-8').replace('\n', ''))

        return image_uri

    @staticmethod
    def fit_image_to_frame(image_data):
        img = PImage.open(BytesIO(image_data.read()))
        width, height = img.size
        if width > MAX_IMAGE_SIZE and height > MAX_IMAGE_SIZE:
            if width > height:
                height = int((MAX_IMAGE_SIZE / width) * height)
                width = MAX_IMAGE_SIZE
            else:
                width = int((MAX_IMAGE_SIZE / height) * width)
                height = MAX_IMAGE_SIZE

        new_img = img.resize((width, height))
        img_byte_array = BytesIO()
        new_img.save(img_byte_array, format='png')
        return img_byte_array.getvalue()

    @staticmethod
    def rotate_image(image, direction):
        img = PImage.open(BytesIO(image))
        radius = None
        if direction == 'R':
            radius = 270
        elif direction == 'L':
            radius = 90

        if radius is not None:
            new_img = img.rotate(radius)
            img_byte_array = BytesIO()
            new_img.save(img_byte_array, format='png')
            return img_byte_array.getvalue()

        return None
