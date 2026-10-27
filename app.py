from flask import Flask, request, render_template, send_from_directory
from threading import Thread
from datetime import datetime

from Scripts.TestSuccessMessage import TestSuccessMessage
from Utilities.driver_store import drivers
from Utilities.user_context import set_user_ip
from test import test

app = Flask(__name__)

# Store logs per printer
log_store = {}
job_status = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/logs/<printer_ip>")
def get_logs(printer_ip):
    return "<br>".join(log_store.get(printer_ip, []))


def run_test_async(form_data, logger, client_ip):
    set_user_ip(client_ip)
    try:
        test(
            choice=int(form_data["choice"]),
            printer_ip=form_data["printer_ip"],
            password=form_data["password"],
            domain=form_data.get("domain", ""),
            ip1=form_data.get("ip1", ""),
            fax_number=form_data.get("fax_number", ""),
            old_password=form_data.get("old_password", ""),
            new_password=form_data.get("new_password", ""),
            logger=logger
        )
        job_status[client_ip] = "COMPLETED"
    except Exception as e:
        print(e)
        if("Connection aborted" in str(e)):
            logger("Execution stopped by the user")
        else:
            logger("Error: Run time error. Please Refresh and Resubmit.\n")
    job_status[client_ip] = "COMPLETED"


@app.route("/run", methods=["POST"])
def run():

    client_ip = request.remote_addr

    printer_ip = request.form["printer_ip"]

    log_store[printer_ip] = []

    job_status[client_ip] = "RUNNING"

    def logger(message):
        timestamp = datetime.now().strftime("%H:%M:%S")

        log_store[printer_ip].append(
            f"[{timestamp}] {message}"
        )

    form_data = dict(request.form)

    thread = Thread(
        target=run_test_async,
        args=(form_data, logger, client_ip)
    )

    thread.start()

    return render_template(
        "logs.html",
        printer_ip=printer_ip
    )

@app.route("/stop", methods=["POST"])
def stop():
    data = request.get_json()
    printer_ip = data.get("printer_ip")
    driver = drivers.get(printer_ip)
    client_ip = request.remote_addr
    try:
        if driver:
            driver.quit()
        drivers.pop(printer_ip, None)
        log_store.pop(printer_ip, None)
        job_status[client_ip] = "COMPLETED"
        return "Stopped", 200
    except Exception as e:
        print(e)
        job_status[client_ip] = "COMPLETED"
        return str(e), 500


@app.route("/status")
def get_status():
    user_ip = request.remote_addr
    return job_status.get(
        user_ip,
        "RUNNING"
    )

@app.route("/screenshots/<path:filename>")
def screenshots(filename):
    return send_from_directory("Screenshots", filename)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=6767,
        debug=True,
        threaded=True
    )