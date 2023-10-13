from ctypes import windll

import Admin
import DBconnect
import customtkinter
from PIL import Image
import os


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


class Application(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mycurser = DBconnect.mydb.cursor()
        self.admin_window = None
        self.data = None
        self.title("Travel Time Approximation for Students")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(True, True)

        # configure grid layout (4x4)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=1)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        print(current_path)
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/Images/bg_img.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0))
        self.insertion_page()

        # create Insertion Frame

    def insertion_page(self):

        self.initial_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.initial_frame.grid(row=0, column=0, padx=0, pady=(0, 0), sticky="ns")

        self.appearance_mode_label = customtkinter.CTkLabel(self.initial_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=0, column=0, padx=(360, 0), pady=(0, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.initial_frame,
                                                                       values=["System", "Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=0, column=0, padx=(630, 0), pady=(10, 10))

        self.initial_label = customtkinter.CTkLabel(self.initial_frame, text="Insert a new \n Record in DataBase",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.initial_label.grid(row=1, column=0, padx=300, pady=(25, 15))

        self.Roll_entry = customtkinter.CTkEntry(self.initial_frame, width=300, height=40,
                                                 placeholder_text="Enter Roll Number", )
        self.Roll_entry.grid(row=2, column=0, padx=30, pady=(15, 15))

        self.Name_entry = customtkinter.CTkEntry(self.initial_frame, width=300, height=40,
                                                 placeholder_text="Student Name")
        self.Name_entry.grid(row=3, column=0, padx=30, pady=(0, 15))

        self.Email_entry = customtkinter.CTkEntry(self.initial_frame, width=300, height=40,
                                                  placeholder_text="Student Email address")
        self.Email_entry.grid(row=4, column=0, padx=30, pady=(0, 15))

        self.Distance_entry = customtkinter.CTkEntry(self.initial_frame, width=300, height=40,
                                                     placeholder_text="Distance in Km")
        self.Distance_entry.grid(row=5, column=0, padx=30, pady=(0, 15))

        self.Signals_entry = customtkinter.CTkEntry(self.initial_frame, width=300, height=40,
                                                    placeholder_text="No of Traffic signals")
        self.Signals_entry.grid(row=6, column=0, padx=30, pady=(0, 15))

        self.initial_label = customtkinter.CTkLabel(self.initial_frame, text="In scale of 1 to 10 Rate Traffic "
                                                                             "You Endure",
                                                    font=customtkinter.CTkFont(size=12, weight="bold"))
        self.initial_label.grid(row=7, column=0, padx=10, pady=(0, 0))

        self.TrafficR_entry = customtkinter.CTkSlider(self.initial_frame, from_=1, to=10, border_width=12, width=300,
                                                      number_of_steps=20, progress_color="Red")
        self.TrafficR_entry.grid(row=8, column=0, padx=10, pady=(0, 0))
        self.TrafficR_entry.set(3.5)

        self.initial_label = customtkinter.CTkLabel(self.initial_frame, text="1",
                                                    font=customtkinter.CTkFont(size=10, weight="bold"))
        self.initial_label.grid(row=8, column=0, padx=(0, 320), pady=(0, 0))

        self.initial_label = customtkinter.CTkLabel(self.initial_frame, text="10",
                                                    font=customtkinter.CTkFont(size=10, weight="bold"))
        self.initial_label.grid(row=8, column=0, padx=(320, 0), pady=(0, 0))

        self.submit_button = customtkinter.CTkButton(self.initial_frame, text="Submit", command=self.submit_event,
                                                     width=200, corner_radius=5, height=30)
        self.submit_button.grid(row=9, column=0, padx=30, pady=(15, 0))

        self.admin_button = customtkinter.CTkButton(self.initial_frame, text="Admin", command=self.open_admin,
                                                    width=200, corner_radius=5, height=30)
        self.admin_button.grid(row=10, column=0, padx=30, pady=(15, 0))


        # create main frame
        self.result_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.result_frame.grid_columnconfigure(0, weight=1)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def open_admin(self):
        if self.admin_window is None or not self.admin_window.winfo_exists():
            print("new window....")
            self.admin_window = Admin.AdminApplication(self)  # create window if its None or destroyed

        else:
            self.admin_window.focus()  # if window exists focus it

    def warning(self, e):
        self.main_label = customtkinter.CTkLabel(self.result_frame, text="Warning\n" + e,
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        self.back_button = customtkinter.CTkButton(self.result_frame, text="Back", command=self.back_event, width=200)
        self.back_button.grid(row=1, column=0, padx=30, pady=(15, 15))

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def success_insertion(self):
        self.main_label = customtkinter.CTkLabel(self.result_frame, text="Your response was recorded successfully\n"
                                                                         "have a great day!!",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        self.back_button = customtkinter.CTkButton(self.result_frame, text="Back", command=self.back_event, width=200)
        self.back_button.grid(row=1, column=0, padx=30, pady=(15, 15))

    def submit_event(self):
        # print(self.Roll_entry.get(), self.Name_entry.get(), self.Email_entry.get(), self.Distance_entry.get(),
        #       self.TrafficR_entry.get(), self.Signals_entry.get())
        self.data = (self.Roll_entry.get(), self.Name_entry.get(), self.Email_entry.get(), self.Distance_entry.get(),
                     self.Signals_entry.get(), str(self.TrafficR_entry.get()))

        self.initial_frame.grid_forget()  # remove Insertion frame
        self.initial_frame.destroy()
        self.result_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show Warning frame
        datacheck = self.data[0:5]
        if not any(letter.isalnum() for letter in datacheck):
            self.warning("Please Insert Data")
        else:
            self.Insertion()

    def back_event(self):
        self.result_frame.grid_forget()  # remove Warning frame
        self.insertion_page()  # show Insertion frame

    def ConstraintsCheck(self, n, r, e, d, tr, Ns):

        check = "SELECT TrafficRating ,Distance from StudentInfo WHERE RollNo = %s"
        v = (r,)

        self.mycurser.execute(check, v)
        res = self.mycurser.fetchall()
        if len(res) > 0:
            self.warning("Invalid Roll Number, There is already an existing respond for this student..")
            return False

        if len(n) <= 40:
            if not all(letter.isalpha() for letter in n.replace(" ", "")):
                self.warning("A Name should not contain anything other then alphabets")
                return False
        else:
            self.warning("A Name should not excite mare then 40 characters")
            return False

        if len(r) <= 15:
            if not all(letter.isalnum() for letter in r.replace("-", "")):
                self.warning(
                    "A roll number should not contain thing other then alphabet and numbers")
                return False
            if len(r) < 8:
                self.warning("Enter a valid Student Roll number")
                return False

        else:
            self.warning("A Roll Number should not excite mare then 15 characters")
            return False

        if len(e) <= 25:
            if len(e) < 10:
                self.warning("Enter a valid Email address")
                return False
        else:
            self.warning("An Email should not excite mare then 25 characters")
            return False

        if not all(letter.isdigit() for letter in d.replace(".", "")):
            self.warning("Distance should only contain float value")
            return False

        if not all(letter.isdigit() for letter in tr.replace(".", "")):
            self.warning("Traffic Ratting should only contain float value")
            return False

        if 1 > float(tr) > 10:
            self.warning("Please enter valid Ratings")
            return False

        if not all(letter.isdigit() for letter in Ns):
            self.warning("Number of Traffic Signals should be an integer value")
            return False

        return True

    def Insertion(self):

        Roll = self.data[0]
        Name = self.data[1]
        Email = self.data[2]
        dis = self.data[3]
        Nosignal = self.data[4]
        Trate = self.data[5]
        AvgTime = 0.0

        if self.ConstraintsCheck(Name, Roll, Email, dis, Trate, Nosignal):
            dis = float(dis)
            Trate = float(Trate)
            Nosignal = int(Nosignal)
            AvgSpeed = 40
            SpeedFactor = AvgSpeed - AvgSpeed / (10.5 - Trate) / 5
            AvgTime = ((dis * 1000) + (Trate * dis * 100)) / ((SpeedFactor * 5) / 18) + 75 * Nosignal
            AvgTime = round(AvgTime)

            AvgTravelTime = convert(AvgTime)

        else:
            return False

        try:
            sql = "INSERT INTO StudentInfo (RollNo,StudentName,EmailId,Distance,TrafficRating,NoTrafficSignal," \
                  "AvgTime) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (Roll, Name, Email, dis, Trate, Nosignal, AvgTravelTime)
            self.mycurser.execute(sql, val)
            DBconnect.mydb.commit()
            self.success_insertion()
            return True
        except:
            self.warning("An Error occurred while Insertion of data,Please Retry again!!!")
            return False


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    windll.shcore.SetProcessDpiAwareness(2)
    # customtkinter.set_widget_scaling(1)  # widget dimensions and text size
    # customtkinter.set_window_scaling(1)  # window geometry dimensions
    try:
        mycurser = DBconnect.mydb.cursor()

        mycurser.execute("CREATE TABLE IF NOT EXISTS StudentInfo( \
            RollNo varchar(15)not null Primary Key, \
            StudentName varchar(40) not null, \
            EmailId varchar(25)not null, \
            Distance float not null, \
            TrafficRating float not null, \
            NoTrafficSignal int not null, \
            AvgTime time not null );")

    except:
        print("Fail to create Data Base")

    app = Application()
    app.mainloop()
