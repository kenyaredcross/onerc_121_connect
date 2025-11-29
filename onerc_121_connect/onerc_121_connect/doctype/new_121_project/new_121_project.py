# Copyright (c) 2025, Kelvin Njenga and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class New121Project(Document):
	def validate (self):
		self.project_title = f"{self.project_code} | {self.name_of_project}"
		self.calculations()
	def onload(self):
		self.project_title = f"{self.project_code} | {self.name_of_project}"
		self.calculations()

		


	def calculations(self):

		households = 0
		disbursement = 0.0
		transaction_charges = 0.0
		total_amount = 0.0
		withdrawal = 0.0

		for row in self.details:
			households += (row.number_targeted or 0)
			disbursement += ((row.base_transfer_value or 0) + (row.withdrawal_charges or 0)) * (row.number_targeted or 0) * (row.number_of_tranches or 0)
			transaction_charges += (row.transactional_charges or 0)
			withdrawal += (row.withdrawal_charges or 0)
		
		self.total_disbursement = disbursement
		self.total_targeted_households = households
		self.service_charge = (self.total_disbursement + withdrawal)  * 0.015
		self.total_budget = self.service_charge + self.total_disbursement + transaction_charges + self.service_charge

