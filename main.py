import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import csv
import os


base_path = os.path.dirname(__file__)
os.chdir(base_path)
base_path = os.getcwd()
resume = os.path.join(base_path,"AttachingFiles","resume.pdf")
sender_email = "************@gmail.com" #Your Email Id
sender_pass = "***************" #Insert password if you have no 2FA enabled if you have enabled 2FA insert the app key after generating through security setting to 2FA section.
info = dict()


def read_data_csv():
    with open(os.path.join(base_path,"requests.csv"), 'r') as csvfile:
        data = csv.reader(csvfile)
        data = [i for i in data]
    for i in data:
        if i[4] in ["NS","S"]:
            temp = {
                "position":i[1],
                "mail":i[2],
                "name":i[3],
                "status":i[4],
            }
            info[i[0]] = temp


def sendmail():
    try:
        for k, v in info.items():
            if v["status"] == "NS":
                 message= MIMEMultipart()
                message["From"] = sender_email
                attachment = open(resume,'rb')
                part = MIMEBase("application","octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',f'attachment; filename=cheena_kachroo_resume.pdf')
                message.attach(part)
                pos = v["position"].upper()
                message["Subject"] = f"Akhilesh Pratap Shahi - {pos}"
                #Edit body before sending using the script
                body = f"""Hello {v["name"]},\n\nI trust this message finds you well.\n\nI am writing to express my keen interest in the {pos} position at your esteemed company.\n\n JOB LINK: {k}.\n\n ***** (INSERT YOUR CONTENT)\n\nFor your convenience, I have attached my resume to this email.\n\nI am enthusiastic about the prospect of contributing my skills and expertise to your team and am eager to discuss how my background aligns with the requirements of the {pos} position. I look forward to the opportunity to speak with you further.\n\n\nThank you for considering my application.\n\n\n\nWarm regards,\nYOUR NAME"""
                message.attach(MIMEText(body,'plain'))
                message["To"]= v["mail"]
                recepient = v["mail"]
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
                        server.login(sender_email,sender_pass)
                        server.sendmail(sender_email,recepient,message.as_string())
                    v["status"] = "S"
                except Exception as ex:
                    v["status"] = f"Error: {str(ex)}"
                info[k] = v
        with open(os.path.join(base_path,"requests.csv"),'w',newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["link","position","email","name","status"])
            for link,detail in info.items():
                csv_writer.writerow([link,detail["position"],detail["mail"],detail["name"],detail["status"]])
    except Exception as ex:
        print("Experiencing an exception while message creation")
        print(ex)


read_data_csv()
sendmail()
print(info)
