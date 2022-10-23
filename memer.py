from PIL import Image
import helpers


class Meme:
    def __init__(self, images, texts):
        self.images = images
        self.texts = texts
        self.cropped_images = []
        self.images_w_text = []
        self.result_image = None
        self.pre_grid_images = []

    def compose_images(self, template_type="single", position="up"):
        template_number = len(self.images)

        if template_number > 1 and template_type == "single": template_type = "horizontal"

        self.__resize_images(template_type)
        for index, image in enumerate(self.cropped_images):
            self.__add_text(image, self.texts[index], position=position)

        if template_number == 1:
            self.result_image = self.images_w_text[0]
            return helpers.save_image(self.result_image)

        if template_number > 1:
            w, h = 0, 0
            w_sum, h_sum = 0, 0
            for image in self.images_w_text:
                w, h = image.size
                w_sum += w
                h_sum += h
            if template_type == "horizontal":
                return self.__combine_image(w_sum, h, delta_x_change=1, delta_y_change=0)
            elif template_type == "vertical":
                return self.__combine_image(w, h_sum, delta_x_change=0, delta_y_change=1)

    def __combine_image(self, width, height, delta_x_change, delta_y_change):
        delta_x, delta_y = 0, 0
        self.result_image = Image.new("RGBA", (width, height))

        for image in self.images_w_text:
            self.result_image.paste(image, (delta_x, delta_y))
            delta_x += image.size[0] * delta_x_change
            delta_y += image.size[1] * delta_y_change

        return helpers.save_image(self.result_image)

    def __resize_images(self, composition_type):
        min_width = min([helpers.get_size(image)[0] for image in self.images])
        min_height = min([helpers.get_size(image)[1] for image in self.images])

        for image in self.images:
            new_image = Image.open(image)
            x, y = new_image.size

            if composition_type == "single":
                pass
            elif composition_type == "horizontal":
                x = (x / (y / min_height)).__int__()
                y = min_height
            elif composition_type == "vertical":
                y = (y * min_width / x).__int__()
                x = min_width

            resized_image = new_image.resize((x, y))
            self.cropped_images.append(resized_image)

    def __add_text(self, image, text, position):
        x, y = image.size

        text_pos = {
            "down": [(x / 2).__int__(), y - 50],
            "up": [(x / 2).__int__(), 10],
            "middle": [(x / 2).__int__(), (y / 2 - 25).__int__()]
        }

        self.images_w_text.append(helpers.draw_text_on_image(image, text, text_pos[position][0], text_pos[position][1]))


if __name__ == '__main__':
    i1 = Meme(('data/1.jpg', 'data/2.jpg', 'data/2.jpg'), ("Meme", "Maker 1.0", "asdqwe"))
    # i1 = Meme(('data/1.jpg', ), ("Meme", ))
    im_name = i1.compose_images("single", position="up")
    im = Image.open(f"./results/{im_name}")
    im.show()
