def contact_row(accountName, contactId, firstName, lastName, title, email, contactSource):
    return {
        'Account Name': accountName,	
        'Contact ID': contactId,	
        'First Name': firstName,	
        'Last Name': lastName, 	
        'Title': title,	
        'Email': email,
        'Contact Source': contactSource
    }

if __name__ == "__main__":
    records = []
    records.append(contact_row('Sigma Nu-The University of Alabama', '', 'Clyde', 'Yelverton','Commander', '', 'http://sigmanualabama.com/chapter-news/2016-theta-chapter-officers/'))
    records.append(contact_row('Sigma Nu-The University of Alabama', '', 'Andrew', 'Palmer', 'Lt. Commander', '', 'http://sigmanualabama.com/chapter-news/2016-theta-chapter-officers/'))
    records.append(contact_row('Sigma Nu-The University of Alabama', '', 'George', 'McMillan','Treasurer', '', 'http://sigmanualabama.com/chapter-news/2016-theta-chapter-officers/'))
    records.append(contact_row('Sigma Nu-The University of Alabama', '', 'John', 'Perrett', 'Marshal', '', 'http://sigmanualabama.com/chapter-news/2016-theta-chapter-officers/'))
    records.append(contact_row('Sigma Nu-The University of Alabama', '', 'Wilson', 'Landers', 'Recorder', '', 'http://sigmanualabama.com/chapter-news/2016-theta-chapter-officers/'))
    records.append(contact_row('Sigma Nu-The University of Alabama', '', 'Keith', 'Taylor', 'House Manager', '', 'http://sigmanualabama.com/chapter-news/2016-theta-chapter-officers/'))
    records.append(contact_row('Sigma Nu-The University of Alabama', '', 'Brad', 'Nelson', 'Social Chair', '', 'http://sigmanualabama.com/chapter-news/2016-theta-chapter-officers/'))
    records.append(contact_row('Sigma Nu-The University of Alabama', '', 'James', 'McCool', 'Sentinel', '', 'http://sigmanualabama.com/chapter-news/2016-theta-chapter-officers/'))

    records.append(contact_row('Sigma Nu-University of South Carolina', '', 'Errol', 'McGillewie', 'Commander', 'SOSigNu@mailbox.sc.edu', 'http://sigmanudeltachapter.com/'))
    records.append(contact_row('Sigma Nu-University of South Carolina', '', 'Patrick', 'Wright', 'Advisor', 'patrick.wright@moore.sc.edu', 'http://sigmanudeltachapter.com/'))

    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Jared', 'Shely', 'Commander', 'shelyj18@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Tyler', 'Murphy', 'Lieutenant Commander', 'murphyt18@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Jacob', 'Ingber', 'Treasurer', 'ingberj19@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Davis', 'Alliger', 'Marshal', 'alligerb19@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Bennett', 'Newman', 'Senior Recruitment Chairman', 'newmanb19@mail.wlu.edu, 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Hunter', 'Ward', 'Senior Social Chairman', 'wardh18@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Keeghan', 'Sweeney', 'Chaplain', 'sweeneyk18@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Daniel', 'Morris', 'House Manager', 'morrisj20@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'John', 'Harashinski', 'Risk Reduction', 'harashinskij20@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Keith', 'Denning', 'Sentinel', 'denningk18@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
