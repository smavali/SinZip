import os
import tkinter as tk
import encoder, decoder
from tkinter import filedialog


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("SinZip")
        self.resizable(False,False)


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Compress, Decompress):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button1 = tk.Button(self, text="Compress",
                            command=lambda: controller.show_frame("Compress"))
        button2 = tk.Button(self, text="Decompress",
                            command=lambda: controller.show_frame("Decompress"))
        button1.pack(expand = True, fill = 'both')
        button2.pack(expand = True, fill = 'both')


class Compress(tk.Frame):
    def __init__(self, parent, controller):
        file_list = []
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Go to the home page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        def openFile():
            global address
            address = tk.filedialog.askopenfile()

        def openFolder():
            global address
            address = tk.filedialog.askdirectory()
            for subdir, dirs, files in os.walk(address):
                for filename in files:
                    filepath = subdir + os.sep + filename

                    if filepath.endswith(".txt"):
                        file_list.append(filepath)



            print(file_list)

        size2 = tk.Label(self, text='Buffer Size :')
        size2.pack()

        buffer_size = tk.Spinbox(self, from_=1, to=7)
        buffer_size.pack()

        size1 = tk.Label(self, text='Window Size :')
        size1.pack()

        window_size = tk.Spinbox(self, from_=1, to=32)
        window_size.pack()

        open_file_button = tk.Button(self, text='Open File', command=openFile)
        open_file_button.pack()

        open_folder_button = tk.Button(self, text='Open Folder', command=openFolder)
        open_folder_button.pack()

        label_password = tk.Label(self, text="do you want to set password? (8 Character)")
        label_password.pack()

        r = tk.BooleanVar()

        password = tk.StringVar()
        password_entry = tk.Entry(self, textvariable=password, show='*')

        def getPassword():
            return password_entry.get()

        def show_password_entry():
            password_entry.pack()
            compress_button.pack_forget()
            compress_button.pack()
            compress_button_folder.pack_forget()
            compress_button_folder.pack()

        def hide_password_entry():
            password_entry.pack_forget()

        password_Ybutton = tk.Radiobutton(self, variable=r, value=True, text='Yes',
                                          command=lambda: show_password_entry()).pack()
        password_Nbutton = tk.Radiobutton(self, variable=r, value=False, text='No',
                                          command=lambda: hide_password_entry()).pack()

        compress_button = tk.Button(self, text="Compress File"
                                    , command=lambda: encoder.main(buffer_size.get(), window_size.get(), address.name,
                                                                   password_entry.get()))
        compress_button.pack()

        def compress_folder():
            for item in file_list:
                encoder.main(buffer_size.get(),window_size.get(),item,password_entry.get())
                os.remove(item)


        compress_button_folder = tk.Button(self,text = "Compress Folder"
                                           , command = compress_folder)
        compress_button_folder.pack()


class Decompress(tk.Frame):

    def __init__(self, parent, controller):
        file_list = []
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the home page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        global address
        def openFile():
            global address
            address = tk.filedialog.askopenfile()

        def openFolder():
            global address
            address = tk.filedialog.askdirectory()
            for subdir, dirs, files in os.walk(address):
                for filename in files:
                    filepath = subdir + os.sep + filename

                    if filepath.endswith(".sinzip"):
                        file_list.append(filepath)



            print(file_list)

        open_file_button = tk.Button(self, text='Open File', command=openFile)
        open_file_button.pack(expand = True)

        open_folder_button = tk.Button(self, text='Open Folder', command=openFolder)
        open_folder_button.pack(expand = True)

        label_password = tk.Label(self, text="If your file doesn't have password\n Enter 0 in the below box,\n else enter your password.")
        label_password.pack(expand = True)

        password = tk.StringVar()
        password_entry = tk.Entry(self, textvariable=password, show='*')
        password_entry.pack(expand = True)

        def getPassword():
            return password_entry.get()
        prompt = tk.Label(self)
        prompt.pack(expand=True)

        def decomp_file():
            original_password = decoder.getData(address.name)[2]
            if (int(original_password) == int(getPassword())):
                decoder.main(address.name)
                prompt.config(text = 'Done!')
            else:
                prompt.config(text = 'Incorrect Password!')

        def decomp_folder():
            for item in file_list:
                original_password = decoder.getData(item)[2]
                if (int(original_password) == int(getPassword())):
                    decoder.main(item)
                    os.remove(item)
                    prompt.config(text='Done!')
                else:
                    prompt.config(text='Incorrect Password!')



        decomp_file_button = tk.Button(self, text="Decompress File!"
                                      , command=lambda : decomp_file())
        decomp_file_button.pack()

        decomp_folder_button = tk.Button(self, text="Decompress Folder!"
                                      , command=lambda : decomp_folder())
        decomp_folder_button.pack()



if __name__ == "__main__":
    app = SampleApp()
    app.title = "My Compressor"
    app.mainloop()
