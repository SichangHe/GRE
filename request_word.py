from dataclasses import dataclass
from os import system
from random import choice
from time import sleep


@dataclass
class WordEntry:
    word: str
    meaning: str


def read_words(path: str):
    words: list[WordEntry] = list()
    word: str | None = None
    with open(path, "r") as file:
        for line in file.readlines():
            if line == "":
                continue
            if word == None:
                word = line
            else:
                words.append(WordEntry(word, line))
                word = None
    return words


def notify(
    body: str,
    title: str = "",
    subtitle: str = "",
):
    to_run = f"""osascript -e 'display notification "{body}" """
    if title:
        to_run = f"""{to_run}with title "{title}" """
    if subtitle:
        to_run = f"""{to_run}with subtitle "{subtitle}" """
    to_run = f"{to_run}'"
    return system(to_run)


def main():
    words = read_words("word_list.txt")
    while 1:
        word = choice(words)
        notify(word.meaning, word.word)
        sleep(5 * 60)


main() if __name__ == "__main__" else None