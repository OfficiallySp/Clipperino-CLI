import os
import random
import subprocess
from datetime import datetime

def output(string):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"{current_time} | {string}")

def getLength(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def download_clip(clip_url):
    output(f"Downloading clip: {clip_url}")
    os.system(f"twitch-dl download -q source {clip_url} > NUL")

def createCompilationAuto(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            streamer, period, videoNum, minDuration = line.strip().split()
            createCompilation(streamer, period, int(videoNum), int(minDuration))

def createCompilation(streamer, period='last_week', videoNum=0, minDuration=10):
    output(f"Creating compilation for {streamer}.")

    # make output directory if it does not exist
    output_directory = f'output/{streamer}'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output("Retrieving clips.")

    # get list of clips from twitch-dl
    os.system(f'twitch-dl clips {streamer} --period {period} --limit 100 > temp.txt')
    with open('temp.txt', encoding='utf-8') as f:
        clipLines = f.readlines()
    os.remove('temp.txt')

    # reformat into style retrieved from twitch
    channelClips = []
    i = 0
    while (i < len(clipLines)):
        if ('Clip' in clipLines[i]):
            try:
                tempClip = {}
                tempClip['id'] = clipLines[i][9:-5]
                tempClip['title'] = clipLines[i + 1][5:-5]
                tempClip['url'] = clipLines[i + 4][4:-5]
                tempClip['game'] = clipLines[i + 2].split('playing')[1][6:-5]
                channelClips.append(tempClip)
                i = i + 5
            except:
                i = i + 1
        else:
            i = i + 1

    output("Beginning clip download. (THIS WILL TAKE SOME TIME)")

    duration = 0
    i = 0
    downloads = []
    games = []
    titles = []
    invalid = []
    # downloads required clips
    while ((duration < minDuration * 60) and i < len(channelClips)):
        try:
            title = channelClips[i]['title']
        except:
            i += 1
            continue
        if '\\' in title:
            i += 1
            continue

        oldFiles = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]

        download_clip(channelClips[i]['url'])

        newFiles = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]
        download = ""
        for file in newFiles:
            if file not in oldFiles:
                download = file
        if (len(newFiles) == len(oldFiles)) or (download == ""):
            invalid.append(channelClips[i]['url'])
            i += 1
            continue

        duration += getLength(download)
        while True:
            try:
                titles.append(title)
                break
            except:
                title = title[:-1]
        if (channelClips[i]['game'] not in games):
            games.append(channelClips[i]['game'])
        downloads.append(f'output/{streamer}/' + download)
        output_path = f'output/{streamer}/' + download
        if os.path.exists(download):
            if os.path.exists(output_path):
                output(f"File {download} already exists in output directory. Skipping.")
            else:
                os.rename(download, output_path)
                output(f"Downloaded: {title}")
        else:
            output(f"File {download} does not exist. Skipping.")
        i += 1
    if not downloads:  # If the list is empty, no clips were downloaded
        output(f"No clips could be downloaded for {streamer} in the specified timeframe ({period}). Skipping to next streamer.")
        return

    # join clips
    output("Joining clips.")
    random.shuffle(downloads)
    tsClipLocations = []
    f = open("temp.txt", "w+")
    for clip in downloads:
        # convert to .ts
        clipname = clip[:-4]
        os.system(f"ffmpeg -loglevel error -i {clipname}.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts {clipname}.ts")
        tsClipLocations.append(clipname + ".ts")
        # concatenate .ts to mp4
        f.write(f"file '{clipname}.ts'\n")
    f.close()
    os.system("ffmpeg -loglevel error -f concat -safe 0 -i temp.txt -c copy output.mp4")
    os.remove("temp.txt")
    os.system(f'ffmpeg -loglevel error -err_detect ignore_err -i output.mp4 -c copy output/{streamer}/{streamer}_{videoNum}.mp4')
    os.remove('output.mp4')


    # create text file
    output("Creating text file.")
    f = open(f'output/{streamer}/{streamer}_{videoNum}.txt', "w+")
    # title
    random.shuffle(titles)
    count = 0
    while(True):  # tries titles until it finds a valid one
        try:
            title = titles[count]
            break
        except:
            count += 1

    f.write(title + "\n")
    # description
    desc = streamer + "'s Twitch Channel: https://www.twitch.tv/" + streamer
    f.write(desc + "\n")
    # tags
    tags = ""
    for game in games:
        tags += game + ', '
    f.write("Categories: " + tags + "\n")
    f.close()

    # clean up
    for file in tsClipLocations:
        try:
            os.remove(file)
        except:
            output(f"Unable to delete {file}")
    for file in invalid:
        try:
            os.remove(file)
        except:
            output(f"Unable to delete {file}")

    output("Compilation creation completed!\n")
    return
    output("COMPLETE")