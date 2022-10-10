from PIL import Image, ImageFont, ImageDraw
import random, string

class Meme:
    def __init__(self, images, texts):
        self.images = images
        self.texts = texts
        self.cropped_images = []
        self.images_w_text = []
        self.result_image = None

    def compose_images(self, template_type="single", position="up"):
        '''
        :param template_number:
        0 - single image
        1 - horizontal
        2 - vertical
        3 - grid (for 4 more paired images)
        :return:
        return an composed image
        '''
        self.resize_images(template_type)
        for index, image in enumerate(self.cropped_images):
            self.__add_text(image, self.texts[index], position=position)

        template_number = len(self.images)
        if template_number == 1:
            self.result_image = self.images_w_text[0]
            return self.__save_image()

        if template_number == 2:
            w, h = 0, 0
            w_sum, h_sum = 0, 0
            delta = 0
            for image in self.images_w_text:
                w, h = image.size
                w_sum += w
                h_sum += h
            if template_type == "horizontal":
                self.result_image = Image.new("RGBA", (w_sum, h))
                for image in self.images_w_text:
                    self.result_image.paste(image, (delta, 0))
                    delta += image.size[0]
                return self.__save_image()
            elif template_type == "vertical":
                self.result_image = Image.new("RGBA", (w, h_sum))
                for image in self.images_w_text:
                    self.result_image.paste(image, (0, delta))
                    delta += image.size[1]
                return self.__save_image()

        if template_number == 3:
            pass

    def resize_images(self, composition_type):
        sizes = []
        if composition_type == "single":
            resized_image = Image.open(self.images[0])
            self.cropped_images.append(resized_image)
        elif composition_type == "horizontal":
            for image in self.images:
                sizes.append(self.__get_size(image)[1])
            sizes.sort()
            min_height = sizes[0]
            for image in self.images:
                resized_image = Image.open(image)
                x, y = resized_image.size
                x = (x / (y / min_height)).__int__()
                y = min_height
                resized_image = resized_image.resize((x, y))
                self.cropped_images.append(resized_image)
        elif composition_type == "vertical":
            for image in self.images:
                sizes.append(self.__get_size(image)[0])
            sizes.sort()
            min_width = sizes[0]
            for image in self.images:
                resized_image = Image.open(image)
                x, y = resized_image.size
                x = min_width
                y = (y / (x/min_width)).__int__()
                resized_image = resized_image.resize((x, y))
                self.cropped_images.append(resized_image)
        elif composition_type == "grid":
            return None

    def __add_text(self, image, text, position):
        x, y = image.size

        if position == "down":
            x = (x/2).__int__()
            y = y - 50
        elif position == "up":
            x = (x / 2).__int__()
            y = 10
        elif position == "middle":
            x = (x / 2).__int__()
            y = (y / 2 - 25).__int__()

        self.__draw_text_on_image(image, text, x, y)

    def __draw_text_on_image(self, image, text, x, y):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("impact.ttf", 40)
        w, h = draw.textsize(text, font=font)
        # border
        draw.text((x - w / 2 - 1, y - 1), text, font=font, fill=(0, 0, 0))
        draw.text((x - w / 2 + 1, y - 1), text, font=font, fill=(0, 0, 0))
        draw.text((x - w / 2 - 1, y + 1), text, font=font, fill=(0, 0, 0))
        draw.text((x - w / 2 + 1, y + 1), text, font=font, fill=(0, 0, 0))

        # entire text
        draw.text((x - w / 2, y), text, (255, 255, 255), font=font)

        self.images_w_text.append(image)

    def __save_image(self):
        title = self.generate_name()
        self.result_image.save(f"./results/{title}")
        return title

    def generate_name(self):
        chars = ''.join(random.sample(string.ascii_lowercase, 20))
        name = f"{chars}.png"
        return name

    def __get_size(self, image):
        im = Image.open(image)
        return im.size

if __name__ == '__main__':
    i1 = Meme(('data/1.jpg', 'data/2.jpg'), ("Meme", "Maker 1.0"))
    #i1 = Meme(('data/1.jpg', ), ("Meme", ))
    im_name = i1.compose_images("vertical", position="middle")
    im = Image.open(f"./results/{im_name}")
    im.show()