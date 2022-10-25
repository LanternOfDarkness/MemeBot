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
        else:
            w_sum = sum([image.size[0] for image in self.images_w_text])
            h_sum = sum([image.size[1] for image in self.images_w_text])
            image_amount = len(self.images_w_text)

            if template_type == "horizontal":
                return self.__combine_image(w_sum, int(h_sum/image_amount), delta_horizontal=1)
            elif template_type == "vertical":
                return self.__combine_image(int(w_sum/image_amount), h_sum, delta_horizontal=0)


    def __combine_image(self, width, height, delta_horizontal):
        delta_x, delta_y = 0, 0
        self.result_image = Image.new("RGBA", (width, height))

        for image in self.images_w_text:
            self.result_image.paste(image, (delta_x, delta_y))
            delta_x += image.size[0] * delta_horizontal
            delta_y += image.size[1] * abs(delta_horizontal - 1)

        return helpers.save_image(self.result_image)

    def __resize_images(self, composition_type):

        if composition_type != "grid":
            widths = [helpers.get_size(image)[0] for image in self.images]
            heights = [helpers.get_size(image)[1] for image in self.images]
            min_width = min(widths)
            min_height = min(heights)
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

        else:
            self.__resize_images(composition_type="vertical")

            temp_image = []
            counter = 0
            for i, img in enumerate(self.cropped_images):
                temp_image.append(img)

                if len(temp_image) == 2:
                    width = min([image.size[0] for image in temp_image])
                    height = max([image.size[1] for image in temp_image])

                    for image in temp_image:
                        resized_image = Image.new("RGB", size=(width, height))
                        resized_image.paste(image, (0, int((height - image.size[1])/2)))
                        self.cropped_images[counter] = resized_image
                        counter +=1

                    temp_image.clear()


    def __add_text(self, image, text, position):
        x, y = image.size

        text_pos = {
            "down": [(x / 2).__int__(), y - 50],
            "up": [(x / 2).__int__(), 10],
            "middle": [(x / 2).__int__(), (y / 2 - 25).__int__()]
        }
        image = helpers.draw_text_on_image(image, text, text_pos[position][0], text_pos[position][1])
        self.images_w_text.append(image)
        image.show()


if __name__ == '__main__':
    i1 = Meme(('data/1.jpg', 'data/2.jpg', 'data/2.jpg' , 'data/1.jpg'), ("1", "2", "3", "4"))
    # i1 = Meme(('data/1.jpg', ), ("Meme", ))
    im_name = i1.compose_images("grid", position="up")
    im = Image.open(f"./results/{im_name}")
    im.show()
