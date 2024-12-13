from tkinter.filedialog import askopenfilename

import pygame

from loader import loadFileAndConvert
from scene import Scene
from widgets import *

from threading import Thread


class SentenceGenerator(Scene):
    def onInit(self):
        self.output = Paragraph("", self.width / 2 - 40, self.height / 2 - 40, (30, 30, 30), 40, "Arialblack",  self.width/30, center=True)
        self.importDataButton = Label(0, 0, "Unclicked Tab", "Import Data Set", color=(255, 255, 255),
                                      font="Arialblack",
                                      size=30,
                                      clickedLabelName="Clicked Tab", stretchBuffer=15, stretchToFit=True)
        self.outputText = []
        self.inputData = loadFileAndConvert("Stock Data/data.json")
        self.startButton = Label(self.importDataButton.rect.right, 0, "Unclicked Tab", "Start", color=(255, 255, 255),
                                 font="Arialblack",
                                 size=30,
                                 clickedLabelName="Clicked Tab", stretchBuffer=15, stretchToFit=True)
        self.promptText = Text("Prompt", self.startButton.rect.right, 0, color=(30, 30, 30), size=30, font="Arialblack")
        self.prompt = Label(self.promptText.rect.right, 0, "Unclicked Tab", "", color=(255, 255, 255),
                                 font="Arialblack",
                                 size=30,
                                 clickedLabelName="Clicked Tab", stretchBuffer=15, stretchToFit=True)

    def mouseDown(self, event):
        self.importDataButton.clicked(event)
        self.startButton.clicked(event)
        self.prompt.clicked(event)

    def mouseUp(self, event):
        if self.importDataButton.released(event):
            path = askopenfilename()
            try:
                self.inputData = loadFileAndConvert(askopenfilename())
            except FileNotFoundError:
                pass
        if self.startButton.released(event):
            Thread(target=self.generateText).start()
        self.prompt.released(event)

    def display(self) -> None:
        self.importDataButton.display(self.window)
        self.output.display(self.window)
        self.startButton.display(self.window)
        self.prompt.display(self.window)
        self.promptText.display(self.window)

    def keyDown(self, event):
        if event.key == pg.K_RETURN:
            self.outputText = self.prompt.text().split()
            self.updateText()
        self.prompt.textUpdate(event)

    def updateText(self):
        self.output.text = " ".join(self.outputText)
        self.output.reload()

    def videoResize(self):
        self.output.lineLength = self.width / 30
        self.output.rect.center = self.width / 2 - 40, self.height / 2 - 40
        self.output.reload()

    def getNextWord(self):
        wordVal = {}
        for i, item in enumerate(self.inputData):
            if item.lower() == self.outputText[-1].lower() and not self.inputData[i + 1] in self.outputText:
                try:
                    self.inputData[i + 1]
                except IndexError:
                    continue
                try:
                    wordVal[self.inputData[i+1]] += 1
                except KeyError:
                    wordVal[self.inputData[i+1]] = 0
        if len(wordVal) == 0:
            return "End of Line"
        maxValWord = max(wordVal, key=wordVal.get)
        return maxValWord

    def generateText(self):
        while self.run:
            nextWord = self.getNextWord()
            if nextWord == "End of Line":
                return
            self.outputText.append(nextWord)
            Thread(target=self.updateText).start()


SentenceGenerator((900, 500), "Sentence Generator").start()
