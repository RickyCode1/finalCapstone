def view_main_menu(user):
    """
    creates the main menu view.
    param: user - the current logged in user
    return: the correct menu for the current user
    """
    if user == "admin":
        menu = """Select one of the following options below:

       USER OPTIONS              TASK OPTIONS              REPORT OPTIONS 

    r -  Register a user       a -  Add a task          gr - Generate reports
    vu - View all users        va - View all tasks      ds - Display statistics
    du - Delete a user         vm - View my task

    lo - Logout
    :  """
    else:
        menu = """Select one of the following options below:
    vm - View my task
    lo - logout
    :  """
    return menu


def view_task_menu():
    """
    creates the menu for tasks.
    return: the task view menu
    """
    menu = """Select one of the following options below:
    mc - Mark as complete
    et - Edit my task 
    e -  Exit
    :  """
    return menu


def view_edit_task_menu():
    """
    creates the menu for editing tasks.
    return: the edit task view menu
    """
    menu = """Select one of the following options below:
        cu - Change user assigned to task
        cd - Change the due date
        e -  Exit
        :  """
    return menu


def view_users(user_list):
    """
    displays a list of user names.
    param: user_list - list of user objects.
    """
    user_str = "All registed users\n\n"
    for user in user_list:
        user_str += f"    {user['username']}\n"
    print(user_str)


def view_all(task_list, get_task_cb, info_box_cb):
    """
    displays a message if there are no tasks to display else
    all current tasks are displayed.
    param: task_list - list of task objects.
    param: get_task_cb - function which consumes the task object returns formatted string.
    param: info_box_cb - function which adds a box around the str argument.
    """
    if not len(task_list):
        print(info_box_cb("No tasks available"))
    for task in task_list:
        print(get_task_cb("#", task))


def view_my_tasks(user_tasks, get_task_cb):
    """
    displays all current tasks assigned to the current logged in user.
    param: user_tasks -  list of task objects. each object only contains task data for the current logged in user.
    param: get_task_cb - function which consumes the task object returns formatted string.
    """
    task_str = ""
    for task in user_tasks:
        task_str += get_task_cb(task["task_num"], task["task_info"])
    print(task_str)


def view_task(task):
    """
    displays information about a single task assigned to the current logged in user.
    namely the task number, time remaining to complete and the task description.
    param: task - a task object.
    """
    info = task["task_info"]
    td = info["due_date"] - info["assigned_date"]
    dur_val = td.days
    dur_unit = "days" if dur_val > 1 else "day"
    task_str = ""
    task_str += "\n***********************************************\n"
    task_str += f"You selected task number {task['task_num']}"
    task_str += f"\nYou have {dur_val} {dur_unit} to complete this task\n"
    task_str += "\n               ASSIGNED TASK"
    task_str += f"\n{info['description']}"
    task_str += "\n***********************************************\n"
    print(task_str)


def view_stats(
    read_task_overview_file_cb,
    read_user_overview_file_cb,
    info_box_cb,
):
    """
    displays all stats about tasks and users or a message if nothing to display.
    param: read_task_overview_file_cb - function which returns the file contents.
    param: read_user_overview_file_cb - function which returns the file contents.
    """
    task_stats = read_task_overview_file_cb()
    user_stats = read_user_overview_file_cb()
    if task_stats == -1 or user_stats == -1:
        print(info_box_cb("No statistics to display. Type gr to generate reports"))
    else:
        print(task_stats)
        print(user_stats)
