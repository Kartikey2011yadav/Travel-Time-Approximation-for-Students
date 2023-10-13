import customtkinter
import os
import DBconnect
from tabulate import tabulate
from PIL import Image

theame = "dark"


class AdminApplication(customtkinter.CTkToplevel):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        customtkinter.set_appearance_mode(theame)

        self.title("Travel Time Approximation for Students")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.focus()

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/Images/bg_img.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=20)
        self.login_frame.grid(row=0, column=0, sticky="ns", padx=(300, 300), pady=(110, 110))
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Travel Time Approximation\nAdmin Login",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(40, 15))
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="Username",
                                                     height=37)
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*",
                                                     height=37, placeholder_text="Password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))

    def DisplayAll(self):
        mycurser = DBconnect.mydb.cursor()

        mycurser.execute("SELECT * FROM StudentInfo;")

        results = mycurser.fetchall()
        display_records = tabulate(results,
                                   headers=['Roll No', 'Name', 'Email', 'Distance', 'Traffic Rating', 'Traffic signals',
                                            'Time'],
                                   tablefmt='grid', numalign="center", stralign="center")

        self.main_frame.destroy()
        print(tabulate(results,
                       headers=['Roll No', 'Name', 'Email', 'Distance', 'Traffic Rating', 'Traffic signals', 'Time'],
                       tablefmt='fancy_outline',
                       showindex=True, numalign="center", stralign="center"))

        # create display frame
        self.display_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=(0, 10))  # show display frame

        self.back_button = customtkinter.CTkButton(self.display_frame, text="Back", command=self.display_exit,
                                                   width=200)
        self.back_button.grid(row=0, column=0, padx=(10, 550), pady=(10, 0))

        self.display_box = customtkinter.CTkTextbox(self.display_frame, corner_radius=0, height=450,
                                                    font=customtkinter.CTkFont(family="<Monospaced>"),
                                                    wrap="word", width=500)
        self.display_box.grid(row=1, column=0, sticky="nsew", pady=(15, 15))
        self.display_box.insert("0.0", display_records)

    def display_exit(self):
        self.display_frame.destroy()
        self.admin()

    def search_exit(self):
        self.search_display_frame.destroy()
        self.admin()

    def search_click_event(self):
        dialog = customtkinter.CTkInputDialog(text="Enter Student Roll Number:", title="Search Record")
        result = dialog.get_input()
        self.Search(result)

    def Search(self, id):
        mycurser = DBconnect.mydb.cursor()
        self.main_frame.destroy()

        Searchsql = "SELECT * FROM StudentInfo where RollNo = %s"
        val = (id,)
        mycurser.execute(Searchsql, val)

        res = mycurser.fetchall()
        if not len(res) > 0:
            self.warning("Invalid Roll Number No record found..")

        else:
            for r in res:
                display_record = " Roll Number: " + r[0] + "\n\n Student Name: " + r[1] + "\n\n Student Email address: " \
                                 + r[2] + "\n\n Distance Traveled by student: " + str(
                    r[3]) + "Km" + "\n\n Student Traffic Rating: " + str(
                    r[4]) + "\n\n Number of Traffic Signals on students way: " + str(
                    r[5]) + "\n\n Traveling Time: " + str(
                    r[6])
            # create display frame
            self.search_display_frame = customtkinter.CTkFrame(self, corner_radius=0)
            self.search_display_frame.grid_columnconfigure(0, weight=1)
            self.search_display_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=(0, 10))  # show display frame

            self.back_button = customtkinter.CTkButton(self.search_display_frame, text="Back",
                                                       command=self.search_exit, width=200)
            self.back_button.grid(row=0, column=0, padx=(10, 550), pady=(10, 0))

            self.display_box = customtkinter.CTkTextbox(self.search_display_frame, corner_radius=0, height=450,
                                                        wrap="word", font=customtkinter.CTkFont(size=20, weight="bold"))
            self.display_box.grid(row=1, column=0, sticky="nsew", pady=(15, 15))
            self.display_box.insert("0.0", display_record)

    def admin(self):
        # create main frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame

        self.appearance_mode_label = customtkinter.CTkLabel(self.main_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=0, column=0, padx=(255, 0), pady=(0, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.main_frame,
                                                                       values=["System", "Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=0, column=0, padx=(520, 0), pady=(10, 10))
        self.main_label = customtkinter.CTkLabel(self.main_frame, text="Travel Time Approximation\nAdmin Main Page",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=1, column=0, padx=30, pady=(30, 15))

        self.display_all = customtkinter.CTkButton(self.main_frame, text="Display All Records", command=self.DisplayAll,
                                                   width=200)
        self.display_all.grid(row=2, column=0, padx=30, pady=(15, 15))

        self.search_res = customtkinter.CTkButton(self.main_frame, text="Search a Record",
                                                  command=self.search_click_event, width=200)
        self.search_res.grid(row=3, column=0, padx=30, pady=(15, 15))

        self.back_button = customtkinter.CTkButton(self.main_frame, text="Logout", command=self.back_event, width=200)
        self.back_button.grid(row=4, column=0, padx=30, pady=(15, 15))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def warning_login(self, e):
        # create warning frame
        self.warn_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.warn_frame.grid_columnconfigure(0, weight=1)
        self.warn_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show warning frame
        self.main_label = customtkinter.CTkLabel(self.warn_frame, text="Warning\n" + e,
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        self.back_button = customtkinter.CTkButton(self.warn_frame, text="Back", command=self.back_event_warning_login
                                                   , width=200)
        self.back_button.grid(row=1, column=0, padx=30, pady=(15, 15))

    def warning(self, e):
        # create warning frame
        self.warn_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.warn_frame.grid_columnconfigure(0, weight=1)
        self.warn_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show warning frame
        self.main_label = customtkinter.CTkLabel(self.warn_frame, text="Warning\n" + e,
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        self.back_button = customtkinter.CTkButton(self.warn_frame, text="Back", command=self.back_event_warning
                                                   , width=200)
        self.back_button.grid(row=1, column=0, padx=30, pady=(15, 15))

    def login_event(self):
        # print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get())

        if self.username_entry.get() == "kartikey" and self.password_entry.get() == "1234":
            self.login_frame.grid_forget()  # remove login frame
            self.admin()

        else:
            self.login_frame.grid_forget()  # remove login frame
            self.warning_login("Invalid Username or Password")

    def back_event(self):
        self.main_frame.grid_forget()  # remove login frame
        self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame

    def back_event_warning_login(self):
        self.warn_frame.destroy()  # remove warning frame
        self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame

    def back_event_warning(self):
        self.warn_frame.destroy()  # remove warning frame
        self.admin()


if __name__ == "__main__":
    app = AdminApplication()
    app.mainloop()
