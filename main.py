from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
import os
import streamlit as st

# SIMILAR_ACCOUNT = "eminem"
# username = os.environ.get("username")
# password = os.environ.get("password")





class InstaFollower:

    def __init__(self):
        # Optional - Keep browser open (helps diagnose issues during a crash)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        url = "https://www.instagram.com/accounts/login/"
        self.driver.get( url )
        time.sleep( 4.2 )

        # Check if the cookie warning is present on the page
        decline_cookies_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]"
        cookie_warning = self.driver.find_elements( By.XPATH, decline_cookies_xpath )
        if cookie_warning:
            # Dismiss the cookie warning by clicking an element or button
            cookie_warning[0].click()

        username_input = self.driver.find_element( by=By.NAME, value="username" )
        password_input = self.driver.find_element( by=By.NAME, value="password" )

        username_input.send_keys(username)
        password_input.send_keys(password)

        time.sleep(2)
        password_input.send_keys(Keys.ENTER)



        time.sleep(10)
        # Click "not now" on notifications prompt
        notifications_prompt = self.driver.find_element( by=By.XPATH, value="// button[contains(text(), 'Not Now')]" )
        if notifications_prompt:
            notifications_prompt.click()





    def find_followers(self):
        new_url = self.driver.get(f"https://www.instagram.com/{similar_account}/followers/")
        time.sleep(3)
        modal_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]"
        modal = self.driver.find_element( by=By.XPATH, value=modal_xpath )
        for i in range(10):
            # In this case we're executing some Javascript, that's what the execute_script() method does.
            # The method can accept the script as well as an HTML element.
            # The modal in this case, becomes the arguments[0] in the script.
            # Then we're using Javascript to say: "scroll the top of the modal (popup) element by the height of the modal (popup)"
            self.driver.execute_script( "arguments[0].scrollTop = arguments[0].scrollHeight", modal )


    def follow(self):
        # Check and update the (CSS) Selector for the "Follow" buttons as required.
        all_buttons = self.driver.find_elements( By.CSS_SELECTOR, value='._aano button' )

        for button in all_buttons:
            try:
                button.click()
                time.sleep( 1.1 )
            # Clicking button for someone who is already being followed will trigger dialog to Unfollow/Cancel
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element( by=By.XPATH, value="//button[contains(text(), 'unfollow')]" )
                cancel_button.click()


# Streamlit Configuration
st.title("Instagram Bot")

# Get User Input
username = st.text_input("Your Instagram Username")
password = st.text_input("Your Instagram Password", type="password")
similar_account = st.text_input("Target Account (Similar to Find Followers)")

# Action Button
if st.button("Start Bot"):
    # Store credentials securely (consider using Streamlit Secrets)
    os.environ["username"] = username
    os.environ["password"] = password

    with st.spinner("Initializing Bot..."):
        bot = InstaFollower()
        bot.login()
        bot.find_followers()
        bot.follow()

    st.success("Bot actions completed!")


