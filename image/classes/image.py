from django.conf import settings
from pathlib import Path
import cv2
import os


class Image:
    def __init__(self,  django_path, media_root=settings.MEDIA_ROOT) -> None:

        # django path
        self.django_path = str(django_path)
        self.media_root = media_root

        self.source_image_path = self.get_full_path()
        self.source_image_path_obj = Path(self.source_image_path)
        self.source_image_name = self.source_image_path_obj.name
        self.source_image_ext = self.source_image_path_obj.suffix
        self.target_image_name = self.source_image_name.replace(
            self.source_image_ext, '_sketch'+self.source_image_ext)
        self.target_image_path = self.source_image_path.replace(
            self.source_image_name, self.target_image_name)

        # helper path
        self.target_url_path = os.path.join(
            settings.API_MEDIA_ROOT_URL, self.target_image_path)

    def convert_image2sketch(self):

        # read image
        img = cv2.imread(self.source_image_path)

        # turn image to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        invert = cv2.bitwise_not(gray)

        # blur
        blur_img = cv2.GaussianBlur(invert, (7, 7), 0)
        invert_blur = cv2.bitwise_not(blur_img)
        sketch_img = cv2.divide(gray, invert_blur, scale=256.0)

        # save image
        cv2.imwrite(self.target_image_path, sketch_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return self.target_url_path

# ===================================
# Get full path for source file
# ===================================
    def get_full_path(self) -> str:
        if os.name == 'nt':
            return os.path.join(self.media_root, self.django_path).replace('/', '\\')
