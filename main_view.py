from tkinter import *
from tkinter.filedialog import askopenfile
from connection import *
import glob
f = ''
remark = ''
r = ''
def fileselector():
    global f
    f = askopenfile(initialdir = '/home/him/Documents')
    print(f)

def send(pid):
    if len(sys.argv) > 1:
        s = Client(sys.argv[1], int(sys.argv[2]))
    else:
        s = Client()
    s.send_file(f.name, pid)
    remark = s.sockobj.recv(1024).decode()
    if remark == 'ACCEPTED':
        r.config(text = remark, bg = 'green')
    else:
        r.config(text = remark, bg = 'red')

def view_problem(pid):
    win = Tk()
    win.title('Problem'+str(pid))
    c = Canvas(win, width = 450, height = 450)
    with open('problems/'+str(pid)+'.st') as f:
        #print(f.read())
        l = Label(c, text = f.read(),)
    l.pack()
    c.create_window(225, 50, window = l)
    b = Button(c, text = 'Choose file', command = lambda:fileselector())
    b.pack()
    c.create_window(225, 300, window = b)
    bd = Button(c, text = 'Submit', command = lambda:send(pid))
    bd.pack()
    c.create_window(225, 330, window = bd)
    global r
    r = Label(c, text = remark)
    r.pack()
    c.create_window(225, 350, window = r)
    c.pack()

if __name__ == '__main__':
    root = Tk()
    root.title('RNS Judge')
    c = Canvas(root, width = 450, height = 450)
    heading = Label(root, text = '--- RNS Judge ---', font = ('Helvetica',16,'bold'))
    heading.pack()
    c.create_window(225, 30, window = heading)
    i = 1
    for file in glob.glob('problems/*.in'):
        w = Label(root, text = 'Problem'+str(i), )
        w.pack()
        b = Button(root, text = 'View', command = lambda i = i:view_problem(i))
        b.pack()
        c.create_window(50, 40+40*i, window = w)
        c.create_window(400, 40+40*i, window = b)
        i += 1
    c.pack()
    root.mainloop()
