import requests
import json
import re

#Obtain the version information for each software from their corresponding API from Github
r1 = requests.get('https://api.github.com/repos/django/django/tags')
r2 = requests.get('https://api.github.com/repos/tensorflow/tensorflow/tags')
r3 = requests.get('https://api.github.com/repos/apache/kafka/tags')

#Function to preprocess version text, specifically when there is a letter 'v' in the front, we will remove it
def preprocess_version(version_str):
	if re.findall('^v',version_str):
		return version_str[1:]

#Function to retrieve version number from API and return the version ids as a list
#When flag == 1, the function will call the preprocess_version function to remove the 'v' in front of the version ids.
def get_version(r,flag=0):
	if(r.ok):
		repoItem = json.loads(r.text or r.content)
		version_list = []
		for i in range(len(repoItem)):
			version = repoItem[i]['name']
			if re.findall('^[0-9,v]',version):
				if flag == 1:
					version = preprocess_version(version)
				version_list.append(version)
		return version_list
	else:
		print('Please check the input API URL.')
django_version_list = get_version(r1)
tensorflow_version_list = get_version(r2)
tensorflow_version_list_processed = get_version(r2,1)
kafka_version_list = get_version(r3)

original_dict = {'django':django_version_list,'tensorflow':tensorflow_version_list,'kafka':kafka_version_list}
print(original_dict)
processed_dict = {'django':django_version_list,'tensorflow':tensorflow_version_list_processed,'kafka':kafka_version_list}
print(processed_dict)

filename = 'original.json'
with open(filename,'w') as f_obj:
	json.dump(original_dict,f_obj)

filename = 'processed.json'
with open(filename,'w') as f_obj:
	json.dump(processed_dict,f_obj)
