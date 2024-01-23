class TextStreamer:
    """TODO"""

    def __init__(self):
        # This is determined once the sample file is played.
        self._delayed_start_s = None
        # Total duration of the sample file.
        self._sample_file_len = 1.75
        # Sample filename.
        self._sample_filename = 'sample.mp3'
