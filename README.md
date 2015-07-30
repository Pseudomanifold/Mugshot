# `mugshot.py`

Inspired by [Neal Stephenson's *Cryptonomicon*](https://www.goodreads.com/book/show/816.Cryptonomicon),
I wrote a "Mugshot" script. Using [OpenCV](http://opencv.org), it detects whenever there is a face
in front of the primary webcam. Mugshots are taken if at least ten seconds have passed between last
detecting a face or the number of faces changed between two capture frames. All captured faces are
stored in the current directory, indexed by the current time and their number.

# Usage

By default, run

    ./mugshot.py

and have some fun seeing faces being detected.

If you do not want to see any intermediary results, run:

    ./mugshot.py --hide

This will more or less silently (the webcam's LED is still visible) capture faces and store them in
the current directory.

# Why?

Because it is a fun exercise in getting to know OpenCV a little bit more.
