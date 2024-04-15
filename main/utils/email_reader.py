from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
PROJECT_DIR = os.getcwd()
test_data_dir_utils = os.path.join(PROJECT_DIR, "main/utils")
test_data_dir_email = os.path.join(PROJECT_DIR, "test_data/files")
# if 'utils' in PROJECT_DIRECTORY:
#     PROJECT_DIR = PROJECT_DIRECTORY.replace("utils", "test_data")
print(PROJECT_DIR)


def get_email():
    count = 0
    creds = None
    with open(test_data_dir_utils+'/token.pickle', 'rb') as token:
        creds = pickle.load(token)
    with open(test_data_dir_utils+'/cred.json', 'r') as infile:
        my_data = json.load(infile)

    if not creds.valid:
        try:
            creds.refresh(Request())
        except:
            print("Try to refresh token failed")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # creds.refresh(Request())
            creds = None
            flow = InstalledAppFlow.from_client_secrets_file(test_data_dir_utils+'/cred.json', scopes=SCOPES)
            creds = flow.run_local_server(port=0, timeout_seconds=10)
            session = flow.authorized_session()

        with open(test_data_dir_utils+'/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        my_data['installed']['refresh_token'] = creds.refresh_token
        with open(test_data_dir_utils+'/cred.json', 'w') as outfile:
            json.dump(my_data, outfile, indent=4)

    service = build('gmail', 'v1', credentials=creds)
    result = service.users().messages().list(userId='me').execute()
    messages = result.get('messages')
    counter = 0
    for msg in messages:
        if counter > 10:
            break
        counter = counter + 1
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        try:
            payload = txt['payload']
            headers = payload['headers']
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
                if d['name'] == 'To':
                    receiver = d['value']
                if d['name'] == 'Date':
                    date = d['value']
            part1 = payload.get('parts')[0]
            part2 = payload.get('parts')[1]
            data = part1['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            url_data = part2['body']['data']
            url_data = url_data.replace("-", "+").replace("_", "/")
            count = count + 1
            if count == 15:
                break
            with open(test_data_dir_email + "/email_reader.txt", "a") as f:
                f.write("Subject" + " : " + subject + '\n')
                f.write("From" + " : " + sender + '\n')
                f.write("To" + " : " + receiver + '\n')
                f.write("Date" + " : " + str(date) + '\n')
                f.write("Message" + " : " + str(data) + '\n')
                f.write("Url" + " : " + str(url_data) + '\n')
                f.write('\n')
        except:
            pass

    f.close()


def try_to_convert_to_int(val):
    try:
        val = int(val)
    except:
        pass
    return val


def create_json():
    fp = open(test_data_dir_email + "/email_reader.txt", "w")
    fp.close()
    jp = open(test_data_dir_email + "/email_data.json", "w")
    jp.close()
    get_email()

    data, group = [], {}
    with open(test_data_dir_email + "/email_reader.txt", "r") as f_in:
        for line in map(str.strip, f_in):
            if line == "":
                if group:
                    data.append(group)
                group = {}
            else:
                k, v = map(str.strip, line.split(':', maxsplit=1))
                group[k] = try_to_convert_to_int(v) if v else None

    if group:
        data.append(group)

    json_data = json.dumps(data, indent=4)
    with open(test_data_dir_email + "/email_data.json", "w") as f_in:
        f_in.write(json_data)
        f_in.close()
