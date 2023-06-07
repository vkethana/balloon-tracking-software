# Balloon Tracker Software
Python3 code that uses the OpenCV library to track small, balloon-like objects given a user-defined anchor point. 

## Instructions

To test out the code, download the entire repository and run the `tracker.py` file.
For additional information, see pp. 4-6 of [this document](https://docs.google.com/document/d/1BlSEalDKJdNWVXWj4crKdMKH4CGX_jqdr1-A1DC-urU/edit).

## What does each file do?
`tracker.py`: Python tracking code that tracks a user-defined object in an inputted video file (`video.mov`).

`graph_generator.py`: Generates (smoothed) graphs of the data given CSV file input

`propeller_controller.ino`: Arduino code that controls the propellers. More info available [here](https://docs.google.com/document/d/1BlSEalDKJdNWVXWj4crKdMKH4CGX_jqdr1-A1DC-urU/edit).

`video.mov`: An example of what type of video file works with the tracker.
