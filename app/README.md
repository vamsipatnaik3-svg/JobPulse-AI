so first we will go with the architecture

JobPulse AI – System Architecture
Gmail Inbox

LinkedIn · Naukri · Indeed · Company career portals · Recruiters


1. Email Collection Service
Python + Gmail API
Fetch new emails and relevant historical emails


2. Email Processing Engine
Python
Clean HTML · Remove duplicates · Extract content


3. GenAI Intelligence Engine
Gemini API
Classify emails · Extract details · Summarize · Identify urgency


4. Job Information Database
SQLite
Store jobs, companies, recruiters, interviews and application status


5. Daily Briefing Generator
Python + GenAI
Generate a personalized 8 AM report


6. Voice & Notification Service
Text-to-Speech
Convert the briefing into spoken audio


7. Your Oppo Android Phone

8:00 AM · Automated voice briefing

so first we have created the files in gmail folder
1)authentication
2)email_fetcher

in authentication file we wrote the code to authenticate our email and get the token
in email_fetcher we wrote the code to fetch the email

next we have created the folder processing and craeted the following files
1)email_cleaner
2)job_filter
3)deduplication
3)pipeline

in email_cleaner we have wrote the code to clean the code
in job_filter we have wrote the code to filer the job with keywords
in deduplication we have wrote the code to remove the duplicate mails
in pipline we have wrote the code to crate a the pipline to combine all the indipendent function flows which are in above three files

after creating this we can check through 
python -m app.processing.pipeline

next we will craete a folder intelligence
1. Classifier — What type of email is this?

Example: Keyloop application confirmation.

Output: APPLICATION_CONFIRMATION


2. Extractor — What information does it contain?
- Company: Keyloop
- Role: AI Enablement Engineer
- Status: Application received
- Salary: Not mentioned


3. Summarizer — What should the user know?

"Keyloop has received your application for AI Enablement Engineer. The recruitment team will review your profile."

we have used this pakages
groq pydantic

next we will create the folder Intelligence and create files
1)classifier
2)extractor
3)summarizer
4)intelligence_pipline

classifier is used to classify the mail
{'category': 'APPLICATION_CONFIRMATION', 'is_job_related': True, 'confidence': 0.98}
extractor is used to extract the details from the mail
summarizer is used to summarize the mail
intelligence_pipline is used to connect above three features

so after creating the intelligence pipeline we need to change the processing pipeline to integrate analize_email from intelligence pipeline

We'll start by saving every analyzed email as a database record. This is a good first design because one job application can have multiple emails over time: confirmation, assessment, interview, rejection or offer. We should preserve each email rather than overwrite previous updates.

Our first database table will be called email_analyses.

It will store:
- Original email information.
- AI classification and confidence.
- Extracted job details.
- Generated summary.
- Processing status and errors.

we will crate the database folder and craete the files
1)db.py
2)models.py
3)repository.py

we will use this files to save the analized mail in the database

next we will be crating the folder briefing and create the files
1)generator
we will use this to generate the voice means we will return what the voice should say when we get a call

next we need a voice to read out the text means text to speech so we used eleven labs for that
now after craeting the account we will select the voice id and create the api key and past them in the env file after that we will create the voice.py file in the briefing folder to create the audio file of the analized emails

next we will be using the macrodroid to get the audio file downloaded by the eleven labs into our android phone

we add voice.py file in briefing folder and inside that we will get the text to voice for analized mails and will save that as mp3 audio file in generated_audio folder

and we craete a file called audio_server to create a http secure protol to send the downloaded mp3 to our phone through macrodroid

now we will create the main file to connect everything
Fetch actual Gmail emails.


Skip previously processed emails.
Analyze new job-related emails.
Generate the daily briefing.
Generate the ElevenLabs MP3.

Technology choices
Component	Recommendation
Backend hosting	Railway or Render
Scheduled execution	Cloud cron job
Database	PostgreSQL (Supabase or Neon)
Audio storage	Supabase Storage
AI analysis	Your existing Groq integration
Voice	Your existing ElevenLabs integration
Phone automation	Existing MacroDroid setup

We can retain most of your existing Python code. We don't need to rebuild JobPulse AI from scratch.
Deployment plan
We'll migrate in this order:
1. Prepare the Python project for cloud deployment.
2. Move SQLite data to PostgreSQL.
3. Configure Gmail OAuth securely for cloud execution.
4. Configure Groq and ElevenLabs credentials as cloud secrets.
5. Move generated MP3 files to cloud storage.
6. Deploy the backend.
7. Schedule automatic execution at 7:45 AM IST.
8. Update MacroDroid to download the cloud MP3 at 8 AM.
9. Test the entire workflow without your laptop.
One important detail: We'll secure the audio download endpoint so nobody else can access your personal job updates.


Great. Now let's set up the cloud database.
Step 8: Create your Supabase PostgreSQL database
Currently, JobPulse AI uses SQLite (jobpulse.db). That database is stored on your laptop, so we need to move to PostgreSQL for cloud deployment.

create a superbase.io account and create a project and copy the postsql onnection link

postgresql://postgres:Hello@6541@db.yfmpqjzcxqxtqydnzbai.supabase.co:5432/postgres

we need to connect to postgres from our db.py file

create a table insupabase
python -c "from app.database.db import init_db; init_db()" run this command

