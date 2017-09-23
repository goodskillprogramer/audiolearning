一,提取音频文件,从视频中
	-ar 音频采样率
	-ac 频道数
	
	ffmpeg -i AomawaShields_2015U.mp4 -ac 1 -ar 16000 -f wav -vn ted80001.wav
	
	提取效率分析
	大概是10-15s/G的提取速度
	1.6G->85M音频 91min
	55M->5M音频 5min
	200M->66M  72min
	视频质量越高提取率越低 大概5%-30%左右 但是生成音频大小约为 50M/h
	

二,合成字幕 1-2min/h

	嵌入外挂字幕 ffmpeg -i AomawaShields_2015U.mp4 -i ted80001.srt -c:s mov_text -c:v copy -c:a copy AomawaShields_2015U2.mp4	

	合成带字幕视频ffmpeg -i AomawaShields_2015U.mp4 -vf subtitles=ted80001.srt AomawaShields_2015U2.mp4	
	
三,剪辑视频

	ffmpeg  -i AomawaShields_2015U.mp4 -vcodec copy -acodec copy -ss 00:00:00 -to 00:04:30 4.flv -y