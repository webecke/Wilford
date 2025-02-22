"""
Copyright (c) 2024 ForestBlue Development. All Rights Reserved.
This file is part of the "Wilford" program, which is licensed under the MIT License.
View it on GitHub: https://github.com/DallinFromEarth/Wilford
"""
import shutil
import sys

# ANSI escape codes
ITALIC_START = '\x1B[3m'
ITALIC_END = '\x1B[0m'

CONTEXT: str = ""


def set_context(context:str):
    global CONTEXT
    CONTEXT = context


def get_input(input_prompt="", can_skip=False):
    try:
        field = input(input_prompt + "\n> ").strip()
        field_lower = field.lower()

        if (not can_skip) and field == "":
            print("No input provided")
            return get_input(input_prompt, can_skip)
        elif (field_lower == "home") or (field_lower == "main"):
            print("\n\n\n")
            print("!!! Returning to the main menu !!!")
            raise ReturnToMainMenu
        elif field_lower == "restart":
            restart_program()
            return get_input(input_prompt, can_skip)
        elif field_lower == "help":
            show_help_menu()
            return get_input(input_prompt, can_skip)
        elif field_lower == "terms":
            display_terms()
            return get_input(input_prompt, can_skip)
        elif field_lower == "quit":
            close_program()
            return get_input(input_prompt, can_skip)

        return field
    except EOFError:
        print("\nError reading input. Please try again.")
        return get_input(input_prompt, can_skip)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        close_program()
        return get_input(input_prompt, can_skip)

def get_boolean_input(input_prompt):
    try:
        print(input_prompt)
        verification = get_input("y -> yes, anything else -> no", True)
        return verification.lower().strip() == 'y'
    except Exception as e:
        print(f"Error getting boolean input: {e}")
        return False


def show_help_menu():
    print("=" * 21)
    print("  Wilford Help Menu")
    print("=" * 21 + "\n")

    print("UNIVERSAL")
    print(make_italic("*these can be called anytime*"))
    print("'home' or 'main' - return to the main menu")
    print("'restart' - restart the app")
    print("'help' - view the available commands")
    print("'terms' - view the terms of using this program")
    print("'quit' - close the program (it will confirm before quiting)")
    print()

    if CONTEXT == "main":
        print("MAIN MENU")
        print("'speakers' - view the list of speakers")
        print("'speakers {name}' - search the list of speakers")
        print("'download' - open the download dialogue to download conference talks")
        print("'download {name}' - open the download dialogue for that speaker")
        print("'config' - open the config menu")
        print()

    elif CONTEXT == "download":
        print("DOWNLOAD MENU")
        print(make_italic("The download menu will step you through what you need to type"))
        print()

    elif CONTEXT == "config":
        print("CONFIG MENU")
        print("'view' - view the full set of config settings")
        print("'default' - reset config to default settings")
        print("'set' - set a config value " + make_italic("(it will then walk you through setting a config value)"))
        print("'set {config value}' - set that specific config value")
        print()


def display_terms():
    try:
        with open('terms.txt', 'r') as file:
            print("=" * 20)
            print(file.read())
            print("=" * 20)
    except FileNotFoundError:
        print("Terms of use file not found.")
    except IOError:
        print("An error occurred while reading the terms of use file.")


def close_program():
    try:
        verification = get_boolean_input("Are you sure you want to quit?")
        if verification:
            print("Thank you for using Wilford")
            sys.exit(0)
        else:
            return None
    except Exception as e:
        print(f"Error during program closure: {e}")
        sys.exit(1)


def restart_program():
    verification = get_boolean_input("Are you sure you want to restart?")
    if verification:
        raise RestartApp
    else:
        return None


def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    padding = (terminal_width - len(text)) // 2
    return " " * padding + text


def print_centered(text):
    print(center_text(text))


def make_italic(text):
    return ITALIC_START + text + ITALIC_END


class ReturnToMainMenu(Exception):
    pass


class RestartApp(Exception):
    pass
