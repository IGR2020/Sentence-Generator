"""GUI for pygame (2.5.2 or beyond)"""

import pygame as pg

pg.font.init()
from assets import assets, fontLocation

mouseButtonMapping = {"left": 0, "middle": 1, "right": 2}


class BasicObject:
    def __init__(self, x: int, y: int, name: str):
        image = assets[name]
        self.rect = pg.Rect(x, y, image.get_width(), image.get_height())
        self.name = name

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0):
        window.blit(assets[self.name], (self.rect.x - x_offset, self.rect.y - y_offset))

    def updateOwnedObjects(self): ...


class ObjectGroup:
    def __init__(self, x: int = 0, y: int = 0):
        self.objects = []
        self.rect = pg.Rect(x, y, 1, 1)

    def setRect(self):
        for obj in self.objects:
            if obj.rect.x < self.rect.x:
                self.rect.x = obj.rect.x
            if obj.rect.y < self.rect.y:
                self.rect.y = obj.rect.y
            if obj.rect.right > self.rect.right:
                self.rect.width = obj.rect.right - self.rect.x
            if obj.rect.bottom > self.rect.bottom:
                self.rect.height = obj.rect.bottom - self.rect.y

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0):
        for obj in self.objects:
            obj.display(window, x_offset, y_offset)

    def updateOwnedObjects(self):
        ...

    def stackHorizontal(self):
        for i, obj in enumerate(self.objects):
            if i == 0:
                obj.rect.topleft = self.rect.topleft
                obj.updateOwnedObjects()
                continue

            obj.rect.left = self.objects[i - 1].rect.right
            obj.updateOwnedObjects()

    def stackVertical(self):
        for i, obj in enumerate(self.objects):
            if i == 0:
                obj.rect.topleft = self.rect.topleft
                obj.updateOwnedObjects()
                continue

            obj.rect.top = self.objects[i - 1].rect.bottom
            obj.updateOwnedObjects()


class Button(BasicObject):
    def __init__(self, x: int, y: int, releasedImageName: str, pressedImageName: str,
                 mouseButtonAccepted: str | int = None, data=None):
        """mouseButtonAccepted argument allows for you to check for only certain mouse button presses, possible arguments are 'left', 'right', 'middle', 0, 1, 2
        \nPlace any associated data of the button as the data argument"""
        super().__init__(x, y, releasedImageName)

        self.releasedImageName = releasedImageName
        self.pressedImageName = pressedImageName

        self.heightDifference = assets[self.releasedImageName].get_height() - assets[self.pressedImageName].get_height()

        self.pressed = False
        if isinstance(mouseButtonAccepted, str): mouseButtonAccepted = mouseButtonMapping[mouseButtonAccepted]

        self.mouseButtonAccepted = mouseButtonAccepted

        self.data = data

    def clicked(self, event, *args) -> bool:
        """Call within event loop under the if condition of pg.MOUSEBUTTONDOWN"""
        mousePos = pg.mouse.get_pos()

        if self.rect.collidepoint(mousePos) and (
                self.mouseButtonAccepted is None or event.button == self.mouseButtonAccepted):
            self.pressed = True
            self.name = self.pressedImageName
            self.rect.y += self.heightDifference
            return True

        self.pressed = False
        return False

    def released(self, *args):
        """Call within event loop under the if condition of pg.MOUSEBUTTONUP"""
        if self.pressed:
            self.pressed = False
            self.name = self.releasedImageName
            self.rect.y -= self.heightDifference
            return True

        return False

    def reload(self):
        super().__init__(self.rect.x, self.rect.y, self.releasedImageName)

        self.releasedImageName = self.releasedImageName
        self.pressedImageName = self.pressedImageName

        self.heightDifference = assets[self.releasedImageName].get_height() - assets[self.pressedImageName].get_height()


class Text:
    def __init__(self, text, x, y, color, size, font, center=False) -> None:

        # saving reconstruction data
        self.text = str(text)
        self.color = color
        self.size = size
        self.font = font
        self.center = center

        # creating text surface
        font_style = pg.font.Font(fontLocation + self.font + ".ttf", self.size)
        text_surface = font_style.render(self.text, True, self.color)
        if center:
            x -= text_surface.get_width() // 2
            y -= text_surface.get_height() // 2

        self.image = text_surface
        self.rect = text_surface.get_rect(topleft=(x, y))

        self.type = "Text"

    def reload(self, reloadRect=True):
        font_style = pg.font.Font(fontLocation + self.font + ".ttf", self.size)
        text_surface = font_style.render(self.text, True, self.color)

        self.image = text_surface

        if reloadRect:
            if self.center:
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0):
        window.blit(self.image, (self.rect.x - x_offset, self.rect.y - y_offset))

    def updateOwnedObjects(self):
        ...


class Label(ObjectGroup, Button):
    """A dynamic widget, usable as a text box, button and label"""

    def __init__(self, x: int, y, labelName, text, color: tuple[int, int, int], size, font,
                 clickedLabelName: str = None, validTextInputs: str = None, stretchToFit=False, stretchBuffer=0, data=None):
        if clickedLabelName is None: clickedLabelName = labelName

        ObjectGroup.__init__(self)
        Button.__init__(self, x, y, labelName, clickedLabelName, data=data)
        self.objects.append(
            Text(text, self.rect.x, self.rect.y, color, size, font)
        )

        self.originalReleasedImageName = labelName
        self.originalPressedImageName = clickedLabelName
        self.stretchToFit = stretchToFit
        self.stretchBuffer = stretchBuffer

        if stretchToFit:
            assets[f"Stretched {labelName} {id(self)}"] = pg.transform.scale(assets[labelName], (
                self.objects[0].rect.width + stretchBuffer, self.objects[0].rect.height + stretchBuffer))

            assets[f"Stretched {clickedLabelName} {id(self)}"] = pg.transform.scale(assets[clickedLabelName], (
                self.objects[0].rect.width + stretchBuffer,
                self.objects[0].rect.height + stretchBuffer - self.heightDifference))

            self.releasedImageName = f"Stretched {labelName} {id(self)}"
            self.pressedImageName = f"Stretched {clickedLabelName} {id(self)}"

            Button.reload(self)

        self.objects[0].rect.center = self.rect.center

        if validTextInputs is None:
            self.validTextInputs = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMN,./;'[]-=1234567890`~!@#$%^&*()_+}{|:\"<>?\\"
        else:
            self.validTextInputs = validTextInputs
        self.is_selected = False

    def stretch(self):
        assets[f"Stretched {self.originalReleasedImageName} {id(self)}"] = pg.transform.scale(assets[self.originalReleasedImageName], (
            self.objects[0].rect.width + self.stretchBuffer, self.objects[0].rect.height + self.stretchBuffer))

        assets[f"Stretched {self.originalPressedImageName}"] = pg.transform.scale(assets[self.originalPressedImageName], (
            self.objects[0].rect.width + self.stretchBuffer,
            self.objects[0].rect.height + self.stretchBuffer - self.heightDifference))

        self.releasedImageName = f"Stretched {self.originalReleasedImageName} {id(self)}"
        self.pressedImageName = f"Stretched {self.originalPressedImageName} {id(self)}"

        Button.reload(self)

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0):
        Button.display(self, window, x_offset, y_offset)
        ObjectGroup.display(self, window, x_offset, y_offset)

    def textUpdate(self, event):
        """Expects event to be from under the if event.type == pg.KEYDOWN within the for loop, if using scenes under the keydown function"""
        if not self.is_selected:
            return
        if event.key == pg.K_BACKSPACE:
            self.objects[0].text = self.objects[0].text[:-1]
        elif event.unicode in self.validTextInputs:
            self.objects[0].text += event.unicode
        self.objects[0].reload()
        if self.stretchToFit:
            self.stretch()
        else:
            self.reload()

    def clicked(self, event, *args) -> bool:
        val = Button.clicked(self, event, *args)
        if val:
            self.objects[0].rect.y += self.heightDifference
            self.is_selected = True
        else:
            self.is_selected = False
        return val

    def released(self, *args):
        val = Button.released(self, *args)
        if val:
            self.objects[0].rect.y -= self.heightDifference
        return val

    def updateOwnedObjects(self):
        self.objects[0].rect.center = self.rect.center

    def text(self) -> str:
        return self.objects[0].text


class Paragraph(ObjectGroup):
    def __init__(self, text, x, y, color, size, font, lineLength, center=False):
        super().__init__()
        self.text = text
        self.lineLength = lineLength
        self.color = color
        self.font = font
        self.size = size
        self.center = center
        self.rect.center = x, y
        for i in range(round(len(self.text) / self.lineLength)):
            try:
                self.objects.append(Text(text[round(i*lineLength):round((i+1)*lineLength)], x, y, color, size, font, center))
            except IndexError:
                break
        self.stackVertical()

    def reload(self):
        for i in range(round(len(self.text) / self.lineLength)):
            try:
                self.objects[i]
            except IndexError:
                self.objects.append(
                    Text(self.text[round(i * self.lineLength):round((i + 1) * self.lineLength)], self.rect.x, self.rect.y, self.color, self.size, self.font, self.center))
            try:
                self.objects[i].text = self.text[round(i*self.lineLength):round((i+1)*self.lineLength)]
                self.objects[i].rect.center = self.rect.center
                self.objects[i].reload()
            except IndexError:
                break
        self.stackVertical()


class Hotbar(ObjectGroup):
    def __init__(self, x: int, y: int, objects: list[ObjectGroup | BasicObject | Text], stackOrientation: str | int,
                 scrollMin: int = 0, scrollMax: int = 0):
        """Define stackOrientation as either vertical or horizontal, or 0 and 1 respectively
        \nscrollMin is for the maximum scroll to the left and scrollMax is for the maximum scroll to the right, NOTE: scrollMin and Max are not relative to original position, but the x itself"""
        super().__init__(x, y)

        if isinstance(stackOrientation, int):
            if stackOrientation == 1:
                stackOrientation = "horizontal"
            else:
                stackOrientation = "vertical"
        self.stackOrientation = stackOrientation.lower()

        self.scrollMin = scrollMin
        self.scrollMax = scrollMax

        [self.objects.append(obj) for obj in objects]

        if self.stackOrientation == "horizontal":
            self.stackHorizontal()
        else:
            self.stackVertical()

        self.updateLimitScroll()

    def updateLimitScroll(self):
        """WARNING: make sure that you have updated both the scrollMin and scrollMax before calling this function"""
        self.setRect()

        if self.stackOrientation == "horizontal":
            self.scrollMax = max(self.scrollMin, self.scrollMax - self.objects[0].rect.width)
        else:
            self.scrollMax = max(self.scrollMin, self.scrollMax - self.objects[0].rect.height)

        if self.stackOrientation == "horizontal":
            self.scrollMin = min(self.scrollMax, self.scrollMin + self.objects[-1].rect.width - self.rect.width)
        else:
            self.scrollMin = min(self.scrollMax, self.scrollMin + self.objects[-1].rect.height - self.rect.height)

    def updateX(self, x: int):
        self.rect.x = x
        if self.stackOrientation == "horizontal":
            self.stackHorizontal()
        else:
            self.stackVertical()

    def updateY(self, y: int):
        self.rect.y = y
        if self.stackOrientation == "horizontal":
            self.stackHorizontal()
        else:
            self.stackVertical()

    def scroll(self, event, limitScroll: bool, scrollFactor: int = 10):
        """This is to be called withing the event for loop, under the if event.type == pg.MOUSEWHEEL: i.e when working with scenes under the scroll function
        \nlimitScroll if false allows the player to scroll the hotbar off-screen, while limiting is based on what the scroll min and scroll max were defined as in the __init__
        \nscrollMin is for the maximum scroll to the left and scrollMax is for the maximum scroll to the right"""
        if self.stackOrientation == "horizontal":
            self.updateX(self.rect.x + ((event.y + event.x) * scrollFactor))
        else:
            self.updateY(self.rect.y + ((event.y + event.x) * scrollFactor))

        if limitScroll:
            if self.stackOrientation == "horizontal":
                self.updateX(min(max(self.rect.x, self.scrollMin), self.scrollMax))
            else:
                self.updateY(min(max(self.rect.y, self.scrollMin), self.scrollMax))


class AttributeEdit(Hotbar):
    """Allows one to easily get user data for basic types such as int, string, bool, etc. (only string implemented)
    \nOutputs will be in a dictionary with the input type names for each input, accessible via AttributeEdit.objectOutput"""

    def __init__(self, x, y, inputTypes: dict[str, type[str]], themeSize: int, themeColor: tuple[int, int, int], labelName: str, stackOrientation: str, clickedLabelName: str = None, validTextInputs: str = None, themeFont: str = "Arialblack", scrollMin: int = 0, scrollMax: int = 0, stretchToFit: bool = False, stretchBuffer: int = 0):

        objects = []
        for inputName in inputTypes:
            if inputTypes[inputName] == str:
                objects.append(Text(inputName, x, y, themeColor, themeSize, themeFont))
                objects.append(Label(x, y, labelName, "", themeColor, themeSize, themeFont, stretchToFit=stretchToFit, stretchBuffer=stretchBuffer, clickedLabelName=clickedLabelName, validTextInputs=validTextInputs))

        super().__init__(x, y, objects, stackOrientation, scrollMin, scrollMax)

        self.inputTypes = list(inputTypes.values())
        self.objectOutput = {name: None for name in self.inputTypes}

    def tick(self): ...

    def keyDown(self, event):
        for i, inputName in enumerate(self.inputTypes):
            objectIndex = i*2 + 1

            if inputName == str:
                self.objects[objectIndex].textUpdate(event)
                self.objectOutput[inputName] = self.objects[objectIndex].objects[0].text

    def mouseDown(self, event):
        for i, inputName in enumerate(self.inputTypes):
            objectIndex = i*2 + 1

            if inputName == str:
                self.objects[objectIndex].clicked(event)

    def mouseUp(self, event):
        for i, inputName in enumerate(self.inputTypes):
            objectIndex = i * 2 + 1

            if inputName == str:
                self.objects[objectIndex].released(event)