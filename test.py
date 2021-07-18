import numpy as np # for numerical operations
from pprint import pprint
from moviepy.editor import VideoFileClip, concatenate
from pymediainfo import MediaInfo
import json
import sys

max_file_size = 4_000_000_000

minimums = {
  1920: {
    'bitrate': 4_000_000
  },
  1280: {
    'bitrate': 2_500_000
  }
}

data = {}

file_name = sys.argv[1]

media_info = MediaInfo.parse(file_name)

general_track = media_info.general_tracks[0]

# print("general_track data:")
# pprint(general_track.to_data())

container_format = general_track.format

data['container_format'] = {
  'ok': container_format == "MPEG-4",
  'actual': container_format,
  'human_readable': f'{general_track.format} / {general_track.file_extension}',
  'required': "MPEG-4"
}

data['filesize'] = {
  'ok': general_track.file_size < max_file_size,
  'actual': general_track.file_size,
  'required_max': max_file_size,
  'human_readable': general_track.other_file_size[0]
}

data['duration'] = {
  'actual': general_track.duration,
  'human_readable': general_track.other_duration[0]
}

# First video

video_track_count = len(media_info.video_tracks)

data['video_track_count'] = {
  'ok': video_track_count == 1,
  'actual': video_track_count,
  'required': 1
}

video_track = media_info.video_tracks[0]
# print("video_track data:")
# pprint(video_track.to_data())

data['video_codec'] = {
  'ok': video_track.format == "AVC",
  'actual': video_track.format,
  'required': "AVC",
  'human_readable': f'{video_track.format_info} ({video_track.other_format[0]}) {video_track.format_url}'
}

# maybe: format_profile: 'High@L4', format_settings...?
# maybe:
#  'codec_id': 'avc1',
#  'codec_id_info': 'Advanced Video Coding',
#  'color_primaries': 'BT.709',
#  'color_range': 'Limited',
#  'color_space': 'YUV',
#  'scan_type': 'Progressive',

# * Are we 720p or 1080p?
data['video_resolution'] = {
  'ok': (video_track.width == 1920 and video_track.height == 1080) or
    (video_track.width == 1280 and video_track.height == 720),
  'actual': { 'width': video_track.width, 'height': video_track.height },
  'human_readable': f'{video_track.width}x{video_track.height}'
}

# * Is our bitrate high enough (720p = >2.5mbps, 1080p = >4Mbps)
min_bitrate = video_track.width in minimums and minimums[video_track.width]['bitrate'] or 0

if video_track.bit_rate != None:
  data['video_bitrate'] = {
    'ok': video_track.bit_rate > min_bitrate,
    'actual': video_track.bit_rate,
    'required': min_bitrate,
    'human_readable': video_track.other_bit_rate[0]
  }
else:
  data['video_bitrate'] = {
    'ok': general_track.overall_bit_rate > min_bitrate,
    'actual': general_track.overall_bit_rate,
    'required': min_bitrate,
    'human_readable': general_track.other_overall_bit_rate[0]
  }

# * Is our frame rate ideal (30) or ok (29.97, 30, 50, 60)
data['video_framerate'] = {
  'ok': video_track.frame_rate == '29.970' or 
    video_track.frame_rate == '30.000' or 
    video_track.frame_rate == '50.000' or 
    video_track.frame_rate == '59.940' or
    video_track.frame_rate == '60.000',
  'preferred': video_track.frame_rate == '30.000',
  'actual': video_track.frame_rate,
  'human_readable': video_track.other_frame_rate[0]
}

# Now audio

audio_track_count = len(media_info.audio_tracks)

data['audio_track_count'] = {
  'ok': audio_track_count == 1,
  'actual': audio_track_count
}

audio_track = media_info.audio_tracks[0]

audio_channels = audio_track.channel_s

data['audio_channels'] = {
  'ok': audio_channels == 1 or audio_channels == 2,
  'actual': audio_channels,
  'required_min': 1,
  'required_max': 2
}

# * Are we AAC?

data['audio_codec'] = {
  'ok': audio_track.format == "AAC",
  'actual': audio_track.format,
  'required': "AAC",
  'human_readable': f'{audio_track.format_info} ({audio_track.other_format[0]})'
}

# maybe audio_track.format_additionalfeatures == "LC"
# maybe audio.codec_id == "mp4a-40-2"
# maybe audio.channel_layout == "L R"
# maybe audio.bit_rate > something, e.g. 103521


# print("audio_track data:")
# pprint(audio_track.to_data())

# clip = VideoFileClip(file_name)
# # Get size on disk from ... :shrug: filesystem?


# # fps = 29.97002997002997, duration = 1620.45, size = [1920, 1080], aspect_ratio = 1.7777777777777777
# print('fps = {}, duration = {}, size = {}, aspect_ratio = {}'.format(clip.fps, clip.duration, 
# clip.size, clip.aspect_ratio))

json_data = json.dumps(data)

print(json_data)

# cut = lambda i: clip.audio.subclip(i,i+1).to_soundarray(fps=22000)
# volume = lambda array: np.sqrt(((1.0*array)**2).mean())
# volumes = [volume(cut(i)) for i in range(0,int(clip.audio.duration-2))] 

# print(f'Results of the {volumes}')


# Look at Pycon video requirements
# MP4 H.264 with AAC audio (Handbrake preset “Youtube HQ 1080 or 720”).
# Video Bitrate: At least 2.5mbit for 720p, 4mbit for 1080p.
# Audio Bitrate: At least 160kbit, mono or stereo.
# File size: Under 4GB
# Framerate: 30 (but 29.97/30/50/60 OK too)
# Also audio quality / levels

# * we have 1 & only 1 video track
# * we have 1 audio tracks
# * audio is mono or stereo only ()
# * Are we h.264?
# * Are we AAC?
# * Are we 720p or 1080p?
# * Is our bitrate high enough (720p = >2.5mbps, 1080p = >4Mbps)
# * Is our file size under 4GB?
# * Is our frame rate ideal (30) or ok (29.97, 30, 50, 60)
# ! Audio level is ok
# ! Audio quality is... :shrug: