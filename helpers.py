from PIL import Image, ImageFont, ImageDraw
import random, string


def generate_name():
    chars = ''.join(random.sample(string.ascii_lowercase, 20))
    name = f"{chars}.png"
    return name


def draw_text_on_image(image, text, x, y):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("impact.ttf", 40)
    w = draw.textlength(text, font=font)

    draw_text_outline(draw, font, text, (x-w/2), y)
    draw.text((x - w / 2, y), text, (255, 255, 255), font=font)
    return image


def draw_text_outline(draw, font, text, x, y):
    for delta_x in range(-1, 2, 2):
        for delta_y in range(-1, 2, 2):
            draw.text((x - delta_x, y - delta_y), text, font=font, fill=(0, 0, 0))


def get_size(image):
    return Image.open(image).size


def save_image(image):
    title = generate_name()
    image.save(f"./results/{title}")
    return title
