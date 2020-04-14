import json
import tempfile

from cortex.utils.storage_util import storage_dir
import matplotlib.pyplot as plt
import numpy as np


class DepthImageParser:
    field = 'depth_image'
    temp_dir = tempfile.mkdtemp(dir=storage_dir)

    def parse(self, depth_image):
        fd, path = tempfile.mkstemp(dir=self.temp_dir, suffix='.png')
        with open(depth_image['path'], 'r') as content_file:
            content = json.loads(content_file.read())
            data = np.reshape(content, (-1, depth_image['width']))
            # print(data)
            # plt.imshow(data,
            #            cmap='hot', interpolation='nearest')
            plt.imsave(path, data, cmap='hot')
        return path