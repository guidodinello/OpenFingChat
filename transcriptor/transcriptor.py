"""
1. For each lecture document in MONGODB
  1.1 Download lectue video in MP4 format
  1.2 Convert lecture to MP3 format
  1.3 Transcribe lecture using Whisper
  1.4 Save transcription
  1.5 Delete MP4 and MP3 files
"""

import pathlib
from typing import List, Union

import torch

import constants
from transcriptor import concurrent


def transcript(subject_names: List[str], max_lessons: Union[int | None] = None) -> None:
    # change sequential to concurrent for a parallel implementation

    concurrent.transcript(
        {
            "CACHE_PATH": pathlib.Path(constants.CACHE_PATH) / "whisper",
            "DEVICE": "cuda:0" if torch.cuda.is_available() else "cpu",
            "MODEL": "base",
            "MAX_DOWNLOAD_WORKERS": 5,
            "MAX_CONVERT_WORKERS": 5,
        },
        subject_names,
        max_lessons,
    )
