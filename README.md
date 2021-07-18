# A simple video linter

Uses python, probably badly. Assumes python3, that you have pip to install the requirements, and probably that you've installed [MediaInfo](https://mediaarea.net/en/MediaInfo) installed (on macOS I did this with `brew install mediainfo`, other platforms... 🤷🏻)

## Usage

`python3 test.py FILE_NAME.mp4`

## Example output

Passed through `jq` for pretty printing.

### .mov, h264 + aac, 1080p, 29.97fps

```json
{
  "container_format": {
    "ok": true,
    "actual": "MPEG-4",
    "human_readable": "MPEG-4 / mov",
    "required": "MPEG-4"
  },
  "filesize": {
    "ok": true,
    "actual": 3071569118,
    "required_max": 4000000000,
    "human_readable": "2.86 GiB"
  },
  "duration": {
    "actual": 1620452,
    "human_readable": "27 min 0 s"
  },
  "video_track_count": {
    "ok": true,
    "actual": 1,
    "required": 1
  },
  "video_codec": {
    "ok": true,
    "actual": "AVC",
    "required": "AVC",
    "human_readable": "Advanced Video Codec (AVC) http://developers.videolan.org/x264.html"
  },
  "video_resolution": {
    "ok": true,
    "actual": {
      "width": 1920,
      "height": 1080
    },
    "human_readable": "1920x1080"
  },
  "video_bitrate": {
    "ok": true,
    "actual": 15056425,
    "required": 4000000,
    "human_readable": "15.1 Mb/s"
  },
  "video_framerate": {
    "ok": true,
    "preferred": false,
    "actual": "29.970",
    "human_readable": "29.970 (30000/1001) FPS"
  },
  "audio_track_count": {
    "ok": true,
    "actual": 1
  },
  "audio_channels": {
    "ok": true,
    "actual": 2,
    "required_min": 1,
    "required_max": 2
  },
  "audio_codec": {
    "ok": true,
    "actual": "AAC",
    "required": "AAC",
    "human_readable": "Advanced Audio Codec Low Complexity (AAC LC)"
  }
}
```

### .mkv, h264 + opus, 1080p, 23.976fps

```json
{
  "container_format": {
    "ok": false,
    "actual": "Matroska",
    "human_readable": "Matroska / mkv",
    "required": "MPEG-4"
  },
  "filesize": {
    "ok": true,
    "actual": 281222172,
    "required_max": 4000000000,
    "human_readable": "268 MiB"
  },
  "duration": {
    "actual": 632501,
    "human_readable": "10 min 32 s"
  },
  "video_track_count": {
    "ok": true,
    "actual": 1,
    "required": 1
  },
  "video_codec": {
    "ok": true,
    "actual": "AVC",
    "required": "AVC",
    "human_readable": "Advanced Video Codec (AVC) http://developers.videolan.org/x264.html"
  },
  "video_resolution": {
    "ok": true,
    "actual": {
      "width": 1920,
      "height": 1080
    },
    "human_readable": "1920x1080"
  },
  "video_bitrate": {
    "ok": false,
    "actual": 3556955,
    "required": 4000000,
    "human_readable": "3 557 kb/s"
  },
  "video_framerate": {
    "ok": false,
    "preferred": false,
    "actual": "23.976",
    "human_readable": "23.976 (24000/1001) FPS"
  },
  "audio_track_count": {
    "ok": true,
    "actual": 1
  },
  "audio_channels": {
    "ok": true,
    "actual": 2,
    "required_min": 1,
    "required_max": 2
  },
  "audio_codec": {
    "ok": false,
    "actual": "Opus",
    "required": "AAC",
    "human_readable": "None (Opus)"
  }
}
```

### .webm, VP9 + Vorgis, 1080p, 30fps

```json
{
  "container_format": {
    "ok": false,
    "actual": "WebM",
    "human_readable": "WebM / webm",
    "required": "MPEG-4"
  },
  "filesize": {
    "ok": true,
    "actual": 539822895,
    "required_max": 4000000000,
    "human_readable": "515 MiB"
  },
  "duration": {
    "actual": 3875069,
    "human_readable": "1 h 4 min"
  },
  "video_track_count": {
    "ok": true,
    "actual": 1,
    "required": 1
  },
  "video_codec": {
    "ok": false,
    "actual": "VP9",
    "required": "AVC",
    "human_readable": "None (VP9) None"
  },
  "video_resolution": {
    "ok": true,
    "actual": {
      "width": 1920,
      "height": 1080
    },
    "human_readable": "1920x1080"
  },
  "video_bitrate": {
    "ok": false,
    "actual": 933461,
    "required": 4000000,
    "human_readable": "933 kb/s"
  },
  "video_framerate": {
    "ok": true,
    "preferred": true,
    "actual": "30.000",
    "human_readable": "30.000 FPS"
  },
  "audio_track_count": {
    "ok": true,
    "actual": 1
  },
  "audio_channels": {
    "ok": true,
    "actual": 2,
    "required_min": 1,
    "required_max": 2
  },
  "audio_codec": {
    "ok": false,
    "actual": "Vorbis",
    "required": "AAC",
    "human_readable": "None (Vorbis)"
  }
}
```

### .webm, VP8 + Vorbis, 720p, 30fps

```json
{
  "container_format": {
    "ok": false,
    "actual": "WebM",
    "human_readable": "WebM / webm",
    "required": "MPEG-4"
  },
  "filesize": {
    "ok": true,
    "actual": 869879639,
    "required_max": 4000000000,
    "human_readable": "830 MiB"
  },
  "duration": {
    "actual": 2877869,
    "human_readable": "47 min 57 s"
  },
  "video_track_count": {
    "ok": true,
    "actual": 1,
    "required": 1
  },
  "video_codec": {
    "ok": false,
    "actual": "VP8",
    "required": "AVC",
    "human_readable": "None (VP8) http://www.webmproject.org/"
  },
  "video_resolution": {
    "ok": true,
    "actual": {
      "width": 1280,
      "height": 720
    },
    "human_readable": "1280x720"
  },
  "video_bitrate": {
    "ok": false,
    "actual": 2057504,
    "required": 2500000,
    "human_readable": "2 058 kb/s"
  },
  "video_framerate": {
    "ok": true,
    "preferred": true,
    "actual": "30.000",
    "human_readable": "30.000 FPS"
  },
  "audio_track_count": {
    "ok": true,
    "actual": 1
  },
  "audio_channels": {
    "ok": true,
    "actual": 2,
    "required_min": 1,
    "required_max": 2
  },
  "audio_codec": {
    "ok": false,
    "actual": "Vorbis",
    "required": "AAC",
    "human_readable": "None (Vorbis)"
  }
}
```