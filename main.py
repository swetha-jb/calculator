"""
File: calculator.py
Author: Brooke Mattos
Date: December 16, 2022 
Description: 
    Modern, aesthetic ui with multiple page tkinkter gui implementation.
    Emulates a calculator, calculating user inputted, complex algebraic and calculus computations.
    Complex word problem solution capabilities with utilization of ChatGPT API.
"""

import customtkinter as ctk
from calculator import calculate
from vector import vector_calc
from graph import graph
from solver_ai import generate


# Setup window
root = ctk.CTk()
root.geometry('1010x653')
root.title('VectorCalc')
ctk.set_appearance_mode('dark')  # always dark background

# Title
main_title = ctk.CTkLabel(root, text='CalCulator', font = ctk.CTkFont(size=30, weight='bold'))
main_title.pack(padx=(180, 10), pady=(20, 20))


# Menu frame
menu = ctk.CTkFrame(root, fg_color='#3f3f3f', width=150, height=600)
menu.pack(side='left', padx=(20, 0), pady=(0, 40))
menu.pack_propagate(False)
menu_title = ctk.CTkLabel(menu, text='Menu', font = ctk.CTkFont(size=15, weight='bold'))
menu_title.pack(pady=(15, 0))
menu_frame = ctk.CTkFrame(menu, fg_color='#545454')
menu_frame.pack(fill='x', padx=(15, 15), pady=(15, 15))

# Menu buttons
calc_menu = ctk.CTkButton(menu_frame, height=50, width=100, text='Calculator', fg_color='#253da1',
                    command= lambda: indicate(calc_menu, calc_page))
vector_menu = ctk.CTkButton(menu_frame, height=50, width=100, text='Functions', fg_color='#253da1',
                    command= lambda: indicate(vector_menu, vector_page))
graph_menu = ctk.CTkButton(menu_frame, height=50, width=100, text='Graphs', fg_color='#253da1', 
                    command= lambda: indicate(graph_menu, graphs_page))
wp_menu = ctk.CTkButton(menu_frame, height=50, width=100, text='Solve AI', fg_color='#253da1', 
                    command= lambda: indicate(wp_menu, wp_page))
calc_menu.pack(padx=15, pady=(30, 15))
vector_menu.pack(padx=15, pady=(50, 15))
graph_menu.pack(padx=15, pady=(50, 15))
wp_menu.pack(padx=15, pady=(50, 30))

# Main frame
main_frame = ctk.CTkFrame(root, fg_color='#3f3f3f')
main_frame.pack(fill='x', padx=20)


def calc_page():
    """
    Creates calculator page (p.1) using customtkinter as well as implements 
    calculation functions
    """

    # Calculator buttons
    top_frame = ctk.CTkFrame(main_frame, fg_color='#3f3f3f')
    top_frame.pack(fill='x', padx=20)
    b1_frame = ctk.CTkFrame(top_frame, fg_color='#545454')
    b1_frame.pack(fill='x', padx=(15, 15), pady=(15, 10))
    b2_frame = ctk.CTkFrame(top_frame, fg_color='#545454')
    b2_frame.pack(fill='x', padx=(15, 15), pady=(0, 15))

    def click_button(value):
        """
        Command called by any button press

        :param value: string representing button that was pressed
        :return: None
        """

        # Clear all entryboxes if clear pressed
        if value == 'clear':
            entrybox.delete(0, ctk.END)
            wrt.delete(0, ctk.END)
            lim.delete(0, ctk.END)
            integral_l.delete(0, ctk.END)
            integral_r.delete(0, ctk.END)
            sum_i.delete(0, ctk.END)
            sum_n.delete(0, ctk.END)
        
        # Calculate expression and replace entrybox with answer
        elif value == 'calculate':
            expr = str(entrybox.get())

            # Get conditions array
            condi = [wrt.get(), lim.get(), integral_l.get(),
                          integral_r.get(), sum_i.get(), sum_n.get()]
            result = calculate(expr, condi)
            entrybox.delete(0, ctk.END)

            if str(result) == None:
                # Catch any errors with result
                entrybox.insert(0, 'ERROR')
            else:
                entrybox.insert(0, str(result))
        else:
            # Add to entrybox if var buttons clicked
            entrybox.insert(ctk.END, value) 
        
    def calc_buttons(gui, inText, cmd):
        """
        General format for calculator button 
        setup, all buttons have same sizing

        :param gui: frame to be packed in
        :param inText: button function in text format
        :param cmd: result of button click
        :return: button
        """

        return ctk.CTkButton(gui, height=50, width=50, text=inText, command=cmd)

    # Variable buttons row 1
    derivate = calc_buttons(b1_frame, 'd/dx', lambda: click_button('d/dx['))  # conditional: wrt
    integral = calc_buttons(b1_frame, '∫', lambda: click_button('∫['))  # conditional: top, bottom
    limit = calc_buttons(b1_frame, 'lim', lambda: click_button('lim['))  # conditional: -> ?
    sqrt = calc_buttons(b1_frame, 'sqrt', lambda: click_button('sqrt('))
    pi = calc_buttons(b1_frame, 'π', lambda: click_button('π'))
    exp = calc_buttons(b1_frame, 'e', lambda: click_button('e'))
    ln = calc_buttons(b1_frame, 'ln', lambda: click_button('ln('))
    log = calc_buttons(b1_frame, 'log', lambda: click_button('log('))
    partial = calc_buttons(b1_frame, '∂/∂x', lambda: click_button('∂/∂x['))  # conditional: wrt

    derivate.pack(padx=(20,10), pady=10, side='left')
    integral.pack(padx=(20,10), pady=10, side='left')
    limit.pack(padx=(20,10), pady=10, side='left')
    sqrt.pack(padx=(20,10), pady=10, side='left')
    pi.pack(padx=(20,10), pady=10, side='left')
    exp.pack(padx=(20,10), pady=10, side='left')
    ln.pack(padx=(20,10), pady=10, side='left')
    log.pack(padx=(20,10), pady=10, side='left')
    partial.pack(padx=(20,10), pady=10, side='left')

    # Variable buttons row 2
    sigma = calc_buttons(b2_frame, 'Σ', lambda: click_button('Σ['))  # condtional: n, i=?
    pow = calc_buttons(b2_frame, '^', lambda: click_button('^'))
    inverse = calc_buttons(b2_frame, 'arc', lambda: click_button('arc'))
    sin = calc_buttons(b2_frame, 'sin', lambda: click_button('sin('))
    cos = calc_buttons(b2_frame, 'cos', lambda: click_button('cos('))
    tan = calc_buttons(b2_frame, 'tan', lambda: click_button('tan('))
    sec = calc_buttons(b2_frame, 'sec', lambda: click_button('sec('))
    csc = calc_buttons(b2_frame, 'csc', lambda: click_button('csc('))
    cot = calc_buttons(b2_frame, 'cot', lambda: click_button('cot('))

    sigma.pack(padx=(20,10), pady=10, side='left')
    pow.pack(padx=(20,10), pady=10, side='left')
    inverse .pack(padx=(20,10), pady=10, side='left')
    sin.pack(padx=(20,10), pady=10, side='left')
    cos.pack(padx=(20,10), pady=10, side='left')
    tan.pack(padx=(20,10), pady=10, side='left')
    sec.pack(padx=(20,10), pady=10, side='left')
    csc.pack(padx=(20,10), pady=10, side='left')
    cot.pack(padx=(20,10), pady=10, side='left')


    # Conditional select
    mid_frame = ctk.CTkFrame(main_frame, border_width=5)
    mid_frame.pack(padx=140, pady=(20,5), fill='both')
    vars_title = ctk.CTkLabel(mid_frame, text='Conditions:', font=ctk.CTkFont(weight='bold'))
    vars_title.pack(pady=(5, 10))

    # wrt conditional entryboxes
    wrt_lbl = ctk.CTkLabel(mid_frame, text='wrt:')
    wrt = ctk.CTkEntry(mid_frame, width=20, height=25)  # wrt = _
    wrt_lbl.pack(side='left', padx=(30, 10), pady=(0, 15))
    wrt.pack(side='left', pady=(0, 15))

    # lim conditional entryboxes
    lim_lbl = ctk.CTkLabel(mid_frame, text='lim ->')
    lim = ctk.CTkEntry(mid_frame, width=40, height=25)  # -> = _
    lim_lbl.pack(side='left', padx=(20, 10), pady=(0, 15))
    lim.pack(side='left', pady=(0, 15))

    # integral conditional entryboxes
    integral_lbl = ctk.CTkLabel(mid_frame, text='∫:')
    integral_l = ctk.CTkEntry(mid_frame, width=40, height=25)  # left bound = _
    integral_r = ctk.CTkEntry(mid_frame, width=40, height=25)  # right bound = _
    integral_lbl.pack(side='left', padx=(20, 10), pady=(0, 15))
    integral_l.pack(side='left', pady=(0, 15))
    integral_r.pack(side='left', pady=(0, 15), padx=(5, 15))

    # sum conditional entryboxes
    sum_lbl = ctk.CTkLabel(mid_frame, text='Σ:')
    sum_lbl_i = ctk.CTkLabel(mid_frame, text='i')
    sum_lbl_n = ctk.CTkLabel(mid_frame, text='n')
    sum_i = ctk.CTkEntry(mid_frame, width=40, height=25)  # i = _
    sum_n = ctk.CTkEntry(mid_frame, width=40, height=25)  # n = _
    sum_lbl.pack(side='left', padx=(0, 10), pady=(0, 15))
    sum_lbl_i.pack(side='left', padx=(0, 10), pady=(0, 15))
    sum_i.pack(side='left', pady=(0, 15))
    sum_lbl_n.pack(side='left', padx=10, pady=(0, 15))
    sum_n.pack(side='left', pady=(0, 15), padx=(0, 15))

    # EntryBox
    entrybox = ctk.CTkEntry(main_frame, width=700, height=100, font=ctk.CTkFont(size=30))
    entrybox.pack(pady=(30, 15))

    # Calculate / clear buttons
    calc_btn = ctk.CTkButton(main_frame, text='calculate', command = lambda: click_button('calculate'))
    clear_btn = ctk.CTkButton(main_frame, text='clear', fg_color='#ff4f4b', command = lambda: click_button('clear'))
    calc_btn.pack(padx=150, fill='x', pady=(5, 20))
    clear_btn.pack(pady=(0, 20))


# Initialize entryboxes for vector_page to be accessed in build()
a_entry, b_entry, result_entry = None, None, None

def vector_page():
    """Creates vector function page (p.2) using customtkinter and handles input"""

    # Choose operation menu drop-down
    fnction_lst = ['[select]', 'vector addition', 'dot product', 'cross product', 'projection', 
                   'determinant', 'norm of vector', 'arc length', 'derivative']
    vector_title = ctk.CTkLabel(main_frame, text='Vector Calculator', 
                                font = ctk.CTkFont(weight='bold', size=40))
    drop_frame = ctk.CTkFrame(main_frame, border_width=5, width=100, height=50, fg_color='#545454')
    drop_title = ctk.CTkLabel(drop_frame, text='Choose Operation:', 
                              font=ctk.CTkFont(weight='bold', size=15))
    vector_drop = ctk.CTkComboBox(drop_frame, values=fnction_lst, width=200)  # Drop down select
    func_frame = ctk.CTkFrame(main_frame, border_width=5, height=240)
    reset_btn = ctk.CTkButton(drop_frame, text='reset', width=40, fg_color='#36454f', 
                              font=ctk.CTkFont(size=10, weight='bold'), command = lambda: reset())
    choose_btn = ctk.CTkButton(drop_frame, text='☑', width=40, command = lambda: select())  # Choose from drop down
    calc_btn = ctk.CTkButton(main_frame, text='calculate', width=400,
                             command = lambda: calc(vector_drop.get()))  # Calculate (based on drop down)
    clear_btn = ctk.CTkButton(main_frame, text='clear', fg_color='#ff4f4b', width=100, 
                              command = lambda: clear())

    vector_title.pack(fill='x', padx=20, pady=(30, 0))
    drop_frame.pack(fill='x', padx=200, pady=20)
    drop_title.pack(pady=(20, 5))
    reset_btn.pack(padx=(40, 0), pady=(0, 30), side='left')
    vector_drop.pack(pady=(0, 30), padx=(20, 20), side='left')
    choose_btn.pack(padx=(0, 20), pady=(0, 30), side='left')
    func_frame.pack(fill='x', padx=50, pady=(0, 20))
    calc_btn.pack(fill='x', padx=(140, 0), pady=(0, 20), side='left')
    clear_btn.pack(padx=(10, 30), pady=(0, 20), side='left')

    # Initialize frames housing input data for different functions
    vec_frame = ctk.CTkFrame(func_frame)

    def select():
        """Pack initialized frames and build function"""

        # Only when functions are selected in drop-down
        if vector_drop.get() != '[select]':
            vec_frame.pack(padx=(10, 10), pady=10, fill='x', side='left')  # Pack frames
            build(vector_drop.get())  # Call build

    def reset():
        """Resets entire page for new select"""

        delete_frames(main_frame)
        vector_page()  # Rebuild to base page

    def clear():
        """Clear all input fields in vec_frame (housing user text input)"""

        # Only when functions are selected in drop-down
        if vector_drop.get() != '[select]':
            delete_frames(vec_frame)
            build(vector_drop.get())  # Doesn't rebuild the select frame

    def calc(func_selected):
        """
        Call imported vector_calc function and 
        insert calculation into result_entry

        :param: func_selected: string of function type
        """

        # Clear entry to prep for new entry insertion
        result_entry.delete(0, ctk.END)
        
        # Insert vector_calc calculation depending on current selected function
        if func_selected == 'vector addition':
            result_entry.insert(0, str(vector_calc('add', a_entry.get(), b_entry.get())))
        elif func_selected == 'dot product':
            result_entry.insert(0, str(vector_calc('dot', a_entry.get(), b_entry.get())))
        elif func_selected == 'cross product':
            result_entry.insert(0, str(vector_calc('cross', a_entry.get(), b_entry.get())))
        elif func_selected == 'determinant':
            result_entry.insert(0, str(vector_calc('det', a_entry.get())))
        elif func_selected == 'norm of vector':
            result_entry.insert(0, str(vector_calc('norm', a_entry.get())))
        elif func_selected == 'arc length':
            result_entry.insert(0, str(vector_calc('length', a_entry.get())))
        elif func_selected == 'derivative':
            result_entry.insert(0, str(vector_calc('deriv', a_entry.get())))

    def build(drop_type):
        """
        Build interior function frames based on function selection

        :param drop_type: string of operation name from fnction_lst
        """

        # Globalize pre-initialized entryboxes to be accessed outside of following if statements
        global a_entry, b_entry, result_entry


        # Hashmap of all function labels
        lbls = {'vector addition': 'a + b  = ', 
                'dot product': 'a * b  = ', 
                'cross product': 'a x b  = ', 
                'projection': 'proj  = ',
                'determinant': 'det  =',
                'norm of vector': '||a||  =',
                'arc length': 'L  =',
                'derivative': 'deriv  ='}
        
        # Frame / page structure for vector addition, dot product, cross product, and projection function selections
        if drop_type == 'vector addition' or drop_type == 'dot product' or \
            drop_type =='cross product' or drop_type == 'projection':
            
            seper_1 = ctk.CTkFrame(vec_frame, width=450, height=50)
            seper_2 = ctk.CTkFrame(vec_frame, width=450, height=50)
            result_entry = ctk.CTkEntry(vec_frame, width=520, height=40, border_width=3, font = ctk.CTkFont(size=20),
                                  fg_color='#222222', text_color='white')
            result_lbl = ctk.CTkLabel(vec_frame, text=lbls[drop_type], font = ctk.CTkFont(weight='bold', size=18))
            vec_a = ctk.CTkLabel(seper_1, text='a  =')
            vec_b = ctk.CTkLabel(seper_2, text='b  =')
            a_entry = ctk.CTkEntry(seper_1, width=200, height=30)
            b_entry = ctk.CTkEntry(seper_2, width=200, height=30)
            seper_1.pack(padx=120, pady=20)
            seper_2.pack(padx=120, pady=(0, 20))
            result_lbl.pack(padx=(40, 10), pady=(0, 17), side='left')
            result_entry.pack(padx=(0, 60), pady=(0, 20))
            vec_a.pack(padx=(20, 10), pady=10, side='left')
            a_entry.pack(side='left', padx=(0, 20))
            vec_b.pack(padx=(20, 10), pady=10, side='left')
            b_entry.pack(padx=(0, 20), pady=10, side='left')
        
        # Frame / page structure for determinant, norm of vector, arc length, and derivative function selections
        elif drop_type == 'determinant' or drop_type == 'norm of vector' or \
            drop_type == 'arc length' or drop_type == 'derivative':

            seper = ctk.CTkFrame(vec_frame, width=450, height=50)
            result_entry = ctk.CTkEntry(vec_frame, width=520, height=40, border_width=3, font = ctk.CTkFont(size=20),
                                  fg_color='#222222', text_color='white')
            result_lbl = ctk.CTkLabel(vec_frame, text=lbls[drop_type], font = ctk.CTkFont(weight='bold', size=18))
            vec_lbl = ctk.CTkLabel(seper, text='v  =')
            a_entry = ctk.CTkEntry(seper, width=200, height=30)
            seper.pack(padx=120, pady=(70, 40))
            result_lbl.pack(padx=(40, 10), pady=(0, 17), side='left')
            result_entry.pack(padx=(0, 60), pady=(0, 20))
            vec_lbl.pack(padx=(20, 10), pady=10, side='left')
            a_entry.pack(padx=(0, 20), side='left')


def graphs_page():
    """
    Creates graph page (p.3) using customtkinter 
    to represent graphs from user input functions
    """

    # f(x) entrybox
    graph_title = ctk.CTkLabel(main_frame, text='function:', 
                               font = ctk.CTkFont(size=20, weight='bold'))
    func_frame = ctk.CTkFrame(main_frame, height=50, fg_color='#545454', 
                              border_width=3, border_color='#aaaaaa')
    f_enter = ctk.CTkButton(func_frame, text='☑', width=40, 
                            command = lambda: draw(f_entry.get()))
    f_title = ctk.CTkLabel(func_frame, text='f ( x )  =', 
                           font = ctk.CTkFont(size=15, slant='italic'))
    f_entry = ctk.CTkEntry(func_frame)
    graph_title.pack(fill='x', padx=20, pady=(200, 15))
    func_frame.pack(fill='x', padx=100, pady=(0, 235))
    f_enter.pack(padx=(20, 0), pady=15, side='left')
    f_title.pack(padx=20, pady=15, side='left')
    f_entry.pack(fill='x', padx=(0, 50), pady=15)

    def draw(expr):
        """
        Outputs a graph using user input function upon press 
        of f_enter & clear f_entry after graph displayed

        :param expr: user input function
        """

        f_entry.delete(0, ctk.END)
        graph(expr)


def wp_page():
    """Creates word problem page (p.4) using costumtkinter"""

    def solve():
        """
        Solve input question in problem_text entrybox, 
        inserting answer statement into chat_text entrybox
        """

        chat_text.delete('1.0', 'end-1c')
        problem = problem_text.get('1.0', 'end-1c')
        answer = generate(problem)
        chat_text.insert('1.0', answer)

    # Construct page
    problem_lbl = ctk.CTkLabel(main_frame, text='Enter Problem:', font = ctk.CTkFont(size=15, weight='bold'))
    problem_text = ctk.CTkTextbox(main_frame, border_width=5, width=600, height=110, font = ctk.CTkFont(size=20))
    enter_btn = ctk.CTkButton(main_frame, text='solve', command = lambda: solve())
    problem_lbl.pack(pady=(20, 10))
    problem_text.configure(spacing1=5, spacing2=5)
    problem_text.pack(padx=30)
    problem_text.mark_set('insert', '1.0')
    enter_btn.pack(pady=(10, 10), fill='x', padx=110)

    chat_text = ctk.CTkTextbox(main_frame, border_width=5, width=500, height=245, font = ctk.CTkFont(size=20))
    chat_text.configure(spacing1=5, spacing2=5)
    chat_text.pack(padx=50, pady=(35, 40))
    chat_text.mark_set('insert', '1.0')


# Menu traversal Functions

def reset_indicators():
    """Reset colors and borders for menu buttons"""

    calc_menu.configure(fg_color='#253da1', border_width=0)
    vector_menu.configure(fg_color='#253da1', border_width=0)
    graph_menu.configure(fg_color='#253da1', border_width=0)
    wp_menu.configure(fg_color='#253da1', border_width=0)

def delete_frames(frame):
    """Destroy frame when switching page"""

     # Loops through all frames in main_frame
    for f in frame.winfo_children():
        f.destroy()

def indicate(menu, page):
    """
    Switches pages and updates button color

    :param menu: selected menu button
    :param page: page connected to selected menu button
    """

    reset_indicators()
    menu.configure(fg_color='#624aa1', border_width=3)  # Change selected button to purple
    delete_frames(main_frame)
    page()  # Calls page's function


# Create & run window:
indicate(calc_menu, calc_page)  # Always start on calculator page
root.mainloop()
