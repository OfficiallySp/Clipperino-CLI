# Clipperino-CLI
This Python script is used to create a compilation of clips from a specified Twitch streamer's channel. The compilation is created by downloading and concatenating a number of clips from the streamer's channel.
Requirements

This script requires the following dependencies:

    Twitch-dl
    FFmpeg

Usage

The script can be executed with the following command:

bash

python <path/to/script.py>

The script can also be imported and used programmatically. The createCompilation function takes four arguments:

    streamer: The name of the Twitch streamer.
    period: The period for which to retrieve clips. Must be one of past_day, past_week, past_month, or all_time. Default is last_week.
    videoNum: The number of the output video. Default is 0.
    minDuration: The minimum duration of the compiled video in minutes. Default is 10.

Functionality

The script performs the following tasks:

    Retrieves a list of clips from the specified Twitch streamer's channel using Twitch-dl.
    Downloads a number of clips from the list until the minimum duration is reached.
    Concatenates the downloaded clips into a single video using FFmpeg.
    Creates a text file containing the video title, description, and tags.
    Cleans up temporary files.

Example

An example usage of the script is as follows:

```from twitch import createCompilation

def main():
    createCompilation("streamer_name", 'past_week', 1, 15)

if __name__ == "__main__":
    main()
 ```

This would create a compilation video for the specified streamer, using clips from the past week, with a target duration of 15 minutes. The output video and text file would be named streamer_name_1.mp4 and streamer_name_1.txt, respectively.
