'''
Created on Jun 21, 2022

@author: riaps
'''

import threading
import time

class Ticker(threading.Thread):
    '''
    Simple periodic ticker
    '''
    def __init__(self,period, callback):
        threading.Thread.__init__(self,name='Ticker-%r' % period,daemon=True)
        self.period = period
        self.callback = callback
        self.finished = threading.Event()
    
    def run(self):
        while True:
            self.finished.wait(timeout=self.period)
            if not self.finished.is_set():
                self.callback()
                continue
            else:
                break
    
    def cancel(self):
        self.finished.set()

if __name__ == '__main__':
    def tick():
        print('> tick')
    ticker = Ticker(1.0,tick)
    ticker.start()
    time.sleep(5)
    ticker.cancel()
    ticker.join()
