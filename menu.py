import time
import curses
import sys
import textwrap
from write_mail import Write_Mail_UI
from curses.textpad import rectangle
from get_credentials import Credentials
import getpass
import login



'''Temporary function to check if passing function to dictionary is working'''
# TODO: Remove this later


def temp(stdscr):
    # Get height and width of screen
    h, w = stdscr.getmaxyx()

    # Print that particular item at center of screen
    stdscr.clear()
    msg = "You entered into temporary mode!"
    x_pos = w // 2 - len(msg) // 2
    y_pos = h // 2
    stdscr.addstr(y_pos, x_pos, msg)
    stdscr.refresh()

    # If backspace is pressed go back to menu
    # TODO: Later will need to switch this to some other key
    key = stdscr.getch()

    # While key is not backspace take input from user
    # TODO: Later delete this might cause problem
    while key != curses.KEY_BACKSPACE:
        key = stdscr.getch()


class Menu:
    '''Utility Menu class which displays menu on screen

    Arguements \t
    stdscr: Stdscr of curses \t
    menu_options: Options available for menu \t
    '''

    # <-------------------------------------------------Variables------------------------------------------------->
    __curr_index = 0  # Current position in menu
    __stdscr = None  # Stdscr variable of curses
    __menu = []  # Available menu options
    __is_main = False
    # TODO: Change this message later
    __screen_size_msg = "Screen size is too small! Please increase screen size"
    __title = ""

    # Confirm Email Variables
    __curr_confirm_index = 0
    __confirm_menu = ["YES", "NO"]

    # <---------------------------------------------------Functions------------------------------------------------->

    def __init__(self, stdscr, menu_options, title, isMain=False):
        curses.curs_set(0)

        self.__stdscr = stdscr
        self.__menu = menu_options
        self.__title = " " + title.upper() + " "
        self.__is_main = isMain
        self.__setup_color_pairs()
        self.__display_menu()

        while 1:
            key = self.__stdscr.getch()

            # Get the key pressed by user and do action accordingly
            if key == curses.KEY_UP and self.__curr_index != 0:
                # Decrease the index if up key is pressed
                self.__curr_index -= 1

            elif key == curses.KEY_DOWN and self.__curr_index != len(self.__menu) - 1:
                # Increase the index if down key is pressed
                self.__curr_index += 1

            elif key == curses.KEY_ENTER or key in [10, 13]:
                # If the element is last in array then it is exit signal
                if self.__curr_index == len(self.__menu) - 1:
                    # If it is main menu then exit out of the app
                    if self.__is_main:
                        sys.exit()
                    # If not go back
                    else:
                        break
                elif self.__curr_index == len(self.__menu) - 2 and self.__is_main:
                    self.__set_confirm_email_bar()
                    break
                else:
                    self.__on_enter_pressed()
                    continue

            self.__display_menu()

    # <-------------------------------------------Private Functions------------------------------------->

    def __display_menu(self):
        '''Main function which displays menu'''

        # Get height and width of screen (Required for centering menu)
        h, w = self.__stdscr.getmaxyx()

        # Variable to store maximum length
        max_len = 0

        # Clear the screen
        self.__stdscr.clear()

        y_start = h // 2 - len(self.__menu) // 2

        # Iterate over each option in menu
        for index, item in enumerate(self.__menu):

            # Determine the center position of menu
            x_pos = w // 2 - len(item['title']) // 2
            y_pos = y_start + index

            # Check if index is of currently selected item if yes make its background white
            if self.__curr_index == index:
                self.__stdscr.attron(curses.color_pair(1))

            title = "  " + item['title'] + "  "

            # Find the maximum length title for padding
            if max_len < len(title):
                max_len = len(title)

            # Print string on screen
            self.__stdscr.addstr(y_pos, x_pos, title)

            # turn off the attribute
            if self.__curr_index == index:
                self.__stdscr.attroff(curses.color_pair(1))

        # Start position of menu
        y_end = h // 2 + len(self.__menu) // 2
        x_start = w // 2 - max_len // 2
        x_end = w // 2 + max_len // 2

        # To add padding to menu
        if x_start - 4 > 1:
            x_start -= 4
        else:
            x_start -= 2

        if x_start + 8 < w - 1:
            x_end += 8
        else:
            x_start += 2

        if y_start - 4 > 1:
            y_start -= 4
        else:
            y_start -= 2

        if y_end + 4 < h - 1:
            y_end += 4
        else:
            y_end += 1

        try:
            # Show the title of menu and rectangle
            rectangle(self.__stdscr, y_start, x_start, y_end, x_end)
            self.__stdscr.attron(curses.A_BOLD)
            self.__stdscr.addstr(
                y_start, w // 2 - len(self.__title) // 2 + 2, self.__title)
            self.__stdscr.attroff(curses.A_BOLD)

            # Refresh the screen
            self.__stdscr.refresh()
        except:
            # If it is not possible to show the menu
            # then show the message that it cannot be shown on the screen
            self.__stdscr.clear()
            wrapper = textwrap.TextWrapper(width=w-2)
            error_msgs = wrapper.wrap(self.__screen_size_msg)
            for index, msg in enumerate(error_msgs):
                x_pos = w // 2 - len(msg) // 2
                y_pos = h // 2 + index
                self.__stdscr.addstr(y_pos, x_pos, msg)
            self.__stdscr.refresh()

    def __on_enter_pressed(self):
        '''When enter is pressed for particular item'''

        if self.__menu[self.__curr_index]['args'] == "STDSCR_NR":
            self.__menu[self.__curr_index]['Function']()
        elif self.__menu[self.__curr_index]['args'] != None:
            arguements = self.__menu[self.__curr_index]['args']
            arg1, arg2 = arguements
            self.__menu[self.__curr_index]['Function'](
                self.__stdscr, arg1, arg2)
        else:
            # TODO: Also pass arguements to this function
            # Call the desired function
            self.__menu[self.__curr_index]['Function'](self.__stdscr)

        # Display menu again after pressing enter
        self.__display_menu()

    # <--------------------------------------------Utility functions---------------------------------------->

    def __setup_color_pairs(self):
        '''Function to setup color pairs required'''

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def __display_bottom_bar_menu(self):
        '''To display UI of confirm email bottom bar for logout'''

        h, _ = self.__stdscr.getmaxyx()

        start_h = h - 3
        for index, item in enumerate(self.__confirm_menu):

            y_pos = start_h + index
            # Check if index is of currently selected item if yes make its background white
            if self.__curr_confirm_index == index:
                self.__stdscr.attron(curses.color_pair(1))

            # Print string on screen
            self.__stdscr.addstr(y_pos, 2, item)

            if self.__curr_confirm_index == index:
                self.__stdscr.attroff(curses.color_pair(1))

        self.__stdscr.refresh()

    def __set_confirm_email_bar(self):
        '''Setup confirm email bar for logout'''

        h, w = self.__stdscr.getmaxyx()
        title = " Do you want to logout ".upper()
        rectangle(self.__stdscr, h - 4, 0, h - 1, w - 2)
        self.__stdscr.attron(curses.A_BOLD)
        self.__stdscr.addstr(h - 4, 1, title)
        self.__stdscr.attroff(curses.A_BOLD)
        self.__display_bottom_bar_menu()

        while 1:
            key = self.__stdscr.getch()

            if key == curses.KEY_UP and self.__curr_confirm_index != 0:
                self.__curr_confirm_index -= 1
            elif key == curses.KEY_DOWN and self.__curr_confirm_index != len(self.__confirm_menu) - 1:
                self.__curr_confirm_index += 1

            # TODO: Do the functionality according to choice of user
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if self.__curr_confirm_index == 0:
                    # Remove the .env file
                    # Get the environment filepath
                    cred = Credentials()
                    cred.remote_credentials()
                    # sys.exit()
                    login.LOGIN_UI(self.__stdscr)
                break

            self.__display_bottom_bar_menu()


menu_strings = ["Show email", "Logout", "Exit"]


def main(stdscr):
    menu = [{'title': "Write mail", 'Function': Write_Mail_UI}]
    for item in menu_strings:
        # Alert: Function will expect first arguement as stdscr for sure
        menu.append({'title': item, 'Function': temp})
    Menu(stdscr, menu, "Sample", isMain=True)


if __name__ == "__main__":
    curses.wrapper(main)
