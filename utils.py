from config import cfg
import csv
from prettytable import PrettyTable
from app import App
import os


def list_probs():
    ret = dict()
    with open(cfg.data_csv_filepath, "r", encoding="utf-8") as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            ret[row["name"]] = float(row["value"])
    sorted_list = sorted(ret.items(), key=lambda item: item[1], reverse=True)
    table = PrettyTable(["姓名", "概率"])
    for items in sorted_list:
        table.add_row([items[0], "{:.2f}%".format(items[1] * 100)])

    return str(table)


def draw(num: int, absent: list[str]):
    myApp = App(cfg.data_csv_filepath, None)
    if num > len(myApp.stu_handle.students):
        return f"[Error]: You want to draw {num} people, but only {len(myApp.stu_handle.students)} exists"
    ret = myApp.draw_some_students(absent, num)
    table = PrettyTable(["幸运人员"])
    for item in ret:
        table.add_row([str(item)])
    myApp.dump_stu_data(myApp.dataFilePath)
    return str(table)


def new_data(stus: list[str]):
    # print("debug" + str(stus))
    if os.path.exists(cfg.data_csv_filepath) is True:
        if os.path.exists(cfg.data_csv_filepath + ".bak") is True:
            os.remove(cfg.data_csv_filepath + ".bak")
        os.rename(cfg.data_csv_filepath, cfg.data_csv_filepath + ".bak")
    myApp = App(cfg.data_csv_filepath, stus)
    myApp.dump_stu_data(myApp.dataFilePath)


def import_data(chosen_count: dict[str, int], absent_count: dict[str, int]):
    myApp = App(cfg.data_csv_filepath, None)
    for stu in chosen_count.keys():
        for times in range(chosen_count[stu]):
            myApp.stu_handle.adjust_probabilities_for_selected(stu)
    for stu in absent_count.keys():
        for times in range(absent_count[stu]):
            myApp.stu_handle.adjust_probabilities_for_absent(stu)
    myApp.dump_stu_data(myApp.dataFilePath)


if __name__ == "__main__":
    # new_data(["",,])
    ...
