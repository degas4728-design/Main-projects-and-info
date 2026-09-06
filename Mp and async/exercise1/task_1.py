import time
import random
import multiprocessing
from prettytable import PrettyTable
import os

def read_questions_f():
    ls = []
    with open('questions.txt', 'r', encoding='utf-8') as f:
        file_ = f.readlines()

    for i in file_:
        ls.append(i)

    return ls

def read_students_f():
    ls = []
    with open('students.txt', 'r', encoding='utf-8') as f:
        file_ = f.readlines()

    for i in file_:
        ls.append(i)

    return ls

def read_examiners_f():
    ls = []
    with open('examiners.txt', 'r', encoding='utf-8') as f:
        file_ = f.readlines()

    for i in file_:
        ls.append(i)

    return ls

def check_students():
    ls = []
    status = True
    with open('students.txt', 'r', encoding='utf-8') as f:
        file_ = f.readlines()

    for i in file_:
        ls.append(i[0:len(i)-1])
    if len(ls) == 0:
        status = False
    return status

def print_image(shared_list_student, shared_list_examiner):

    with lock:
        os.system('cls' if os.name == 'nt' else 'clear')
        main_table = PrettyTable()
        status_table = PrettyTable()
        main_table.field_names = ["Экзаменатор", "Текущий студент","Всего студентов","Завалил","Время работы"]
        status_table.field_names = ["Студент", "Статус"]

        for i in shared_list_student: status_table.add_row([i.name, i.status])
        for i in shared_list_examiner: 
            main_table.add_row([i.name,i.current_s, i.total_s, i.failed, i.time])
        print(status_table,"\n\n",main_table)

class Questions:
    all_questions = read_questions_f()

    def give_3_questions():
        tmp = 0
        ls_ans = []

        list_questions = list(range(0, len(Questions.all_questions)))
        for i in range(3):
            tmp = random.choice(list_questions)
            ls_ans.append(tmp)
            list_questions.remove(tmp)

        return ls_ans
            
    def calculete_probability(words,gender, count_ans):
        ls_ans = []
        f = 1.618
        words = words.split()
        if gender == 'Ж': words.reverse()
        if len(words) == 1:ls_ans.append(words[0])
        else:
            ls_ans.append(1 / f)  
            tmp = 1
            for i in range(len(words)):
                
                if len(ls_ans) % 2 == 0 or len(ls_ans) == 1:
                    for i in ls_ans:
                        tmp = tmp - i
                    tmp = tmp / f
                elif len(ls_ans) % 2 != 0 and len(ls_ans) > 1:
            
                    for i in ls_ans:
                        tmp = tmp - i
                
                ls_ans.append(tmp)
                tmp = 1

        ans = []
        while len(ans) != count_ans:
            tmp = random.choices(words, weights=ls_ans[:len(words)])
            if tmp[0] not in ans:
                ans.extend(tmp)
        return ans
    
    def calculete_probability_ex(words,gender, len_words):
        ls_ans = []
        chances = []
        f = 1.618
        if type(words) != list:words = words.split()
        if gender == 'Ж': words.reverse()
        
        chances.append(1 / f) 
        tmp = 1
        for i in range(len(words)):
    
            if len(chances) % 2 == 0:
                for i in chances:
                    tmp = tmp - i
                tmp = tmp / f
            elif len(chances) % 2 != 0 and len(chances) > 1:
                for i in chances:
                    tmp = tmp - i
                
            chances.append(tmp)
            tmp = 1
            
        words_list = words_list = list(random.choices(words, weights=chances[:len(words)]))
        
        tmp = random.choices([True ,False],[0.3,0.6])
        if  tmp[0] == True:
            Flag = False
            while True:
                tmp = Questions.calculete_probability_ex(words,gender, len(words))
                for i in words_list:
                    if i != tmp[0]:
                        Flag = True
                        break
                if Flag == True:
                    words_list.append(tmp[0])
                    break
        return words_list
        
    def comparison_ans(proba_s, proba_e):
        ans = True
        proba_s.sort()
        proba_e.sort()
        if proba_s != proba_e:
            ans = False
        return ans

    def exam_end(c_r_ans, c_w_ans):
        ans = False
        tmp = random.choices(['n','s','p'],[0.125, 0.25, 0.625])
        if tmp[0] == 'p':
            if c_r_ans >= c_w_ans: 
                ans = True
        elif tmp[0] == 's':
            ans = True
        
        return ans

class Students:

    def __init__(self,name,gender):
        self.name = name
        self.status = 'Очередь'
        self.gender = gender
        self.c_r_answer = 0
        self.exam_time = 0
        self.wich_que = []
        
    def make_students():
        ls = read_students_f()
        tmp = 0
        ans = []
        for i in range(len(ls)):
            tmp = ls[i].split()
            ans.append(Students(tmp[0],tmp[1]))
        return ans

    def take_one(shared_list_student,already_been_students):
        free_student = 0
        for i in shared_list_student:
            if i.name not in already_been_students:
                already_been_students.append(i.name)
                free_student = i
                break

        return free_student
    
    def put_object(shared_list_student, student):
        for ind, elem in enumerate(shared_list_student):
            if student.name == elem.name:
                shared_list_student[ind] = student
                break

    def best_student(shared_list_student):
        best_time = 1000000
        names_of_best = []
        for i in shared_list_student:
            if i.exam_time < best_time and i.status == 'Сдал':
                best_time = i.exam_time
        

        for i in shared_list_student:
            if i.exam_time <= best_time and i.status == 'Сдал':
                names_of_best.append(i.name)
                best_time = i.exam_time

        return names_of_best

    def who_will_deleted(shared_list_student):
        min_date_name = ''
        min_time = 1000000000
        worse_stidents = [0]
        for i in shared_list_student:
            if i.status == 'Провалил' and i.exam_time < min_time:
                min_date_name = i.name
                min_time = i.exam_time

        worse_stidents[0] = min_date_name
        for i in shared_list_student:
            if i.status == 'Провалил' and i.exam_time == min_time and i.name != worse_stidents[0]:
                worse_stidents.append(i.name)

        return worse_stidents
    
    def best_que(shared_list_student, que_list):
        all_que = [[i,0] for i in range(len(que_list))]
        x,y = 0,0
        for i in shared_list_student:
            for j in i.wich_que:
                for x in range(len(que_list)):
                    if j == all_que[x][0]:
                        all_que[x][1] = all_que[x][1] + 1
                        break
        best_questions_num = []
        max_orders = 0
        num_max_orders = 0
        best_questions = []
        for i in all_que:
            if i[1] > max_orders:
                max_orders = i[1]
            
        for i in all_que:
            if i[1] == max_orders:
                best_questions_num.append(i[0])
        
        for i in range(len(best_questions_num)):
            best_questions.append(que_list[best_questions_num[i]])

        
        return best_questions
    
class Examiners:

    def __init__(self,name, gender):
        self.name = name
        self.gender = gender
        self.time = 0
        self.failed = 0
        self.total_s = 0
        self.current_s = ''

    def make_examiners():
        ls = read_examiners_f()
        tmp = 0
        ans = []
        for i in range(len(ls)):
            tmp = ls[i].split()
            ans.append(Examiners(tmp[0],tmp[1]))
        return ans

    def take_one(shared_list_examiner):
        free_examiner = 0
        for i in shared_list_examiner:
            if i.current_s == '':
                free_examiner = i
                break
        
        return free_examiner

    def lunch(start_time, lunch_status):
        if lunch_status == 0:
            tmp = 0
            if time.time() - start_time > 30:
                tmp = random.choice([12,13,14,15,16,17,18])
                time.sleep(tmp)
                lunch_status = 1
    
    def put_object(shared_list_examiner, examiner):
        for ind, elem in enumerate(shared_list_examiner):
            if examiner.name == elem.name:
                shared_list_examiner[ind] = examiner
                break

    def best_examiner(shared_list_examiner):
        min_date_name = ''
        min_failed = 1000000000
        max_count = 0
        best_examiner = []
        for i in shared_list_examiner:
            if i.total_s > max_count and i.failed < min_failed :
                min_date_name = i.name
                min_failed = i.failed
                max_count = i.total_s
            elif i.total_s > max_count and i.failed <= min_failed:
                min_date_name = i.name
                min_failed = i.failed
                max_count = i.total_s
            elif i.total_s >= max_count and i.failed < min_failed:
                min_date_name = i.name
                min_failed = i.failed
                max_count = i.total_s

        best_examiner.append(min_date_name)

        for i in shared_list_examiner:
            if i.failed == min_failed and i.total_s == max_count and i.name != best_examiner[0]:
                best_examiner.append(i.name)

        return best_examiner

    def exam_is_good(shared_list_student): 
        procent = round(len(shared_list_student) / 100, 3)
        who_pass_exam = []
        status = False
        for i in shared_list_student:
            if i.status == 'Сдал':
                who_pass_exam.append(i.name)
        
        if round(len(who_pass_exam) / procent) > 85:
            status = True
        return status

def do_exam(start_time, already_been_students, lock, shared_list_student, shared_list_examiner):
    start_exam_time = time.time()
    while True:
        start_exam_for_student = time.time() 
        with lock:
            examiner = Examiners.take_one(shared_list_examiner)
            student = Students.take_one(shared_list_student, already_been_students)
            if type(student) == int:return 
            examiner.current_s = student.name
            Examiners.put_object(shared_list_examiner, examiner)
        que_for_s = Questions.give_3_questions()
        c_r_ans, c_w_ans, lunch_status = 0,0,0
        while True:  
            Examiners.lunch(start_time,lunch_status)
            words = random.choice(que_for_s)
            que_for_s.remove(words)

            proba_e = Questions.calculete_probability_ex(Questions.all_questions[words], examiner.gender, len(Questions.all_questions[words].split()))
            proba_s = Questions.calculete_probability(Questions.all_questions[words], student.gender, len(proba_e))

            if Questions.comparison_ans(proba_s, proba_e): 
                c_r_ans = c_r_ans + 1
                with lock:
                    student.wich_que.append(words)
                    Students.put_object(shared_list_student, student)
            else:c_w_ans = c_w_ans + 1
            if len(que_for_s) == 0:break

        result = Questions.exam_end(c_r_ans, c_w_ans)
        print_image(shared_list_examiner, shared_list_student,already_been_students , lock, start_time)
        exam_time = random.choice([len(examiner.name)-1,len(examiner.name)+1])
        if time.time() > (start_exam_time - exam_time):
            time.sleep(exam_time)
        with lock:
            if result == True:
                examiner.current_s = ''
                student.status = 'Сдал'
                examiner.total_s = examiner.total_s + 1
                student.c_r_answer = c_r_ans
                examiner.time = round(time.time() - start_exam_time,2)
                student.exam_time = round(time.time() - start_exam_for_student,2)
                Students.put_object(shared_list_student, student)
                Examiners.put_object(shared_list_examiner, examiner)
            else:
                examiner.current_s = ''
                student.status = 'Провалил'
                examiner.total_s = examiner.total_s + 1
                student.c_r_answer = c_r_ans
                examiner.failed =  examiner.failed + 1
                student.exam_time = round(time.time() - start_exam_for_student,2)
                examiner.time = round(time.time() - start_exam_time,2)
                Students.put_object(shared_list_student, student)
                Examiners.put_object(shared_list_examiner, examiner)
        

        print_image(shared_list_examiner, shared_list_student,already_been_students ,  lock, start_time)

def check_students(shared_list_student):
    status = True 
    for i in shared_list_student:
        if i.status == 'Очередь':
            status = False
    

    return status 

def print_image(shared_list_examiner, shared_list_student, already_been_students ,lock, start_time):
    with lock:
        os.system('cls' if os.name == 'nt' else 'clear')
        main_table = PrettyTable()
        status_table = PrettyTable()
        status_table.clear_rows()
        main_table.clear_rows()
        main_table.field_names = ["Экзаменатор", "Текущий студент","Всего студентов","Завалил","Время работы"]
        status_table.field_names = ["Студент", "Статус"]
        
        for i in shared_list_student: 
            if i.status == 'Очередь':
                status_table.add_row([i.name, i.status])
        for i in shared_list_student:
            if i.status == 'Сдал':
                status_table.add_row([i.name, i.status])
        for i in shared_list_student:
            if i.status == 'Провалил':
                status_table.add_row([i.name, i.status])

        for i in shared_list_examiner: 
            if i.current_s == '':
                main_table.add_row([i.name, "-", i.total_s, i.failed, i.time])
            else:
                main_table.add_row([i.name, i.current_s, i.total_s, i.failed, i.time])
        print(status_table,"\n\n",main_table)
        print(f"\n\nОсталось в очереди: {len(shared_list_student) - len(already_been_students)} из {len(shared_list_student)}")
        print(f"Время с момента начала экзамена: {round(time.time() - start_time,2)}")
      
def print_lust_image(shared_list_examiner, shared_list_student, already_been_students ,lock, start_time, all_questions):
    os.system('cls' if os.name == 'nt' else 'clear')
    main_table = PrettyTable()
    status_table = PrettyTable()
    main_table.clear_rows()
    main_table.field_names = ["Экзаменатор","Всего студентов","Завалил","Время работы"]
    status_table.field_names = ["Студент", "Статус"]

    for i in shared_list_student:
        if i.status == 'Сдал':
            status_table.add_row([i.name, i.status])
    for i in shared_list_student:
        if i.status == 'Провалил':
            status_table.add_row([i.name, i.status])
    for i in shared_list_examiner: main_table.add_row([i.name, i.total_s, i.failed, i.time])

    print(status_table,"\n\n",main_table)
    print(f"\n\nВремя с момента начала экзамена и до момента и его завершения: {round(time.time() - start_time,2)}")
    list_best_students = ", ".join(Students.best_student(shared_list_student))
    print(f"Имена лучших студентов: {list_best_students}")
    list_best_examiners =  ", ".join(Examiners.best_examiner(shared_list_examiner))
    print(f"Имена лучших экзаменаторов: {list_best_examiners}")
    list_worse_students = ", ".join(Students.who_will_deleted(shared_list_student))
    print(f"Имена студентов, которых после экзамена отчислят: {list_worse_students}")
    list_best_que = Students.best_que(shared_list_student,all_questions)
    for i in range(len(list_best_que)): list_best_que[i] = list_best_que[i][0:len(list_best_que[i])-1]
    list_best_que = ", ".join(list_best_que)
    print(f"Лучшие вопросы: {list_best_que}")
    if Examiners.exam_is_good(shared_list_student) == True:
        print("Вывод: Экзамен удался")
    else:
        print("Вывод: Экзамен не удался")

if __name__ == "__main__":
    start_time = time.time()

    manager = multiprocessing.Manager()
    shared_list_student = manager.list()
    shared_list_examiner = manager.list()
    already_been_students = manager.list()
    shared_list_student.extend(Students.make_students())
    shared_list_examiner.extend(Examiners.make_examiners())
    lock = multiprocessing.Lock()
    processes = []

    for i in range(len(shared_list_examiner)):
            p = multiprocessing.Process(target=do_exam, args=(start_time, already_been_students, lock, shared_list_student, shared_list_examiner))
            processes.append(p)
            p.start()

    for i in processes:
        i.join()

    print_lust_image(shared_list_examiner, shared_list_student, already_been_students ,lock, start_time, Questions.all_questions)