from flask import Blueprint, render_template, session, flash, redirect, url_for, request, send_file
from io import BytesIO
from pytube import YouTube

from src.main.form import DownloadForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')


@main.route('/video', methods=['GET', 'POST'])
def video():
    form = DownloadForm()

    if form.validate_on_submit():
        #pobieramy url
        session['link'] = form.url.data
        try:
            url = YouTube(session['link'])
            #sprawdza czy url jest właściwy
            url.check_availability()
        except:
            #jeśli url jest błędny
            flash('Wronga adress URL', 'error')
        #jeśli wszystko ok
        return render_template('download.html', url=url, form=form)

    return render_template('video.html', form=form)

@main.route('/download', methods=['GET', 'POST'])
def download():
    form = DownloadForm()

    if form.validate_on_submit():
        # deklarujemy pusty buffer
        buffer = BytesIO()
        #pobieramy url
        url = YouTube(session['link'])
        #pobieramy video rozdzielczość
        itag = request.form.get('itag')
        #zapisujemy video w zmiennej
        video = url.streams.get_by_itag(itag)
        #przekazujemy do bufora
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        #zapis do pliku as_attachment to jest save as
        return send_file(buffer, as_attachment=True, download_name='video.mp4', mimetype='video/mp4')

    return redirect(url_for('mian.home'))

@main.route('/music', methods=['GET', 'POST'])
def music():
    form = DownloadForm()

    if form.validate_on_submit():
        session['link'] = form.url.data
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            flash('Wronga adress URL', 'error')
        
        url = form.url.data
        yt = YouTube(url)
        music = yt.streams.filter(only_audio=True)
        music_save = music[0].download('/path')
        return send_file(music_save, as_attachment=True, download_name="audio.mp3", mimetype="audio/mp3")
        
    return render_template('music.html', form=form)