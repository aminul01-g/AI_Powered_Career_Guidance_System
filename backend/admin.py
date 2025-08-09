from flask_admin.contrib.sqla import ModelView
from models import User, Profile, Upload, GuidanceSession, Event
from extensions import admin, db

def init_admin(app):
    # Only add views (do not call admin.init_app here — app.py already does that)
    # To avoid duplicate views on hot reloads, clear existing views first if present.
    try:
        # remove existing views if any (safe for dev)
        admin._views = []
    except Exception:
        pass

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Profile, db.session))
    admin.add_view(ModelView(Upload, db.session))
    admin.add_view(ModelView(GuidanceSession, db.session))
    admin.add_view(ModelView(Event, db.session))
