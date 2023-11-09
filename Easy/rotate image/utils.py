import utils
from skimage.data import astronaut


def test_rotated_image():
    '''test'''

    image = astronaut()[300:,:]
    result = utils.rotated_image(image)
    assert result.shape == image.shape
