from pathlib import Path
from IPython.display import HTML
from base64 import b64encode
from ._video_to_frames import video_to_frames
from ._combine_video import _write_videos_to_txt
import os

__all__ = ['show_short_video', 'video_to_frames', 'combine_videos']

def show_short_video(file, seconds = 10):

	path = Path(file)

	new_file_name = path.stem + '_short' + path.suffix
	output_file = path.parents[0]/str(new_file_name)
	print(output_file)

	end_time = '00:00:'+str(seconds)
	cmd = 'ffmpeg -loglevel warning -y -ss 00:00:00 -i '+str(file)+' -c copy -t '+str(end_time) + ' ' + str(output_file)
	os.system(cmd) # TODO use ffmpy instead of os.system
	
	mp4 = open(output_file,'rb').read()
	data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
	return HTML("""
	<video width=400 controls>
				<source src="%s" type="video/mp4">
	</video>
	""" % data_url)

def frame_extractor(video_path, frames_dir, overwrite=False, every=1, chunk_size=1000):
	video_to_frames(video_path, frames_dir, overwrite, every, chunk_size)

def combine_videos(folder, output, merge_file = 'merge_file.txt'):

	# write all videos to txt
	_write_videos_to_txt(merge_file, folder)

	# combine videos (TODO: replace with ffmpy)
	cmd = 'ffmpeg -loglevel warning -y -f concat -safe 0 -i ' + str(merge_file) + ' -c copy ' + str(output)
	os.system(cmd)



