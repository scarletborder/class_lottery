import random


class StudentLotteryFinalTuning:

    def __init__(
        self,
        students: list[str],
        mean,
        std_dev,
        initial_draws,
        adjustment_step,
        probDict: dict[str, float],
    ):
        self.students = students
        self.probabilities = probDict
        self.mean = mean
        self.std_dev = std_dev
        self.selection_count = {student: 0 for student in students}
        self.total_draws = initial_draws
        self.adjustment_step = adjustment_step

    def adjust_probabilities_for_selected(self, selected_student):
        # Adjust the probability of the selected student
        deviation = self.selection_count[selected_student] - self.mean
        adjustment = deviation / (10 * self.std_dev**2)
        adjustment *= self.adjustment_step
        self.probabilities[selected_student] -= adjustment

        # Increase probabilities slightly for non-selected students
        increase_step = 0.05 / len(self.students)
        for student in self.students:
            if student != selected_student:
                self.probabilities[student] -= increase_step

        # Ensure no probabilities fall below a minimum threshold
        min_prob = 0.01 / len(self.students)
        for student in self.probabilities:
            if self.probabilities[student] < min_prob:
                self.probabilities[student] = min_prob

        # Normalize probabilities
        total = sum(self.probabilities.values())
        for student in self.probabilities:
            self.probabilities[student] /= total

    def adjust_probabilities_for_absent(self, selected_student):
        # Adjust the probability of the selected student
        deviation = self.selection_count[selected_student] - self.mean
        adjustment = deviation / (10 * self.std_dev**2)
        adjustment *= -self.adjustment_step
        self.probabilities[selected_student] += adjustment

        # Increase probabilities slightly for non-selected students
        increase_step = 0.05 / len(self.students)
        for student in self.students:
            if student != selected_student:
                self.probabilities[student] += increase_step

        # Ensure no probabilities fall below a minimum threshold
        min_prob = 0.01 / len(self.students)
        for student in self.probabilities:
            if self.probabilities[student] < min_prob:
                self.probabilities[student] = min_prob

        # Normalize probabilities
        total = sum(self.probabilities.values())
        for student in self.probabilities:
            self.probabilities[student] /= total

    def draw_student(self, absent_students: set[str]):
        # Draw a single student based on their probabilities
        selected_student = random.choices(
            list(self.probabilities.keys()),
            weights=list(self.probabilities.values()),
            k=1,
        )[0]
        # judge whether this student is absent
        is_absent = selected_student in absent_students

        # Increment the draw count, add extra draw if absent
        if is_absent:
            return None
        else:
            self.selection_count[selected_student] += 1

        # Adjust probabilities after each draw
        self.adjust_probabilities_for_selected(selected_student)

        return selected_student

    def draw_some_students(self, absent_students: set[str], stu_num: int):
        # Draw a series of students
        ret = []
        chosen_students = set(absent_students)
        while len(ret) < stu_num:
            selected_student = self.draw_student(chosen_students)
            if selected_student is None:
                continue
            else:
                ret.append(selected_student)
                chosen_students.add(selected_student)

        # adjust those who are absent
        for stu in absent_students:
            self.adjust_probabilities_for_absent(stu)

        return ret
