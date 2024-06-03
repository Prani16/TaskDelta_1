import tkinter as tk
from tkinter import messagebox
from itertools import cycle

class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = None
        self.points = 0

       
      #  self.player_colors = {"Player 1": "red", "Player 2": "blue"}
        

    

class GameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.player_colors = {"Player 1": "pink", "Player 2": "purple"}  # Define colors for players
        self.flag1="N"
        self.flag2="N"
        self.err ='N'
        self.cplayer=''
        self.lock=0

        self.title("Multi-Page Game Application")
        self.geometry("600x300")

        # Create a container frame to hold all pages
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for F in (StartPage, GamePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            # Stack all pages on top of each other
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name,**kwargs):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'update_player_names'):
            frame.update_player_names(**kwargs)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Player Information", font=("Helvetica", 18))
        label.pack(pady=10, padx=10)

        self.player1_name = tk.StringVar()
        self.player2_name = tk.StringVar()

        player1_label = tk.Label(self, text="Player 1 Name:")
        player1_label.pack()
        player1_entry = tk.Entry(self, textvariable=self.player1_name)
        player1_entry.pack()

        player2_label = tk.Label(self, text="Player 2 Name:")
        player2_label.pack()
        player2_entry = tk.Entry(self, textvariable=self.player2_name)
        player2_entry.pack()

        rules_button = tk.Button(self, text="Show Rules", command=self.show_rules)
        rules_button.pack(pady=5)

        button1 = tk.Button(self, text="Start Game", command=self.start_game)
        button1.pack(pady=5)


    def show_rules(self):
        messagebox.showinfo("Game Rules", "1. 1st Turn of each player: Players can choose any tile on the grid on this turn only. \n 2.Clicking a tile assigns your colour to it and awards you 3 points on that tile.\n 3.Subsequent Turns: After the first turn, players can only click on tiles that already have their own colour. Clicking a tile with your colour adds 1 point to that tile.\n 4.The background colour indicates the next player.\n Conquest and Expansion: When a tile with your colour reaches 4 points, it triggers an expansion:\n The colour completely disappears from the original tile.Your colour spreads to the four surrounding squares in a plus shape (up, down, left, right).Each of the four surrounding squares gains 1 point with your colour.\n If any of the four has your opponent’s colour, you conquer the opponent's points on that tile while adding a point to it, completely erasing theirs.The expansion is retriggered if the neighbouring tile as well reaches 4 points this way.Players take turns clicking on tiles and the objective is to eliminate your opponent's colour entirely from the screen.")

    def start_game(self):
        player1 = self.player1_name.get() or "Player 1"
        player2 = self.player2_name.get() or "Player 2"
        self.controller.player_names = (player1, player2)
        self.controller.show_frame("GamePage",player_names=(player1, player2))

class GamePage(tk.Frame):
    def __init__(self, parent, controller):        
        super().__init__(parent)
        self.controller = controller
        self.rows = 5
        self.cols = 5
        #self.tiles = [[Tile(row, col) for col in range(cols)] for row in range(rows)]
        self.current_player = cycle(["Player 1", "Player 2"])
      #  self.player_colors = {"Player 1": "red", "Player 2": "blue"}
        self.buttons = []
        print("test")
        self.player_colors = {"Player 1": "pink", "Player 2": "purple"}  # Define colors for players
        self.flag1="N"
        self.flag2="N"
        self.err ='N'
        self.cplayer=''
        self.lock=0
        self.points =0
        self.color=""
        self.first_tile_color ='white'
        self.board_colors = {"Player 1": 'pink',  "Player 2": 'purple'}  # Define player colors for the board background
        self.player1score =0
        self.player2score=0
 
       
        for row in range(5):
            button_row = []
            for col in range(5):
                button = tk.Button(self, text="", bg="white", width=5, height=3,relief="groove", borderwidth=2)
                button.grid(row=row+1, column=col+1, padx=5, pady=5)
                button.config(command=lambda r=row, c=col: self.click_tile(r, c))  # Bind click event
                button_row.append(button)
                self.master.config(bg='pink')
                self.config(bg='pink')
            self.buttons.append(button_row)

        reset_button = tk.Button(self, text="Reset Grid", command=self.reset_grid)
        reset_button.grid(row=9, column=1, columnspan=3, pady=10)

        back_button = tk.Button(self, text="Back to Start Page", command=lambda: controller.show_frame("StartPage"))
        back_button.grid(row=10, column=0, columnspan=3, pady=10)

    def click_tile(self, row, col):
        print(row)
        print(col)
        if self.lock ==0 :       
            # print(f"error {self.err} ")
            button_text = self.buttons[row][col].cget("text")
            button_color = self.buttons[row][col].cget("bg")
            if self.flag1 == "N" or self.flag2 == "N":
                self.choose_tile(row, col ,self.err,'','','')
                print(self.color)
                print(self.points)
            else:
                # if button_color == "white":
                self.choose_tile(row, col ,self.err,self.cplayer,button_text,button_color)
                print(self.color)

            color=self.color
            points=self.points

            self.update_board(row, col, self.color, self.points)
            if color == "Player 1" and self.flag1 == "N":
                self.flag1 = "Y"
            elif color == "Player 2" and self.flag2 == "N":
                self.flag2  = "Y"

            self.first_tile_color =self.chec_tile_color()
        
    def choose_tile(self,row, col, err ,cplayer,button_text,button_color):
        points=0
        color=""
        
        print(err)
        if err == "N":
            current_player = next(self.current_player)
            print(f"test {current_player}")
            self.err = "N"
            cplayer = ""
        else:
            print(cplayer)
            current_player = cplayer
            self.err = "N"

        button = self.buttons[row][col]
        current_color = button.cget("bg")
        print(row,col)
        print(f"Before: {self.color}, {self.points}")  # Debugging print statement
        print(button_text)
        print(current_color)

        if (current_color is None or current_color =='white') and button_text =="":
            self.color = current_player
            points += 3
            self.points =points
    
        elif button_text is not None:
            
            print("test")
            print(button_text)
            if button_text:
                points=int(button_text)
                self.color = current_player
                points +=1
                self.points =points
            else:
                self.color = current_player
            # if tile.points >= 4:
                # self.expand_tile(row,col )
        else:
            points +=1
            self.points = points
            self.color =current_player
        print(f"After: {self.color}, {self.points}")  # Debugging print statement
        # return color, points          
    def update_player_names(self, player_names):
        player1_name, player2_name = player_names
        self.action_button = tk.Button(self, text="Player 1 :" + player1_name, bg='pink')
        self.action_button.grid()
        self.action_button = tk.Button(self, text="Player 2 :" + player2_name, bg='purple')
        self.action_button.grid()
        
    def update_board(self, row, col, color, points):
        button_text = self.buttons[row][col].cget("text")
        button_color = self.buttons[row][col].cget("bg")
        player_color = self.player_colors.get(color, "white")  # Get player's color or default to white
        print(self.flag1)
        print(player_color)
        print(button_color)
        print(color)
        
        
        if self.flag1 == "Y" and player_color != button_color and color == "Player 1":
           # print(f"wrong selection : {player_color}{button_color}{color} ")
            self.err ='Y'
            self.cplayer=color
            messagebox.showinfo("Error","Wrong Selection")
        elif self.flag2 == "Y" and player_color != button_color and color == "Player 2" and button_color != "white" :
            # print(f"wrong selection : {player_color}{button_color}{color} ")
            self.err ='Y'
            self.cplayer=color
            messagebox.showinfo("Error","Wrong Selection")
        elif self.flag2 == "N" and self.flag1 == "Y" and player_color != button_color and color == "Player 2" and button_color != "white":
            # print(f"wrong selection : {player_color}{button_color}{color} ")
            self.err ='Y'
            self.cplayer=color
            messagebox.showinfo("Error","Wrong Selection")
        
        
       
        elif points < 4:
            player_color = self.player_colors.get(color, "white")  # Get player's color or default to white
            self.buttons[row][col].config(text=points, bg=player_color)  # Set text and background color
            print(points)
            self.cplayer=color
            self.err ='N'
            if player_color == 'Player 1':
                self.player1score +=points
            elif player_color == 'Player 2':
                self.player2score +=points
  
        else:
            self.split_tile(row, col, color, points)
            self.cplayer=color
            self.err ='N'
            if player_color == 'Player 1':
                self.player1score +=points
            elif player_color == 'Player 2':
                self.player2score +=points
        # Switch player
        if self.err =='N':
            self.cplayer = "Player 2" if self.cplayer == "Player 1" else "Player 1"

        self.player2score=0
        
        self.update_board_background()
        
        if self.flag1 == "Y" and self.flag2  == "Y":
            if self.check_board_color():           
                if self.first_tile_color == 'pink':
                    messagebox.showinfo("Result","Player1 wins!")
                    self.lock=1
                elif self.first_tile_color == 'purple':
                    messagebox.showinfo("Result","Player2 wins!")
                    self.lock=1

        
    def update_board_background(self):
        print(f"cplayer {self.cplayer}")
        new_board_color = self.board_colors[self.cplayer]
        self.master.config(bg=new_board_color)
        self.config(bg=new_board_color)
            
    def split_tile(self, row, col, color, points):

        self.buttons[row][col].config(text="", bg="white")  # Set text and background color
        player_color = self.player_colors.get(color, "white")  # Get player's color or default to white
          
         # expand to 4 tiles
        for i in range(1):
            col1 = col + 1
            col2 = col - 1
            if col1 < 5:
                if self.buttons[row][col1].cget("text") =="":
                    Leftpoint=1
                    self.buttons[row][col1].config(text=Leftpoint, bg=player_color)  # Set text and background color
                else:
                    Leftpoint = int(self.buttons[row][col1].cget("text"))
                    Leftpoint +=1
                    if Leftpoint >=4:
                        self.split_tile(row, col1, color, points)
                    else:
                        self.buttons[row][col1].config(text=Leftpoint, bg=player_color)
            if col2 >= 0:
                if self.buttons[row][col2].cget("text") =="":
                    Rightpoint=1
                    self.buttons[row][col2].config(text=Rightpoint, bg=player_color)  # Set text and background color
                else:
                    Rightpoint=int(self.buttons[row][col2].cget("text"))
                    Rightpoint +=1
                    if Rightpoint >=4:
                        self.split_tile(row, col2, color, points)
                    else:
                        self.buttons[row][col2].config(text=Rightpoint, bg=player_color)  # Set text and background color

         
            row1 = row + 1
            row2 = row - 1
            print (f"{row1}{row2}")
            if row1 < 5 :
                if self.buttons[row1][col].cget("text") =="":
                    Upeerpoint=1
                    self.buttons[row1][col].config(text=Upeerpoint, bg=player_color)  # Set text and background color
                else:
                    print(int(self.buttons[row1][col].cget("text")))
                    Upeerpoint = int(self.buttons[row1][col].cget("text"))
                    Upeerpoint +=1
                    if Upeerpoint >= 4:
                        self.split_tile(row1, col, color, points)
                    else:
                        self.buttons[row1][col].config(text=Upeerpoint, bg=player_color)
            if row2 >= 0:
                if self.buttons[row2][col].cget("text") =="":
                    Lowerpoint=1
                    self.buttons[row2][col].config(text=Lowerpoint, bg=player_color)  # Set text and background color
                else:
                    Lowerpoint=int(self.buttons[row2][col].cget("text"))
                    Lowerpoint +=1
                    if Lowerpoint >=4:
                        self.split_tile(row2, col, color, points)
                    else:
                        self.buttons[row2][col].config(text=Lowerpoint, bg=player_color)  # Set text and background color

    def chec_tile_color(self):
        first_tile_color = self.buttons[0][0].cget("bg")
        if first_tile_color == "white":
            for row in range(5) :
                for col in range(5):                                 
                    first_tile_color = self.buttons[row][col].cget("bg")
                    if first_tile_color !='white':
                        return first_tile_color
        return first_tile_color

    
    def check_board_color(self):
       
        self.first_tile_color =self.chec_tile_color()
        
        for row in range(5):
            for col in range(5):
                B_color = self.buttons[row][col].cget("bg")
                if B_color != self.first_tile_color and B_color !='white' :
                    return False
        return True
    def reset_grid(self):
        for row in self.buttons:
            for button in row:
                button.config(text="", bg="white")
        self.current_player = "Player 1"



if __name__ == "__main__":
    app = GameGUI()
    app.mainloop()
