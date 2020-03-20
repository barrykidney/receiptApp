import os
from ocr import ocr
import receipt_parser


def get_list_of_unconverted_jpg_files_in_folder(directory):
    txt_fl = []
    jpg_fl = []

    try:
        for file in os.listdir(directory):
            if os.path.splitext(file)[1] == ".jpg":
                jpg_fl.append(os.path.splitext(file)[0])
            elif os.path.splitext(file)[1] == ".txt":
                txt_fl.append(os.path.splitext(file)[0])
            else:
                print("File '" + file + "' is not a compatible type.")

    except IndexError:
        print("\nERROR: Folder '" + directory + "' is empty.")

    return [directory + "/" + s + ".jpg" for s in list(set(jpg_fl) - set(txt_fl))]


def get_list_of_txt_files_in_folder(directory):
    txt_fl = []
    try:
        for file in os.listdir(directory):
            if os.path.splitext(file)[1] == ".txt":
                txt_fl.append(directory + "/" + os.path.splitext(file)[0] + ".txt")

    except IndexError:
        print("\nERROR: Folder '" + directory + "' is empty.")

    return txt_fl


def open_text_file(tf):
    f = open(tf, "r")
    t = f.read()
    f.close()
    return t


def save_text_file(t, n):
    fp = n[:-4] + ".txt"
    f = open(fp, "w+")
    f.write(t)
    f.close()
    return fp


def convert_unconverted_jpg_files_to_txt_in_folder(folder):
    print("Processing files found in folder " + folder)
    jpg_file_list = get_list_of_unconverted_jpg_files_in_folder(folder)
    txt_file_list = []
    for jpg_file in jpg_file_list:
        txt_file_list.append(convert_jpg_file_to_txt(jpg_file))
    print("Converted files to txt: ", txt_file_list)


def convert_jpg_file_to_txt(f):
    print("Processing file " + f)
    tesseract = ocr.TessOCR()
    text = tesseract.process_image(f, "blur")

    return save_text_file(text, f)


if __name__ == "__main__":

    #
    # other_date_identifiers = ["dd/mm/yy", "dd/mm/yyyy", "dd-mm-yy", "dd-mm-yyyy", "dd.mm.yy", "dd.mm.yyyy", "january",
    #                           "jan", "feburary", "feb", "march", "mar", "april", "apr", "may", "june", "jun", "july",
    #                           "jul", "august", "aug", "september", "sep", "sept", "october", "oct", "november", "nov",
    #                           "december", "dec"]

    directory_name = "2020-02"
    directory_path = os.getcwd() + "/receipts/" + directory_name

    convert_unconverted_jpg_files_to_txt_in_folder(directory_path)
    list_of_txt_files = get_list_of_txt_files_in_folder(directory_path)
    if len(list_of_txt_files) < 1:
        print("No txt files found in folder " + directory_path)
    else:
        rp = receipt_parser.ReceiptParser()
        for txt_file in list_of_txt_files:
            text_data = open_text_file(txt_file)
            rp.parse_text(text_data)
