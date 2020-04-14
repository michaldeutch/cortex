import base64
import tempfile
from concurrent.futures.thread import ThreadPoolExecutor

from PIL import Image as PIL
from cortex.utils.storage_util import storage_dir

NUM_THREADS = 5


class ColorImageParser:
    field = 'color_image'
    temp_dir = tempfile.mkdtemp(dir=storage_dir)
    executor = ThreadPoolExecutor(NUM_THREADS)

    def parse(self, color_image):
        fd, path = tempfile.mkstemp(dir=self.temp_dir, suffix='.jpg')
        size = color_image['width'], color_image['height']
        image = PIL.new('RGB', size)
        old_path = color_image['path']
        self.executor.submit(self.create_image, old_path, path, image)
        return path

    @staticmethod
    def create_image(old_path, new_path, image):
        with open(old_path, 'r') as content_file:
            content = content_file.read()
            data = base64.b64decode(content)
            image.putdata([(R, G, B) for R, G, B in zip(*[iter(data)] * 3)])
            image.save(new_path)
