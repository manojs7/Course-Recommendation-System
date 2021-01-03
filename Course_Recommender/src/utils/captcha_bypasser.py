#modules for the program
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#modules for audio captcha
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub
from pydub import AudioSegment

def captcha_bypasser(driver):
    #bypassing captcha
    try:
        #audio button
        audio_btn=driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button")
        audio_btn.click()
        time.sleep(5)
        f=0
        
        #inputing the text until the captchas succeeds
        while(f==0):
            try:
                play=WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div[3]/div/button")))
                time.sleep(2)
                play=driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button")
                play.click()
                
                #getting the link to the audio file
                #/html/body/div/div/div[3]/audio
                #audio=WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div[3]/audio")))
                audio=driver.find_element_by_xpath("/html/body/div/div/div[3]/audio").get_attribute("src")
                
                #downloading the audio file
                urllib.request.urlretrieve(audio, "sample.mp3")
                pydub.AudioSegment.ffmpeg = "/absolute/path/to/ffmpeg"
                sound =AudioSegment.from_mp3("sample.mp3")
                sound.export("sample.wav", format="wav")
                sample_audio = sr.AudioFile("sample.wav")
                r= sr.Recognizer()
                with sample_audio as source:
                    audio = r.record(source)
                    
                #text to speech
                time.sleep(5)
                key=r.recognize_google(audio,language="en-US")
                print("Recaptcha Passcode: %s"%key)
                time.sleep(5)
                
                #entering the output
                audio_text=driver.find_element_by_xpath("/html/body/div/div/div[5]/input")
                audio_text.send_keys(key)
                time.sleep(5)
                verify=driver.find_element_by_xpath("/html/body/div/div/div[7]/div[2]/div[1]/div[2]/button")
                verify.click()
            except:
                print("Wrong")
                f=1
    except:
        print("Error or Bypassed")
        pass
        
    