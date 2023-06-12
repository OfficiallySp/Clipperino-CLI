# Clipperino-CLI

This Python script is used to create a compilation of clips from a specified list of Twitch streamers' channels. The compilation is created by downloading and concatenating a number of clips from each streamer's channel.
## Requirements

This script requires the following dependencies:

- Python 3.9+
- Twitch-dl
- FFmpeg

## Usage

First, you need to prepare the streamers.txt file where you specify the details of the Twitch streamers and the clips you want to download. Each line of the file should have the following format:
```
streamer, period, videoNum, minDuration
```
streamer: The name of the Twitch streamer.
period: The period for which to retrieve clips. Must be one of past_day, past_week, past_month, or all_time.
videoNum: The number of the output video.
minDuration: The minimum duration of the compiled video in minutes.

Once you have prepared the streamers.txt file, you can run the script with the following command:
```
bash
python execute.py
```
## Functionality

The script performs the following tasks:

- Reads the streamers.txt file and retrieves the details of each Twitch streamer and the clips to download.
- Retrieves a list of clips from the specified Twitch streamer's channel using Twitch-dl.
- Downloads a number of clips from the list until the minimum duration is reached.
- Concatenates the downloaded clips into a single video using FFmpeg.
- Creates a text file containing the video title, description, and tags.
- Cleans up temporary files.

## Example

An example of what your streamers.txt file should look like is as follows:

```
streamer1 past_week 1 15
streamer2 past_month 2 20
streamer3 all_time 3, 25
```

This would create a compilation video for each specified streamer, using clips from the given period, with a target duration specified for each. The output video and text file for each streamer would be named as streamerName_videoNum.mp4 and streamerName_videoNum.txt, respectively.
