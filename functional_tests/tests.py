from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
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
		time.sleep(1)
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		inputBox = self.browser.find_element_by_id('id_new_item')
		inputBox.send_keys('Use peacock feathers to make a fly')
		inputBox.send_keys(Keys.ENTER)
		time.sleep(1)
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

		# table = self.browser.find_element_by_id('id_list_table')
		# rows = table.find_elements_by_tag_name('tr')
		# self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
		# self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])

		self.fail('Finish the test!')
