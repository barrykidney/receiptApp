from PIL import Image
import pytesseract
import cv2
import os


class TessOCR:

    @staticmethod
    def load_image(fp):
        img = cv2.imread(fp)
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def preprocess_image(img, p):
        if p == "thresh":
            return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        elif p == "blur":
            return cv2.medianBlur(img, 3)

    @staticmethod
    def write_img_to_temp_file(img):
        tf = "{}.png".format(os.getpid())
        cv2.imwrite(tf, img)
        return tf

    @staticmethod
    def generate_text(fp):
        return pytesseract.image_to_string(Image.open(fp))

    def process_image(self, filepath, preprocess="thresh"):
        image = self.load_image(filepath)
        image = self.preprocess_image(image, preprocess)
        temp_file = self.write_img_to_temp_file(image)
        text = self.generate_text(temp_file)
        os.remove(temp_file)
        return text
