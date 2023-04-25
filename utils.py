import cv2
import fitz
from pyzbar.pyzbar import decode


class Utils:

    @staticmethod
    def barcode_reader(image):
        # read the image in numpy array using cv2
        img = cv2.imread(image)

        # Decode the barcode image
        detectedBarcodes = decode(img)

        decoded_codes = []
        # If not detected then print the message
        if not detectedBarcodes:
            print("Barcode Not Detected or your barcode is blank/corrupted!")
        else:

            # Traverse through all the detected barcodes in image
            for barcode in detectedBarcodes:

                # Locate the barcode position in image
                (x, y, w, h) = barcode.rect

                # Put the rectangle in image using
                # cv2 to highlight the barcode
                cv2.rectangle(img, (x - 10, y - 10),
                              (x + w + 10, y + h + 10),
                              (255, 0, 0), 2)

                if barcode.data != "":
                    # Print the barcode data
                    decoded_codes.append([barcode.data, barcode.type])

        return decoded_codes

    @staticmethod
    def check_file_quality(file):
        lines = []  # the result
        doc = fitz.open(file)
        for page in doc:
            page_lines = []  # lines on this page
            all_text = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)
            for block in all_text["blocks"]:
                for line in block["lines"]:
                    text = "".join([span["text"] for span in line["spans"]])
                    bbox = fitz.Rect(line["bbox"])  # the wrapping rectangle
                    # append line text and its top-left coord
                    page_lines.append((bbox.y0, bbox.x0, text))
            # sort the page lines by vertical, then by horizontal coord
            page_lines.sort(key=lambda l: (l[0], l[1]))
            lines.append(page_lines)  # append to lines of the document
        return lines

    @staticmethod
    def get_elements_positions(file, include_fields=False):
        file_elements = Utils.check_file_quality(file)
        elem_positions = []

        end_index = 2
        if include_fields:
            end_index = None

        for index, value in enumerate(file_elements[0]):
            element = list(value[0:end_index])
            if include_fields:
                try:
                    element[2] = element[2].split(':')[0]
                except:
                    pass

            elem_positions.append(element)
        del elem_positions[18]
        return elem_positions
