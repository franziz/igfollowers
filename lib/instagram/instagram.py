from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui                  import WebDriverWait
from selenium                                       import webdriver
from .user                                          import User
from ..logger										import Logger

class Instagram(object):
	def __init__(self):
		self.logger 		 = Logger()
		self.logger.app_name = "igfollowers"

		cap                                               = DesiredCapabilities.PHANTOMJS.copy()
		cap["phantomjs.page.settings.userAgent"]          = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
		cap["phantomjs.page.settings.loadImages"]         = False
		cap["phantomjs.page.settings.webSecurityEnabled"] = False

		service_args = ['--ignore-ssl-errors=true','--ssl-protocol=tlsv1']
		self.driver  = webdriver.PhantomJS(
							desired_capabilities = cap,
							        service_args = service_args
					   )
		self.wait    = WebDriverWait(self.driver,30)
		self.driver.set_window_size(1366,768)

		self.username  = None
		self.password  = None
		self.logged_in = False

	def quit(self):
		self.driver.quit()

	def login(self):
		try:
			assert self.username is not None, "username is not defined."
			assert self.password is not None, "password is not defined."
			
			self.logger.debug("Login-ing")
			self.driver.get("https://instagram.com")

			self.wait.until(lambda driver:driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a'))	
			btn_login = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')
			btn_login.click()

			self.wait.until(lambda driver:driver.find_element_by_xpath("//input[@aria-label='Username']"))
			txt_username = self.driver.find_element_by_xpath("//input[@aria-label='Username']")
			txt_password = self.driver.find_element_by_xpath("//input[@aria-label='Password']")
			btn_login    = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button')

			txt_username.send_keys(self.username)
			txt_password.send_keys(self.password)
			btn_login.click()

			try:
				self.wait.until(lambda driver:driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div/div/div/div[1]/div'))
				self.logged_in = True
			except selenium.common.exceptions.TimeoutException:
				# TODO: Check if you need to try logged in or inform that the user got blocked
				# This is because the user cannot login, should we try it again?
				raise
		except AssertionError:
			raise
		except:
			raise

	def goto_user(self,username=None):
		assert username is not None, "username is not defined."
		assert username            , "username cannot be empty."
				
		self.logger.debug("Go to {}".format(username))
		url = "https://www.instagram.com/{}/".format(username)
		self.driver.get(url)

		user       = User(username=username, session=[self.driver, self.wait])
		user.crawl = True
		return user
