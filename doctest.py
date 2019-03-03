import argparse
from enum import Enum
import io

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image


def get_document_bounds(image_file, feature):
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    bounds = []
    words_list= []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)
                        words_list.append(word)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)

        if (feature == FeatureType.PAGE):
            bounds.append(block.bounding_box)

    #print(words_list)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds, words_list
    #return words_list

def render_doc_text(filein, fileout):
    image = Image.open(filein)
    bounds, page_list = get_document_bounds(filein, FeatureType.PAGE)
    draw_boxes(image, bounds, 'blue')
    bounds, para_list = get_document_bounds(filein, FeatureType.PARA)
    draw_boxes(image, bounds, 'red')
    bounds, words_list = get_document_bounds(filein, FeatureType.WORD)
    draw_boxes(image, bounds, 'yellow')

    if fileout is not 0:
        image.save(fileout)
    else:
        image.show()
    return words_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('detect_file', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    args = parser.parse_args()

    words_list = render_doc_text(args.detect_file, args.out_file)
    #words_list = get_document_bounds(args.detect_file, args.out_file)

    # print(words_list)
    # print("--------------------------------------------")
    words_list.sort(key=lambda word:word.bounding_box.vertices[0].y)
    #words_list.sort(key=lambda word:word.bounding_box.vertices[0].x)


    receipt_line = []
    prev_word = words_list[0]
    cur_line = []

    #print(words_list)
    for word in words_list:
        #means it's a new line, stored separately
        if (abs(word.bounding_box.vertices[3].y - prev_word.bounding_box.vertices[3].y) > 45):
            #print(abs(word.bounding_box.vertices[0].y - word.bounding_box.vertices[3].y))
            ##sort the current line
            cur_line.sort(key=lambda word:word.bounding_box.vertices[3].x)

            ##append the current line to the receipt
            receipt_line.append(cur_line)

            ##clear out the current line
            cur_line = []
            prev_word = word

        else:
            cur_line.append(word)
            #receipt_line[-1][-1].append(word)

    #print(receipt_line)

    words_in_row_list = []
    string_word= ""

    #going through each row in the main list
    for i in range (0, len(receipt_line)):
        #going through each word in the main list
        for word in range (0, len(receipt_line[i])):
            #print(receipt_line[i][word])
            for symbol in receipt_line[i][word].symbols:
                string_word += symbol.text
                #row_list.append(symbol.text)
                #print(symbol.text)
            words_in_row_list.append(string_word.encode('utf-8').strip())
            string_word = ""
        final_string = ' '.join(words_in_row_list)
        print(final_string)
        words_in_row_list = []

        # print(words_in_row_list[i])


        #print(receipt_line[i][0].symbols)
        #char_list = [line.text for line in [symbol.text for symbol in receipt_line[i].symbols]]
        #print(''.join(list(char_list)).encode('utf-8').strip())



        #print(word.bounding_box.vertices[0].y)
