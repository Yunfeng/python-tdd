from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:	
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_can_start_a_list_for_one_user(self):
		self.browser.get(self.live_server_url)

		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		inputBox = self.browser.find_element_by_id('id_new_item')
		self.assertEquals(
			inputBox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		inputBox.send_keys('Buy peacock feathers')
		inputBox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		inputBox = self.browser.find_element_by_id('id_new_item')
		inputBox.send_keys('Use peacock feathers to make a fly')
		inputBox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')


	def test_multiple_users_can_start_lists_at_different_urls(self):
		# edith create a new to-do list
		self.browser.get(self.live_server_url)
		inputBox = self.browser.find_element_by_id('id_new_item')
		inputBox.send_keys('Buy peacock feathers')
		inputBox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# she notice than there is only url for to-do
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')


		#now, a new user visit our website
		self.browser.quit()
		self.browser = webdriver.Firefox()

		#francis visit homepage , there is nothing
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		#he input a new to-do 
		inputBox = self.browser.find_element_by_id('id_new_item')
		inputBox.send_keys('Buy milk')
		inputBox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		francis_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		self.assertNotEqual(edith_list_url, francis_list_url)

		#There is not edith's to-do list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# two users close browser
