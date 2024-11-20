import easyocr
import os
import pandas as pd
from rapidfuzz import process


PATH = 'screenshots'


def pic_deleter(pic_path):
    try:
        if os.path.isfile(pic_path):
            os.remove(pic_path)
            print(f"'{pic_path}' deleted.")
        else:
            print(f"'{pic_path}' is not a file.")
    except FileNotFoundError:
        print(f"'{pic_path}' do not exist")
    except PermissionError:
        print(f"No permission")
    except Exception as e:
        print(f"Error: {e}")
    return None


def text_reader(pic_path):
    reader = easyocr.Reader(['ja', 'en'])   #japanese and english
    result = reader.readtext(pic_path)
    strr = result[0][1]
    return strr


# def a function for Fast Fuzzy Matching
def fuzzy_match(target, candidates, limit=1):
    # using lib rapidfuzz process.extractOne or process.extract
    return process.extract(target, candidates, limit=limit)


def file_list_getter(folder_path, target_extension=".xlsx"):
    # to get all the filename in the directory
    file_names_list = [f for f in os.listdir(folder_path) if f.endswith(target_extension)]
    return file_names_list


def collector(path, filenames):
    """
    :path: "answer"
    :param filenames: should be a list
    :return:
    """
    all_sheetfile_list = []
    for fn in filenames:
        excel_workbook = ExcelReader(path + "/" + fn)
        for sn in excel_workbook.sheetnames:
            if sn == excel_workbook.sheetnames[0]:
                pass
            else:
                all_sheetfile_list.append(SheetReader(excel_workbook, sn))
    return all_sheetfile_list


def answer_finder(sheetfile_list, target):
    list_tuple = pd.DataFrame(map(lambda x: fuzzy_match(target, x.candidates), sheetfile_list))[0].to_list()
    result_list = list(map(list, list_tuple))
    results = pd.DataFrame(result_list, columns=['match_str', 'probability', 'index'])
    pd_index = results['probability'].idxmax(0)
    index = results['index'][pd_index]
    match_str = results['match_str'][pd_index]
    anwers = sheetfile_list[pd_index].keys[index]
    result_dic = {
        "question": match_str,
        "answer": anwers
    }
    return result_dic


def main_func(pic_path):
    # pic_path = file_list_getter(PATH, 'png')[-1]
    target = text_reader(pic_path)
    folder_path = "../answers"
    file_list = file_list_getter(folder_path)
    sheetlist = collector(folder_path, file_list)
    result_dic = answer_finder(sheetlist, target)
    pic_deleter(pic_path)
    return result_dic


class ExcelReader(object):
    """
    to read the excel and get all sheet
    the first sheet should be skipped
    """
    def __init__(self, file_path):
        self.path = file_path
        self.workbook = pd.ExcelFile(self.path)
        self.sheetnames = self.workbook.sheet_names


class SheetReader(object):
    """
    for each useful sheet: the first column should be question stem and the second column should be answers
    """
    def __init__(self, father, sheet_name):
        """father should be a excel workbook"""
        self.father = father
        self.sheetname = sheet_name
        self.sheet = father.workbook.parse(sheet_name)
        self.colunmnames = self.sheet.columns.tolist()
        self.candidates = self.sheet[self.colunmnames[0]].tolist()
        self.candidates = list(map(lambda x: str(x) if x is not None else '', self.candidates))     # change format into string
        self.keys = self.sheet[self.colunmnames[1]].tolist()


# if __name__ == '__main__':
#     pic_path = 'pic/img.png'
#     target = text_reader(pic_path)
#     folder_path = "../answers"
#     file_list = file_list_getter(folder_path)
#     sheetlist = collector(folder_path, file_list)
#     print(answer_finder(sheetlist, target))

