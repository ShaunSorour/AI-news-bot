from bardapi import Bard
from dotenv import load_dotenv
load_dotenv()
import params
import bard_queries
import re

 
def call_bard(query):
   try:
      bard = Bard()
      answer = bard.get_answer(query)
      return (answer['content'])
   except Exception as e:
      print("Error calling Bard")
      print(e)


def get_related_interests():
   try:
      response = call_bard(bard_queries.interest)
      pattern = r'keywords_list = \[(.*?)\]'
      match = re.search(pattern, response, re.DOTALL)
      keywords = []

      if match:
         keywords_part = match.group(1)
         keywords_list = [keyword.strip() for keyword in keywords_part.split(',')]
         modified_list = [item.strip("'").replace('"', '') for item in keywords_list]
      else:
         print("No keyword list found in Bard response")

      for word in modified_list:
         keywords.append(word)

      params.interests.extend(keywords)
      params.interests = [item for item in params.interests if item != '']
      print("Updated interests successfully: ")
      print(params.interests)
   except Exception as e:
      print("Error updating interest list")
      print(e)


def get_related_news_sources():
   try:
      response = call_bard(bard_queries.news_sources)
      pattern = r"url_list\s*=\s*{(.+?)}"
      match = re.search(pattern, response, re.DOTALL)

      if match:
         url_list_str = match.group(1)
         url_list = eval("{" + url_list_str + "}")
         params.news_sources = url_list
      else:
         print("No url list found in Bard response")
      
      print("Updated urls successfully: ")
      print(params.news_sources)
   except Exception as e:
      print("Error updating url list")
      print(e)