import os
from pathlib import Path

import pytest
from cortex.parsers.parsers.color_image import ColorImageParser
from cortex.parsers.parsers.depth_image import DepthImageParser


def test_rgrs_color_image(input_dir, expected_output_dir):
    color_image = {
        'width': 1920,
        'height': 1080,
        'path': f'{input_dir}/color_data'
    }
    parser = ColorImageParser()
    image = parser.parse(color_image)
    assert image.endswith('.jpg')
    assert_equal_pictures(f'{expected_output_dir}/color_image.jpg', image)
    os.remove(image)


def test_rgrs_depth_image(input_dir, expected_output_dir):
    depth_image = {
        'width': 224,
        'height': 172,
        'path': f'{input_dir}/depth_data'
    }
    parser = DepthImageParser()
    image = parser.parse(depth_image)
    assert image.endswith('.png')
    assert_equal_pictures(f'{expected_output_dir}/depth_image.png', image)
    os.remove(image)


def assert_equal_pictures(expected, found):
    with open(expected, "rb") as expected_fd:
        with open(found, "rb") as found_fd:
            assert expected_fd.read() == found_fd.read()


@pytest.fixture
def input_dir(parent_dir):
    return parent_dir.joinpath('input')


@pytest.fixture
def expected_output_dir(parent_dir):
    return parent_dir.joinpath('expected_output')


@pytest.fixture
def parent_dir():
    return Path(__file__).parent

