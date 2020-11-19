import PySimpleGUI as gui
import re
from NumericStringParser import NumericStringParser

# Layout
# User can see an entry pad containing buttons for the digits 0-9, operations - '+', '-', '/', and '=',
# a 'C' button (for clear), and an 'AC' button (for clear all).
layout = [[gui.Txt('' * 14)],
          [gui.Text('', size=(15, 1), font=('Arial', 24), text_color='Black', key='input')],
          [gui.Txt('' * 14)],
          [gui.ReadFormButton('sqr'), gui.ReadFormButton('log'), gui.ReadFormButton('C'), gui.ReadFormButton('AC')],
          [gui.ReadFormButton('7'), gui.ReadFormButton('8'), gui.ReadFormButton('9'), gui.ReadFormButton('/')],
          [gui.ReadFormButton('4'), gui.ReadFormButton('5'), gui.ReadFormButton('6'), gui.ReadFormButton('*')],
          [gui.ReadFormButton('1'), gui.ReadFormButton('2'), gui.ReadFormButton('3'), gui.ReadFormButton('-')],
          [gui.ReadFormButton('.'), gui.ReadFormButton('0'), gui.ReadFormButton('='), gui.ReadFormButton('+')],
          ]

form = gui.FlexForm('flexForm', default_button_element_size=(9, 3), auto_size_buttons=False, grab_anywhere=False)
form.Layout(layout)

# Stack to keep track of Order of Operations
storedInput = ''

# Instantiate NumericStringParser object
nsp = NumericStringParser()

# Regex used to parse equation string
p_equation = re.compile(r"((-?(?:\d+(?:\.\d+)?))|([-+\/*()])|(-?\.\d+))")

# Loop until the program is closed
while True:
    button, value = form.Read()

    # User can click on an operation button to display the result of that operation on:
    #   the result of the preceding operation and the last number entered OR
    #   the last two numbers entered OR
    #   the last number entered

    # TODO: Bonus
    # User can click a '+/-' button to change the sign of the number that is currently displayed.
    # User can see a decimal point ('.') button on the entry pad to that allows floating point numbers up to 3 places
    # to be entered and operations to be carried out to the maximum number of decimal places entered for any one number.

    print("storedInput = ", storedInput)

    # User can click the 'AC' button to clear all internal work areas and to set the display to 0.
    if button == 'AC':
        storedInput = ''
    # User can click the 'C' button to clear the last number or the last operation. If the users last entry was an
    # operation the display will be updated to the value that preceded it.
    elif button == 'C':
        storedInput = str(storedInput[:-1])
    elif str(button) in '1234567890.':
        storedInput += str(button)
    elif str(button) in '+-':
        storedInput += str(button)
    elif button == '*':
        storedInput += '*'
    elif button == '/':
        storedInput += '/'

    # do the actual calculation based on the Equal Stack.  Can't use Eval
    elif button == '=':
        storedInput = str(nsp.calculate(storedInput))

    elif button == 'Quit' or button is None:  # QUIT Program
        print('quit')
        break

    print(len(storedInput))

    # User can enter numbers as sequences up to 8 digits long by clicking on digits in the entry pad. Entry of any
    # digits more than 8 will be ignored.
    if len(storedInput) > 8:
        pIndex, mIndex, tIndex, dIndex = 0
        pIndex = storedInput.indexOf('+')
        mIndex = storedInput.indexOf('-')
        tIndex = storedInput.indexOf('*')
        dIndex = storedInput.indexOf('/')
        # User can see 'ERR' displayed if any operation would exceed the 8 digit maximum.
        if pIndex > 0 or mIndex > 0 or tIndex > 0 or dIndex > 0:
            if len(storedInput) - max([pIndex, mIndex, tIndex, dIndex]) > 8:
                storedInput = 'ERR'
        else:
            storedInput = 'ERR'

    # User can see a display showing the current number entered or the result of the last operation.
    form.FindElement('input').Update(storedInput)
