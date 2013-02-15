Django Protetected Downloads
============================

This app provides simple ownership verification before allowing a file download.
A file can be only downloaded by the owner or by a staff member (someone that
can access the `admin` site).

The ownership is verified using a filename generator function that should be
provided as a string in `settings.py` (`PROTECTED_DOWNLOADS_GENERATOR`). This
function receives the `user` and the original `filename` as parameters (it is
supposed the same function that handles the upload). It should return a unique
filename for that user.
