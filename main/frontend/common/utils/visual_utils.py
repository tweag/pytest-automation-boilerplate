
from collections import namedtuple
from pathlib import Path

from PIL import Image, ImageChops


class FileFormatMismatchError(Exception):
    pass


class ImageSizeMismatchError(Exception):
    pass


def read_image(img_pth: Path, color_mode: str = "RGB") -> Image:
    with Image.open(img_pth) as f:
        img = f.convert(color_mode)
    return img


def file_paths(image_name_with_ext: str):
    screenshot_paths = namedtuple("screenshot_paths", "base test diff")
    return screenshot_paths(
        Path(Path.cwd() / "test_data" / "visualtesting" / "base" / f"{image_name_with_ext}").resolve(),
        Path(Path.cwd() / "test_data" / "visualtesting" / "test" / f"{image_name_with_ext}").resolve(),
        Path(Path.cwd() / "output" / "visualtesting" / "diff" / f"{image_name_with_ext}").resolve(),
    )


def raise_for_missing_file(file_path: Path, exc_msg: str):
    if not file_path.is_file():
        raise FileNotFoundError(exc_msg)


def raise_for_missing_images(bse_img_pth: Path, tst_img_pth: Path):
    raise_for_missing_file(
        bse_img_pth, f"No Base Image found at location {bse_img_pth}"
    )
    raise_for_missing_file(
        tst_img_pth, f"No Test Image found at location {tst_img_pth}"
    )


def raise_for_format_mismatch(bse_img: Image, tst_img: Image):
    if (bse_img_frmt := bse_img.format) != (tst_img_frmt := tst_img.format):
        raise FileFormatMismatchError(
            f"Cannot compare images with different format."
            f" Base Image ({bse_img_frmt}) & Test Image ({tst_img_frmt}) have different formats."
        )


def raise_for_size_mismatch(bse_img: Image, tst_img: Image):
    if (bse_img_size := bse_img.size) != (tst_img_size := tst_img.size):
        raise ImageSizeMismatchError(
            f"Cannot compare images with different sizes. "
            f"Base Image ({bse_img_size}) & Test Image ({tst_img_size}) have different sizes."
        )


def _diff_img(bse_img: Image, tst_img: Image) -> Image:
    diff_img = ImageChops.difference(bse_img, tst_img)

    # parameter to know if there is a difference - getbbox() is None implies no change in base vs test.
    is_same = diff_img.getbbox() is None

    if not is_same:
        return diff_img
    return None


def are_images_same(image_name_with_ext: str, color_mode: str = "RGB") -> bool:
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
