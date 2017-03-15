from flask import Flask
from flask import request, redirect, flash, url_for, render_template
import telepot
from tasks import reply_message

ENDPOINT = "https://celerybot.ngrok.io"
app = Flask(__name__)
app.secret_key = 'this_is_my_no_so_secret_please_change_it'

@app.route("/set_webhook", methods=['GET', 'POST'])
def set_webhook():
    if request.method == 'POST':
        print request.form['token']
        token = request.form['token']
        callback = "{endpoint}/telegram/{token}".format(
            endpoint=ENDPOINT,
            token=token
        )
        bot = telepot.Bot(token)
        bot.setWebhook(callback)
        flash('webhook set!')
        return redirect(url_for('set_webhook'))
    else:
        return render_template('set_webhook.html')


@app.route("/telegram/<token>", methods=['POST'])
def on_message(token):
    event = request.json
    chat_id = event['message']['chat']['id']
    # Maybe we want to store token and chat_id to contact this user later
    reply_message.delay(token, chat_id, event['message']['text'])
    return 'OK'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333, debug=True)
