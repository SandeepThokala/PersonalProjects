from re import search, split
from os import listdir, startfile
from os.path import isdir, join, splitext, basename
from random import choice
from datetime import datetime
from csv import writer
from subprocess import run, DEVNULL
from shutil import move

year_pattern = r"\.(\d{4})\."
isall_dir = lambda x: all([isdir(join(x, i)) for i in listdir(x)])
get_year = lambda x: search(year_pattern, x).group(1)
git = r"C:\Users\sande\Desktop\Deepu\MyData\PersonalProjects"

def ask(message):
  try: response = input(f'{message}? (Y/n): ').upper()[0]
  except IndexError: response = 'Y'
  if response in ['Y', 'N']: return response == 'Y'
  else: print('Invalid Input'); return ask(message)


# ###################################################### MOVIE WATCHER ########################################################

Languages = ['FRENCH', 'CHINESE', 'KOREAN', 'JAPANESE', 'ITALIAN', 'SPANISH', 'SWEDISH', 'DANISH', 'RUSSIAN']

def set_moviedata(movie_name, year):
  print(chr(9658), movie_name, year)
  with open('MovieData.txt', 'a', newline='\n') as movie_data:
    data_writer = writer(movie_data, delimiter='\t')
    now = datetime.now().astimezone()
    date, time, tz_name = now.strftime('%b %d, %Y'), now.strftime('%I:%M %p'), ''.join(i for i in now.strftime('%Z') if i.isupper())
    data_writer.writerow([date, f"{time} {tz_name}", movie_name, year])
    # run(f'git add Watcher && git commit -m "{movie_name} ({year})" && git push', cwd = git, shell = True, stdout = DEVNULL)


def start(inpath_arg):
  data = open('MovieData.txt', 'r').read()
  file_name = list(filter(lambda x: splitext(x)[-1].lower() in ['.mp4', '.mkv', '.avi'], listdir(inpath_arg))).pop()
  movie_name, year, tags = split(year_pattern, file_name)
  try: language = list(filter(lambda x: x in Languages, tags.split('.'))).pop()
  except IndexError: language = ''
  movie_name = ' '.join([movie_name.replace('.', ' '), language]).strip()
  watched = search(rf"{movie_name}\t{year}", data)
  if not(watched) or (watched and ask(f'Already watched {movie_name} {year}\nRewatch')):
    startfile(join(inpath_arg, file_name))
    set_moviedata(movie_name, year)


def watch(inpath_arg):
  if isall_dir(inpath_arg):
    print(basename(inpath_arg))
    series = listdir(inpath_arg)
    series.sort(key = get_year)
    count = len(series)
    for i, part in enumerate(series): 
      start(join(inpath_arg, part))
      if (count != i + 1) and ask(f'Play part {i + 2}'): continue
      else: break; return
  else: start(inpath_arg)
  try: return move(inpath_arg, r"E:\Watched") if ask('Move to Watched (Y) or Delete (n) folders') else move(inpath_arg, r"E:\Delete")
  except: pass


watchlist = lambda inpath_arg: watch(join(inpath_arg, choice(listdir(inpath_arg))))

watchlist(r"E:\Watchlist")
# watch(r"E:\Watchlist\The.Rock.1996.1080p.BluRay.x265-RARBG")