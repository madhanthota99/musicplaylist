from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("Music player")
root.geometry("800x600")

#intialize pygame
pygame.mixer.init()

#function to show time

def play_time():
	#check to see if song is stopped
	if stopped:
		return 


	#grab cur song time
	current_time = pygame.mixer.music.get_pos() /1000
	#convert song time to time format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	


	#reconstuct the song filename
	song = playlist_box.get(ACTIVE)
	song =f'E:/musicplaylist/audio/{song}.mp3' # change dir according to ur need
	
	#find cur song length
	song_mut = MP3(song)
	global song_length
	song_length =song_mut.info.length

	#convert to time format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

	#check whether song is over
	if int(song_length) == int(song_slider.get()):
		stop()

	elif paused:
		#check to see if paused, if paused end
		pass
	else:

		#move slider along 1 sec at a time
		next_time = int (song_slider.get())+1
		#output new time value to slider, and to length  of song
		song_slider.config(to=song_length, value=next_time)



		# convert slider postion to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime(int (song_slider.get())))
		#output slider 
		status_bar.config(text=f'Time Elapsed: { converted_current_time } of { converted_song_length } ')





	#add current time to status bar
	if current_time > 0:
		status_bar.config(text=f'Time Elapsed: { converted_current_time } of { converted_song_length } ')
	#create a loop to check time every second 
	status_bar.after(1000, play_time)



#funtion to add songs
def add_song():
	song = filedialog.askopenfilename(initialdir='audio/', title="choose a song", filetypes=(("mp3 Files","*.mp3"), ))
	#strip dir from .mp3
	song=song.replace("E:/musicplaylist/audio/",'')
	song=song.replace(".mp3",'')
	#add to playlist
	playlist_box.insert(END,song)

def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='audio/', title="choose a song", filetypes=(("mp3 Files","*.mp3"), ))
	#loop through songs
	for song in songs:
		#strip dir from .mp3
		song=song.replace("E:/musicplaylist/audio/",'')
		song=song.replace(".mp3",'')
		#add to playlist
		playlist_box.insert(END,song)

#function to delete songs
def delete_song():
	playlist_box.delete(ANCHOR)

def delete_all_songs():
	playlist_box.delete(0,END)



#play function

def play():
	#set stopeed to false since song  is now playing
	global stopped
	stopped = False
	#reconstuct the song filename
	song = playlist_box.get(ACTIVE)
	song =f'E:/musicplaylist/audio/{song}.mp3'
	#my_label.config(text=song)

	#play song with pygame
	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops=0)

	play_time()


global stopped
stopped=False






def stop():
	#stop the song
	pygame.mixer.music.stop()
	#clear playlist bar
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text='')

	#set our slider to zero
	song_slider.config(value=0)

	#set stop var to true
	global stopped
	stopped = True

#create a pause var

global paused

paused= False

#pause function
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		#play
		pygame.mixer.music.unpause()
		paused=False
	else:
		#pause
		pygame.mixer.music.pause()
		paused=True

#forward funtion

def forward():
	#reset slider postion and status bar
	status_bar.config(text='')
	song_slider.config(value=0)

	#get current song
	next_one = playlist_box.curselection()
	#add one to the current song number tuple
	next_one = next_one[0]+1


	#grab song title from playlist
	song = playlist_box.get(next_one)

	#add dir
	song=f'E:/musicplaylist/audio/{song}.mp3'
	#load

	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops=0)

	#clear active bar
	playlist_box.selection_clear(0,END)

	#move active bar to next
	playlist_box.activate(next_one)

	#set active bar to next 
	playlist_box.selection_set(next_one, last=None)

#backward funtion

def backward():

	#reset slider postion ans status bar
	status_bar.config(text='')
	song_slider.config(value=0)

	#get current song
	next_one = playlist_box.curselection()
	#minus one to the current song number tuple
	next_one = next_one[0]-1


	#grab song title from playlist
	song = playlist_box.get(next_one)

	#add dir
	song=f'E:/musicplaylist/audio/{song}.mp3'
	#load

	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops=0)

	#clear active bar
	playlist_box.selection_clear(0,END)

	#move active bar to back
	playlist_box.activate(next_one)

	#set active bar to back
	playlist_box.selection_set(next_one, last=None)


#create vol function

def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

#create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

#create a slide funtion for aong pos

def slide(x):
	#reconstuct the song filename
	song = playlist_box.get(ACTIVE)
	song =f'E:/musicplaylist/audio/{song}.mp3'
	#my_label.config(text=song)

	#play song with pygame
	pygame.mixer.music.load(song)
	#play song
	pygame.mixer.music.play(loops=0, start=song_slider.get())



#create playlist box
playlist_box = Listbox(main_frame,bg ='black', fg='green',height=20, width=100, selectbackground="green",selectforeground="black")
playlist_box.grid(row=0,column=0)

#create volume slider frame
volume_frame = LabelFrame(main_frame, text='volume')
volume_frame.grid(row=0, column=1, padx=10)

#create vol slider
volume_slider = ttk.Scale(volume_frame, from_=1, to= 0, value=0.5, orient=VERTICAL, length=150, command=volume)
volume_slider.pack(pady=10)


#create song slider
song_slider = ttk.Scale(main_frame, from_=0, to= 1, orient=HORIZONTAL,length=360, value=0, command=slide )
song_slider.grid(row=2, column=0, pady=20)




#define button imgs for controls
back_btn_img = PhotoImage(file = 'images/back50.png') 
stop_btn_img =PhotoImage(file = 'images/stop50.png')
forward_btn_img =PhotoImage(file = 'images/forward50.png')
play_btn_img =PhotoImage(file = 'images/play50.png')
pause_btn_img = PhotoImage(file= 'images/pause50.png')


#button frame
control_frame = Frame(main_frame)
control_frame.grid(row=1,column=0,pady=20)

# buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=backward)
stop_button =Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)
forward_button =Button(control_frame, image=forward_btn_img, borderwidth=0, command=forward)
play_button =Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button =Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda:pause(paused))

back_button.grid(row=0, column=0, padx=10)
stop_button.grid(row=0, column=1, padx=10)
forward_button.grid(row=0, column=4, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0 , column=3, padx=10)


#main menu 
Mymenu=Menu(root)
root.config(menu= Mymenu)

#add song menu
add_song_menu = Menu(Mymenu,tearoff=0)
Mymenu.add_cascade(label="Add Songs", menu=add_song_menu)
#add one song
add_song_menu.add_command(label="Add one song to playlist", command =add_song)
# add many songgs
add_song_menu.add_command(label="Add many songs to playlist", command =add_many_songs)

#delete song menu dropdown

delete_song_menu = Menu(Mymenu,tearoff=0)
Mymenu.add_cascade(label="delete songs", menu=delete_song_menu)
delete_song_menu.add_command(label="delete a song from playlist", command=delete_song)
delete_song_menu.add_command(label="delete all songs from playlist", command=delete_all_songs)

#create a status bar
status_bar = Label(root, text='', bd=1, relief= GROOVE, anchor=E)
status_bar.pack(fill=X,side=BOTTOM, ipady=2)



# tmp label
my_label= Label(root, text="")
my_label.pack(pady=20)

root.mainloop() 