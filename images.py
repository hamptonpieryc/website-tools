from PIL import Image, ImageDraw, ImageFilter


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_best_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def crop_best_letterbox(pil_img):
    return crop_center(pil_img, min(pil_img.size) * 3, min(pil_img.size))


# def crop_best_letterbox(pil_img):
#     pil_img.size
#     return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


thumb_width = 300
crop_best_square(Image.open('content/images/kayak.png')) \
    .resize((thumb_width, thumb_width), Image.LANCZOS) \
    .save('kayak-square.png', quality=95)

crop_best_square(Image.open('content/images/discover-sailing.png')) \
    .resize((thumb_width, thumb_width), Image.LANCZOS) \
    .save('discover-sailing-square.png', quality=95)

crop_best_square(Image.open('content/images/pubquiz.jpeg')) \
    .resize((thumb_width, thumb_width), Image.LANCZOS) \
    .save('pubquiz-square.jpeg', quality=95)
