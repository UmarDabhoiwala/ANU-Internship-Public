from flask import Flask
from flask import request, escape, send_file, url_for, jsonify, render_template, redirect
from excel_gen import ExcelGen
from powerPointGenCopy import PowerPointGen
from wordDocGen import WordDocGenerator
from audioFileGen import generateSpeech
from ebook_maker import create_book
from resume_gen import resume_gen
from faking_reviews import goodreads_gen, lbox
from recipeMaker import cookbook
from coverLetterGen import cover_letter_gen
import shutil
import tempfile
from blog_gen import pelGen
import os
from pydub import AudioSegment
from testing import run_chat, get_transcript
import json
import ast
import spotifyPlaylist
from flask import Flask, redirect, request, url_for, render_template, session
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from base64 import urlsafe_b64decode
from google.auth.transport.requests import Request
import json
import base64
from bs4 import BeautifulSoup
import re
import openai



AudioSegment.converter = "node_modules/ffmpeg"
AudioSegment.ffprobe = "node_modules/ffprobe"

tmp = tempfile.NamedTemporaryFile()

app = Flask(__name__)
app.debug = True
app.secret_key = 'your secret key'.encode('utf8')
app.config['UPLOAD_FOLDER'] = 'audio_uploads'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # For development only

CLIENT_SECRET_FILE = 'credentials.json'

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'

@app.route('/Gmail_Auth')
def Gmail_Auth():
    return '<a href="/authorize">Authorize Gmail API</a>'

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')

    session['state'] = state  # store state in session
    print(f"Saved state: {state}")

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # Get the state parameter from the user's session
    state = session['state']
    print(f"Retrieved state: {state}")
    flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        json.dump(json.loads(flow.credentials.to_json()), token)

    return redirect(url_for('list_emails', tab = 'primary'))

@app.route('/list_emails/<tab>')
def list_emails(tab):
    # Load credentials from the 'token.json'.
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return redirect(url_for('authorize'))

    gmail_service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    print(tab)
    tab_dict = {'primary': 'CATEGORY_PERSONAL', 'social': 'CATEGORY_SOCIAL', 'promotions': 'CATEGORY_PROMOTIONS', 'updates': 'CATEGORY_UPDATES', 'forum': 'CATEGORY_FORUMS'}
    label = tab_dict.get(tab, 'INBOX')  # Default to 'INBOX' if tab isn't recognized
    print(label)
    next_page_token = request.args.get('next_page_token', None)

    try:
        # Add the 'labelIds' and 'pageToken' parameters to the list request
        list_request = gmail_service.users().messages().list(
            userId='me',
            labelIds=['INBOX', label],
            maxResults=50,
            pageToken=next_page_token,
        )
        results = list_request.execute()
        messages = results.get('messages', [])
        next_page_token = results.get('nextPageToken', None)

        if not messages:
            return 'No messages found.'
        else:
            email_list = []
            for message in messages:
                msg = gmail_service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['subject', 'date']).execute()
                email = {
                    'id': message['id'],
                    'subject': '',
                    'time': '',
                }
                for header in msg['payload']['headers']:
                    if header['name'].lower() == 'subject':
                        email['subject'] = header['value']
                    elif header['name'].lower() == 'date':
                        email['time'] = header['value']

                email_list.append(email)

        return render_template('emails.html', emails=email_list, label=label, tab=tab, next_page_token=next_page_token)

    except HttpError as error:
        return f'An error occurred: {error}'

@app.route('/view-email/<id>')
def view_email(id):
    credentials = Credentials.from_authorized_user_file('token.json')
    gmail_service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    try:
        msg = gmail_service.users().messages().get(userId='me', id=id).execute()
        email = {
            'id': id,
            'subject': '',
            'time': '',
            'body': '',
            'refinedText': ''
        }
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    text = urlsafe_b64decode(data).decode('utf-8')
                    soup = BeautifulSoup(text, 'html.parser')
                    email['body'] = text
                    cleaned_text = re.sub(r'\s+', ' ', soup.get_text().strip())
                    email['refinedText'] = cleaned_text

        for header in msg['payload']['headers']:
            if header['name'] == 'Subject':
                email['subject'] = header['value']
            elif header['name'] == 'Date':
                email['time'] = header['value']

        return render_template('view_email.html', email=email)
    except HttpError as error:
        return f'An error occurred: {error}'

@app.route('/view-email/chatGPT-response/<id>')
def chatGPT_response(id):
    # Load the email as before
    credentials = Credentials.from_authorized_user_file('token.json')
    gmail_service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    try:
        msg = gmail_service.users().messages().get(userId='me', id=id).execute()
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    text = urlsafe_b64decode(data).decode('utf-8')
                    soup = BeautifulSoup(text, 'html.parser')
                    cleaned_text = re.sub(r'\s+', ' ', soup.get_text().strip())
                    chatGPTResponse = chatGPTEmail(cleaned_text)
                    return chatGPTResponse
    except HttpError as error:
        return f'An error occurred: {error}'

def chatGPTEmail(textToReplyTo):

    system_prompt = """
    You are a to help the user write replies to email.
    The user will give you the email text, You will then compose an appropriate reply to the email.
    Only respond with the draft email, nothing else.
    Use everyday language and maintain a professional tone.
    """

    message = [{"role": "system", "content": system_prompt},
                    {"role": "user", "content": textToReplyTo}]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= message
    )

    response = completion['choices'][0]["message"]["content"]

    return response

def create_message_with_reply(subject, message_text, to, thread_id):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    raw_message = raw_message.decode()

    body = {'raw': raw_message, 'threadId': thread_id}
    return body


@app.route('/')
def index():

    if os.path.exists('messages.txt'):
        os.remove('messages.txt')
        print("File deleted successfully")
    else:
        print("File not found")

    return render_template('landing.html')


@app.route('/Word')
def Word():
    return render_template('wordDoc.html')

@app.route('/Spotify_Rec')
def Spotify_Rec():
    return render_template('spotifyRec.html')

@app.route('/generate-playlist', methods=['POST'])
def generate_playlist():

    media_list = request.form.getlist('media[]')
    media_type = request.form.get('sheet-type')

    trackList, media= spotifyPlaylist.getTrackList(media_type, media_list)

    return render_template('trackList.html', trackList=trackList, media_type=media_type, media=media)


@app.route('/generate-more-tracks', methods=['POST'])
def generate_more_tracks():
    media_type = request.form.get('media_type')
    media = request.form.get('media').split(',')

    trackList = spotifyPlaylist.moreTracks(media_type, media)

    # Return the new track list to the same template
    return render_template('trackList.html', trackList=trackList)


@app.route('/generate-playlist2', methods=['POST'])
def generate_playlist2():

    playlist_url = spotifyPlaylist.generate_playlist()

    return redirect(url_for('display_playlist', playlist_url=playlist_url))


@app.route('/display-playlist', methods=['GET'])
def display_playlist():
    playlist_url = request.args.get('playlist_url')
    return render_template('display_playlist.html', playlist_url=playlist_url)


@app.route('/AudioFile')
def AudioFile():
    return render_template('audioFile.html')

@app.route('/Excel')
def Excel():
    return render_template('excelPage.html')

@app.route('/Fake_Reviews')
def Fake_Reviews():
    return render_template('fake_review.html')


@app.route('/PowerPoint')
def PowerPoint():

    return render_template('powerpoint.html')


@app.route('/Resume')
def Resume():

    return render_template('resume.html')

@app.route('/Cover_Letter')
def Cover_Letter():

    return render_template('cover_letter.html')


@app.route('/Blog')
def Blog():

    return render_template('blog.html')

@app.route('/Talk_To_Robots')
def Talk_To_Robots():

    return render_template('talk.html')


@app.route('/EBook')
def EBook():

    return render_template('ebook.html')

@app.route('/generate-ebook', methods=['POST'])
def generate_ebook():


    num_pages = int(request.form.get('num_pages') or 1)
    authorname = str(request.form.get('author_name') or '')
    genre = str(request.form.get('genre') or '')
    style = str(request.form.get('style') or '')
    setting = str(request.form.get('setting') or '')

    print(num_pages, authorname,genre, style, setting)

    create_book(num_pages, authorname, genre, style, setting)

    path = "files/book.epub"

    return redirect(url_for('results_page', data= path))


@app.route('/Cookbook')
def Cookbook():

    return render_template('recipe.html')

@app.route('/generate-cookbook', methods=['POST'])
def generate_cookbook():


    num_recipes = int(request.form.get('num_recipes') or 1)
    cuisine = str(request.form.get('cuisine') or '')

    print(num_recipes, cuisine)
    cookbook(num_recipes, cuisine, True, False)

    path = "files/cookbook.pdf"

    return redirect(url_for('results_page', data= path))


@app.route('/audio_wait', methods=['POST'])
def audio_wait():
    try:
        with open("messages.txt", "r") as file:
                read_list = [line.strip() for line in file]
        messages = [ast.literal_eval(item) for item in read_list]

        transcript = get_transcript(messages)


        with open("files/audio_transcript.txt", "w") as file:
            file.write(transcript)

    except:
        print("No messages yet")


    return redirect(url_for ('results_page', data = "files/audio_transcript.txt"))


@app.route('/save_audio', methods=['POST'])
def save_audio():
    print("saving audio")
    audio_file = request.files.get('audio')

    #Check if messages.txt exists represents the history of the chat
    if os.path.exists('messages.txt'):
        with open("messages.txt", "r") as file:
            read_list = [line.strip() for line in file]
        messages = [ast.literal_eval(item) for item in read_list]
    else:
        messages = []

    if audio_file:
        filename = 'input.webm'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)
        try:
            messages = run_chat(messages,1)
        except Exception as e:
            print(e)
            messages =[]
            print("uhoh")
        with open("messages.txt", "w") as file:
            for item in messages:
                file.write(f"{item}\n")

        return 'audio file received', 200

    return 'No audio file received', 400



@app.route('/generate-CoverLetter', methods=['POST'])
def generate_CoverLetter():
    uploaded_file = request.files["file"]

    company = request.form.get('company')
    job_title = request.form.get('job_title')

    print(company)
    print(job_title)
    filename = uploaded_file.filename
    pdf_or_doc_x = filename[-4:]

    if pdf_or_doc_x == "docx":
        uploaded_file.save(f'files/input_resume.docx')
        file_path = "files/input_resume.docx"
    elif pdf_or_doc_x == ".pdf":
        pdf_or_doc_x = "pdf"
        uploaded_file.save(f'files/input_resume.pdf')
        file_path = "files/input_resume.pdf"

    cover_letter_gen(file_path, company, job_title)



    return redirect(url_for('results_page', data = "files/coverletter.docx"))



@app.route('/generate-resume', methods=['POST'])
def generate_resume():

    job_title = request.form.get('job_title')
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    address = request.form.get('address')
    company1 = request.form.get('company1')
    company2 = request.form.get('company2')
    company3 = request.form.get('company3')

    filed = [company1, company2, company3, job_title, phone_number, name, address]
    filed = [item if item != '' else None for item in filed]

    print(filed)


    resume_gen.resume_generator("actual", filed)
    try:
        shutil.copy('resume.pdf', 'files/resume.pdf')
        shutil.copy('input.json', 'files/input.json')
        shutil.copy('resume.json', 'files/resume.json')

        os.remove ('resume.pdf')
        os.remove('input.json')
        os.remove('resume.json')
    except FileNotFoundError:
        pass

    path = 'files/resume.pdf'


    return redirect(url_for('results_page', data= path))


@app.route('/generate-blog', methods=['POST'])
def generate_blog():
    author = request.form.get('author')
    blog_num = int(request.form.get('num_blogs'))
    blog_topic = request.form.get('blog_topic')

    print(author, blog_num, blog_topic)

    pelGen.fullrun(blog_num, blog_topic, author)



    path = 'blog_gen/website_serve.zip'

    return redirect(url_for('results_page', data= path))




@app.route('/generate-sheet', methods=['POST'])
def generate_sheet():
    sheet_type = request.form.get('sheet-type')
    rows = request.form.get('num_rows')

    ExcelGen(int(rows), int(sheet_type), graphsWanted = True)

    path = 'files/base.xlsx'

    return redirect(url_for('results_page', data= path))


@app.route('/generate-reviews', methods=['POST'])
def generate_reviews():
    review_type = request.form.get('review-type')
    rows = request.form.get('num_rows')

    if os.path.exists("files/book_reviews.csv"):
            os.remove("files/book_reviews.csv")

    if os.path.exists("files/letterboxd_reviews.csv"):
            os.remove("files/letterboxd_reviews.csv")


    print(review_type, rows)

    if review_type == "books":
        goodreads_gen.generate_book_reviews(int(rows) -1)
        path = 'files/book_reviews.csv'
    else:
        lbox.generate_movie_reviews(int(rows) -1)
        path = 'files/letterboxd_reviews.csv'

    return redirect(url_for('results_page', data= path))

@app.route('/generate-word', methods=['POST'])
def generate_word():
    sheet_type = request.form.get('sheet-type')
    companyA = str(request.form.get('companyA_name') or '')
    companyB = str(request.form.get('companyB_name') or '')
    employeeName = str(request.form.get('companyA_employee_name') or '')
    employeePosition = str(request.form.get('companyA_employee_position') or '')
    custom = str(request.form.get('prompt_type') or '')


    WordDocGenerator(int(sheet_type), companyA, companyB, employeeName, employeePosition, custom)

    path = "files/example.docx"

    return redirect(url_for('results_page', data= path))

@app.route('/generate-PowerPoint', methods=['POST'])
def generate_PowerPoint():
    theme = request.form.get('theme')
    subject = request.form.get('subject')
    slideNum = request.form.get('num-slides')
    images = request.form.get('include_images')

    if images == "yes":
        images = True
    else:
        images = False

    PowerPointGen(theme, subject, slideNum, images)

    return redirect(url_for('results_page', data = "files/example.pptx"))


@app.route('/generate-AudioFile', methods=['POST'])
def generate_AudioFile():
    theme = request.form.get('voice')
    subject = request.form.get('subject')

    generateSpeech(int(theme), subject)

    return redirect(url_for('results_page', data = "files/output.mp3"))



@app.route('/results-page')
def results_page():
    # Display the results here
    url = request.args.get('data')
    return render_template('download.html', path = url)

@app.route('/download')
def download():
    message = request.args.get('message')
    print(message)
    path = message
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(host="127.0.0.1", port=8080, debug=True)


