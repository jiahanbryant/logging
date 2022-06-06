import subprocess
import os
import datetime

ID_file = "uniqueID.txt"
KEY_file = "verified-boot.key"
SIGNATURE_file = "signature.txt"
LOG_dir = "log"
LOGfile_pre = "/test_log_"
FILE_list = [ID_file, KEY_file]

def logging(message, date):
    print(message)

    if not os.path.isdir(LOG_dir):
        try:
            os.mkdir(LOG_dir)
        except FileExistsError:
            print("Folder exists already.")
            pass
    log_file = LOG_dir + LOGfile_pre + date
    with open(log_file, 'a+') as f:
        f.write(message + '\n')
        f.close

def gen_sig(id):
    try:
        for file in FILE_list:
            if os.path.isfile(file):
                logging(file + " file checked OK ...", date)
            else:
                logging(file + " file doesn't exist, quitting...", date)
                exit()
        logging("Processing with ID=" + id, date)
        command = subprocess.run('openssl dgst -sha256 -sign verified-boot.key uniqueId.txt | base64 -w0 > signature.txt', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        logging(command.stdout, date)
        return True
    except:
        logging("Error!", date)
        return False


def main() -> None:
    global date
    date  = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    logging("Welcome to signature generator.", date)

    while True:
        ID = input("Please input Unique ID here:\n").strip()
        if ID == "":
            logging("Error, ID is empty!", date)
            continue
        else:
            with open(ID_file, 'w') as f:
                f.write(ID)
                f.close()
            while(gen_sig(ID)):
                logging("Signature is successfully generated as below(also stored in signature.txt):\n", date)
                command = subprocess.run('cat signature.txt', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
                logging(command.stdout + "\n", date)
                exit()
            logging("Failed generating signature.", date)
            break

if __name__ == "__main__":
    main()
    