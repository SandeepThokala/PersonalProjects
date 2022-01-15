from random import choice
from os import listdir, startfile, path
from shutil import move
# from time import time, sleep, ctime
from re import search, split
from datetime import datetime
from csv import writer

# ###################################################### MOVIE WATCHER ########################################################

Languages = ['FRENCH', 'CHINESE', 'KOREAN', 'JAPANESE', 'ITALIAN', 'SPANISH', 'SWEDISH', 'DANISH', 'RUSSIAN']

def SetMovieData(MovieName, Year):
	with open('MovieData.txt', 'a', newline='\n') as MovieData:
		DataWriter = writer(MovieData, delimiter='\t')
		Now = datetime.now()
		DataWriter.writerow([Now.strftime('%b %d, %Y'), Now.strftime('%I:%M %p'), MovieName.replace('.', ' ').strip(), Year])


def start(pth):
	FileName = pth.split('\\')[-1]
	MovieName, Tags = split(r"\.\d{4}\.", FileName)
	Year = search(r"\.(\d{4})\.", FileName).group(1)
	try: Language = list(filter(lambda x: x in Languages, Tags.split('.'))).pop()
	except IndexError: Language = ''
	SetMovieData(f'{MovieName}.{Language}', Year)
	print(MovieName.replace('.', ' '), Year)
	if path.isfile(pth):
		startfile(pth) 
	else:
		for i in filter(lambda x: path.splitext(x)[1].lower() in ['.mp4', '.mkv'], listdir(pth)):
			startfile(path.join(pth, i))
	return move(pth, r"E:\Delete") if input('Press Enter(<_;) if u wanna keep the movie: ') else move(path, r"E:\Watched")


def watch(pth):
	FileName = choice(listdir(pth))
	MoviePath = path.join(pth, FileName)
	try:
		MovieName, Tags = split(r"\.\d{4}\.", FileName)
		Year = search(r"\.(\d{4})\.", FileName).group(1)
		try: Language = list(filter(lambda x: x in Languages, Tags.split('.'))).pop()
		except IndexError: Language = ''
		SetMovieData(f'{MovieName}.{Language}', Year)
		print(MovieName.replace('.', ' '), Year)
		if path.isfile(pth + MoviePath):
			startfile(pth + MoviePath)
		else:
			for i in listdir(MoviePath):
				if path.splitext(i)[1].lower() in ['.mp4', '.mkv']:
					startfile(path.join(MoviePath, i)) 
	except (AttributeError, ValueError):
		Series = listdir(MoviePath)
		for i in range(len(Series)):
			Series.sort(key = lambda x: search(r"\.(\d{4})\.", x).group(1))
			PartPath = path.join(MoviePath, Series[i])
			PartName = [i for i in listdir(PartPath) if path.splitext(i)[1] == '.mp4'].pop()
			MovieName, Tags = split(r"\.\d{4}\.", PartName)
			Year = search(r"\.(\d{4})\.", PartName).group(1)
			Tag = Tags.split('.')[0]
			Language = Tag if Tag in ['FRENCH', 'CHINESE', 'KOREAN', 'JAPANESE', 'ITALIAN'] else ''
			print(MovieName.replace('.', ' '), Year)
			if not(input('Play?\t')):
				SetMovieData(f'{MovieName}.{Language}', Year)
				startfile(path.join(PartPath, PartName))
			else:
				continue
	return move(MoviePath, r"E:\Delete") if input('Press Enter(<_;) if u wanna keep the movie: ') else move(MoviePath, r"E:\Watched")


# ###################################################### SHOW WATCHER ########################################################

def MyData(kind, ShowName, season, nxt):
	with open('TvShowData.txt' if kind == 'tv' else 'AnimeData.txt', 'a', newline='\n') as DataFile:
		Now = datetime.now()
		DataWriter = writer(DataFile, delimiter = '\t')
		DataWriter.writerow([Now.strftime('%b %d, %Y'), Now.strftime('%I:%M %p'), ShowName, season, nxt + 1])


def SetData(season, episode):
	lines = open('data.txt', 'r').readlines()
	lines[0] = f'Season: {season}\n'
	lines[1] = f'Episode: {episode}\n'
	open('data.txt','w').write(''.join(lines))


def show(ShowPath):
	
	kind, ShowName = ShowPath.split('\\')[-2:]
	season = int(open('data.txt', 'r').readlines()[0].split(' ')[-1]) 
	try:
		SeasonPath = ShowPath + '\\' + listdir(ShowPath)[season - 1]
	except IndexError:
		print(r'#'*25, 'The End', r'#'*25)
		SetData(1, 0) 
	else:
		nxt = int(open('data.txt', 'r').readlines()[-1].split(' ')[-1])
		try:	
			episodes = [i for i in listdir(SeasonPath) if path.splitext(i)[1] in ['.mkv', '.mp4', '.avi']]	
			print(f'watching {ShowName}, S{season}E{nxt+1}')
			# startfile(SeasonPath + '\\' + episodes[nxt])
			print(episodes[nxt])
		except NotADirectoryError:
			episodes = [i for i in listdir(ShowPath) if path.splitext(i)[1] in ['.mkv', '.mp4', '.avi']]
			try:
				startfile(ShowPath + '\\' + episodes[nxt])
				# print(episodes[nxt])
				print(f'watching {ShowName}, E{nxt+1}')
				SetData(1, nxt + 1)
				# MyData(kind, ShowName, season, nxt)
				show(ShowPath) if not(input('Play next episode?\n\n')) else print('Very Well...')
			except IndexError: 
				print(r'#'*25, 'The End', r'#'*25)
				SetData(1, 0)
		except IndexError:
			if not(input('End of season, Press enter to start next season:\n')):
				SetData(season + 1, 0)
				show(ShowPath)
			else:
				print('Very Well...')
		else:		
			SetData(season, nxt + 1)
			# MyData(kind, ShowName, season, nxt) 
			show(ShowPath) if not(input('Play next episode?\n\n')) else print('Very Well...')
				
# SetData(1, 4)
show(r"E:\Udemy\[DesireCourse.Net] Udemy - The Modern Angular Bootcamp [2020]\08 Routing and Navigation Between Pages")

# (?# Movie = r"E:\Watchlist\Black.Widow.2021.1080p.WEBRip.x265-RARBG")
# start(r"E:\Watchlist\Dont.Look.Up.2021.1080p.WEBRip.x265-RARBG")

# watchlist = r"E:\Watchlist"
# watch(watchlist)
