import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import *
from tkinter import messagebox
import threading

class EmailSenderApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Sender")

        self.frame = Frame()
        self.frame.grid(column=0, row=0, padx=10, pady=10)

        Label(self.frame, text="Sender's Email:").grid(column=0, row=0, sticky="w")
        self.sender_email_entry = Entry(self.frame)
        self.sender_email_entry.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Sender's Password:").grid(column=0, row=1, sticky="w")
        self.sender_password_entry = Entry(self.frame, show="*")
        self.sender_password_entry.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Recipient's Email:").grid(column=0, row=2, sticky="w")
        self.recipient_email_entry = Entry(self.frame)
        self.recipient_email_entry.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        # Create a button with the name Add Recipient and update the all below row property values
        self.add_button = Button(self.frame, text="Add Recipient", command=self.add_recipient)
        self.add_button.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        # Create a Listbox with the name Recipients List.
        Label(self.frame, text="Recipients List:").grid(column=0, row=4, sticky="w")
        self.recipients_listbox = Listbox(self.frame)
        self.recipients_listbox.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Subject:").grid(column=0, row=5, sticky="w")
        self.subject_entry = Entry(self.frame)
        self.subject_entry.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Message:").grid(column=0, row=6, sticky="w")
        self.message_body_text = Text(self.frame, width=40, height=10)
        self.message_body_text.grid(column=1, row=6, padx=10, pady=5, columnspan=2)

        
        self.send_button = Button(self.frame, text="Send Email", command=self.send_email)
        self.send_button.grid(column=1, row=7, padx=10, pady=10, columnspan=2)

        # Declare recipients email list
        self.recipients_email = []


    # Declare add_recipient function to add the recipient to the list.
    def add_recipient(self):
        email = self.recipient_email_entry.get()
        if(email):
            self.recipients_email.append(email)
            self.update_listbox()
            # Clear the text input of recipient_email_entry 
            self.recipient_email_entry.delete(0, END)
    
    # Declare update_listbox function to update list box.
    def update_listbox(self):
        self.recipients_listbox.delete(0, END)
        for recipient in self.recipients_email:
            self.recipients_listbox.insert(END, recipient)
   
    def send_email(self):
        threading.Thread(target=self.send_single_email).start()

    def send_single_email(self):
        sender_email = self.sender_email_entry.get()
        sender_password = self.sender_password_entry.get()
        # Comment the below line
        # recipient_email = self.recipient_email_entry.get()
        subject = self.subject_entry.get()
        message_body = self.message_body_text.get("1.0", "end")
        
        # Write for loop to send email to each recipient
        for recipient_email in self.recipients_email:
            try:
                smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
                smtp_server.starttls()
                smtp_server.login(sender_email, sender_password)

                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = recipient_email
                message["Subject"] = subject
                message.attach(MIMEText(message_body, "plain"))
        
                smtp_server.sendmail(sender_email, recipient_email, message.as_string())
                smtp_server.quit()
                messagebox.showinfo("Email Sent", "Email sent successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")


def main():
    app = EmailSenderApp()
    app.mainloop()

if __name__ == "__main__":
    main()
