from random import choice
from os import listdir, startfile, path
from os.path import isdir, join
from shutil import move
from re import search, split
from datetime import datetime
from csv import writer

year_pattern = r"\.(\d{4})\."
isall_dir = lambda x: all([isdir(join(x, i)) for i in listdir(x)])
get_year = lambda x: search(year_pattern, x).group(1)

# ###################################################### MOVIE WATCHER ########################################################

Languages = ['FRENCH', 'CHINESE', 'KOREAN', 'JAPANESE', 'ITALIAN', 'SPANISH', 'SWEDISH', 'DANISH', 'RUSSIAN']

def set_moviedata(movie_name, year):
  with open('MovieData.txt', 'a', newline='\n') as movie_data:
    data_writer = writer(movie_data, delimiter='\t')
    now = datetime.now()
    data_writer .writerow([now.strftime('%b %d, %Y'), now.strftime('%I:%M %p'), movie_name, year])


def start(inpath_arg):
  data = open('MovieData.txt', 'r').read()
  file_name = list(filter(lambda x: path.splitext(x)[-1].lower() in ['.mp4', '.mkv', '.avi'], listdir(inpath_arg))).pop()
  movie_name, year, tags = split(year_pattern, file_name)
  try: language = list(filter(lambda x: x in Languages, tags.split('.'))).pop()
  except IndexError: language = ''
  movie_name = ' '.join([movie_name.replace('.', ' '), language]).strip()
  print(chr(9658), movie_name, language, year)
  set_moviedata(movie_name, year)
  if search(rf"{movie_name}\t{year}", data):
    print(f'Already watched {movie_name} {year}')
    rewatch = input('Rewatch? (Y/n): ')
    if not(rewatch) or (rewatch.upper() == 'Y'): startfile(join(inpath_arg, file_name))
    else: pass
  else: startfile(join(inpath_arg, file_name))


def watch(inpath_arg):
  if isall_dir(inpath_arg):
    data = open('MovieData.txt', 'r').read()
    series = listdir(inpath_arg)
    series.sort(key = get_year)
    for i in series: start(join(inpath_arg, i))
  else: start(inpath_arg)
  the_end = input('Move to Watched folder? (Y/n): ')
  try: return move(inpath_arg, r"E:\Watched") if (the_end or (the_end.upper() == 'Y')) else move(inpath_arg, r"E:\Delete")
  except: pass


watchlist = lambda inpath_arg: watch(join(inpath_arg, choice(listdir(inpath_arg))))

watchlist(r"E:\Watchlist")
# watch(r"E:\Watched\Spider-Man")