from lottery_handle import StudentLotteryFinalTuning
import csv


class App:
    def __init__(self, filePath: str, new_students: list | None) -> None:
        self.dataFilePath = filePath
        probDict = dict()
        if new_students is None:
            # load
            probDict = self.load_stu_data()
        else:
            # init
            probDict = {student: 1.0 / len(new_students) for student in new_students}

        # Initialize variables for tuning
        initial_draws_tuning = 10000
        mean_selections_tuning = initial_draws_tuning / len(probDict.keys())
        std_dev_selections_tuning = 10
        step = 0.05

        self.stu_handle = StudentLotteryFinalTuning(
            students=list(probDict.keys()),
            mean=mean_selections_tuning,
            std_dev=std_dev_selections_tuning,
            initial_draws=initial_draws_tuning,
            adjustment_step=step,
            probDict=probDict,
        )
        pass

    def draw_some_students(self, absent_students: list, num: int):
        absent = set()
        for stu in absent_students:
            absent.add(stu)
        return self.stu_handle.draw_some_students(absent, num)

    def load_stu_data(self):
        ret = dict()
        with open(self.dataFilePath, "r", encoding="utf-8") as fin:
            reader = csv.DictReader(fin)
            for row in reader:
                ret[row["name"]] = float(row["value"])

        return ret

    def dump_stu_data(self, dst: str | None = None):
        if dst is None:
            dst = self.dataFilePath

        fieldnames = ["name", "value"]
        with open(dst, mode="w", newline="", encoding="utf-8") as csvfile:
            # 创建一个DictWriter对象
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # 写入标题行
            writer.writeheader()

            # 遍历字典，将数据写入CSV文件
            for name, value in self.stu_handle.probabilities.items():
                writer.writerow({"name": name, "value": value})
