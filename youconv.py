#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess, re, shutil
from mpd import MPDClient
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RPENIST'

@app.route('/')
def welcome():
	return render_template("welcome.html")

@app.route('/run', methods=['POST'])
def run():
	if not request.form['url']:
		flash('Please provide an URL')
		return redirect(url_for('welcome'))
	# do stuff
	try:
		p = subprocess.check_output(['/usr/bin/python','youtube-dl','-t','--no-progress','--extract-audio','--max-quality','18','--',request.form['url']])
	except:
		flash("Nice try.")
		return redirect(url_for('welcome'))
	m = re.search("\[ffmpeg\] Destination: (.+?)\s", p)
	myfile = m.group(1)
	shutil.move(myfile, "static/%s" % myfile)
	try:
		mpd = MPDClient()
		try:
			mpd.connect(host="trillian", port="6600")
			mpd.add("http://toolbox.labor.koeln.ccc.de/static/%s" % myfile)
		except:
			raise
	except:
		raise
		flash('mpd failure')
		return redirect(url_for('welcome'))
	flash('your song has been added to the playlist')
	return redirect(url_for('welcome'))

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True)
