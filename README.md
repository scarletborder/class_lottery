# class_lottery
a method for balanced choice of class activities.更公平的抽取班级活动人员

## 用法
`python cli.py [-l] [-d number_of_student [-a student1,student2,student3]] [-n stu1,stu2,stu3,stu4]`
- `-l`/`--list-probs` : 展示当前环境下所有同学被抽取的概率
- `-d`/`--draw` `number_of_student` : 抽取数量为number_of_student(int)数量个的人员
  - `-a`/`--absent` `stu1,stu2,...` : 在本次抽取中过滤人员，使用`,`分隔。过滤的人员在这次抽取结束后概率会提升
- `-n`/`--new-data` `stu1,stu2`: 重置数据，人员标记使用`,`隔开。同时旧数据保存在`<data_csv_filepath>.bak`
- `-i`/`--import-data` `stu1:4,stu2:5;stu1:1`: 导入数据，`#`分隔开左边是参加人数状态，右边是请假人数状态，每一状态用`,`隔开，键值对为`name:count`。左右两边均可以为空

## config
请直接在`config.py`中对参数进行修改。  
- `data_csv_filepath = "data.csv"` : name-value表格，对应当前状态下每个人被抽取的概率
- `initial_draws_tuning = 10000` : 预估的抽奖次数，每次按一人计算。即如果预估本学期有10场活动且每次参加均为20人，则此值为200
- `std_dev_selections_tuning = 10` : 预计的标准差
- `step = 0.05` : 调整概率时用到的步长