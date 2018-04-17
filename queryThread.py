import sys
import time

import queue
import threading

class QueryThread(threading.Thread):
    def __init__(self, link, browser, responseQueue):
        threading.Thread.__init__(self, daemon=True)

        self.link = link
        self.browser = browser
        self.responseQueue = responseQueue

    def run(self):
        # Execute Query with Browser and send response time
        try:
            start = time.clock()
            self.query = self.browser.get(self.link)    
            self.responseTime = time.clock() - start
            self.responseQueue.put({'query': self.query,
                                    'response time': self.responseTime})
        except BaseException as e:
            print('Browser Get Lockup')
            print(e)


        