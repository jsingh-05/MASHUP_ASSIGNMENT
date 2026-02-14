from flask import Flask, render_template, request
import os
import smtplib
from email.message import EmailMessage
from mashup_logic import reset_workspace, build_audio_mashup, package_output


server = Flask(__name__)


@server.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            artist_name = request.form["singer"]
            video_count = int(request.form["videos"])
            clip_length = int(request.form["duration"])
            recipient_email = request.form["email"]

            if video_count <= 10 or clip_length <= 20:
                return "Invalid inputs. Check constraints."

            reset_workspace()
            mashup_path = build_audio_mashup(artist_name, video_count, clip_length)
            zip_path = package_output(mashup_path)

            send_email(recipient_email, zip_path)

            return "Mashup generated and emailed successfully."

        except Exception as error:
            return f"Processing failed: {error}"

    return render_template("index.html")


def send_email(receiver, attachment_path):
    sender = os.getenv("MASHUP_EMAIL")
    password = os.getenv("MASHUP_APP_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = "Your Audio Mashup"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("Please find your mashup attached.")

    with open(attachment_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="zip", filename="mashup.zip")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)


if __name__ == "__main__":
    server.run(debug=True)
