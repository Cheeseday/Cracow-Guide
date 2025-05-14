from flask import redirect, render_template, session
from functools import wraps
import re
from PIL import Image


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def is_valid_email(email: str) -> bool:
    email_regex = re.compile(
        r"^(?P<local>[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*)"
        r"@"
        r"(?P<domain>[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
        r"(?:\.[a-zA-Z]{2,})+)$"
    )
    return re.match(email_regex, email) is not None


def is_valid_username(s: str) -> bool:
    return bool(re.fullmatch(r'[A-Za-z0-9_]{4,}', s))


def crop_to_aspect(image_path, output_path, target_ratio):
    try: 
        with Image.open(image_path) as img:
            width, height = img.size
            current_ratio = width / height

            if current_ratio > target_ratio:
                # too wide - cut by width
                new_width = int(height * target_ratio)
                left = (width - new_width) // 2
                img_cropped = img.crop((left, 0, left + new_width, height))
            else:
                # too high - cut by height
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                img_cropped = img.crop((0, top, width, top + new_height))

            img_cropped.save(output_path)

    except IOError:
        print("An error occurred while trying to open the image.")

