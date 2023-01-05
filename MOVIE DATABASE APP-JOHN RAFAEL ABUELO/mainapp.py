#importing modules

from tkinter import *
from PIL import ImageTk,Image
from tkinter import *
import requests
import tmdbsimple as tmdb
from MovieData import get_movie_data, download_img
from PIL import ImageTk, Image
from threading import Thread
import tkinter
import os
import sys

#creating tk window for menu screen
window=Tk()
window.geometry('900x500')
window.configure(bg='#F6F2EC')#12c4c0')
window.resizable(0,0)
window.title('Movie Finder App by John Rafael Abuelo')

#importing API key
API_KEY = '62c29c67169d49f5b6d44ae275e236c5'

tmdb.REQUESTS_TIMEOUT = 5 #requesting timeout from tmdb API
tmdb.REQUESTS_SESSION = requests.Session() #requesting session from tmdb API

#setting up variables for API information
search = tmdb.Search() #search function for searching movies
object_list = []
current_index = 0
poster_img = None




 #creating default home screen for main menu
def default_home(): 
    f2=Frame(window,width=900,height=455,bg='#8F6F5A')
    f2.place(x=0,y=45)
    l2=Label(f2,text='Welcome To The\nMovie Finder\nApplication',fg='white',bg='#8F6F5A')
    l3=Label(f2,text='C r e a t e d  b y :  J o h n  R a f a e l  A b u e l o',fg='#4D2318',bg='#8F6F5A')
    l3.place(x=215,y=400-45)
    l3.config(font=('arial',15))
    l4=Label(f2,text='Click the Menu icon on the top left of the screen to navigate the app.',fg='white',bg='#8F6F5A')
    l4.place(x=145,y=60-45)
    l4.config(font=('arial',15))
    l2.config(font=('Impact',60))
    l2.place(x=175,y=90-45)    
    
    img = ImageTk.PhotoImage(Image.open("deco1.png"))
    label = Label(window, image = img,highlightthickness=0,borderwidth=0)
    label.image = img
    label.place(x=635,y=267)

#creating home screen in main menu
def home():
    f1.destroy()
    f2=Frame(window,width=900,height=455,bg='#8F6F5A')
    f2.place(x=0,y=45)
    l2=Label(f2,text='Welcome To The\nMovie Finder\nApplication',fg='white',bg='#8F6F5A')
    l3=Label(f2,text='C r e a t e d  b y :  J o h n  R a f a e l  A b u e l o',fg='#4D2318',bg='#8F6F5A')
    l3.place(x=215,y=400-45)
    l3.config(font=('arial',15))
    l4=Label(f2,text='Click the Menu icon on the top left of the screen to navigate the app.',fg='white',bg='#8F6F5A')
    l4.place(x=145,y=60-45)
    l4.config(font=('arial',15))
    l2.config(font=('Impact',60))
    l2.place(x=175,y=90-45)
    
    img = ImageTk.PhotoImage(Image.open("deco1.png"))
    label = Label(window, image = img,highlightthickness=0,borderwidth=0)
    label.image = img
    label.place(x=635,y=267)
    toggle_win()
 
#creating function for calling the movie finder app
def main():
    f1.destroy()
    root = Toplevel()

    root.minsize(height=700, width=1400)
    root.title("Movie Details App by John Rafael Abuelo")
    ui_background = "#F6F2EC"
    image = Image.open('bk.png')
    bg = ImageTk.PhotoImage(image)
    ui_foreground = "black"
    root.config(bg=ui_background)
    
    title_font = ("Impact", 40, "bold")
    description_font = ("arial", 12, "bold")
    label = Label(root, image=bg)
    label.place(x = 0,y = 0)


#cache function for clearing data when a new movie is searched by the user
    def delete_prev_cache():
        folder = 'posters/'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    
#function for 'searching for movies' text when user searches a movie
    def search_title(event):
        def execute():
            global search, object_list, current_index
            delete_prev_cache()
            loading_info.config(text="Searching For Movies...!")
            current_index = 0
            query = search_bar.get()
            object_list = get_movie_data(query)
            loading_info.config(text="")
            display_movies()
        Thread(target=execute).start()

#creating function for next movie button 
    def next_movie():
        global current_index
        current_index += 1
        if current_index == len(object_list):
            current_index = 0
        display_movies()
        
#creating function for previous movie button
    def prev_movie():
        global current_index
        current_index -= 1
        if current_index < 0:
            current_index = len(object_list) - 1
        display_movies()
        
#creating function for displaying the movie's poster image and details
    def display_movies():
        def execute():
            global current_index, poster_img, object_list
            if len(object_list) == 0:
                loading_info.config(text="No movie found for the given keyword!") #message for when there are no movies found for given keyword
                return
            loading_info.config(text="Fetching Movie Data...")
            movie = object_list[current_index]
            img = download_img(f"https://image.tmdb.org/t/p/w500{movie.poster}", movie.id) #downloading movie image from api
            poster_img = ImageTk.PhotoImage(Image.open(img))
            poster_canvas.create_image(175, 220, image=poster_img, anchor=CENTER)
            description_box.config(state=NORMAL)
            description_box.delete(1.0, 'end')
            description_box.insert(1.0, movie.description)
            details_box.config(state=NORMAL)
            details_box.delete(1.0, 'end')
            
            #displaying movie details
            
            details_box.insert(1.0, f"Full Name: {movie.title}\n\n"
                                    f"Release Date: {movie.release_date}\n\n"
                                    f"Language: {movie.language}\n\n"
                                    f"Rating: {movie.rating}\n\n"
                                    
                                    f"Movie ID: {movie.id}")
            loading_info.config(text=f"Result {current_index+1} out of {len(object_list)} results")
            description_box.config(state=DISABLED)
            details_box.config(state=DISABLED)
        Thread(target=execute).start()

    title = Label(root, text=f"Movie Finder", font=title_font, bg='#FAF5E2', fg='#4D2318') #creating title of app
    title.pack(pady=(20, 10))

    options_frame = Frame(root, bg=ui_background) #creating a frame for search option
    options_frame.pack(pady=20)
    
    #customizing and setting up search bar and label
    search_label = Label(options_frame, text="Enter A Movie Name: ", bg='#FAF5E2', fg=ui_foreground, font=('helvetica', 16, 'normal'))
    search_label.grid(row=0, column=0)
    search_bar = Entry(options_frame, width=30, font=('helvetica', 16, 'normal'))
    search_bar.grid(row=0, column=1, padx=(0, 20))
    search_bar.focus()
    root.bind('<Return>', search_title)
    

    #creating frame for loading the movie
    loading_frame = Frame(root, bg=ui_background)
    loading_frame.pack(pady=(0, 5))
    
    #customizing loading frame
    loading_info = Label(loading_frame, text="Enter any name of a movie to start browsing movie database", bg='#FAF5E2', fg=ui_foreground,
                        font=('Helvetica', 14, 'normal'))
    loading_info.pack(pady=(0, 0))

    #creating the main frame where user will see the movie description, details, and poster
    main_frame = Frame(root, bg="#8F6F5A", height=100, width=700, highlightbackground='#4D2318', highlightthickness=15)
    main_frame.pack(pady=30)
    
    #creating and customizing canvas for where movie poster will be displayed
    poster_canvas = Canvas(main_frame, height=440, width=350, bg=ui_background, highlightcolor="black")
    poster_canvas.grid(row=0, column=4, rowspan=4, pady=(20,20), padx=30)
    poster_img = ImageTk.PhotoImage(Image.open("default_movie.jpg"))
    poster_canvas.create_image(175, 220, image=poster_img, anchor=CENTER)
    poster_label = Label(main_frame, pady=7, bg="#8F6F5A", fg="#F5EDE1", text="Movie Poster", font=('Impact', 25, "bold"))
    poster_label.place(x=595,y=15)
    
    #creating movie description box
    description_label = Label(main_frame, bg="#8F6F5A",  fg="#F5EDE1", pady=11, text="Movie Description", font=('Impact', 25, "bold"))
    description_label.grid(row=0, column=2)
    description_box = Text(main_frame, width=40, height=9, font=description_font, bg="#F5EDE1",  fg='#4D2318',
                        pady=20, padx=30, wrap='word', highlightcolor="black", borderwidth=2,
                        )
    description_box.grid(row=1, column=2, padx=30, pady=(0, 5))
    description_box.insert(1.0, "Movie plot details and synopsis will be shown here.")
    description_box.config(state=DISABLED)
    
    #creating movie details box
    details_label = Label(main_frame, pady=7, bg="#8F6F5A", fg="#F5EDE1", text="Movie Details", font=('Impact', 25, "bold"))
    details_label.grid(row=2, column=2)
    details_box = Text(main_frame, width=40, height=9, font=description_font, bg="#F5EDE1",  fg='#4D2318',
                    pady=20, padx=30, wrap='word', highlightcolor="black", borderwidth=2,
                    )
    details_box.grid(row=3, column=2, padx=20, pady=(10, 30))
    
    
    #this is where the movie details will be inserted
    details_box.insert(1.0,         f"Full Name: \n\n"
                                    f"Release Date: \n\n"
                                    f"Language: \n\n"
                                    f"Rating: \n\n"
                                    
                                    f"Movie ID: ")
    details_box.config(state=DISABLED)
    
    #creating and customizing the 'next movie' button
    next_btn = Button(main_frame, text=">", height=2, width=5, bg="#F6F2EC", fg='#8F6F5A', font="impact",highlightthickness=0.5, highlightbackground='#4D2318', activebackground="#4D2318",
                    command=next_movie)
    next_btn.place(x=702,y=536)
    
    #creating and customizing the 'previous movie' button
    prev_btn = Button(main_frame, text="<", height=2, width=5, bg="#F6F2EC", fg='#8F6F5A', font="impact",highlightthickness=0.5, highlightbackground='#4D2318',  activebackground="#4D2318",
                    command=prev_movie)
    prev_btn.place(x=627,y=536)



    #running movie finder application   
    root.mainloop() 
    toggle_win()
   
    
#creating function for application details
def details():
    
    f1.destroy()
    f2=Frame(window,width=900,height=455,bg='#8F6F5A')
    f2.place(x=0,y=45)
    l2=Label(f2,text='This is a Movie finding app where you can find the details, descriptions, and synopsis of just about\nevery film ever released! The app uses the TMDB API to access the movie database online.',fg='white',bg='#8F6F5A')
    l3=Label(f2,text='App Created by: John Rafael Abuelo\nBath Spa University\nCreative Computing Year 2\nTutor: Ms. Arshiya',fg='#4D2318',bg='#F6F2EC',padx=10,pady=10)
    l3.place(x=335,y=200-45)
    l3.config(font=('arial',10))
    l2.config(font=('Impact',15))
    l2.place(x=80,y=90-45)
    
    img = ImageTk.PhotoImage(Image.open("deco2.png"))
    label = Label(window, image = img,highlightthickness=0,borderwidth=0)
    label.image = img
    label.place(x=605,y=167)
    toggle_win()

#creating function for application sidebar
def toggle_win():
    global f1
    f1=Frame(window,width=300,height=500,bg='#4D2318')
    f1.place(x=0,y=0)
    
    #designing buttons of sidebar
    def bttn(x,y,text,bcolor,fcolor,cmd):
     
        def on_entera(e):
            myButton1['background'] = bcolor #ffcc66
            myButton1['foreground']= '#4D2318'  #000d33

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground']= 'white'

        myButton1 = Button(f1,text=text,
                       width=42,
                       height=2,
                       fg='white',
                       border=0,
                       bg=fcolor,
                       activeforeground='#4D2318',
                       activebackground=bcolor,            
                        command=cmd)
                      
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x,y=y)
        
    #creating sidebar buttons
    bttn(0,80,'H O M E','#F6F2EC','#4D2318',home)
    bttn(0,117,'M O V I E S','#F6F2EC','#4D2318',main)
    bttn(0,154,'D E T A I L S','#F6F2EC','#4D2318',details)
    

    #creating function for removing application sidebar
    def dele():
        f1.destroy()
        b2=Button(window,image=img1,
               command=toggle_win,
               border=0,
               bg='#F6F2EC',
               activebackground='#4D2318')
        b2.place(x=5,y=8)

    global img2
    img2 = ImageTk.PhotoImage(Image.open("close.png"))
    
    #button for closing application sidebar
    Button(f1,
           image=img2,
           border=0,
           command=dele,
           bg='#4D2318',
           activebackground='#4D2318').place(x=5,y=10)
    

default_home() #running default homepage of the app

img1 = ImageTk.PhotoImage(Image.open("open.png"))

#creating button for opening main menu sidebar
global b2
b2=Button(window,image=img1,
       command=toggle_win,
       border=0,
       bg='#8F6F5A',
       activebackground='#8F6F5A')
b2.place(x=5,y=8)


window.mainloop() #running application