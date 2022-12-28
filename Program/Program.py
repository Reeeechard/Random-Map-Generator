from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import random
import matplotlib.pyplot as plt
import networkx as nx

class UI:
    def __init__(self):
        # as the base value for the user choice
        self.island = 0

        # list of vertices for user Input
        self.locations = []

        # initialize the ui
        self.ui = Tk()

        # set the program title
        self.ui.title("Random Map Generator")

        # set the default window size
        self.ui.geometry("1366x768")

        # set the frame for graph display
        self.graphFrame = Frame(master=self.ui, width=1000, bg="lightblue")
        self.graphFrame.pack_propagate(0)
        self.graphFrame.pack(fill=BOTH, side=LEFT)

        # set the frame for user inputs
        self.userFrame = Frame(master=self.graphFrame, width=1000, height=250, bg="aquamarine")
        self.userFrame.pack_propagate(0)
        self.userFrame.pack(fill=BOTH, side=BOTTOM)

        # set the frame for location display
        self.locationFrame = Frame(master=self.ui, width=366, bg="mediumspringgreen")
        self.locationFrame.pack_propagate(0)
        self.locationFrame.pack(fill=BOTH, side=RIGHT)

        # set the frame for DFS and BFS routes
        self.routeFrame = Frame(master=self.locationFrame, width=366, height=250, bg="mediumspringgreen")
        self.routeFrame.pack_propagate(0)
        self.routeFrame.pack(fill=BOTH, side=BOTTOM)

    def interactable(self):
        # get user choice for islands
        choiceLabel = Label(self.userFrame, text="Choose whether or not the graph can have islands or not:", font=('Helvetica', 12)).pack(fill=X, padx=5)
        # a drop down option
        self.userChoice = StringVar()
        self.choice = ttk.Combobox(self.userFrame, textvariable=self.userChoice, font=('Helvetica', 12))
        # set the drop down values
        self.choice['values'] = ["Island not Possible", "Island Possible"]
        # prevent typing a value
        self.choice['state'] = 'readonly'
        self.choice.pack(padx=5, pady=5)
        # trace what option the user picked
        self.userChoice.trace('w', self.getDropdownChoice)

        # get location from user
        locationLabel = Label(self.userFrame, text="Write each location name here and click submit for each location: ", font=('Helvetica', 12)).pack(fill=X, padx=5,)
        self.locationEntry = Entry(self.userFrame, font=('Helvetica', 12))
        self.locationEntry.pack(fill=X, padx=5)
        locationButton = Button(self.userFrame, text="Submit", command=self.insertLocations, font=('Helvetica', 10)).pack(padx=5, pady=5)

        # get DFS & BFS start
        startLabel = Label(self.userFrame, text="Write the location where you'd like to make as the start for route example: ", font=('Helvetica', 12)).pack(fill=X, padx=5)
        self.startEntry = Entry(self.userFrame, font=('Helvetica', 12))
        self.startEntry.pack(fill=X, padx=5)
        submitButton = Button(self.userFrame, command=self.getStartRoute, text="Submit", font=('Helvetica', 10)).pack(padx=5, pady=5)

        # button that displays the plot
        generateButton = Button(self.userFrame, command = self.createGraph, text = "Generate", font=('Helvetica', 10)).pack(side=BOTTOM)

        # delete vertice (location) UI
        deleteButton = Button(self.locationFrame, command=self.getDeleteLocation, text="Delete", font=('Helvetica', 12)).pack(side=BOTTOM, pady=10)
        self.deleteEntry = Entry(self.locationFrame, font=('Helvetica', 12))
        self.deleteEntry.pack(side=BOTTOM, fill=X, padx= 5)
        tipLabel = Label(self.locationFrame, text="Click Generate to see changes on the graph", font=('Helvetica', 12)).pack(fill=X, side=BOTTOM, pady=10, padx= 5)
        deleteLabel = Label(self.locationFrame, text="Enter which location to delete: ", font=('Helvetica', 12)).pack(fill=X, side=BOTTOM, padx=5)

        # get DFS and BFS display ready
        self.nonInteractable()
        # start the GUI mainloop and aditional stuff
        self.showGUI()

    def nonInteractable(self):
        # display the vertices (locations)
        self.displayLocation = Listbox(self.locationFrame, font=('Helvetica', 12))
        self.displayLocation.pack(fill=BOTH)

        # route display
        self.routes = Listbox(self.routeFrame, font=('Helvetica', 12))
        self.routes.insert(1, "DFS")
        self.routes.insert(2, "BFS")
        self.routes.insert(3, "All Path")
        self.routes.pack(fill=X)
        

    # main loop keeps everything visible until you close the GUI
    def showGUI(self):
        self.ui.mainloop()

    def plot(self):
        try:
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError: 
            pass
        # the figure that will contain the plot
        fig = Figure(figsize=(5,5), dpi=100)

        a = fig.add_subplot(111)
        
        # create a graph object for visualization
        G = nx.Graph()

        # add the edges to the graph object
        G.add_nodes_from(self.graph.node)
        G.add_edges_from(self.graph.visual)

        # plot the graph
        nx.draw_networkx(G, ax=a)
        
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(fig, master = self.graphFrame)  
        self.canvas.draw()
    
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().pack()

    def getDropdownChoice(self, *arg):
        # the choice of the user regarding islands is kept here
        self.island = self.choice.current()

    def getDeleteLocation(self):
        try:
            # get the selected location
            toDelete = self.deleteEntry.get()
        
            # remove the location from the list
            self.locations.remove(toDelete)
        except ValueError:
            messagebox.showerror("Error", "The location specified doesn't exist")
            return
        
        # get the index of the location
        index = self.displayLocation.get(0, END).index(toDelete)
        # delete by index
        self.displayLocation.delete(index)
        # clear the entry box
        self.deleteEntry.delete(0, END)
        
    def insertLocations(self):
        # append the added location to the location list
        self.locations.append(self.locationEntry.get())

        # get the index of the added location
        index = self.locations.index(self.locationEntry.get())

        # add the location to the location display box
        self.displayLocation.insert(index, self.locationEntry.get())
        # clear the entry box
        self.locationEntry.delete(0, END)

    def getStartRoute(self):
        # get the index of the location from the location list
        self.start = self.locations.index(self.startEntry.get())
        # clear the entry box
        self.startEntry.delete(0, END)

    def createGraph(self):
        if (self.island == 0):
            # generate a graph and it's edges without the possibility of islands
            self.graph = AdjMatriks(len(self.locations), self.locations)
            self.graph.randomizeEdges()
            self.plot()
        else:
            # generate a graph and it's edges with the possibility of islands
            self.graph = AdjMatriksIsland(len(self.locations), self.locations)
            self.graph.randomizeEdges()
            self.plot()
        try:
            # run the graph DFS, BFS, and findAllPath
            self.graph.DFS(self.start)
            self.graph.BFS(self.start)
            self.graph.findAllPath(self.start)

            self.routes.delete(0, END)

            # add the finished routes to the route ui
            self.routes.insert(1, "DFS")
            self.routes.insert(2, self.graph.dfs)
            self.routes.insert(3, "BFS")
            self.routes.insert(4, self.graph.bfs)
            self.routes.insert(5, "All Path")
            counter = 6
            for i in range(len(self.graph.allPath)):
                self.routes.insert(counter, self.graph.allPath[i])
                counter = counter + 1
        except ValueError:
            messagebox.showerror("Error", "Start location for DFS and BFS doesn't exist")

#------------------------------------------------------------------------------------------------------------

# code untuk yg klo habis dirandom ada yg msi 0 di row tersebut maka dijadiin 1 di col pertamanya
class AdjMatriks:
    def __init__(self, vertices, city):
        self.node = []
        self.dfs = "" # Untuk simpan hasil rute DFS nya
        self.bfs = "" # Untuk simpen hasil rute BFS nya
        self.allPath= [] # list untuk menyimpan hasil all path dari start vertex tertentu
        self.vertices = vertices
        self.matrix = [] #Untuk simpan adjacency matrix
        self.visual = [] #Untuk simpan rute antar verteks
        self.cities = [] #Untuk simpan list nama2 kota sesuai input
        # loop di bawah untuk inisialisasi adjacency matriks dengan ukuran sesuai input user
        for i in range(vertices):
            temp = []
            for j in range(vertices):
                temp.append(0)
            self.matrix.append(temp)     
        for i in city:
            self.cities.append(i)

    #Fungsi untuk random banyak edges pada graph
    def randomizeEdges(self):
        
        #Untuk random banyak edge yang ada digraf sebanyak verteks(karena setiap verteks harus ada 1 edge) + random int(0 - verteks)
        for edge in range (self.vertices + random.randint(0,self.vertices)):
            a = random.randint(0, self.vertices-1)
            b = random.randint(0, self.vertices-1)

            #Jika a = b nilainya sama maka akan diskip agar edge tidak loop di 1 verteks yang sama
            if a == b: 
                pass
            else:
                for edge in [(a, b)]:
                    if self.matrix[edge[0]][edge[1]] == 0 and self.matrix[edge[1]][edge[0]] == 0:
                        self.matrix[edge[0]][edge[1]] = 1 
                        self.matrix[edge[1]][edge[0]] = 1 
                        temp = [self.cities[a], self.cities[b]]
                        self.visual.append(temp) 
                    else:
                        pass
        
        #Cek apakah masih ada verteks yang tidak memiliki edge
        for row in range(self.vertices):
            count = 0
            for col in range(self.vertices):
                if self.matrix[row][col] == 0:
                    count += 1
                    if count == (self.vertices) or count == (self.vertices-1):
                         for edge in range(self.vertices):
                            for edges in range(self.vertices):
                                #Jika edge == edges nilainya sama maka akan diskip agar edge tidak loop di 1 verteks yang sama
                                if edge != edges:
                                    if self.matrix[edge][edges] == 0 and self.matrix[edges][edge] == 0:
                                        self.matrix[edge][edges] = 1 
                                        self.matrix[edges][edge] = 1 
                                        temp = [self.cities[edge], self.cities[edges]]
                                        self.visual.append(temp)
                                        break
                                elif edge == edges:
                                    pass 
                else: 
                    pass

    #Print Adjacency Matrix
    def print(self):
        for i in self.matrix:
            print(i)

    def BFS(self, start):
        queue = [] # buat queue kosongan
        visited = [False for _ in range(self.vertices)] #list visited ini untuk menunjukkan kota mana saja yang udah divisit
        queue.append(start) # masukkan start vertex ke queue
        visited[start] = True # visited index start jadi True sehingga kota dengan index start tidak bisa masuk queue lagi
        self.bfs = self.bfs + str(self.cities[start]) + ', ' # kota index ke start disimpan di string self.bfs  
        while queue: # diloop selama queuenya masih belum kosong
            vertice = queue.pop(0) # queue dipop
            for i in range(self.vertices): # loop sebanyak vertex
                if visited[i] is False and self.matrix[vertice][i] > 0: #jika kota i belum divisit dan matrix[vertice][i] > 0 (intinya memasukkan semua kota yang belum divisit dan berhubungan dengan vertex yang terakhir divisit)
                    queue.append(i) # i dimasukkan ke queue
                    visited[i] = True # visited index i jadi True
                    self.bfs = self.bfs + str(self.cities[i]) + ', ' # kota index ke i disimpan di string self.bfs

    def DFS(self, start):
        visited = [] # inisialisasi list visited yang menunjukkan kota mana saja yang udah divisit
        stack = [] # buat stack kosong
        stack.append(start) # stacknya diappend start node
        while len(stack) > 0: # selama stacknya belum kosong diloop
            current = stack.pop() # current merupakan node yang dipop
            if current not in visited:
                self.dfs = self.dfs + str(self.cities[current]) + ', ' # cities[current] disimpan di self.dfs
            visited.append(current) 
            for i in range(self.vertices-1, -1, -1): #loop decrement sehingga nanti hasil rute dfsnya urut
                if self.matrix[current][i] > 0 and i not in visited: #pengecekan kota mana aja yang berhubungan dengan kota current dan belum divisit
                    stack.append(i) #dimasukkan dalam stack

    def findAllPath(self, start): # modifikasi konsep BFS 
        queue = [start] # memasukkan node start ke queue
        path = [] 
        path = queue.copy() # list path merupakan hasil copy queue
        pertama = True # boolean pertama diassign True
        while len(queue) > 0: # selama queue belum kosong diloop terus
            if len(queue) == 1 and pertama == True: # jika isi queue hanya ada 1 dan boolean pertama True 
                tujuan = queue.pop(0) # tujuan ini menyimpan path yang pertama kali
                self.allPath.append(self.cities[tujuan]) # cities index ke tujuan dimasukin self.allPath
                pertama = False # pertama jadi False
            else: 
                path = queue.pop(0)
                tujuan = path[len(path)-1] # tujuan ini isinya node terakhir dari path dimana path itu list yang berisi rute yang ada sebelumnya (isi queue yang dipop sebelumnya)
                kota = []
                for i in path:
                    kota.append(self.cities[i]) # simpan semua isi path dalam bentuk cities ke dalam list kota
                self.allPath.append(kota) # list kota dimasukan ke self.allPath
            for i in range(self.vertices): # loop sebanyak self.vertices
                if self.matrix[tujuan][i] > 0 and i not in path: # pengecekan vertex yang berhubungan sama tujuan (node terakhir di suatu path) dan vertex itu sendiri belum ada di dalam path yang dicek sekarang
                    tempPath = path.copy() #tempPath mengcopy path
                    tempPath.append(i) # tempPath tambah vertex i tadi yang dicek di if
                    queue.append(tempPath) # tempPath dimasukkan ke dalam queue

#-----------------------------------------------------------------------------------------------------------

# code untuk yg hanya dirandom
class AdjMatriksIsland:
    def __init__(self, vertices, city):
        self.node = []
        self.bfs = "" # untuk simpan string dari hasil bfs yang nanti ditampilkan
        self.dfs = "" # untuk simpan string dari hasil dfs yang nanti ditampilkan
        self.allPath= [] # untuk simpan string dari hasil all path yang nanti ditampilkan
        self.vertices = vertices
        self.matrix = [] #Untuk simpan adjacency matrix
        self.visual = [] #Untuk simpan rute antar verteks
        self.cities = [] #Untuk simpan list nama2 kota sesuai input
        for i in range(vertices):
            temp = []
            for j in range(vertices):
                temp.append(0)
            self.matrix.append(temp)     
        for i in city:
            self.cities.append(i)

    #Fungsi untuk random banyak edges pada graph
    def randomizeEdges(self):
        #Untuk random banyak edge yang ada digraf sebanyak verteks(karena setiap verteks harus ada 1 edge) + random int(0 - verteks)
        for edge in range (self.vertices + random.randint(0,self.vertices)):
            a = random.randint(0, self.vertices-1)
            b = random.randint(0, self.vertices-1)

            #Jika a = b nilainya sama maka akan diskip agar edge tidak loop di 1 verteks yang sama
            if a == b: 
                pass
            else:
                for edge in [(a, b)]:
                    if self.matrix[edge[0]][edge[1]] == 0 and self.matrix[edge[1]][edge[0]] == 0:
                        self.matrix[edge[0]][edge[1]] = 1 
                        self.matrix[edge[1]][edge[0]] = 1 
                        temp = [self.cities[a], self.cities[b]]
                        self.visual.append(temp) 
                    else:
                        pass

        #Cek apakah masih ada verteks yang tidak memiliki edge
        for row in range(self.vertices): # loop sebanyak row
            count = 0
            for col in range(self.vertices): # loop sebanyak kolom
                if self.matrix[row][col] == 0:
                    count += 1
            if count == (self.vertices): # kalo di row tersebut jumlah count angka 0 = banyak vertex
                n = random.randint(0, self.vertices-1)
                if row != n:
                    self.matrix[row][n] = 1
                    self.matrix[n][row] = 1
                    temp = [self.cities[row], self.cities[n]]
                    self.visual.append(temp)
                else:
                    self.node.append(self.cities[row]) #island

    #Print Adjacency Matrix
    def print(self):
        for i in self.matrix:
            print(i) 

    def BFS(self, start):
        queue = [] # buat queue kosongan
        visited = [False for _ in range(self.vertices)] #list visited ini untuk menunjukkan kota mana saja yang udah divisit
        queue.append(start) # masukkan start vertex ke queue
        visited[start] = True # visited index start jadi True sehingga kota dengan index start tidak bisa masuk queue lagi
        self.bfs = self.bfs + str(self.cities[start]) + ', ' # kota index ke start disimpan di string self.bfs  
        while queue: # diloop selama queuenya masih belum kosong
            vertice = queue.pop(0) # queue dipop
            for i in range(self.vertices): # loop sebanyak vertex
                if visited[i] is False and self.matrix[vertice][i] > 0: #jika kota i belum divisit dan matrix[vertice][i] > 0 (intinya memasukkan semua kota yang belum divisit dan berhubungan dengan vertex yang terakhir divisit)
                    queue.append(i) # i dimasukkan ke queue
                    visited[i] = True # visited index i jadi True
                    self.bfs = self.bfs + str(self.cities[i]) + ', ' # kota index ke i disimpan di string self.bfs

    def DFS(self, start):
        visited = [] # inisialisasi list visited yang menunjukkan kota mana saja yang udah divisit
        stack = [] # buat stack kosong
        stack.append(start) # stacknya diappend start node
        while len(stack) > 0: # selama stacknya belum kosong diloop
            current = stack.pop() # current merupakan node yang dipop
            if current not in visited: # pengecekan untuk current yang akan menjadi hasil rute dfs
                self.dfs = self.dfs + str(self.cities[current]) + ', ' # cities[current] disimpan di self.dfs 
            visited.append(current) # current dimasukkan ke list visited
            for i in range(self.vertices-1, -1, -1): #loop decrement sehingga nanti hasil rute dfsnya urut
                if self.matrix[current][i] > 0 and i not in visited: #pengecekan kota mana aja yang berhubungan dengan kota current dan belum divisit
                    stack.append(i) #dimasukkan dalam stack

    def findAllPath(self, start): # modifikasi konsep BFS 
        queue = [start] # memasukkan node start ke queue
        path = [] 
        path = queue.copy() # list path merupakan hasil copy queue
        pertama = True # boolean pertama diassign True
        while len(queue) > 0: # selama queue belum kosong diloop terus
            if len(queue) == 1 and pertama == True: # jika isi queue hanya ada 1 dan boolean pertama True 
                tujuan = queue.pop(0) # tujuan ini menyimpan path yang pertama kali
                self.allPath.append(self.cities[tujuan]) # cities index ke tujuan dimasukin self.allPath
                pertama = False # pertama jadi False
            else: 
                path = queue.pop(0)
                tujuan = path[len(path)-1] # tujuan ini isinya node terakhir dari path dimana path itu list yang berisi rute yang ada sebelumnya (isi queue yang dipop sebelumnya)
                kota = []
                for i in path:
                    kota.append(self.cities[i]) # simpan semua isi path dalam bentuk cities ke dalam list kota
                self.allPath.append(kota) # list kota dimasukan ke self.allPath
            for i in range(self.vertices): # loop sebanyak self.vertices
                if self.matrix[tujuan][i] > 0 and i not in path: # pengecekan vertex yang berhubungan sama tujuan (node terakhir di suatu path) dan vertex itu sendiri belum ada di dalam path yang dicek sekarang
                    tempPath = path.copy() #tempPath mengcopy path
                    tempPath.append(i) # tempPath tambah vertex i tadi yang dicek di if
                    queue.append(tempPath) # tempPath dimasukkan ke dalam queue

gui = UI()
gui.interactable()