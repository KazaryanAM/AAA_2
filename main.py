import csv


def command_hierarchy(file_name: str) -> str:
    """
    Читает file_name, создает словарь, где ключами будут отделы, а значениями соответсвующие департаменты.
     Разбивает словарь на элементы, сортирует их по департаменту, для каждого департамента выводит его отделы.
      """
    result = ''
    dep_d = {}
    with open(file_name, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            dep_d.setdefault(row["Отдел"], row["Департамент"])
        v = sorted(dep_d.items(), key=lambda x: x[1])
        j = 0
        for i in range(len(v) - 1):
            if j == 0:
                result += f'\nВ департамент {v[i][1]} входят отделы:'
                result += f'{v[i][0]}'
                j = 1
            if v[i][1] == v[i + 1][1]:
                result += f', {v[i + 1][0]}'
            else:
                j = 0
                result += f'.'
    return result


def get_one_dep_report(department: str) -> list:
    """
    Подается департамент, читает Corp_Summary.csv, для данного департамента находит численность, минимальную зарплату,
    максимальную зарплату, среднюю зарплату. Выводит список вида [department, dep_num, min_sal, max_sal, avg_sal].
    """
    result = []
    dep_num = 0
    all_salary = 0
    min_sal = 0
    max_sal = 0
    with open('Corp_Summary.csv', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        for row in reader:
            if row["Департамент"] == department:
                sal = int(row["Оклад"])
                if dep_num == 0:
                    min_sal = sal
                    max_sal = sal
                    all_salary += sal
                    dep_num += 1
                else:
                    if sal < min_sal:
                        min_sal = sal
                    if sal > max_sal:
                        max_sal = sal
                    all_salary += sal
                    dep_num += 1
    avg_sal = all_salary/dep_num
    result.append(department)
    result.append(dep_num)
    result.append(min_sal)
    result.append(max_sal)
    result.append(avg_sal)
    return result


def print_one_dep_report(department: str) -> str:
    """
    Выводит сводный отчет для одного департамента.
    """
    result = get_one_dep_report(department)
    return f'В департаменте {result[0]} {result[1]} человек, Зарплата: мин. {result[2]}, макс. {result[3]}, ' \
           f'Ср. {result[4]}'


def all_dep(file_name: str) -> list:
    """
    Из файла file_name получает список с названиями департаментов.
    """
    with open(file_name, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        result = []
        for row in reader:
            if row["Департамент"] not in result:
                result.append(row["Департамент"])
    return result


def print_dep_report(file_name: str) -> str:
    """
    Выводит сводный отчет для всех департаментов.
    """
    res = ''
    for department in all_dep(file_name):
        res += f'{print_one_dep_report(department)}\n'
    return res


def save_dep_report(r_file_name: str, w_file_name: str) -> int:
    """
    Из файла r_file_name получает сводный отчет для всех департаментов и сохраняет его в файле w_file_name.
    """
    with open(w_file_name, mode='w', encoding='utf-8', newline='') as w_csv_file:
        names = ["Департамент", "Численность", "Мин. оклад", "Макс. оклад", "Ср. оклад"]
        file_writer = csv.DictWriter(w_csv_file, fieldnames=names)
        file_writer.writeheader()
        for department in all_dep(r_file_name):
            result = get_one_dep_report(department)
            file_writer.writerow({"Департамент": result[0], "Численность": result[1], "Мин. оклад": result[2],
                                  "Макс. оклад": result[3], "Ср. оклад": result[4]})
    return 0


def menu():
    """
    Дает пользователю на выбор 4 варианта действий, после выбора действия выполняет это действие и снова предоставляет
    пользователю 4 варианта, если пользователь не выбрал вариант выхода.
    """
    r_file_name = 'Corp_Summary.csv'
    w_file_name = 'Corp_Summary_Report.csv'
    options = ['1', '2', '3', '4']
    option = ''
    while option != '4':
        print(
            '\n1. Вывести иерархию команд. '
            '2. Вывести сводный отчет по департаментам. '
            '3. Сохранить сводный отчет в виде csv-файла. '
            '4. Выход. '
        )
        print('Выберите: {},{},{},{}'.format(*options))
        option = input()
        if option == '1':
            print(command_hierarchy(r_file_name))
        elif option == '2':
            print(print_dep_report(r_file_name))
        elif option == '3':
            save_dep_report(r_file_name, w_file_name)
        else:
            return 0


menu()
