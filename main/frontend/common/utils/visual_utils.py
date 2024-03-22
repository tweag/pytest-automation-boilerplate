"""Utility to compare images using Pillow
"""
from collections import namedtuple
from pathlib import Path

from PIL import Image, ImageChops


class FileFormatMismatchError(Exception):
    pass


class ImageSizeMismatchError(Exception):
    pass


def read_image(img_pth: Path, color_mode: str = "RGB") -> Image:
    """Read Image File

    Args:
        img_pth: Path - Absolute Path of Image File to be read
        color_mode: str - Either "L" or "RGB". Color Conversion mode for diffing.

    Returns:
        Image Object
    """
    with Image.open(img_pth) as f:
        img = f.convert(color_mode)
    return img


def file_paths(image_name_with_ext: str):
    """Function to return a collection of file paths - base, test and diff

    Args:
        image_name_with_ext: str - Image File Name to test. Not the absolute path.

    Returns:
        screenshot_paths - namedtuple object containing base, test and diff image absolute paths.
    """
    screenshot_paths = namedtuple("screenshot_paths", "base test diff")
    return screenshot_paths(
        Path(Path.cwd() / "test_data" / "visualtesting" / "base" / f"{image_name_with_ext}").resolve(),
        Path(Path.cwd() / "test_data" / "visualtesting" / "test" / f"{image_name_with_ext}").resolve(),
        Path(Path.cwd() / "output" / "visualtesting" / "diff" / f"{image_name_with_ext}").resolve(),
    )


def raise_for_missing_file(file_path: Path, exc_msg: str):
    """Checks if a path provided is a file

    Args:
        exc_msg: error message
        file_path: Path

    Raises:
        FileNotFoundError
    """
    if not file_path.is_file():
        raise FileNotFoundError(exc_msg)


def raise_for_missing_images(bse_img_pth: Path, tst_img_pth: Path):
    """Raise Exception for files not found at provided path

    Args:
        bse_img_pth: Path - Absolute Path of Base Image
        tst_img_pth: Path - Absolute Path of Test Image

    Raises:
        FileNotFoundError
    """
    raise_for_missing_file(
        bse_img_pth, f"No Base Image found at location {bse_img_pth}"
    )
    raise_for_missing_file(
        tst_img_pth, f"No Test Image found at location {tst_img_pth}"
    )


def raise_for_format_mismatch(bse_img: Image, tst_img: Image):
    """Raise Exception for files not found at provided path

    Args:
        bse_img: Image
        tst_img: Image

    Raises:
        FileFormatMismatchError - In case base image and test image have different file formats like PNG vs JPEG, etc.
    """
    if (bse_img_frmt := bse_img.format) != (tst_img_frmt := tst_img.format):
        raise FileFormatMismatchError(
            f"Cannot compare images with different format."
            f" Base Image ({bse_img_frmt}) & Test Image ({tst_img_frmt}) have different formats."
        )


def raise_for_size_mismatch(bse_img: Image, tst_img: Image):
    """Raise Exception for files not found at provided path

    Args:
        bse_img: Image
        tst_img: Image

    Raises:
        ImageSizeMismatchError - In case base image and test image have different size/resolution.
    """
    if (bse_img_size := bse_img.size) != (tst_img_size := tst_img.size):
        raise ImageSizeMismatchError(
            f"Cannot compare images with different sizes. "
            f"Base Image ({bse_img_size}) & Test Image ({tst_img_size}) have different sizes."
        )


def _diff_img(bse_img: Image, tst_img: Image) -> Image:
    """Function to return diff image based on comparing base and test images.

    Args:
        bse_img: Image
        tst_img: Image

    Returns: Image | None
        Image - If there is a difference
        None - If base and test images are same.
    """
    diff_img = ImageChops.difference(bse_img, tst_img)

    # parameter to know if there is a difference - getbbox() is None implies no change in base vs test.
    is_same = diff_img.getbbox() is None

    if not is_same:
        return diff_img
    return None


def are_images_same(image_name_with_ext: str, color_mode: str = "RGB") -> bool:
    """Compares Images using Pillow library and returns boolean value indicating if the images are same.

    Args:
        image_name_with_ext: str - File Name of Image to Compare
        color_mode: str - Could be either of RGB or L (B&W). Defaulted to RGB.
            Color Conversion mode for comparison

    Returns:
        True - if base image and test image has no difference in them
        False - if base image and test image has difference.
    """
    base_img_pth, tst_img_pth, diff_img_pth = file_paths(image_name_with_ext)
    raise_for_missing_images(base_img_pth, tst_img_pth)
    # Read Base Image & Test Image.
    base_img = read_image(base_img_pth, color_mode=color_mode)
    test_img = read_image(tst_img_pth, color_mode=color_mode)
    raise_for_format_mismatch(base_img, test_img)
    raise_for_size_mismatch(base_img, test_img)
    diff_img = _diff_img(base_img, test_img)
    if diff_img:
        diff_img.save(diff_img_pth)
        return False
    return True
