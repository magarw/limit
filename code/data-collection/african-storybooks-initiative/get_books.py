
from bs4 import BeautifulSoup
import json
import os
import requests
import multiprocessing

def find_data(i):

	OUTPUT_PATH = "../../../data/raw/african-storybooks-initiative/"

	php_path = "../../../data/raw/african-storybooks-initiative/booklistjs.php"
	response = open(php_path)
	lines = response.readlines()

	book_id = ""
	line_json = ''
	try:
		print('Book Number: ', i)
		line_json = lines[i][1:][:lines[i][1:].index(')')]
		book_id = line_json[line_json.index('id:')+4:line_json.index(',title')-1].strip()
		# book_title = line_json[line_json.index('title:')+7:line_json.index(',date')-1].strip()
		# book_summary = line_json[line_json.index('summary:')+9:line_json.index(',author')-1].strip()
		# book_level = line_json[line_json.index('level:')+7:line_json.index(',dual')-1].strip()

		book = {
			'id': book_id,
		}

		downloaded = os.listdir(OUTPUT_PATH)
		downloaded = [x for x in downloaded if 'json' in x ]   # look at only json files.

		ids = [d.split('-')[0] for d in downloaded]

		# i.e. a new book has been encountered.
		if book_id not in ids:
			print(f"New book, ID: {book_id}")

			URL = "https://africanstorybook.org/read/readbook.php"
			response = requests.post(url=URL, data={'id': book['id']})
			soup = BeautifulSoup(response.text, 'html.parser')
			title = soup.find('div', {'class': 'cover_title'}).text
			author = soup.find('div', {'class': 'bookcover_author'}).text
			copyright = soup.find('div', {'class': 'backcover_copyright'}).text

			book['copyright'] = copyright
			book['author'] = ''
			if 'Author' in author:
				if 'Translation' in author:
					book['author'] = author.split('Author -')[1].split('Translation')[0].strip()
				elif 'Illustration' in author:
					book['author'] = author.split('Author -')[1].split('Illustration')[0].strip()
				else:
					book['author'] = author.split('Author -')[1].strip()

			book['translation'] = ''
			if 'Translation' in author:
				if 'Illustration' in author:
					book['translation'] =author.split('Translation -')[1].split('Illustration -')[0].strip()
				else:
					book['translation'] =author.split('Translation -')[1].strip()

			book['illustration'] = ''
			if 'Illustration' in author:
				if 'Language' in author:
					book['illustration'] =author.split('Illustration -')[1].split('Language -')[0].strip()
				else:
					book['illustration'] =author.split('Illustration -')[1].strip()

			book['language'] = ''
			if 'Language' in author:
				if 'Level' in author:
					book['language'] = author.split('Language -')[1].split('Level')[0].strip()
				else:
					book['language'] = author.split('Language -')[1].strip()

			book['level'] = ''
			if 'Level' in author:
				book['level'] = author.split('Level -')[1].strip()

			trans_list = []
			try:
				trans_list = soup.find('div', {'class': 'list-bliock'}).ul.findAll('li')
			except:
				pass

			versions = []
			for trans_i in range(len(trans_list)):
				book_id = trans_list[trans_i].a['onclick'].split('(')[1][:-1]
				lang = trans_list[trans_i].a.div.div.span.text
				if 'Translation' in lang:
					translation = True
					original = False
					adaptation = False
				elif 'Original' in lang:
					translation = False
					original = True
					adaptation = False
				elif 'Adaptation' in lang:
					translation = False
					original = False
					adaptation = True

				trans_title = trans_list[trans_i].a.div.div.text.replace(lang, '')
				transl = {
					'id': book_id,
					'lang': lang,
					'title': trans_title,
					'translation': translation,
					'original': original,
					'adaptation': adaptation
				}
				versions.append(transl)
			book['related_versions'] = versions

			book['pages'] = [{'pg-no': i + 1  ,'text': x.text} for i, x in enumerate(soup.findAll('div', {'class': 'page-text-story'}))]
			if len(book['pages']) != 0:
				with open(f"{OUTPUT_PATH}{book['id']}.json", 'w') as f:
					json.dump(book, f)
				print("Successfully saved.")
			else:
				with open(OUTPUT_PATH + f"logs/thread{i}.log", 'a') as file:
					file.write(f"MISSING: Empty pages in {book_id}\n")

	except Exception as e:
		with open(OUTPUT_PATH + f"logs/thread{i}.log", 'a') as file:
			file.write("Output Path: children-stories/data/raw/african-storybooks-initiative/ \n")
			file.write("This file logs any errors encountered while parsing book metadata retrieved from the abovementioned Request URL. \n\n\n")
			file.write('EXCEPTION: ' + str(i) + "; " + line_json + ";book-id: " + book_id + ";" + str(e) + "\n")
			file.write(lines[i])

	finally:
		return i

if __name__ == '__main__':

	print("Creating argument list.")
	php_path = "../../../data/raw/african-storybooks-initiative/booklistjs.php"
	response = open(php_path)
	num_lines = len(response.readlines())
	print("Argument list created.")

	# create a process pool that uses all cpus, and automatically closes.
	with multiprocessing.Pool() as pool:
		# call the function for each item in parallel with multiple arguments
		for result in pool.imap(find_data, range(num_lines)):
			print(result)
