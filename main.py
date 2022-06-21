
import random
from tkinter import *;
from  tkinter import ttk
from tkinter import messagebox;
import matplotlib.pyplot as plt;
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class Point(object):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.point = "+"
        self.b = 0
        self.f = -1
        self.k = -1

def info_window():
    global N

    try:
        N = int(insert_count_point.get())
    except:
        messagebox.showinfo("Optimization.com", "Введено некорректное значение!")
        insert_count_point.delete(0, END)
        return

    if N == "" or N == 1:
        messagebox.showinfo("Optimization.com", "Введено некорректное значение!")
        insert_count_point.delete(0, END)
    else:

        info_window = Toplevel();
        info_window.resizable(width=False, height=False)
        info_window.title("Explorer.Dialog")
        info_window.wm_geometry("+%d+%d" % (630, 400))
        lbl = Label(info_window, text="Вы уверены, что хотите сгенерировать новые точки?  Старые будут удалены!", font='Times 13');
        lbl.pack(side='top', ipadx=4, padx=1, ipady=3, pady=3);
        frame_1 = Frame(  info_window)
        frame_1.pack(side = TOP)
        destroy1_window_btn = Button( frame_1, text="Да",  command=lambda:[info_window.destroy(), generate_points()], font='Times 13', width = 15 );
        destroy1_window_btn.pack(side='left', ipadx=6, padx=4, ipady=5, pady=5 );

        destroy2_window_btn = Button( frame_1, text="Нет", command=info_window.destroy, font='Times 13', width = 15);
        destroy2_window_btn.pack(side='left', ipadx=6, padx=4, ipady=5, pady=5);

        info_window.focus_set()
        info_window.grab_set()
        info_window.mainloop();




def default_paint():
    plt.plot([-1, 20], [14, 35], color="white", ms=0.5)
    plt.plot([30, -1], [0, 31], color="white", ms=0.5)
    ax.set_xlabel('f1')
    ax.set_ylabel('f2')


def paint():
    ax.clear()
    ax.add_patch(plt.Circle((n, n), n, color='k', fill=None))
    plt.plot([-1, 20], [14, 35], color="k", ms = 0.5)
    plt.plot([30, -1], [0, 31], color="k", ms = 0.5)
    ax.set_xlabel('f1')
    ax.set_ylabel('f2')

def generate_points():
    insert_count_point.delete(0, END)
    paint();
    list_points.clear();
    table_view.tag_configure('ne2', background='#C9C9C9')
    for i in range(len(table_view.get_children())):
        table_view.delete(i);

    while len(list_points) != N:
        X = random.randint(0, 2 * n)
        Y = random.randint(0, 2 * n)

        if ((X - n) ** 2 + (Y - n) ** 2 <= n ** 2) and (-X + Y <= n) and (X + Y >= 2 * n):
            list_points.append(Point(X, Y));
            plt.plot(X, Y, "o", mfc="#B300E0", mec="#B300E0", ms=4)
            ax.text(X - 0.35, Y + 0.5, len(list_points))

    for i in range(len(list_points)):

        if list_points[i].point != "-":
            for k in range(len(list_points)):
                if k != i:
                    if list_points[k].X <= list_points[i].X and list_points[k].Y <= list_points[i].Y:
                        list_points[k].point = "-"

        for k in range(len(list_points)):
            if k != i:
                if list_points[k].X >= list_points[i].X and list_points[k].Y >= list_points[i].Y:
                    list_points[i].b += 1

        list_points[i].f = round((1 / (1 + list_points[i].b / (N - 1))), 3)
        K = [abs(1 - list_points[i].f), abs(0.85 - list_points[i].f), abs(0.75 - list_points[i].f) ]
        if K.index(min(K)) == 0:
            list_points[i].k = 1
        elif K.index(min(K)) == 1:
            list_points[i].k = 2
        else:
            list_points[i].k = 3

        if i % 2 == 0:
            table_view.insert(parent='', index='end', iid=i, text='',
                              values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                      list_points[i].k), tags = ('ne2'))
        else:
            table_view.insert(parent='', index='end', iid=i, text='',
                              values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                      list_points[i].k))

    table_view.insert(parent='', index='end', iid=i + 1, text='',
                      values=("-", "-", "-", "-", "-",
                              "-"))
    canvas1.draw();


def optimization():
    if len(list_points) == 0:
        messagebox.showinfo("Optimization.com", "Сначала сгенерируйте точки!")
    else:
        paint();
        table_view.tag_configure('ne2', background='#C9C9C9')
        table_view.tag_configure('best', background='#FF7A8C')

        for i in range(len(table_view.get_children())):
            table_view.delete(i);
        for i in range(len(list_points)):

            if list_points[i].point == "+":
                table_view.insert(parent='', index='end', iid=i, text='',
                                  values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                          list_points[i].k), tags=('best'))
                plt.plot(list_points[i].X, list_points[i].Y, "o", mfc="#FF7A8C", mec="#FF7A8C", ms=4)
                ax.text(list_points[i].X - 0.4, list_points[i].Y + 0.5, i+1)
            elif i % 2 == 0:
                table_view.insert(parent='', index='end', iid=i, text='',
                                  values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                          list_points[i].k), tags = ('ne2'))
            else:
                table_view.insert(parent='', index='end', iid=i, text='',
                                  values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                          list_points[i].k))
        table_view.insert(parent='', index='end', iid=i + 1, text='',
                          values=("-", "-", "-", "-", "-",
                                  "-"))
        canvas1.draw()
        #

def view_all():
    if len(list_points) == 0:
        messagebox.showinfo("Optimization.com", "Сначала сгенерируйте точки!")
    else:
        paint()
        for i in range(len(table_view.get_children())):
            table_view.delete(i);
        for i in range(len(list_points)):

            if i % 2 == 0:
                table_view.insert(parent='', index='end', iid=i, text='',
                                  values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                          list_points[i].k), tags=('ne2'))
            else:
                table_view.insert(parent='', index='end', iid=i, text='',
                                  values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                          list_points[i].k))



            plt.plot(list_points[i].X, list_points[i].Y, "o", mfc="#B300E0", mec="#B300E0", ms=4)
            ax.text(list_points[i].X - 0.4, list_points[i].Y + 0.5, i+1)

        table_view.insert(parent='', index='end', iid=i + 1, text='',
                          values=("-", "-", "-", "-", "-",
                                  "-"))
        canvas1.draw()

def insert_point():

    if insert_X.get() != "" or insert_Y.get() != "" :
        list_points.append(Point(int(insert_X.get()), int(insert_Y.get())))

        if (( list_points[len(list_points)-1].X - n) ** 2 + ( list_points[len(list_points) - 1].Y - n) ** 2 <= n ** 2) and (-list_points[len(list_points)-1].X +  list_points[len(list_points) - 1].Y <= n) and (list_points[len(list_points)-1].X +  list_points[len(list_points) - 1].Y >= 2 * n):

            paint();

            table_view.tag_configure('ne2', background='#C9C9C9')
            for i in range(len(table_view.get_children())):
                table_view.delete(i);



            for i in range(len(list_points)):

                plt.plot(list_points[i].X, list_points[i].Y, "o", mfc="#B300E0", mec="#B300E0", ms=4)
                ax.text(list_points[i].X - 0.4, list_points[i].Y + 0.5, i+1)

                if list_points[i].point != "-":
                    for k in range(len(list_points)):
                        if k != i:
                            if list_points[k].X <= list_points[i].X and list_points[k].Y <= list_points[i].Y:
                                list_points[k].point = "-"

                for k in range(len(list_points)):
                    if k != i:
                        if list_points[k].X >= list_points[i].X and list_points[k].Y >= list_points[i].Y:
                            list_points[i].b += 1

                list_points[i].f = round((1 / (1 + list_points[i].b / (N - 1))), 3)
                K = [abs(1 - list_points[i].f), abs(0.85 - list_points[i].f), abs(0.75 - list_points[i].f)]
                if K.index(min(K)) == 0:
                    list_points[i].k = 1
                elif K.index(min(K)) == 1:
                    list_points[i].k = 2
                else:
                    list_points[i].k = 3

                if i % 2 == 0:
                    table_view.insert(parent='', index='end', iid=i, text='',
                                      values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                              list_points[i].k), tags=('ne2'))
                else:
                    table_view.insert(parent='', index='end', iid=i, text='',
                                      values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                              list_points[i].k))

            table_view.insert(parent='', index='end', iid=i + 1, text='',
                              values=("-", "-", "-", "-", "-",
                                      "-"))
        else:
            list_points.pop(len(list_points)-1)
            messagebox.showinfo("Optimization.com", "Точка не попадает в заданную область!")
    else:
        messagebox.showinfo("Optimization.com", "Введено некорректное значение!")
    insert_Y.delete(0, END)
    insert_X.delete(0, END)
    canvas1.draw();


def delete_points():
    if len(list_points) != 0:
        ax.clear()
        for i in range(len(table_view.get_children())):
            table_view.delete(i);
        table_view.insert(parent='', index='end', iid=0, text='',
                          values=("-", "-", "-", "-", "-",
                                  "-"))
        default_paint()
        canvas1.draw()
        messagebox.showinfo("Optimization.com", "Удаление успешно произошло!")
        list_points.clear()
    else:
        messagebox.showinfo("Optimization.com", "Удаление не произошло, не задано ни одной точки!")

def clustering():
    if len(list_points) == 0:
        messagebox.showinfo("Optimization.com", "Не задано ни одной точки!")
    else:

        table_view.tag_configure('1', background='#FF7A8C')
        table_view.tag_configure('2', background='#FFE479')

        paint()
        for i in range(len(table_view.get_children())):
            table_view.delete(i);

        for i in range(len(list_points)):
            if list_points[i].k == 3:
                plt.plot(list_points[i].X, list_points[i].Y, "o", mfc="#B300E0", mec="#B300E0", ms=4)
                ax.text(list_points[i].X - 0.35, list_points[i].Y + 0.5, i+1)


                table_view.insert(parent='', index='end', iid=i, text='',
                                  values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                          list_points[i].k))



            elif list_points[i].k == 2:
                plt.plot(list_points[i].X, list_points[i].Y, "o", mfc="#FFE479", mec="#FFE479", ms=4)
                ax.text(list_points[i].X - 0.35, list_points[i].Y + 0.5, i+1)
                table_view.insert(parent='', index='end', iid=i, text='',
                                  values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                          list_points[i].k), tags=('2'))
            else:
                plt.plot(list_points[i].X, list_points[i].Y, "o", mfc="#FF7A8C", mec="#FF7A8C", ms=4)
                ax.text(list_points[i].X - 0.35, list_points[i].Y + 0.5, i+1)
                table_view.insert(parent='', index='end', iid=i, text='',
                                  values=(i + 1, list_points[i].X, list_points[i].Y, list_points[i].b, list_points[i].f,
                                          list_points[i].k), tags=('1'))
        canvas1.draw()






def disableEvent(event):
    return "break"

N = 20
n = 15
list_points = []

window = Tk()

window.wm_geometry("+%d+%d" % (500, 200))
window.resizable(width=False, height=False)
window.title("Optimization.com");

first_frame = Frame()
first_frame.pack(side=LEFT)
second_frame = Frame()
second_frame.pack(side=RIGHT)
third_frame = Frame(first_frame)
third_frame.pack(side = TOP)

fig, ax = plt.subplots(figsize=(4.5, 4.5))
default_paint()

canvas1 = FigureCanvasTkAgg(fig, master=first_frame)

style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Time', 11)) # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Time', 13, "bold"))
table_view = ttk.Treeview(second_frame, style ="mystyle.Treeview", height= 31)


table_view['columns'] = ('№', 'f1', 'f2', 'b', 'F', 'K')

table_view.column("#0", width=0,  stretch=NO)
table_view.column('№',anchor=CENTER, width=40)
table_view.column("f1",anchor=CENTER, width=59)
table_view.column("f2",anchor=CENTER,width=59)
table_view.column("b",anchor=CENTER,width=59)
table_view.column("F",anchor=CENTER,width=59)
table_view.column("K",anchor=CENTER,width=59)

table_view.heading("#0",text="",anchor=CENTER)
table_view.heading('№',text='№',anchor=CENTER)
table_view.heading("f1",text="f1",anchor=CENTER)
table_view.heading("f2",text="f2",anchor=CENTER)
table_view.heading("b",text="b [i]",anchor=CENTER)
table_view.heading("F",text="F [i]",anchor=CENTER)
table_view.heading("K",text="K",anchor=CENTER)


table_view.bind("<Button-1>", disableEvent)

table_view.insert(parent='', index='end', iid=0, text='',
                      values=("-", "-", "-", "-", "-",
                              "-"))

table_view.pack(ipadx=6, padx=4, ipady=6, pady= 6)

generate_frame = Frame(first_frame)
generate_frame.pack(side = TOP)
optimization_frame = Frame(first_frame)
optimization_frame.pack(side = TOP)
generate_btn = Button(generate_frame, text="Сгенерировать точки", command=info_window, font='Times 13', width=41)
generate_btn.pack(side=LEFT, fill=X, ipadx=6, padx=4, ipady=4, pady=5)
insert_count_point = Entry(generate_frame,  width = 5, font='Times 13')
insert_count_point.pack(side = LEFT, fill = Y, ipadx=6, padx=4, ipady=4, pady=5)
optimization_btn = Button(optimization_frame, text="Оптимальные решения", command=optimization, font='Times 13', width = 23)
optimization_btn.pack(side=LEFT, fill=X, ipadx=6, padx=4, ipady=4, pady=0, )
prosto_btn = Button(optimization_frame, text="Все решения", command=view_all, font='Times 13', width = 23)
prosto_btn.pack(side=LEFT, fill=X, ipadx=6, padx=4, ipady=4, pady=5)
insert_btn=Button(third_frame, text="Ввести точку", command=insert_point, font='Times 13', width= 15)
insert_btn.pack(side = LEFT, ipadx=6, padx=4, ipady=4, pady=5)
insert_X = Entry(third_frame, width = 5, font='Times 13')
insert_X.pack(side = LEFT, fill = Y, ipadx=6, padx=4, ipady=4, pady=5)
insert_Y = Entry(third_frame, width = 5, font='Times 13')
insert_Y.pack(side = LEFT, fill = Y, ipadx=6, padx=4, ipady=4, pady=5)
delete_btn = Button(third_frame, text="Удалить точки", command=delete_points, font='Times 13', width= 15)
delete_btn.pack(side = LEFT, ipadx=6, padx=4, ipady=4, pady=5)
class_btn = Button(first_frame, text = "Кластеризация",  font='Times 13', command=clustering, width= 50)
class_btn.pack(side = TOP, ipadx=6, padx=4, ipady=4, pady=5)

canvas1.get_tk_widget().pack(side=TOP, ipadx=6, padx=4, ipady=4, pady=5)










canvas1.draw()
window.mainloop();
