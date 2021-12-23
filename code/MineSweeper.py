from pipes import SOURCE
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import random
from kivy.config import Config

class mishbezet(ButtonBehavior,Image):
     def __init__(self, line, colom, num = 0, **kwargs ):
        # num = -1  is a bomb in the cell , if not the number in the cell is the number of the bombs around the cell.

        ButtonBehavior.__init__(self,**kwargs)
        Image.__init__(self,**kwargs)
        self.line = line
        self.hidden = True
        self.flagged = False
        self.col = colom
        self.num = num
        self.picNormal = "pics/dolphin.jpg"
        self.bombPic = "pics/bomb.jpg"
        self.source = self.picNormal
    # random.randint(1,101)



class Board(GridLayout):
    def __init__(self, numLines = 10,  **kwargs):
        # constructor of the board
        GridLayout.__init__(self,**kwargs)
        self.cols = numLines # number of colomn in the
        self.myBoard = list() # all the cells in the boardgridLayout
        self.game_over = False
        self.to_reveal = 0
        self.randomBomb()  # choose the bombs in the game
        self.changeNumInCell()
        l = Label(text='num bombs' , font_size='20sp')
        self.l1 = Label(text=str(self.countBomb), font_size='20sp')
        self.add_widget(l)
        self.add_widget(self.l1)



    def randomBomb (self): #  we are written this but the students wouldnt get this
        self.counters = 0  # counting the num of bombs to tell later to the player
        self.countBomb = 0  #count how many bombs R in the Board .
        for i in range (self.cols):
            for j in range(self.cols) :
                x = random.randint(0,6) # normaly there is a 16% chance of cell to be a bomb. so we use random to decide witch is bomb and witch isn't
                if (x == 1) :  # statistics of bombs
                    ta = mishbezet( i,j,-1)
                    ta.bind(on_press=self.click)
                    self.countBomb += 1
                else :
                    ta = mishbezet(i,j)
                    ta.bind(on_press=self.click)
                self.myBoard.append(ta)
                self.add_widget(ta)
        self.to_reveal = self.cols**2 - self.countBomb

    def reveal(self, touch):
        touch.hidden = False
        self.to_reveal-= 1
        touch.source = "pics/" + str(touch.num) + ".jpg"
        if touch.num == 0:
            for x in self.myBoard:
                if x != touch and x.col in [touch.col, touch.col - 1, touch.col + 1] and x.line in [touch.line,
                                                                                                    touch.line - 1,
                                                                                                    touch.line + 1] and x.hidden:
                    self.reveal(x)

    def click(self,touch):
        if not self.game_over:
            if touch.last_touch.button == "left":
                if not touch.flagged:
                    if touch.hidden:
                        if touch.num == -1:
                            touch.source = "pics/bomb.jpg"
                            touch.hidden = False
                            self.game_over = True
                            self.add_widget(Label(text="GAME OVER", font_size='20sp', color=(1, 0, 0, 1)))
                        else:
                            self.reveal(touch)
                            if self.to_reveal == 0 and self.countBomb == 0:
                                self.game_over = True
                                self.add_widget(Label(text="YOU WON", font_size='20sp', color=(1, 0, 0, 1)))
            if touch.last_touch.button == "right":
                if touch.hidden:
                    if not touch.flagged:
                        touch.source = "pics/flag.jpg"
                        touch.flagged = True
                        self.countBomb -= 1
                        self.l1.text = str(self.countBomb)
                    else:
                        touch.source = "pics/dolphin.jpg"
                        touch.flagged = False
                        self.countBomb += 1
                        self.l1.text = str(self.countBomb)
        print (self.to_reveal)


    def changeNumInCell(self):
         for ta in self.myBoard:
             for neighborTa in self.myBoard:
                 if (ta.num != -1):   # if it is not a bomb
                     if (neighborTa.num == -1 ): #check if the neighbor is a bomb
                         if (ta.line+1 == neighborTa.line and ta.col==neighborTa.col):
                             ta.num += 1
                         if (ta.line -1 == neighborTa.line and ta.col==neighborTa.col):
                             ta.num += 1
                         if (ta.line + 1 == neighborTa.line and ta.col - 1 == neighborTa.col):
                             ta.num += 1
                         if (ta.line + 1 == neighborTa.line and ta.col + 1 == neighborTa.col):
                             ta.num += 1
                         if (ta.line - 1 == neighborTa.line and ta.col - 1 == neighborTa.col):
                             ta.num += 1
                         if (ta.line - 1 == neighborTa.line and ta.col + 1 == neighborTa.col):
                             ta.num += 1
                         if  (ta.col +1 == neighborTa.col and ta.line== neighborTa.line):
                             ta.num += 1
                         if (ta.col - 1 == neighborTa.col and ta.line== neighborTa.line):
                             ta.num += 1




class TestApp(App):
    def build(self):
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        self.title = 'based graphics'
        return Board()



TestApp().run()
