#!/usr/bin/python3
# -*- coding: utf-8 -*-

import genanki
import hashlib
import csv
import os
import sys


def printError(string):
    print("[!] {}".format(string), file=sys.stderr)
    exit(1)


def printSuccess(string):
    print("[*] {}".format(string))


def getID(string):
    return int(hashlib.sha256(string.encode("utf-8")).hexdigest()[:12],
               base=16)


def getModel():

    MODEL_NAME = "MODEL"

    css = ".card {\
        font-family: arial; \
            font-size: 30px; \
            text-align: center; \
            color: black; \
            background-color: white; \
        }"

    model = genanki.Model(
                getID(MODEL_NAME),
                MODEL_NAME,
                fields=[
                    {"name": "Question"},
                    {"name": "Answer"}
                ],
                templates=[
                    {
                        "name": "Card 1",
                        "qfmt": "<center>{{Question}}</center>",
                        "afmt": "<center>{{FrontSide}}<hr \
                                id=\"answer\">{{Answer}}</center>"
                    }
                ],
                css=css
            )
    return model

def generateDeck(kursName, kursEinheit):
    deckName = kursName + "::" + kursEinheit
    deck = genanki.Deck(
            getID(deckName),
            deckName,
            "FernUniversität in Hagen - {} {}".format(kursName, kursEinheit))
    

    filePath = kursName + "/" + kursEinheit + "/basic.csv"
    try:
        with open(filePath) as f:
            csvfile = csv.reader(f, delimiter=';', quotechar='"')
            for row in csvfile:
            #for line in f:
                if len(row) != 2:
                    printError("Skipping line: <{}> due to separator problem"
                               .format(";".join(row)) + "\nExpected format: <QUESTION>;<ANSWER>")
                question = row[0]
                answer = row[1]

                note = genanki.Note(
                        model=getModel(),
                        fields=[question, answer])
                deck.add_note(note)
        return deck
            
    except IOError:
        printError("A problem occured while opening the "
                   "file: {}".format(filePath))


def main():
    # find courses
    for kurs in  [f.path for f in os.scandir(".") if f.is_dir()]:
        decks = []
        kursName = kurs[2:]
        if kursName.startswith("."):
            continue
        # find unit
        for einheit in  [f.path for f in os.scandir(kurs) if f.is_dir()]:
            kursEinheit = einheit[len(kursName)+3:]
            if kursEinheit.startswith("."):
                continue
            if kursEinheit.startswith("images"):
                continue
            # generate deck
            decks.append(generateDeck(kursName, kursEinheit))
        
        # pack decks to one project
        anki = genanki.Package(decks)
        # add images to project
        if os.path.isdir(kursName + "/images"):
            anki.media_files = [f.path for f in os.scandir(kursName + "/images") if f.is_file()]

        try:
            anki.write_to_file(kursName + ".apkg")
            printSuccess("Deck {} successfully created.".format(kursName))
        except IOError:
            printError("A problem occured while creating "
                        "file: {}".format(kursName + ".apkg"))


if __name__ == "__main__":
    main()
