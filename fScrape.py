from sheetOutput import *

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
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Bennett', 'Newman', 'Senior Recruitment Chairman', 'newmanb19@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Hunter', 'Ward', 'Senior Social Chairman', 'wardh18@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Keeghan', 'Sweeney', 'Chaplain', 'sweeneyk18@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Daniel', 'Morris', 'House Manager', 'morrisj20@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'John', 'Harashinski', 'Risk Reduction', 'harashinskij20@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))
    records.append(contact_row('Sigma Nu-Washington and Lee University', '', 'Keith', 'Denning', 'Sentinel', 'denningk18@mail.wlu.edu', 'https://sigmanu1.academic.wlu.edu/leadership/'))

    records.append(contact_row('Sigma Nu-University of Kansas', '', 'JACOB', 'SCOTT', 'EMINENT COMMANDER', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'MAX', 'VINCENT', 'LIEUTENANT COMMANDER', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'ZACH', 'MARSO', 'TREASURER', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'RESER', 'HALL', 'RECORDER', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'ZACH', 'SCHMITT', 'MARSHAL', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'BRENT', 'ALFARO', 'RUSH CHAIRMAN', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'MICHAEL', 'DAVIDSON', 'RUSH CHAIRMAN', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'LUKE', 'RATZLAFF', 'RUSH CHAIRMAN', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'WYATT', 'RUGAN', 'CHAPLAIN', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'ADAM', 'GLEASON', 'SCHOLARSHIP CHAIR', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'SAM', 'REINIG', 'ALUMNI CONTACT', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'ZACH', 'LAWRENCE', 'SOCIAL CHAIR', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'BLAKE', 'MARSEE', 'EDUCATOR', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'CAMRON', 'MYERS', 'SENTINEL', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'REID', 'BRUNSWIG', 'HOUSE MANAGER', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'COLE', 'CHALMERS', 'PHILANTHROPY CHAIR', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'EASTON', 'MONTGOMERY', 'INTRAMURAL CHAIR', '', 'http://www.kansassigmanu.com/meet.html'))
    records.append(contact_row('Sigma Nu-University of Kansas', '', 'JOHNNY', 'RICHMOND', 'ENVIRONMENTAL CHAIR', '', 'http://www.kansassigmanu.com/meet.html'))

    records.append(contact_row('Sigma Nu-University of Missouri', '', 'Solomon', 'Douglas', 'Commander', 'solomon4150@gmail.com', 'http://sigmanumu.com/contact/'))
    records.append(contact_row('Sigma Nu-University of Missouri', '', 'Adam', 'Swehla', 'Lieutenant Commander', 'adamswehla98@gmail.com', 'http://sigmanumu.com/contact/'))
    records.append(contact_row('Sigma Nu-University of Missouri', '', 'Logan', 'Clark', 'Treasurer', 'lmcww7@mail.missouri.edu', 'http://sigmanumu.com/contact/'))
    records.append(contact_row('Sigma Nu-University of Missouri', '', 'Jack', 'Kleiss', 'Philanthropy Chairman', 'jrkx59@mail.missouri.edu', 'http://sigmanumu.com/contact/'))
    records.append(contact_row('Sigma Nu-University of Missouri', '', 'Andrew', 'Huertas', 'Recruitment Chairman', 'sigmanurush@gmail.com', 'http://sigmanumu.com/contact/'))
    records.append(contact_row('Sigma Nu-University of Missouri', '', 'Kyler', 'Bayless', 'Recruitment Chairman', 'sigmanurush@gmail.com', 'http://sigmanumu.com/contact/'))

    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'David', 'Vitek', 'Eminent Commander', 'vitek@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Sam', 'Agnew', 'Lieutenant Commander', 'sagnewv1@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Matthew', 'Gurkin', 'Treasurer', 'mgurkin10@gmail.com', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Connor', 'Shaw', 'Recorder', 'cshaw16@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Chris', 'Batchelor', 'Alumni Relations Chair', 'cdbatch@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Ryan', 'Facer', 'House Manager', 'rdfacer@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Seth', 'Hauser', 'Social Chair', 'sethh18@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Blanton', 'Smith', 'Co-Chaplain (Brotherhood Chair)', 'blantonsmith10@gmail.com', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Eric', 'Tomlinson', 'Co-Chaplain (Brotherhood Chair)', 'ectomlin@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Taylor', 'Dameworth', 'Risk Management Officer', 'taylord5@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Ben', 'Albert', 'Scholarship Chair', 'btalbert@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Chris', 'White', 'Co-Rush Chair', 'cwhite96@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Carson', 'Southard', 'Co-Rush Chair', 'carsouth@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Akash', 'Mishra', 'Historian', 'akash97@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Tyler', 'Tonnesen', 'Philanthropy Chair', 'tyler_tonnesen@kenan-flagler.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))
    records.append(contact_row('Sigma Nu-University of North Carolina at Chapel Hill', '', 'Colin', 'Russell', 'LEAD Chair', 'colinunc@live.unc.edu', 'https://uncsigmanu.2stayconnected.com/index.php?option=com_content&view=article&id=49&Itemid=569'))

    records.append(contact_row('Sigma Nu-Auburn University', '', 'Kevin', 'Partlow', 'Commander', 'partlkc@auburn.edu', 'http://www.auburn.edu/student_info/greeks/sigma_nu/officers.html'))
    records.append(contact_row('Sigma Nu-Auburn University', '', 'Will', 'Avery', 'Lt. Commander', 'averywr@auburn.edu', 'http://www.auburn.edu/student_info/greeks/sigma_nu/officers.html'))
    records.append(contact_row('Sigma Nu-Auburn University', '', 'Keith', 'Norman', 'Treasurer', 'normamk@auburn.edu', 'http://www.auburn.edu/student_info/greeks/sigma_nu/officers.html'))
    records.append(contact_row('Sigma Nu-Auburn University', '', 'Bo', 'Bledsoe', 'Recorder', 'bledsrw@auburn.edu', 'http://www.auburn.edu/student_info/greeks/sigma_nu/officers.html'))
    records.append(contact_row('Sigma Nu-Auburn University', '', 'Drew', 'Tatum', 'House Chairman', 'dft0001@auburn.edu', 'http://www.auburn.edu/student_info/greeks/sigma_nu/officers.html'))
    records.append(contact_row('Sigma Nu-Auburn University', '', 'Drew', 'Chapman', 'Social Chairman', 'chapmar@auburn.edu', 'http://www.auburn.edu/student_info/greeks/sigma_nu/officers.html'))
    records.append(contact_row('Sigma Nu-Auburn University', '', 'Charlie', 'Gibson', 'Rush Chairman', 'gibsoch@auburn.edu', 'http://www.auburn.edu/student_info/greeks/sigma_nu/officers.html'))
    records.append(contact_row('Sigma Nu-Auburn University', '', 'Kyle', 'Gaston', 'Alumni Chairman', 'gastoka@auburn.edu', 'http://www.auburn.edu/student_info/greeks/sigma_nu/officers.html'))

    records.append(contact_row('Sigma Nu-Purdue University', '', 'Nick', 'Oetting', 'Eminent Commander', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Forrest', 'Brown', 'Lieutenant Commander', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Eric', 'Eagon', 'Treasurer', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Anders', 'Hovstadius', 'Recorder', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'John', 'Lawicki', 'Chaplain', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Ben', 'Collins', 'Risk Reduction Chairman', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Jackson', 'Glenn', 'Social Chairman', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Kyle', 'Weiss', 'Recruitment Chairman', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Anish', 'Mohan', 'Scholarship Chairman', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Jake', 'Copas', 'LEAD Chairman', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Everett', 'Mitchel ', 'Philanthropy and  Service Chairman', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Logan', 'Plack', 'Athletics Chairman', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Aaron', 'Fischer', 'Alumni Relations Chairman', '', 'https://www.purduesigmanu.org/officers'))
    records.append(contact_row('Sigma Nu-Purdue University', '', 'Austin', 'Duarte', 'Marshal', '', 'https://www.purduesigmanu.org/officers'))

    
