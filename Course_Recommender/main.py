# necessary_imports
import chromedriver_autoinstaller
from src.utils.udemy_scrapper import udemy_scrapper
from src.utils.coursera_scrapper import coursera_scrapper

# automatically installs chromedriver 
chromedriver_autoinstaller.install()
search_entry="java"
#search_entry=input("Enter your Language")

udemy_url='https://www.udemy.com/courses/search/?q=' + search_entry
coursera_url='https://www.coursera.org/search?query=' + search_entry + '&'
#To open the webpage of the given url

#driver_initiation

#class object calling for udemy
p=uscrap("xyz.com","java")
p.udemy_scrapper()
p.store()

udemy_scrapper(udemy_url,search_entry)
#coursera_scrapper(coursera_url,search_entry)