from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random, string

class Meme:
    def __init__(self, images, texts):
        self.images = images
        self.texts = texts

    def compose_images(self, template_number):
        '''
        :param template_number:
        1 - horizontal
        2 - vertical
        3 - grid (for 4 more paired images)
        :return:
        return an composed image
        '''
        if template_number == 1:
            '''
            horizontal composing
            '''
            return self.crop_images(1)

        if template_number == 2:
            pass

    def crop_images(self, crop_type):
        sizes = []
        new_size = 0
        padding = 0
        last_size = 0
        if crop_type == 1:
            for image in self.images:
                print(image)
                sizes.append(self.__get_size(image)[1])
                new_size += self.__get_size(image)[0]
            sizes.sort()
            min_height = sizes[0]
            self.im = Image.new("RGBA", (new_size, min_height))
            for image in self.images:
                appended_image = Image.open(image)
                x, y = appended_image.size
                x = (x / (y/min_height)).__int__()
                y = min_height
                last_size += x
                appended_image = appended_image.resize((x, y))
                index = self.images.index(image)
                '''
                add text for appended image
                '''
                appended_image = self.add_text(appended_image, self.texts[index], x, y, "down")
                self.im.paste(appended_image, (padding, 0))
                padding += x

            self.im = self.im.crop((0, 0, last_size, min_height))
            name = self.__save_image()
            return name

    def add_text(self, image, text, x, y, position):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("impact.ttf", 40)
        if position == "down":
            x = (x/2).__int__()
            y = y - 50
        elif position == "top":
            x = (x / 2).__int__()
            y = 10
        w, h = draw.textsize(text, font=font)
        print(w)

        # thin border
        draw.text((x-w/2 - 1, y), text, font=font, fill=(0, 0, 0))
        draw.text((x-w/2 + 1, y), text, font=font, fill=(0, 0, 0))
        draw.text((x-w/2, y - 1), text, font=font, fill=(0, 0, 0))
        draw.text((x-w/2, y + 1), text, font=font, fill=(0, 0, 0))

        # thicker border
        draw.text((x-w/2 - 1, y - 1), text, font=font, fill=(0, 0, 0))
        draw.text((x-w/2 + 1, y - 1), text, font=font, fill=(0, 0, 0))
        draw.text((x-w/2 - 1, y + 1), text, font=font, fill=(0, 0, 0))
        draw.text((x-w/2 + 1, y + 1), text, font=font, fill=(0, 0, 0))

        draw.text((x-w/2, y), text, (255, 255, 255), font=font)

        return image

    def __save_image(self):
        name = self.generate_name()
        self.im.save(name)
        return name

    def generate_name(self):
        chars = ''.join(random.sample(string.ascii_lowercase, 20))
        name = f"{chars}.png"
        return name

    def __get_size(self, image):
        im = Image.open(image)
        return im.size

if __name__ == '__main__':
    i1 = Meme(('data/1.jpg', 'data/2.jpg'), ("Meme", "Maker 1.0"))
    im_name = i1.compose_images(1)
    im = Image.open(im_name)
    im.show()