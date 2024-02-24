import asyncio
import csv
import datetime
import math
import tkinter as tk
from tkinter import filedialog
from async_tkinter_loop import async_handler, async_mainloop
from tkinter import IntVar, StringVar, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure

# from matplotlib.backends.backend_pdf import PdfPages


def select(mode):

    val1, val2, val3 = checkboxValue1.get(), checkboxValue2.get(), checkboxValue3.get()
    if val1 == val2 == val3 == 0:
        if mode == 1:
            buttonActivator()
        return 12
    elif (val1 == val2) and (val1 == 1) and val3 == 0:
        checkboxValue3.set(1)
        checkboxValue1.set(0)
        checkboxValue2.set(0)
        if mode == 1:
            buttonActivator()
        return 2
    elif val3 == 1 and ((val1 == 1 and val2 == 0) or (val1 == 0 and val2 == 1)):
        checkboxValue3.set(0)
        if val1 == 1:
            checkboxValue1.set(1)
            if mode == 1:
                buttonActivator()
            return 0
        else:
            if mode == 1:
                buttonActivator()
            return 1
    elif val1 == 1:
        if mode == 1:
            buttonActivator()
        return 0
    elif val2 == 1:
        if mode == 1:
            buttonActivator()
        return 1
    elif val3 == 1:
        if mode == 1:
            buttonActivator()
        return 2
    if mode == 1:
        buttonActivator()
    return 12


def focusNext(event):
    event.widget.tk_focusNext().focus()
    return "break"


def focusPrev(event):
    event.widget.tk_focusPrev().focus()
    return "break"


def onEnter(event):
    event.widget.invoke()


def func(x):
    result = None
    try:
        result = (
            ((math.log(1 + math.pi * x)) / x) * (math.e ** (-x)),
            "((math.log(1 + math.pi * x))/x)*(math.e**(-x))",
        )
    except:
        result = (
            None,
            "((math.log(1 + math.pi * x))/x)*(math.e**(-x))",
        )
    return result


def sortByColumn(tree, col, descending):
    data = [(tree.set(child, col), child) for child in tree.get_children("")]
    data = sorted(data, key=lambda x: float(x[0]), reverse=descending)
    for index, (val, child) in enumerate(data):
        tree.move(child, "", index)
    tree.heading(col, command=lambda: sortByColumn(tree, col, not descending))
    if descending:
        arrow = " ▼"
    else:
        arrow = " ▲"
    tree.heading(col, text=col + arrow)


def generateChart(points):
    fig = Figure(figsize=(5, 4), dpi=100)
    fig.set_facecolor(MAINCOLOR)
    ax = fig.add_subplot(111)
    ax.set_facecolor(SECONDARYCOLOR)

    dX = []
    dY = []
    isFuncExist = False
    maxY, maxX = 0, 0
    minY, minX = float("inf"), 0
    for j, point in enumerate(points):
        dX.append(point[0])
        dY.append(point[1])
        if point[1] != None:
            if point[1] > maxY:
                maxY = point[1]
                maxX = point[0]
            if point[1] < minY:
                minY = point[1]
                minX = point[0]
        isFuncExist = True
    if isFuncExist:
        ax.plot(dX, dY, label=points[0][2])
        ax.scatter(maxX, maxY, color="Red", s=50, marker="o")
        ax.scatter(minX, minY, color="Green", s=50, marker="o")

    ax.grid(True, color=TEXTCOLOR, linewidth=1.0)
    ax.legend(fontsize=12, loc="upper right")
    ax.tick_params(axis="x", colors=TEXTCOLOR)
    ax.tick_params(axis="y", colors=TEXTCOLOR)
    return (fig, ax)


def getTableData(table) -> list:
    data = []
    for row in table.get_children():
        item = table.item(row)
        data.append([item["values"]])
    return data


def save_to_file(data, filename):
    file = open(filename, "a+")
    writer = csv.writer(file)
    writer.writerows(data)
    file.close()


def saveTable(tree):
    table_data = getTableData(tree)
    folder = filedialog.askdirectory()
    save_to_file(
        table_data,
        folder
        + f"output{datetime.datetime.now()}".replace(":", "-")
        .replace(".", "-")
        .replace(" ", "-")
        + ".csv",
    )


def openWindow(mode, points):
    newWindow = tk.Toplevel(
        root,
    )
    chart = generateChart(points)
    if mode == 0:
        newWindow.title("График")

        canvas = FigureCanvasTkAgg(
            chart[0],
            master=newWindow,
        )
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, newWindow)
        toolbar.update()

    else:
        newWindow.title("Таблица")
        tree = ttk.Treeview(
            master=newWindow, columns=["X", "Y", "func"], show="headings"
        )

        tree.pack(fill=tk.BOTH, expand=1)
        tree.heading("X", text="X", command=lambda: sortByColumn(tree, "X", False))
        tree.heading("Y", text="Y", command=lambda: sortByColumn(tree, "Y", False))
        tree.heading("func", text="Функция")

        for point in points:
            tree.insert("", tk.END, values=point)
        if mode == 2:
            saveTable(tree=tree)
            newWindow.destroy()


async def activateTabula():
    for window in root.winfo_children():
        if window.winfo_name().startswith("!toplevel"):
            for child in window.winfo_children():
                child.destroy()
            window.destroy()
    chartVisibleMode = select(0)
    points = []
    div = []
    for entry in inputForm.winfo_children():
        if type(entry) == type(tk.Entry()):
            div.append(float(entry.get()))
    if (div[0] == div[1]) and (div[0] + div[1] > 0):
        while div[0] <= div[1]:
            points.append((div[0], *func(div[0])))
            div[0] += div[2]
    elif div[0] < div[1]:
        while div[0] <= div[1]:
            points.append((div[0], *func(div[0])))
            div[0] += div[2]
    else:
        while div[0] >= div[1]:
            points.append((div[0], *func(div[0])))
            div[0] += div[2]

    match chartVisibleMode:
        case 0:
            openWindow(mode=0, points=points)
        case 1:
            folder = filedialog.askdirectory()
            date = str(datetime.datetime.now()).replace(":", "-").replace(".", "-")
            generateChart(points)[0].savefig(f"{folder}/{date}")
        case 2:
            openWindow(mode=0, points=points)
            folder = filedialog.askdirectory()
            date = str(datetime.datetime.now()).replace(":", "-").replace(".", "-")
            generateChart(points)[0].savefig(f"{folder}/{date}")

    switch = tableMode.get()
    match switch:
        case 0:
            openWindow(mode=1, points=points)
        case 1:
            openWindow(mode=2, points=points)
        case 2:
            openWindow(mode=1, points=points)


def validation(event, mode):
    entryWidget = event.widget
    newValue = entryWidget.get()
    if newValue == "":
        entryWidget.config(bg=SECONDARYCOLOR)
    elif newValue[0] == "-" and mode == 0:
        entryWidget.config(bg="yellow3")
    elif newValue == "-" and mode == 1:
        entryWidget.config(bg=SECONDARYCOLOR)
    else:
        try:
            b = float(newValue)
            entryWidget.config(bg=VERIFIEDVALUECOLOR)
            if b == 0:
                entryWidget.config(bg="yellow3")
        except ValueError:
            entryWidget.config(bg=VALUEERRORCOLOR)
    buttonActivator()


def buttonActivator():
    isNum = True
    isRightSegment = True
    entrys = []
    for widget in inputForm.winfo_children():
        if widget.winfo_name().startswith("!entry"):
            entrys.append(widget)
    entry1, entry2, entry3 = entrys
    for num in [entry1.get(), entry2.get(), entry3.get()]:
        try:
            float(num)
        except:
            isNum = False
    try:
        floatEntry1, floatEntry2, floatEntry3 = (
            float(entry1.get()),
            float(entry2.get()),
            float(entry3.get()),
        )
        flager = False
        flagger1 = False

        for x in [floatEntry1, floatEntry2]:
            if x == 0:
                flager = True
            if str(x)[0] == "-":
                flagger1 = True

        if flager:
            err.set(f"В данной функции невозможно идти от/до 0\n а так же с шагом 0")
        elif flagger1:
            err.set(f"Данная функция не существует в отрицаетльном диапазоне")
        elif abs(floatEntry1 - floatEntry2) < abs(floatEntry3):
            err.set(
                f"Данный промежуток с таким шагом не может быть протабулирован!\nШаг слишком велик"
            )
            entry3.config(bg=VALUEERRORCOLOR)
            isRightSegment = False
        elif floatEntry1 <= floatEntry2 and floatEntry3 > 0:
            isRightSegment = True
            err.set("")
        elif floatEntry1 >= floatEntry2 and floatEntry3 < 0:
            isRightSegment = True
            err.set("")
        elif floatEntry3 == 0:
            isRightSegment = False
            err.set(
                f"Данный промежуток с таким шагом не может быть протабулирован!\nШаг Равен Нулю!"
            )
        else:
            isRightSegment = False
            err.set(
                f"Данный промежуток с таким шагом не может быть протабулирован!\nПроверьте знаки у промежутка и шага!"
            )
            entry3.config(bg=VALUEERRORCOLOR)

    except:
        err.set("Не во всех формах введены числа!")
    isRightSelect = False
    if select(0) != 12:
        errSelect.set("")
        isRightSelect = True
    else:
        errSelect.set("Не выбран режим отображения!")
    if isNum and isRightSegment and isRightSelect and (not (flager) and not (flagger1)):
        buttonTabula.config(state="normal")
    else:
        buttonTabula.config(state="disabled")


async def openPopup(message):
    await activateTabula()
    width = root.winfo_width()
    height = root.winfo_height()
    popupFrame = tk.Frame(master=root, width=width, height=30, bg=VERIFIEDVALUECOLOR)
    popupFrame.place(x=0, y=0)
    popupFrame.pack_propagate(False)
    label1 = tk.Label(
        master=popupFrame,
        text=message,
        font=("consolas", 14),
        bg=VERIFIEDVALUECOLOR,
        fg=TEXTCOLOR,
    )
    label1.pack(expand=True)

    popupFrame.update()
    for y in range(0, popupFrame.winfo_height(), 1):
        popupFrame.place(
            y=height - y,
        )
        popupFrame.update()
        await asyncio.sleep(0.005)
    await asyncio.sleep(2)
    for y in range(1, popupFrame.winfo_height(), 1):
        popupFrame.place(
            y=popupFrame.winfo_y() + y,
        )
        popupFrame.update()
        await asyncio.sleep(0.05)


async def doPopups():
    """Creating and starting n... tasks."""
    tasks = [
        asyncio.create_task(openPopup("Функция протабулирована!")),
    ]
    await asyncio.wait(tasks)


MAINCOLOR = "#282828"

SECONDARYCOLOR = "#646464"
ACTIONCOLOR = "#4A4A4A"
TEXTCOLOR = "#D3D3D3"
VALUEERRORCOLOR = "#8B0000"
VERIFIEDVALUECOLOR = "#006400"
BACKGROUNDCOLOR = "#232323"


root = tk.Tk()

root.geometry("800x450")
root.minsize(width=800, height=450)
# root.resizable(False, False)
root.title("Лабораторная работа №4")
root.bind("<Down>", focusNext)
root.config(bg=BACKGROUNDCOLOR)
root.update()

for c in range(3):
    root.columnconfigure(index=c, weight=root.winfo_width() // 3)
for r in range(6):
    root.rowconfigure(index=r, weight=root.winfo_height() // 6)


inputForm = tk.Frame(master=root, bg=MAINCOLOR)
inputForm.grid(
    row=0, column=0, columnspan=3, rowspan=1, sticky="nsew", padx=16, pady=16
)

inputForm.update()

canvasImg = tk.Canvas(
    inputForm, height=100, bg=MAINCOLOR, bd=0, highlightthickness=0, relief="ridge"
)
exePath = "_internal/func.png"
debugPath = "Labarotory/TabulateApp/func.png"
img = tk.PhotoImage(file=debugPath)
image = canvasImg.create_image(inputForm.winfo_width() // 2 - 200, 75, image=img)
canvasImg.grid(row=0, column=0, columnspan=3, sticky="s")

for c in range(3):
    inputForm.columnconfigure(index=c, weight=inputForm.winfo_width() // 3)

for r in range(6):
    inputForm.rowconfigure(index=r, weight=inputForm.winfo_height() // 6)

inputLabel = tk.Label(
    master=inputForm,
    text="Форма ввода промежутка",
    fg=TEXTCOLOR,
    font=("consolas", 16, "bold"),
    bg=MAINCOLOR,
)
inputForm.update()
inputLabel.grid(row=0, column=0, columnspan=3, padx=16, pady=8, sticky="n")
labelText = ["начальное значениe", "конечное значение", "шаг"]
for l in range(1, 4):
    label = tk.Label(
        master=inputForm,
        font=("consolas", 12),
        text=f"Введите {labelText[l-1]}:",
        fg=TEXTCOLOR,
        bg=MAINCOLOR,
    )
    label.grid(
        row=l + 2,
        column=0,
        columnspan=3,
        sticky="sw",
        padx=16,
    )
    entry = tk.Entry(
        master=inputForm,
        font=("consolas", 12),
        bg=SECONDARYCOLOR,
        fg=TEXTCOLOR,
        insertbackground=TEXTCOLOR,
    )
    entry.grid(row=l + 2, column=1, columnspan=3, sticky="nsew", padx=16)

    entry.bind("<KeyRelease>", lambda event: validation(event, (1 if l == 3 else 0)))
    entry.bind("<Down>", focusNext)
    entry.bind("<Up>", focusPrev)
    entry.bind("<Return>", focusNext)

err = StringVar(value="")
errMessage = tk.Label(
    inputForm,
    textvariable=err,
    foreground="red",
    background=MAINCOLOR,
    font=("consolas", 12),
)
errMessage.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=8)
# stub = tk.Label(
#     master=inputForm,
#     font=("consolas", 12),
#     bg=MAINCOLOR,
# )
# stub.grid(row=9, column=0, sticky="s")

selectorForm = tk.Frame(master=root, bg=MAINCOLOR)
selectorForm.grid(row=1, column=0, columnspan=3, rowspan=1, sticky="nsew", padx=16)
selectorForm.update()


for c in range(5):
    selectorForm.columnconfigure(index=c, weight=selectorForm.winfo_width() // 5)

for r in range(3):
    selectorForm.rowconfigure(index=r, weight=selectorForm.winfo_height() // 8)

selectorLabel = tk.Label(
    master=selectorForm,
    text="Параметры отображения",
    fg=TEXTCOLOR,
    font=("consolas", 16, "bold"),
    bg=MAINCOLOR,
)

selectorLabel.grid(row=0, column=0, columnspan=5, padx=16, pady=0, sticky="n")

for i in range(2):
    label = tk.Label(
        master=selectorForm,
        font=("consolas", 12),
        text=["График", "Таблица"][i],
        fg=TEXTCOLOR,
        bg=MAINCOLOR,
    )
    label.grid(row=1 + i, column=0, sticky="nw", padx=16)


checkboxValue1 = IntVar()
checkbox1 = tk.Checkbutton(
    master=selectorForm,
    variable=checkboxValue1,
    bg=MAINCOLOR,
    activeforeground=TEXTCOLOR,
    activebackground=SECONDARYCOLOR,
    fg=TEXTCOLOR,
    text="Окно",
    font=(
        "consolas",
        10,
    ),
    command=lambda: select(1),
    selectcolor=MAINCOLOR,
)
checkbox1.grid(row=1, column=2 + 0, padx=16, sticky="n")
checkbox1.bind("<Left>", focusPrev)
checkbox1.bind("<Right>", focusNext)
checkbox1.bind("<Up>", focusPrev)
checkboxValue2 = IntVar()
checkbox2 = tk.Checkbutton(
    master=selectorForm,
    variable=checkboxValue2,
    bg=MAINCOLOR,
    activeforeground=TEXTCOLOR,
    activebackground=SECONDARYCOLOR,
    fg=TEXTCOLOR,
    text="Сохранить",
    font=(
        "consolas",
        10,
    ),
    command=lambda: select(1),
    selectcolor=MAINCOLOR,
)
checkbox2.grid(row=1, column=2 + 1, padx=16, sticky="n")
checkbox2.bind("<Left>", focusPrev)
checkbox2.bind("<Right>", focusNext)
checkboxValue3 = IntVar()
checkbox3 = tk.Checkbutton(
    master=selectorForm,
    variable=checkboxValue3,
    bg=MAINCOLOR,
    activeforeground=TEXTCOLOR,
    activebackground=SECONDARYCOLOR,
    fg=TEXTCOLOR,
    text="Всё",
    font=(
        "consolas",
        10,
    ),
    command=lambda: select(1),
    selectcolor=MAINCOLOR,
)
checkbox3.grid(row=1, column=2 + 2, padx=16, sticky="n")
checkbox3.bind("<Left>", focusPrev)
checkbox3.bind("<Right>", focusNext)

modeValue = [0, 1, 2]

tableMode = IntVar(value=modeValue[0])
radioButton1 = tk.Radiobutton(
    master=selectorForm,
    variable=tableMode,
    value=modeValue[0],
    bg=MAINCOLOR,
    activeforeground=TEXTCOLOR,
    activebackground=SECONDARYCOLOR,
    fg=TEXTCOLOR,
    text="Окно",
    font=(
        "consolas",
        10,
    ),
    selectcolor=MAINCOLOR,
)
radioButton1.grid(row=2, column=2 + 0, padx=16, sticky="n")
radioButton1.bind("<Right>", focusNext)
radioButton1.bind("<Up>", focusPrev)
radioButton1.bind("<Left>", focusPrev)
radioButton2 = tk.Radiobutton(
    master=selectorForm,
    variable=tableMode,
    value=modeValue[1],
    bg=MAINCOLOR,
    activeforeground=TEXTCOLOR,
    activebackground=SECONDARYCOLOR,
    fg=TEXTCOLOR,
    text="Сохранить",
    font=(
        "consolas",
        10,
    ),
    selectcolor=MAINCOLOR,
)
radioButton2.grid(row=2, column=2 + 1, padx=16, sticky="n")
radioButton2.bind("<Left>", focusPrev)
radioButton2.bind("<Right>", focusNext)
radioButton3 = tk.Radiobutton(
    master=selectorForm,
    variable=tableMode,
    value=modeValue[2],
    bg=MAINCOLOR,
    activeforeground=TEXTCOLOR,
    activebackground=SECONDARYCOLOR,
    fg=TEXTCOLOR,
    text="Всё",
    selectcolor=MAINCOLOR,
    font=(
        "consolas",
        10,
    ),
)
buttonTabula = tk.Button(
    master=root,
    state="disabled",
    text="Протабулировать",
    fg="white",
    bg=ACTIONCOLOR,
    command=async_handler(doPopups),
)
radioButton3.grid(row=2, column=2 + 2, padx=16, sticky="n")
radioButton3.bind("<Left>", focusPrev)
radioButton3.bind("<Right>", buttonTabula.focus())
radioButton3.bind("<Down>", buttonTabula.focus())
radioButton3.bind("<Up>", focusPrev)
errSelect = StringVar(value="")
errMessageSelect = tk.Label(
    selectorForm,
    textvariable=errSelect,
    foreground="red",
    background=MAINCOLOR,
    font=("consolas", 12),
)
errMessageSelect.grid(
    row=3,
    column=0,
    columnspan=5,
)


buttonTabula.bind("<Down>", focusNext)
buttonTabula.bind("<Up>", focusPrev)
buttonTabula.bind("<Return>", onEnter)
buttonTabula.grid(row=3, column=1, sticky="")

buildLabel = tk.Label(
    root,
    text="Build: 100+ reworks by Stepan Bodnar",
    foreground=TEXTCOLOR,
    background=BACKGROUNDCOLOR,
    font=("consolas", 9),
)
buildLabel.grid(row=4, column=1, sticky="")

async_mainloop(root)
