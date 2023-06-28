# Copyright (c) 2023, Vikram Kumar and contributors
# For license information, please see license.txt
import frappe
from frappe import _
from bs4 import BeautifulSoup
import imaplib
import email
import requests
import re
from frappe.model.document import Document

class EmailParser(Document):
	def before_save(self):
		temp = ""
		temp_fields = {}

		raw_email = str(self.email_body)
		body = BeautifulSoup(raw_email,"html.parser")
		plain_text = re.sub(r'\s*<br><br>\s*', '\n', body.get_text())
		clean = re.compile('<.*?>')
		foo = re.sub(clean, ' ', plain_text)
		# frappe.log_error(re.sub(r'\s*	\s*', '\n', foo),'body')
		foo = re.sub(r'(?<=Lead Details:)(.*?)(?=\w+:)', r'\n\1', foo)
		foo = re.sub(r'(?<=:\w)(.*?)\s(?=\w+:)', r'\1\n', foo)
		
		

		# frappe.log_error(foo,'foo')
		
		fields = ['Client Name', 'Company Name', 'Web URL','Company Description','City','Contact Number','Alternate Contact Number','Email','Designation','Client requirement','No of Users/employees','Preferred Deployment type','Implementation time frame','Existing Software Name','Reason to change','Software evaluated','Preferred time to call','Preferred mode of demo','Preferred location of vendor']
		actual_fields = {"Client Name":"client_name","Company Name":"company","Web URL":"website","Company Description":"company_description","City":"city","Contact Number":"mobile_no","Alternate Contact Number":"alternate_contact_number","Email":"email","Designation":"designation","Client requirement":"client_requirement","No of Users/employees":"no_of_usersemployees","Preferred Deployment type":"preferred_deployment_type","Implementation time frame":"implementation_time_frame","Existing Software Name":"existing_software_name","Reason to change":"reason_to_change","Software evaluated":"software_evaluated","Preferred mode of demo":"preferred_mode_of_demo","Preferred time to call":"preferred_time_to_call","Preferred location of vendor":"preferred_location_of_vendor"}
		pattern = r'({}):\s*(.*?)\n'.format('|'.join(fields))
		matches = re.findall(pattern, foo)
		# frappe.log_error(matches,'matches')
		extracted_info = {}
		for match in matches:
			field = match[0]
			value = match[1].strip()
			extracted_info[actual_fields[field]] = value
		# frappe.log_error(extracted_info,"extracted_info")
		for field, value in extracted_info.items():
			# temp = temp + field + ': ' + value + '\n'
			# temp_fields[field] = value
			self.lead_details = temp
		# doc.db_set('lead_details',temp)
		# frappe.log_error(temp,'temp')
		# frappe.log_error(temp_fields,'temp_fields')
		# self.get('client_name = "aaa"
		# for key, value in temp_fields.items():
		# 	setattr(self, key, value)

		frappe.log_error(foo,"foo")
		patterns = {
			'Client Name': r'Client\s+Name:\s+(.+?)\s+Company',
			'Company Name': r'Company\s+Name:\s+(.+?)\s+Web',
			'Web URL': r'Web\s+URL:\s+(.+?)\s+Company\s+Description',
			'Company Description': r'Company\s+Description:\s+(.+?)\s+City',
			'City': r'City:\s+(.+?)\s+Contact\s+Number',
			'Contact Number': r'Contact\s+Number:\s+(.+?)\s+Alternate\s+Contact\s+Number',
			'Alternate Contact Number': r'Alternate\s+Contact\s+Number:\s+(.+?)\s+Email',
			'Email': r'Email:\s+(.+?)\s+Designation',
			'Designation': r'Designation:\s+(.+?)\s+Client\s+requirement',
			'Client requirement': r'Client\s+requirement:\s+(.+?)\s+No\s+of\s+Users/employees',
			'No of Users/employees': r'No\s+of\s+Users/employees:\s+(.+?)\s+Preferred\s+Deployment\s+type',
			'Preferred Deployment type': r'Preferred\s+Deployment\s+type:\s+(.+?)\s+Implementation\s+time\s+frame',
			'Implementation time frame': r'Implementation\s+time\s+frame:\s+(.+?)\s+Existing\s+Software\s+Name',
			'Existing Software Name': r'Existing\s+Software\s+Name:\s+(.+?)\s+Reason\s+to\s+change',
			'Reason to change': r'Reason\s+to\s+change:\s+(.+?)\s+Software\s+evaluated',
			'Software evaluated': r'Software\s+evaluated:\s+(.+?)\s+Preferred\s+time\s+to\s+call',
			'Preferred time to call': r'Preferred\s+time\s+to\s+call:\s+(.+?)\s+Preferred\s+mode\s+of\s+demo',
			'Preferred mode of demo': r'Preferred\s+mode\s+of\s+demo:\s+(.+?)\s+Preferred\s+location\s+of\s+vendor',
			'Preferred location of vendor': r'Preferred\s+location\s+of\s+vendor:\s+(.+?)\s+\t'
		}

		extracted_info = {}
		for field, pattern in patterns.items():
			match = re.search(pattern, foo, re.DOTALL)
			if match:
				extracted_info[actual_fields[field]] = match.group(1)

		# Print the extracted information
		for field, value in extracted_info.items():
			# print(f'{field}: {value}')
			setattr(self, field, value)
			temp = temp + field + ': ' + value + '\n'
		frappe.log_error(temp,'temp')
			