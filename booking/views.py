import os, requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking

# create google event helper
def create_google_event(summary, desc, start_iso, end_iso, attendee_email):
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        creds = Credentials(None,
            refresh_token=settings.GOOGLE_REFRESH_TOKEN,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            token_uri='https://oauth2.googleapis.com/token')
        service = build('calendar', 'v3', credentials=creds)
        event = {
          'summary': summary,
          'description': desc,
          'start': {'dateTime': start_iso},
          'end': {'dateTime': end_iso},
          'attendees': [{'email': attendee_email}],
          'conferenceData': {'createRequest': {'requestId': f"meet-{int(__import__('time').time())}"}}
        }
        created = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        meet = created.get('hangoutLink') or ''
        return meet, created
    except Exception as e:
        return '', None

@api_view(['GET'])
def availability(request):
    date = request.GET.get('date')
    if not date:
        return Response({'error':'date param required'}, status=400)
    base = settings.CAL_COM_API_BASE
    link = settings.CAL_COM_LINK
    key = settings.CAL_COM_API_KEY
    if not base or not link or not key:
        # fallback demo slots
        demo = []
        for h in range(9,16):
            demo.append({ 'start': f"{date}T{str(h).zfill(2)}:00:00" })
            demo.append({ 'start': f"{date}T{str(h).zfill(2)}:30:00:00" })
        return Response(demo)
    try:
        url = f"{base}/availability/{link}?start={date}&end={date}"
        headers = {'Authorization': f'Bearer {key}'}
        r = requests.get(url, headers=headers, timeout=10)
        if not r.ok:
            return Response({'error':'cal_error','details':r.text}, status=502)
        return Response(r.json())
    except Exception as e:
        return Response({'error':'server','details':str(e)}, status=500)

@api_view(['POST'])
def create_booking(request):
    data = request.data
    name = data.get('name')
    email = data.get('email')
    start_iso = data.get('startISO')
    end_iso = data.get('endISO')
    notes = data.get('notes','')
    display = data.get('display','')
    if not (name and email and start_iso and end_iso):
        return Response({'error':'missing_fields'}, status=400)
    meet_link, raw = create_google_event(f"30 Min Meeting - {name}", notes, start_iso, end_iso, email)
    b = Booking.objects.create(name=name, email=email, start_iso=start_iso, end_iso=end_iso, display_time=display, google_meet=meet_link, notes=notes)
    # send simple email (best to configure SMTP in env)
    try:
        import smtplib
        from email.mime.text import MIMEText
        admin = settings.ADMIN_EMAIL
        body = f"New booking:\nName: {name}\nEmail: {email}\nTime: {display} ({start_iso})\nMeet: {meet_link}\nNotes: {notes}"
        msg = MIMEText(body)
        msg['Subject'] = f"New Booking: {name}"
        msg['From'] = settings.EMAIL_HOST_USER or admin
        msg['To'] = f"{email},{admin}"
        s = smtplib.SMTP(os.getenv('SMTP_HOST','smtp.gmail.com'), int(os.getenv('SMTP_PORT',587)))
        s.starttls()
        s.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))
        s.sendmail(msg['From'], [email, admin], msg.as_string())
        s.quit()
    except Exception:
        pass
    return Response({'ok':True, 'id': b.id, 'meet': b.google_meet})
