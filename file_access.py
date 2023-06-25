import os
import sys

DATETIME_STRING_FORMAT = "%Y-%m-%d"
TASKS_PATH = "txt_files/tasks.txt"
USERS_PATH = "txt_files/users.txt"
TASKS_STATS_PATH = "txt_files/task_overview.txt"
USERS_STATS_PATH = "txt_files/user_overview.txt"


# *********************************TASKS************************************#


def read_tasks_file():
    """
    creates tasks.txt file if it doesn't exist.
    reads every line of the file.
    if there is an exception an error message is displayed and the program terminates.
    returns: the file contents.
    """
    if not os.path.exists(TASKS_PATH):
        with open(TASKS_PATH, "w") as default_file:
            pass
    try:
        with open(TASKS_PATH, "r") as f:
            task_data = f.read().split("\n")
            task_data = [t for t in task_data if t != ""]
        return task_data
    except (FileNotFoundError, OSError):
        print("Fatal error opening file: 'tasks.txt'")
        sys.exit(1)


def write_tasks_file(task_list):
    """
    writes to tasks.txt file with new task data.
    if there is an exception an error message is displayed.
    param: task_list - list of objects. each object is the task data.
    """
    try:
        with open(TASKS_PATH, "w") as f:
            task_list_to_write = []
            for task_obj in task_list:
                str_attrs = [
                    task_obj["username"],
                    task_obj["title"],
                    task_obj["description"],
                    task_obj["due_date"].strftime(DATETIME_STRING_FORMAT),
                    task_obj["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if task_obj["completed"] else "No",
                ]
                task_list_to_write.append(";".join(str_attrs))
            f.write("\n".join(task_list_to_write))
    except (FileNotFoundError, OSError):
        print("Error opening file: 'tasks.txt'")


# *********************************USERS************************************#


def read_users_file():
    """
    creates users.txt if it doesn't exist.
    reads every line of the file.
    if there is an exception an error message is displayed and the program terminates.
    returns: the file contents.
    """
    if not os.path.exists(USERS_PATH):
        with open(USERS_PATH, "w") as default_file:
            default_file.write("admin;password")
    try:
        with open(USERS_PATH, "r") as f:
            user_data = f.read().split("\n")
            user_data = [u for u in user_data if u != ""]
        return user_data
    except (FileNotFoundError, OSError):
        print("Fatal error opening file: 'user.txt'")
        sys.exit(1)


def write_users_file(user_list):
    """
    writes to users.txt file with new user data.
    if there is an exception an error message is displayed.
    param: user_list - list of objects. each object is the user data.
    """
    users = ""
    for user_obj in user_list:
        users += f"{user_obj['username']};{user_obj['password']}\n"
    try:
        with open(USERS_PATH, "w") as f:
            f.write(users)
    except (FileNotFoundError, OSError):
        print("Error opening file: 'user.txt'")


# *********************************STATS************************************#


def read_task_overview_file():
    """
    returns -1 if task_overview.txt" doesn't exist or the contents of the file.
    if there is an exception an error message is displayed.
    """
    if not os.path.exists(TASKS_STATS_PATH):
        return -1
    try:
        with open(TASKS_STATS_PATH, "r") as f:
            report = f.read()
        return report
    except (FileNotFoundError, OSError):
        print("Error opening file: 'task_overview.txt'")


def write_task_overview_file(report):
    """
    writes to task_overview.txt" with new task data
    if there is an exception an error message is displayed.
    param: report - string of report data.
    """
    try:
        with open(TASKS_STATS_PATH, "w") as f:
            f.write(report)
    except (FileNotFoundError, OSError):
        print("Error opening file: 'task_overview.txt'")


def read_user_overview_file():
    """
    returns -1 if user_overview.txt" doesn't exist or the contents of the file.
    if there is an exception an error message is displayed.
    """
    if not os.path.exists(USERS_STATS_PATH):
        return -1
    try:
        with open(USERS_STATS_PATH, "r") as f:
            report = f.read()
        return report
    except (FileNotFoundError, OSError):
        print("Error opening file: 'user_overview.txt'")


def write_user_overview_file(report):
    """
    writes to user_overview.txt" with new user data
    if there is an exception an error message is displayed.
    param: report - string of report data
    """
    try:
        with open(USERS_STATS_PATH, "w") as f:
            f.write(report)
    except (FileNotFoundError, OSError):
        print("Error opening file: 'user_overview.txt'")
