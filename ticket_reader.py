import os
from pdf2image import convert_from_path
from pdfminer.high_level import extract_text
from utils import Utils


class TicketReader():

    @staticmethod
    def ticket_read_pdf(file):
        text_data = list(filter(None, extract_text(file).split('\n')))
        result_dict = {}
        for index, field in enumerate(text_data):
            if index == 20:
                break
            try:
                result_dict[field.split(':')[0]] = field.split(':')[1].strip()
            except:
                result_dict[field] = ''
        result_dict['NOTES'] = text_data[20]

        pages = convert_from_path(file, poppler_path=r'poppler-0.68.0\bin')
        for i in range(len(pages)):
            temp_file_name = 'temp_image'+ str(i) +'.jpg'
            pages[i].save(temp_file_name, 'JPEG')
            decoded_codes = Utils.barcode_reader(image=temp_file_name)
            os.remove(temp_file_name)
            result_dict['GRIFFON AVIATION SERVICES LLC'] = str(decoded_codes[1][0])[2:-1]
            result_dict['TAGGED BY'] = str(decoded_codes[0][0])[2:-1]

        return result_dict

if __name__ == '__main__':
    res = TicketReader.ticket_read_pdf(file='files/test_task.pdf')
    for field in res.items():
        print(f'{field[0]}: {field[1]}')
