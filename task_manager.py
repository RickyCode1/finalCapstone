"""This is the main module for a task management program.
file_access.py - contains all functions for file access.
views.py - contains the main functions responsible for output. 
txt_files folder - contains all the generated text files. 
I really enjoyed this assignment and took the liberty of 
adding a few additional features. 
"""

import copy
from datetime import datetime, date
from file_access import (
    read_users_file,
    write_users_file,
    read_tasks_file,
    write_tasks_file,
    read_task_overview_file,
    write_task_overview_file,
    read_user_overview_file,
    write_user_overview_file,
)

from views import (
    view_main_menu,
    view_task_menu,
    view_edit_task_menu,
    view_users,
    view_all,
    view_my_tasks,
    view_task,
    view_stats,
)


DATETIME_STRING_FORMAT = "%Y-%m-%d"

"""SETUP CODE"""


def populate_task_list(read_tasks_file_cb):
    """
    reads the contants of tasks.txt. an object of each task is created and stored in a list.
    param: read_tasks_file_cb - provides the contents of tasks.txt.
    returns: an array of task objects.
    """
    output = []
    for t_str in read_tasks_file_cb():
        curr_t = {}
        username, title, description, due_date, asigned_date, completed = t_str.split(
            ";"
        )
        curr_t["username"] = username
        curr_t["title"] = title
        curr_t["description"] = description
        curr_t["due_date"] = datetime.strptime(due_date, DATETIME_STRING_FORMAT)
        curr_t["assigned_date"] = datetime.strptime(
            asigned_date, DATETIME_STRING_FORMAT
        )
        curr_t["completed"] = True if completed == "Yes" else False
        output.append(curr_t)
    return output


def populate_user_list(read_users_file_cb):
    """
    reads the contants of users.txt. an object of user is created and stored in a list.
    param: read_users_file_cb - provides the contents of users.txt.
    returns: an array of user objects.
    """
    output = []
    for u_str in read_users_file_cb():
        curr_u = {}
        username, password = u_str.split(";")
        curr_u["username"] = username
        curr_u["password"] = password
        output.append(curr_u)
    return output


"""HELPER CODE"""


def contains(list, filter_cb):
    """
    checks a list for a given condition.
    param: list - generic list to iterate over.
    param: filter_cb - function which provides a test the list items
    returns: boolean - value depends on test passing or failing
    """
    for x in list:
        if filter_cb(x):
            return True
    return False


def info_box(msg):
    """
    places a box around a string
    param: msg - the message to box
    returns: boxed in string
    """
    line = ""
    out_str = ""
    for x in range(len(msg) + 4):
        line += "-"
    out_str += f"\n{line}\n! {msg} !\n{line}"
    return out_str


def input_user(msg, users, should_exist=True):
    """
    checks if the user should be or should not be registered.
    depending on the should_exist paramater.
    param: msg - input instructions.
    param: users - list of user objects.
    param: should exist - flips the logic.
    returns: the username.
    """
    valid_user = False
    while not valid_user:
        username = input(msg).strip().lower()
        if contains(users, lambda x: x["username"] == username) == should_exist:
            valid_user = True
        else:
            if should_exist:
                print(info_box("User does not exist."))
            else:
                print(info_box("Username already exists"))
    return username


def input_date():
    """
    ensures the user enters a date in the correct date format.
    returns: the data.
    """
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print(info_box("Invalid datetime format. Please use the format specified"))
    return due_date_time


def check_date(input_date_cb, today):
    """
    ensures the user enters a date in the correct date format and after today's data.
    param: input_date_cb - checks the date format.
    param: today - today's date.
    returns: the data.
    """
    d = input_date_cb()
    while True:
        if d <= today:
            print(info_box(f"Invalid date. Date must be after today's date"))
            d = input_date_cb()
        else:
            break
    return d


def input_int(msg):
    """
    ensures the user enters an integer.
    param: msg - input instructions.
    """
    while True:
        try:
            value = int(input(msg))
            return value
        except ValueError:
            print("Error - Please enter a number")
            continue


def filter_user_tasks(task_list, username):
    """
    filters all tasks down into a list of tasks related to one user.
    only tasks that havent been completed are included.
    param: task_list - list of all task objects.
    param: username - the user's name
    returns:  [{"task_num": assigned task number, "idx_num": the index number in the main task_list, "task_info": {an object of all the task info} }]
    """
    output = []
    filtered_tasks = [
        (idx, task)
        for idx, task in enumerate(task_list)
        if (task["username"] == username and task["completed"] == False)
    ]
    for task_num, idx_task in enumerate(filtered_tasks, start=1):
        output.append(
            {"task_num": task_num, "idx_num": idx_task[0], "task_info": idx_task[1]}
        )
    return output


def get_task(t_num, t):
    """
    creates a task string
    param: t_num - the task number.
    param: t - the task object.
    returns: task string.
    """
    if t_num == "#":
        task = f"\nTask Completed: {t['completed']}\n"
    else:
        task = f"\nTask Number: {t_num}\n"
    task += f"Task: \t\t {t['title']}\n"
    task += f"Assigned to: \t {t['username']}\n"
    task += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    task += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    task += f"Task Description: \n {t['description']}\n\n"
    return task


def get_task_data(list_of_tasks):
    """
    calculates the number of tasks, number of completed tasks, number of uncompleted tasks and
    the number of tasks overdue.
    param: list_of_tasks - list of task objects.
    returns: [num_tasks, num_completed, num_incomplete, num_overdue].
    """

    today_date = date.today()
    output = []
    if len(list_of_tasks) < 1:
        return output

    # number of tasks
    output.append(len(list_of_tasks))
    # number of completed tasks
    output.append(len([task for task in list_of_tasks if task["completed"] == True]))
    # number of uncompleted  tasks
    output.append(output[0] - output[1])
    # number of overdue tasks
    output.append(
        len(
            [
                task
                for task in list_of_tasks
                if task["completed"] == False and today_date > task["due_date"].date()
            ]
        )
    )
    return output


def format_task_stats(task_stats):
    """
    formats a string of task statistics and writes to task_overview.txt.
    param: task_stats - a list containing the task statistics.
    """
    out_str = ""
    out_str += "\n-----------------TASK STATS-------------------\n"
    out_str += f"The total number of tasks -             {task_stats[0]}\n"
    out_str += f"The total number of completed tasks -   {task_stats[1]}\n"
    out_str += f"The total number of uncompleted tasks - {task_stats[2]}\n"
    out_str += f"The total number of overdue tasks -     {task_stats[3]}\n"
    out_str += f"The percentage of incomeplete tasks -   {task_stats[4]}%\n"
    out_str += f"The percentage of overdue tasks -       {task_stats[5]}%\n"
    out_str += "-----------------------------------------------\n"

    """write to file here"""
    write_task_overview_file(out_str)


def format_user_stats(user_stats):
    """
    formats a string of user statistics and writes to user_overview.txt.
    param: user_stats - a list containing the user statistics.
    """
    out_str = ""
    # for the heading
    g_stats = user_stats[:2]
    out_str += "\n-----------------USER STATS--------------------\n"
    out_str += f"The total number of users -             {g_stats[0]}\n"
    out_str += f"The total number of tasks -             {g_stats[1]}\n\n"
    # for each user
    u_stats = user_stats[2:]
    for sl in u_stats:
        out_str += "-----------------------------------------------\n"
        out_str += f"                 {sl[0]}\n".upper()
        out_str += f"Number of tasks assigned -              {sl[1]}\n"
        out_str += f"The percentage of tasks assigned -      {sl[5]}%\n"
        out_str += f"The percentage of completed tasks -     {sl[6]}%\n"
        out_str += f"The percentage of uncompleted tasks -   {sl[7]}%\n"
        out_str += f"The percentage of overdue tasks -       {sl[8]}%\n"
        out_str += "-----------------------------------------------\n"

    """write to file here"""
    write_user_overview_file(out_str)


"""MAIN CODE"""


def login(user_list):
    """
    checks if a valid user and password.
    param: user_list - a list of user objects.
    returns: name of the user.
    """
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ").strip()
        curr_pass = input("Password: ").strip()
        if not contains(user_list, lambda x: x["username"] == curr_user):
            print(info_box("User does not exist"))
            continue
        elif not contains(user_list, lambda x: x["password"] == curr_pass):
            print(info_box("Wrong password"))
            continue
        else:
            print(info_box("Login Successful!"))
            logged_in = True
    return curr_user


def reg_user(user_list):
    """
    registers a new user if not already registered.
    a copy of user_list is return to avoid mutation.
    param: user_list - a list of user objects.
    returns: a copy of the user_list.
    """
    # check the user is not already registered
    new_user = input_user("New Username: ", user_list, False)
    passwords_match = False
    while not passwords_match:
        new_password = input("New Password: ").strip()
        confirm_password = input("Confirm Password: ").strip()
        if new_password == confirm_password:
            passwords_match = True
        else:
            print(info_box("Passwords do no match"))
    user_obj = {"username": new_user, "password": new_password}
    # make a copy and append new user
    user_copy = copy.deepcopy(user_list)
    user_copy.append(user_obj)
    print(info_box(f"You have successfully registered {new_user}"))
    return user_copy


def delete_user(user_list, task_list):
    """
    deletes a user if no tasks assigned.
    a copy of user_list is return to avoid mutation.
    param: user_list - a list of user objects.
    param: task_list - a list of task objects.
    returns: -1 if the user has tasks assigned or no user confirmation
             else returns a copy of the user_list.
    """
    # check the user is registered
    user = input_user("Name of user to delete :", user_list)
    # check if the user has any tasks assigned
    user_tasks = filter_user_tasks(task_list, user)
    if len(user_tasks) > 0:
        print(info_box("This user has tasks assign, cannot delete"))
        return -1
    else:
        # get index number of user
        index = next(
            (i for i, item in enumerate(user_list) if item["username"] == user), -1
        )
        # make a copy and delete the user
        user_copy = copy.deepcopy(user_list)
        del user_copy[index]

    # no actual deletion is made before user confirmation
    print(info_box(f"Are you sure you want to delete {user} ? "))
    confirm = input("Type 'yes' to confirm :").strip()
    if confirm == "yes":
        print(info_box(f"You have deleted {user}"))
        return user_copy
    return -1


def add_task(task_list, user_list):
    """
    adds a tasks for a registered user.
    param: task_list - a list of task objects.
    param: user_list - a list of user objects.
    returns: a copy of the task_list.
    """
    # check the user is registered
    task_username = input_user("Name of person assigned to task :", user_list)
    task_title = input("Title of task: ").strip()
    task_description = input("Description of task: ").strip()
    curr_date = datetime.today()
    # checks the date entered is after today's date
    due_date_time = check_date(input_date, curr_date)
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False,
    }
    # make a copy and append new task
    task_copy = copy.deepcopy(task_list)
    task_copy.append(new_task)
    print(info_box(f"New task assigned to {task_username}"))
    return task_copy


def edit_my_task(task, users):
    """
    allows user to edit certain properties of a task.
    param: task - a task objects.
    param: users - a list of user objects.
    returns: a copy of a task object or -1.
    """
    task_copy = copy.deepcopy(task["task_info"])
    choice = input(view_task_menu()).strip().lower()
    if choice == "mc":
        task_copy["completed"] = True
        print(
            info_box(
                f"Task - {task['task_info']['title']} - has been marked as complete"
            )
        )
    elif choice == "et":
        # if choice == "et" and user == "admin":
        selected = input(view_edit_task_menu())
        if selected == "cu":
            new_user = input_user("New user for this task :", users)
            task_copy["username"] = new_user
        elif selected == "cd":
            new_date = check_date(input_date, datetime.today())
            task_copy["due_date"] = new_date
        elif selected == "e":
            return -1
        print(info_box(f"Task - {task['task_info']['title']} - has been edited"))
    elif choice == "e":
        return -1
    return task_copy


def view_mine(task_list, user_list, user):
    """
    allows user to view all assigned tasks and
    edit a task.
    param: task_list - list of task objects.
    param: user_list - list of user objects.
    param: user - current user.
    returns: a copy of a task object or -1.
    """
    # get all tasks for the user
    user_tasks = filter_user_tasks(task_list, user)
    # check if any tasks available
    if not len(user_tasks):
        print(info_box("You don't have any tasks"))
        return -1
    # displays all tasks for user
    view_my_tasks(user_tasks, get_task)

    # get task number
    task_number = input_int("Enter number of task to select or -1 for main menu: ")
    if task_number == -1:
        return -1

    edited_task = {}
    # check if valid task number
    if task_number <= 0 or task_number > len(user_tasks):
        print(info_box("Not a valid task number"))
        return -1

    # display the selected task
    view_task(user_tasks[task_number - 1])

    # edit the selected task
    edited_task = edit_my_task(user_tasks[task_number - 1], user_list)

    # if any edits have been made
    if edited_task != -1:
        task_copy = copy.deepcopy(task_list)
        task_copy[user_tasks[task_number - 1]["idx_num"]] = edited_task
        return task_copy
    else:
        return -1


"""REPORT CODE"""


def gen_reports(task_list, user_list):
    """
    allows user to generate task and user reports and
    save in task_overview.txt and user_overview.txt.
    param: task_list - list of task objects.
    param: user_list - list of user objects.
    """
    if not len(task_list):
        print(info_box("Cannot generate any reports. No tasks are available"))
        return

    """for task_overview.txt"""
    # all_task_data = list[num_tasks, num_completed, num_incomplete, num_overdue]
    all_task_data = get_task_data(task_list)

    # pct incomplete
    all_task_data.append(round((all_task_data[2] / all_task_data[0]) * 100))
    # pct overdue
    all_task_data.append(round((all_task_data[3] / all_task_data[0]) * 100))

    # creates a readable format and writes to task_overview.txt
    format_task_stats(all_task_data)

    """for user_overview.txt"""
    all_user_data = []
    all_user_data.append(len(user_list))
    all_user_data.append(all_task_data[0])
    for user in user_list:
        # get all assigned tasks for user
        tasks_for_user = [
            task for task in task_list if task["username"] == user["username"]
        ]
        if len(tasks_for_user) > 0:
            user_task_data = get_task_data(tasks_for_user)
            user_task_data.insert(0, user["username"])
            # pct assigned
            user_task_data.append(round((user_task_data[1] / all_task_data[0]) * 100))
            # pct complete
            user_task_data.append(round((user_task_data[2] / all_task_data[0]) * 100))
            # pct incomplete
            user_task_data.append(round((user_task_data[3] / all_task_data[0]) * 100))
            # pct overduer
            user_task_data.append(round((user_task_data[4] / all_task_data[0]) * 100))
            all_user_data.append(user_task_data)

    # creates a readable format and writes to user_overview.txt
    format_user_stats(all_user_data)


def admin_save(user_list, save_users, task_list, save_tasks):
    """
    called when admin logs out.
    param: user_list - list of user objects.
    param: save_users - boolean flag.
    param: task_list - list of task objects.
    param: save_tasks - boolean flag.
    """
    if save_users:
        write_users_file(user_list)
    if save_tasks:
        write_tasks_file(task_list)
    if save_users or save_tasks:
        print(info_box("All changes saved"))
    print(info_box("Logged out as admin"))


def user_save(task_list, save_tasks, user):
    """
    called when a user logs out.
    param: task_list - list of task objects.
    param: save_tasks - boolean flag.
    param: user - user logged in.
    """
    if save_tasks:
        write_tasks_file(task_list)
        print(info_box("All changes saved"))
    print(info_box(f"Logged out as {user}"))


"""MAIN FUNCTION"""


def task_manager():
    """
    main program loop.
    """
    user_list = []  # main store for user data
    task_list = []  # main store for task data
    save_users = False  # set to true when user_list needs updating
    save_tasks = False  # set to true when task_list needs updating

    # setup
    user_list = populate_user_list(read_users_file)
    task_list = populate_task_list(read_tasks_file)

    print("\nWelcome to DO-IT-NOW! Task Management System")
    print("--------------------------------------------")
    while True:
        c = input("\nEnter 'l' to login 'e' to exit : ").strip()
        if c == "l":
            user = login(user_list)

            logged_in = True
            while logged_in:
                choice = input(view_main_menu(user)).strip().lower()
                if user == "admin":
                    match choice:
                        case "r":
                            user_list = reg_user(user_list)
                            save_users = True
                        case "vu":
                            view_users(user_list)
                        case "du":
                            result = delete_user(user_list, task_list)
                            if result != -1:
                                user_list = result
                                save_users = True
                        case "a":
                            task_list = add_task(task_list, user_list)
                            save_tasks = True
                        case "va":
                            view_all(task_list, get_task, info_box)
                        case "vm":
                            result = view_mine(
                                task_list,
                                user_list,
                                user,
                            )
                            if result != -1:
                                task_list = result
                                save_tasks = True
                        case "gr":
                            gen_reports(task_list, user_list)
                        case "ds":
                            view_stats(
                                read_task_overview_file,
                                read_user_overview_file,
                                info_box,
                            )
                        case "lo":
                            admin_save(user_list, save_users, task_list, save_tasks)
                            logged_in = False
                        case _:
                            print(info_box("Invalid choice"))
                            continue
                else:
                    match choice:
                        case "vm":
                            result = view_mine(
                                task_list,
                                user_list,
                                user,
                            )
                            if result != -1:
                                task_list = result
                                save_tasks = True
                        case "lo":
                            user_save(task_list, save_tasks, user)
                            logged_in = False
                        case _:
                            print(info_box("Invalid choice"))
                            continue
        elif c == "e":
            print(info_box("Good Bye :)"))
            exit()
        else:
            print(info_box("Invalid choice"))


"""MAIN PROGRAM"""
task_manager()
