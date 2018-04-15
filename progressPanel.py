import sys
import time
from tkinter import *
import tkinter.ttk as ttk


class ProgressPanel:
    def __init__(self, master=None, width=50, top=10, bottom=10):
        # Has a frame
        self.frame = Frame(master)
        self.frame.pack(expand=True)
        self.status = Label(self.frame, pady=4, relief=SUNKEN, text='Progress Panel at your service!')
        self.status.pack(expand=True, pady=0 ,ipady=0 ,side=TOP, anchor=N, fill=X)
        self.progressBarPosition = 0
        self.progressBarStops = 10
        self.progressBarState = 0
        self.progress = ttk.Progressbar(self.frame, orient='horizontal', length=400, mode='determinate', maximum=200, variable=self.progressBarPosition)
        self.progress.pack(side=TOP, expand=True, fill=X, ipady=1, pady=2)
        self.inProgress = False
        
    def move_progress(self, pos):
        points = pos * self.progress['maximum'] - 1
        #print('__moveProgresstoState', pos, '__current', self.progress['value'], '__value', points)
        
        while self.progress['value'] < points:
            if not self.inProgress:
                #print('Progress Bar terminated mid run prior to step')
                break
            self.progress.step()
            self.frame.update()
            #print('__value', self.progress['value'])
            time.sleep(.01)

        #print(self.progress['value'])
    
    def finnish_sequence(self):
        #print('__progressWeAreFinnshing')
        # Move Bar to End
        self.move_progress(1/1)
        
        # Set Flag
        self.inProgress = False
        
        # Final Step
        self.progress.step()
        self.frame.update()
        
    def set_progress_clicks(self, clicks):
        self.progressBarStops = clicks
        self.restart()
        return self
    
    def advance(self):
        ## Timing Error ## NEEDS FIXING ## Race Condition
        ## If two calls to the advance() method occur within the time it takes for a progress bar to travel
        ## progress bar locks until it is reset.  The advance needs to have accomodate a collistion or block calls
        if self.inProgress:
            self.progressBarState += 1
            if self.progressBarState == (self.progressBarStops):
                #print('__progressFINALStateCall', self.progressBarState)
                self.finnish_sequence()
                #print('Progress Bar State FINAL {}'.format(str(self.progressBarState)))
                #print('__progressFinalValue', self.progress['value'])
            else:
                #print('__progressStateCall', self.progressBarState)
                self.move_progress((self.progressBarState + 1) / (self.progressBarStops))
                self.frame.update()
                #print('Progress Bar State {}'.format(str(self.progressBarState)))
                #print('__progressValue', self.progress['value'])
        else:
            print('Progress Expired')
            self.frame.update()
        return self
    
    def restart(self):
        self.inProgress = True
        self.progressBarState = 0
        delta = self.progress['maximum'] - self.progress['value']
        self.progress.step(delta)
        self.frame.update()
        self.move_progress((self.progressBarState + 1) / (self.progressBarStops))
        return self
    
    def done(self):
        return not self.inProgress
    
    def message(self, msg):
        self.status.configure(text=msg)
        return self

class ProgressPanelGD(ProgressPanel):
    def __init__(self, master=None, width=50, top=10, bottom=10):
        # Has a frame
        self.frame = Frame(master)
        self.master = master
        
        self.status = Label(self.master, pady=4, relief=SUNKEN, text='Progress Panel at your service!')
        self.status.grid(row=0, column= 2,  sticky=E+W, padx=10)
        #self.status.pack(expand=True, pady=0 ,ipady=0 ,side=TOP, anchor=N, fill=X)
        
        self.progressBarPosition = 0
        self.progressBarStops = 10
        self.progressBarState = 0
        self.progress = ttk.Progressbar(self.master, orient='horizontal', length=395, mode='determinate', maximum=200, variable=self.progressBarPosition)
        self.progress.grid(row=1, column= 2)
        #self.progress.pack(side=TOP, expand=True, fill=X, ipady=1, pady=2)
        
        self.inProgress = False

        #self.frame.grid()
        #self.frame.pack(expand=True)
        
            
            
    
    
if __name__ == '__main__':
    
    class TestProgressPanel(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)              # Do superclass init
            self.pack()
            self.parent = master
            self.ProgressPanel = ProgressPanelGD(self)
            self.loops = 0
            
        def move(self):
            self.ProgressPanel.advance().advance().advance().set_progress_clicks(3).advance().advance().advance().advance().message('Test Done')
            
        def move_start(self):
            self.loops = 1
            self.ProgressPanel.message('Loop {}'.format(str(self.loops)))
            self.ProgressPanel.set_progress_clicks(4)
            time.sleep(.5)
            self.parent.after(200, self.move_loop())
            
            
        def move_loop(self):
            self.loops += 1
            self.ProgressPanel.message('Loop {}'.format(str(self.loops)))
            self.ProgressPanel.advance()
            time.sleep(.5)
            
            if self.ProgressPanel.done():
                self.ProgressPanel.message('Process Done')
                return
            self.parent.after(200, self.move_loop())
            
            
            
    root = Tk()
    root.title('The Progress Panel')
    app = TestProgressPanel(master=root)
    app.after(500, app.move_start())
    app.mainloop()
    root.destroy()