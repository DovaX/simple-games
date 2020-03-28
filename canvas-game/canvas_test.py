import pantograph

class Rectangle:
    def __init__(self,app,pos,size):
        self.app=app
        self.pos=pos
        self.size=size
    
    def draw(self,fill_color="#ffffff"):
        self.app.draw_rect(self.pos[0],self.pos[1],self.size[0],self.size[1],"#000000")
        self.app.fill_rect(self.pos[0],self.pos[1],self.size[0],self.size[1],fill_color)
            
    def is_clicked(self,pos):
        in_range_bool=True
        for i in range(2):
            if self.pos[i]>pos[i] or pos[i]>self.pos[i]+self.size[i]:
                in_range_bool=False
        if in_range_bool:
            print("Clicked")

class Grid(Rectangle):
    def __init__(self,app,rows,columns,pos=[0,0],cell_size=[20,20],margin=1):
        self.size=[(cell_size[0]+margin)*columns+margin,(cell_size[1]+margin)*columns+margin]
        super().__init__(app,pos,self.size)
        self.cell_size=cell_size
        self.margin=margin
        self.rows=rows
        self.columns=columns
        self.grid = []
        self.rectangles=[]
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.columns):
                self.grid[i].append(0)

    def init_rectangle_grid(self):
        for i in range(self.rows):
            self.rectangles.append([])
            for j in range(self.columns):
                self.rectangles[i].append(Rectangle(self.app,[self.pos[0]+j*(self.cell_size[0]+self.margin),self.pos[1]+i*(self.cell_size[1]+self.margin)],self.cell_size))                 
                
    def update_rectangle_grid(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j]==0:
                    self.rectangles[i][j].draw()
                if self.grid[i][j]==1:
                    self.rectangles[i][j].draw("#cc5500")

    def evaluate_row_column_indices(self,click):
        column = (click[0]-self.pos[0]) // (self.cell_size[0] + self.margin)
        row = (click[1]-self.pos[1]) // (self.cell_size[1] + self.margin)
        return(row,column)

class Game(pantograph.PantographHandler):
    def setup(self):
        self.grid1=Grid(self,15,15)
        self.grid1.init_rectangle_grid()
        
        
    def update(self):

        self.clear_rect(0, 0, self.width, self.height)           
        self.grid1.update_rectangle_grid()
        
    def on_key_down(self,event):
        key_code=event[-1]
        if key_code==37: #left
            pass
        if key_code==38: #up
            pass
        if key_code==39: #right
            pass
        if key_code==40: #bottom
            pass
        if key_code==13: #NUM ENTER
            pass
        if key_code==96: #0
            pass
        print(event)
        
    def on_click(self,event):
        pos=[event[1],event[2]]
        row,column=self.grid1.evaluate_row_column_indices(pos)
        print(row,column)
        self.grid1.grid[row][column]=1
        for i in range(len(self.grid1.rectangles)):
            for j in range(len(self.grid1.rectangles[i])):
                self.grid1.rectangles[i][j].is_clicked(pos)
    
if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Game)
    app.run()