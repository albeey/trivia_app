"""
Description
"""

import requests
import random
import html

# returns a dictionary with two keys, "response_code" and "results"
NUM_OF_CHOICES = 3
MIN_QUESTIONS = 1
MAX_QUESTIONS = 10


def main():
    score = {"Film 🎬": {"rounds_played": 0, "total_questions": 0, "correct_answers": 0},
             "Computers 💻": {"rounds_played": 0, "total_questions": 0, "correct_answers": 0},
             "Geography 🌎": {"rounds_played": 0, "total_questions": 0, "correct_answers": 0},
             "Animals 🐱": {"rounds_played": 0, "total_questions": 0, "correct_answers": 0},
             "Music 🎵": {"rounds_played": 0, "total_questions": 0, "correct_answers": 0}}

    has_played_at_least_once = False
    game_over = False

    print_title()

    while not game_over:
        menu = main_menu()
        menu_selection = get_user_menu_input(menu)

        if menu_selection == "a":
            play(score)
            if not has_played_at_least_once:
                has_played_at_least_once = True
        elif menu_selection == "b":
            print_stats(score)
        else:
            game_over = True
            end_game(score, has_played_at_least_once)


def print_title():
    """
    prints an ASCII text banner
    :return: None
    """
    print("""\
    ████████╗██████╗ ██╗██╗   ██╗██╗ █████╗      ██████╗  █████╗ ███╗   ███╗███████╗
    ╚══██╔══╝██╔══██╗██║██║   ██║██║██╔══██╗    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
       ██║   ██████╔╝██║██║   ██║██║███████║    ██║  ███╗███████║██╔████╔██║█████╗  
       ██║   ██╔══██╗██║╚██╗ ██╔╝██║██╔══██║    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  
       ██║   ██║  ██║██║ ╚████╔╝ ██║██║  ██║    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝""")


def end_game(score, has_played_at_least_once):
    """
    thanks user for playing, if the user has played at least once round it will also print stats
    :param score: a dictionary
    :param has_played_at_least_once: bool value
    :return: None
    """
    print("Thank you for playing!")

    if has_played_at_least_once:
        print()
        print_stats(score)


def play(score):
    """
    plays one round of trivia
    :param score: dictionary containing current scores
    :return: None
    """
    trivia_dict, current_category = pick_category()
    num_of_questions = get_num_of_questions()
    round_score = play_round(trivia_dict, current_category, num_of_questions)
    adjust_score(score, num_of_questions, round_score, current_category)


def get_user_menu_input(menu):
    """
    prompts user for input
    :param menu: a dictionary containing a, b, c as keys
    :return: user_input as string
    """
    user_input = input("Your answer: ").lower()

    # checks if user_input is valid, must be a key in the menu dictionary
    while user_input not in menu:
        user_input = input("Please enter a valid option: ").lower()

    print()
    return user_input


def main_menu():
    """
    prints main menu options
    :return: dictionary containing menu keys and values
    """
    menu = {"a": "Play ▶️", "b": "Stats 📊", "c": "Exit 🚶"}
    print("What do you want to do?")

    for option in menu:
        print("   " + option + ") " + menu[option])

    return menu


def get_best_category(score):
    """
    :param score: a dictionary containing scores
    :return: the key with the highest value as a string
    """
    highest_val = 0
    key = ""

    for category in score:
        if score[category]["correct_answers"] > highest_val:
            key = category
            highest_val = score[category]["correct_answers"]

    return key


def print_stats(score):
    """
    prints users statistics
    :param score: a dictionary containing current scores
    :return: no returns
    """
    total_rounds = 0
    total_questions = 0
    correct_answers = 0
    best_category = get_best_category(score)

    for category in score:
        total_rounds += score[category]["rounds_played"]
        total_questions += score[category]["total_questions"]
        correct_answers += score[category]["correct_answers"]

    print("STATS")
    # if its equal to 0 means the users hasn't played
    if sum([total_rounds, total_questions, correct_answers]) == 0:
        print("You haven't played yet!")
    else:
        print("You played a total of", total_rounds, "games and out of", total_questions, "questions you answered to",
              correct_answers, "correctly!")
        if correct_answers > 0:
            print("Your best category is", best_category, " with", score[best_category]["correct_answers"],
                  "correct answers 👍")

    print()


def adjust_score(score, num_of_questions, last_round_score, category):
    """
    updates score dictionary, according with the last round scores
    :param score: a dictionary containing the previous scores that will be updated
    :param num_of_questions: how many questions were in a round, an int
    :param last_round_score: and int indicating how many questions the user got right
    :param category: a string, indicating the last played category
    :return: dictionary with updated scores
    """
    score[category]["rounds_played"] += 1
    score[category]["total_questions"] += num_of_questions
    score[category]["correct_answers"] += last_round_score
    return score


def get_num_of_questions():
    """
    prompts user to chose the amount of questions in a round, min 1, max 10 or random if left blank
    :return: returns an int
    """
    user_input = input("How many questions do you want (must a number 1-10 or leave blank for random)?: ")

    if len(user_input) == 0:
        print()
        return random.randint(MIN_QUESTIONS, MAX_QUESTIONS)

    # checks if the user_input is valid
    while not user_input.isnumeric() or (int(user_input) < MIN_QUESTIONS or int(user_input) > MAX_QUESTIONS):
        user_input = input("Enter a valid option (must be a number 1-10 or leave blank for random): ")

    print()
    return int(user_input)


def play_round(trivia_dict, category, number_of_questions):
    """
    :param trivia_dict: a dictionary containing all information for the trivia
    :param category: the chosen category
    :param number_of_questions: the number of questions to print out (length of round)
    :return: how many questions the user answered correctly
    """
    print("CATEGORY:", category)
    print(number_of_questions, "QUESTIONS")

    score = 0
    for i in range(number_of_questions):
        correct_answer, answer_dict = give_question(trivia_dict, i)
        user_answer = get_user_answer()
        is_user_correct = check_answer(user_answer, correct_answer, answer_dict)

        if is_user_correct:
            print("Correct!")
            score += 1
        else:
            print("Incorrect! The correct answer is:", correct_answer)

        print()
    print("Out of", number_of_questions, "questions you answered", score, "correctly.")
    print()

    return score


def pick_category():
    """
    prompts user to select a category
    :return: api of chosen category and the category name
    """
    # APIs
    film_trivia = requests.get("https://opentdb.com/api.php?amount=10&category=11&type=multiple")
    computer_trivia = requests.get("https://opentdb.com/api.php?amount=10&category=18&type=multiple")
    geography_trivia = requests.get("https://opentdb.com/api.php?amount=10&category=22&type=multiple")
    animal_trivia = requests.get("https://opentdb.com/api.php?amount=10&category=27&type=multiple")
    music_trivia = requests.get("https://opentdb.com/api.php?amount=10&category=12&type=multiple")

    # dictionary with the available categories
    categories = {
        "a": {"name": "Film", "emoji": "🎬", "api": film_trivia},
        "b": {"name": "Computers", "emoji": "💻", "api": computer_trivia},
        "c": {"name": "Geography", "emoji": "🌎", "api": geography_trivia},
        "d": {"name": "Animals", "emoji": "🐱", "api": animal_trivia},
        "e": {"name": "Music", "emoji": "🎵", "api": music_trivia},
    }

    # prints a "list" of the categories based on the dictionary "categories"
    print("Select a Category: ")
    for category in categories:
        print("   " + category + ") " + categories[category]["name"] + " " + categories[category]["emoji"])

    # gets input from the user
    user_choice = input("Your answer: ").lower()

    # checks if user input is valid, must be a key in the dictionary
    while user_choice not in categories:
        user_choice = input("Please enter a valid choice (a, b, c, d or e): ")
    print()

    return get_dict(categories[user_choice]["api"]), categories[user_choice]["name"] + " " + categories[user_choice][
        "emoji"]


def check_answer(user_answer, correct_answer, answers_dict):
    """
    checks in the answers_dict if the value of the key user_answer matches the correct_answer
    :param user_answer: contains user answer, string
    :param correct_answer: correct answer, string
    :param answers_dict: dictionary with keys a,b,c,d and 3 incorrect values and 1 correct value matching correct_answer
    :return: True/False
    """
    if correct_answer == answers_dict[user_answer]:
        return True
    return False


def get_user_answer():
    """
    prompts user for input (can only be a, b, c, d)
    :return: user answer as a string
    """
    valid_choices = ["a", "b", "c", "d"]

    user_answer = input("Your answer: ").lower()
    while user_answer not in valid_choices:
        user_answer = input("Please enter a valid choice (a, b, c or d): ").lower()

    return user_answer


def gen_dict_of_answers(answer_list):
    """
    fills dictionary keys with a random value from the list of answers
    :param answer_list: list of answers
    :return: a dictionary with a, b, c, d as keys and the elements of the list as values
    """
    options_dict = {"a": "", "b": "", "c": "", "d": ""}  # dictionary with empty keys a-d

    idx_used = []
    for key in options_dict:
        num = random.randint(0, NUM_OF_CHOICES)

        while num in idx_used:
            num = random.randint(0, NUM_OF_CHOICES)

        options_dict[key] = normalize(answer_list[num])
        idx_used.append(num)

    return options_dict


def normalize(string):
    """
    certain questions/answers include html characters, this converts them into regular character and removes whitespace
    :param string: string that possibly has an html character
    :return: normalized string
    """
    return html.unescape(string).strip()


def print_options(option_list, correct_answer):
    """
    :param option_list: a list of 3 incorrect answers
    :param correct_answer: a string with the correct answer
    :return: a dictionary with a, b, c, d as keys and each answer as value
    """
    option_list.append(correct_answer)  # appends the correct answer to the list of the incorrect answers
    answers = gen_dict_of_answers(option_list)

    # prints each key of the dictionary answers in the format: "   key) dictionary[key]"
    for key in answers:
        print("   " + key + ") " + normalize(answers[key]))

    return answers


def give_question(dictionary, q_num):
    """
    prints question and a list of a multiple choices for answers
    :param dictionary: dictionary, contains; a question, correct answer, 3 incorrect answers ,category,
    type and difficulty
    :param q_num: number of the question
    :return: returns a dictionary with all answers and the correct answer as a string
    """
    question = get_question(dictionary[q_num])
    answer = get_answer(dictionary[q_num])
    options = get_options(dictionary[q_num])

    print(str(q_num + 1) + ".", question)
    answers_dict = print_options(options, answer)
    return answer, answers_dict


def get_options(dictionary):
    """
    :param dictionary:
    :return: "incorrect_answers" key of type list, to use as the options of a multiple choice question
    """
    return dictionary["incorrect_answers"]


def get_answer(dictionary):
    """
    :param dictionary:
    :return: the "correct_answer" key from the passed dictionary
    """
    return normalize(dictionary["correct_answer"])


def get_question(dictionary):
    """
    :param dictionary:
    :return: the "question" key from the passed dictionary
    """
    return normalize(dictionary["question"])


def get_dict(obj):
    """
    :param obj:
    :return: list of dictionaries, each contains; a question, correct answer, 3 incorrect answers ,category,
    type and difficulty
    """
    return obj.json()["results"]


if __name__ == '__main__':
    main()
