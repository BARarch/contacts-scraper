    # Termination States for Organizations checked through this class
    nothing_passed_merge = {}
    link_not_open = {}
    not_extracted = {}
    extracted = {}

	def add_to_nothing_passed_merge_dict(cls, numStarts):
	ContactScraperVerifier.nothing_passed_merge[ContactScraperVerifier.currentOrgName] = numStarts