from dataclasses import dataclass
from os import system
from random import choice
from sys import argv
from time import sleep


@dataclass
class WordEntry:
    word: str
    meaning: str


def read_words(path: str):
    words: dict[str, str] = {}
    word: str | None = None
    with open(path, "r") as file:
        for line in file.readlines():
            line = line.strip()
            if line == "":
                continue
            if word is None:
                word = line
            else:
                words[word] = line
                word = None
    return words


def escape(text: str):
    return text.replace("'", "`").replace('"', "``")


def notify(
    body: str,
    title: str = "",
    subtitle: str = "",
):
    to_run = f"""osascript -e 'display notification "{escape(body)}" """
    if title:
        to_run = f"""{to_run}with title "{escape(title)}" """
    if subtitle:
        to_run = f"""{to_run}with subtitle "{escape(subtitle)}" """
    to_run = f"{to_run}'"
    if system(to_run) != 0:
        print(to_run)


def depend_on_other(meaning: str, words: dict[str, str]):
    for word in meaning.split():
        if word in words:
            return True
    return False


def select_words(words: dict[str, str], no_dep=True):
    select_from: list[WordEntry] = []
    for word, meaning in words.items():
        if no_dep and depend_on_other(meaning, words):
            continue
        select_from.append(WordEntry(word, meaning))
    print(f"Selecting among {len(select_from)} words from {len(words)}.")
    return select_from


def open_dict(word: str):
    to_run = f"""osascript -e 'open location "dict://{word}"'"""
    if system(to_run) != 0:
        print(to_run)


def get_delay(argv):
    for arg in argv:
        if arg.startswith("--delay="):
            return int(arg.split("=")[1])
    return 5 * 60


def main():
    open = any(arg == "--open" for arg in argv)
    no_dep = any(arg == "--no-dep" for arg in argv)
    words = read_words("word_list.txt")
    words = select_words(words, no_dep)
    delay = get_delay(argv)
    while 1:
        word = choice(words)
        notify(word.meaning, word.word)
        if open:
            open_dict(word.word)
        sleep(delay)


try:
    main() if __name__ == "__main__" else None
except KeyboardInterrupt:
    print()
