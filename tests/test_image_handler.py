from src.image_processing.image_handler import ImageHandler

def test_load_image():
    handler = ImageHandler()
    image = handler.load_image("test_image.jpg")
    assert image is not None

def test_get_tile():
    handler = ImageHandler()
    image = handler.load_image("test_image.jpg")
    tile = handler.get_tile(image, (0, 0))
    assert tile is not None