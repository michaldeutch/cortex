import base64
import tempfile

from PIL import Image as PIL
from cortex.utils.storage import storage_dir


class ColorImageParser:
    field = 'color_image'
    temp_dir = tempfile.mkdtemp(dir=storage_dir)

    def parse(self, color_image):
        fd, path = tempfile.mkstemp(dir=self.temp_dir, suffix='.jpg')
        size = color_image['width'], color_image['height']
        image = PIL.new('RGB', size)
        with open(color_image['path'], 'r') as content_file:
            content = content_file.read()
            data = base64.b64decode(content)
            image.putdata([(R, G, B) for R, G, B in zip(*[iter(data)] * 3)])
            image.save(path)
        return path
