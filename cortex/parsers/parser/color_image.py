from PIL import Image as PIL


class ColorImageParser:
    field = 'colorImage'

    def parse(self, color_image):
        return 'color_parser'
        # path = context.path('color_image.jpg')
        # size = snapshot.color_image.width, snapshot.color_image.height
        # image = PIL.new('RGB', size)
        # image.putdata(snapshot.color_image.data)
        # image.save(path)
