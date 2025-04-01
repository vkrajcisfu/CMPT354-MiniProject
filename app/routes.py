from flask import Blueprint, render_template, flash, redirect
from app.forms import *
import query

routes = Blueprint("routes", __name__)

@routes.route("/")
def index():
    return render_template("index.html")


@routes.route("/view-database")
def view_database():
    data = query.fetch_all_data()
    return render_template("view_database.html", data=data)


@routes.route("/find-item", methods=["GET", "POST"])
def find_item():
    form = FindItemForm()
    results = []
    if form.validate_on_submit():
        results = query.find_item(form.query.data)
    return render_template("find_item.html", form=form, results=results)


@routes.route("/borrow", methods=["GET", "POST"])
def web_borrow_item():
    form = BorrowForm()
    if form.validate_on_submit():
        try:
            query.borrow_item(form.uid.data, form.iid.data)
            flash("Item borrowed Successfully!", "success")
            return redirect("/borrow")
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(f"Error: {e}", "error")
    return render_template("borrow.html", form=form)


@routes.route("/return", methods=["GET", "POST"])
def return_item():
    form = ReturnForm()
    if form.validate_on_submit():
        try:
            query.return_item(form.uid.data, form.iid.data)
            flash("Item returned successfully!", "success")
            return redirect("/return")
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(str(e), "error")
    return render_template("return.html", form=form)


@routes.route("/donate", methods=["GET", "POST"])
def donate():
    form = DonateForm()
    if form.validate_on_submit():
        try:
            query.donate_item(form.title.data.title(), form.item_type.data.title())
            flash("Thank you for your donation!", "success")
            return redirect("/donate")
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(str(e), "error")
    return render_template("donate.html", form=form)

@routes.route("/find-event", methods=["GET", "POST"])
def find_event():
    form = FindEventForm()
    results = []
    if form.validate_on_submit():
        results = query.find_event(form.query.data)
    return render_template("find_event.html", form=form, results=results)


@routes.route("/register-event", methods=["GET", "POST"])
def register_event():
    form = RegisterEventForm()
    if form.validate_on_submit():
        try:
            query.register_event(form.uid.data, form.eid.data)
            flash("Event registration successful!", "success")
            return redirect("/register-event")
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(str(e), "error")
    return render_template("register_event.html", form=form)


@routes.route("/volunteer", methods=["GET", "POST"])
def volunteer():
    form = VolunteerForm()
    if form.validate_on_submit():
        try:
            query.volunteer(form.uid.data, form.hours.data)
            flash("Thanks for volunteering!", "success")
            return redirect("/volunteer")
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(str(e), "error")
    return render_template("volunteer.html", form=form)


@routes.route("/help", methods=["GET", "POST"])
def ask_help():
    form = HelpForm()
    results = []
    if form.validate_on_submit():
        try:
            results = query.ask_help()
            flash(f"User ID: {form.uid.data}", "success")
            flash(f"You have submitted '{form.message.data}'", "success")
            flash("No librarian is currently available to view your message", "success")
            flash("Feel free to contact any of our librarians:", "success")
            # no redirect since submission protection doesn't matter for a harmless form
        except Exception as e:
            flash(str(e), "error")
    return render_template("help.html", form=form, results=results)