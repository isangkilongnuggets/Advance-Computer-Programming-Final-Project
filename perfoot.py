import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter import ttk
import decimal
from ctypes import windll
import mysql.connector

# changes the color of the button when the cursor is hovering    
def button_hover(button, white, green):
    button.bind('<Enter>', lambda e: button.configure(bg = white, fg = green))
    button.bind('<Leave>', lambda e: button.configure(bg = green, fg = white))

# program's default icon and title    
def icon_title(var):
    var.iconbitmap('images/logo.ico')
    var.title('PerFoot: Personal Carbon Footprint Tracker')

# sets the window size and position
def window_size (var, width, height):
    screendime_width = var.winfo_screenwidth()
    screendime_height = var.winfo_screenheight()

    centerp_x = int(screendime_width / 2 - width / 2)
    centerp_y = int(screendime_height / 2 - height / 2)

    return var.geometry(f'{width}x{height}+{centerp_x}+{centerp_y}')

# saves the current user's 'user_id' on 'loggedon_userid' variable
def current_userid(copy_username):
    global loggedon_userid

    pfdbcur.execute('SELECT user_id FROM user WHERE username = %s', (copy_username,))
    user_id = pfdbcur.fetchone()

    loggedon_userid = user_id[0]

# verifies if the username entered already exists in the database and determines if the password matches with username    
def database_user_verification(copy_username, copy_password):
    # checks the 'User' table if the user do or do not exist
    pfdbcur.execute('SELECT user_id, password FROM user WHERE username = %s', (copy_username,))
    userver = pfdbcur.fetchall()

    if not userver:
        return None 

    if len(userver) > 1:
        return None

    stored_password = userver[0][1]  

    if copy_password == stored_password:
        global loggedon_userid
        loggedon_userid = userver[0][0]
        return True
    else:
        return False 
    
# background text for entry
def entry_background_text(entry, placeholder_text, password = False):
    def entering(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')
        
        if password:
            entry.config(show='*')

    def not_entering(event):
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.config(fg='gray')
            
            if password:
                entry.config(show='')

    entry.bind('<FocusIn>', entering)
    entry.bind('<FocusOut>', not_entering)
    
    if entry.get() == '':
        entry.insert(0, placeholder_text)
        entry.config(fg='gray')
        
        if password:
            entry.config(show='')

# checks the database_user_verification if the conbditions desired are met
def verify_entry(username, password, window):
    # log in entry error handling
    if username.get() == 'Username':
        showerror('Error', 'Please fill in the username.', parent = window)
    elif password.get() == 'Password':
        showerror('Error', 'Please fill in the password.', parent = window)
    else:
        user_verification = database_user_verification(username.get(), password.get())

        if user_verification == True:
            # if all of the condition are true it prompts the main dashboard of the program
            show_dashboard()        
            window.destroy()
            
        elif user_verification == False:
            showerror('Error', 'The password you\'ve entered is wrong.', parent = window)
            
        elif user_verification == None:
            showerror('Error', 'The entered username does not exist.', parent = window)

# user log in window
def login_window():
    login_win = tk.Toplevel(main)
    window_size(login_win, 300, 300)
    login_win.resizable(False, False)
    login_win.iconbitmap('images/alt_logo.ico')
    login_win.title('Log In')
    login_win.grab_set()
    login_win.focus()
    
    def reset_login_entry():
        login_username_entry.delete(0, tk.END)
        login_password_entry.delete(0,tk.END)
        
        entry_background_text(login_username_entry, 'Username')
        entry_background_text(login_password_entry, 'Password', True)    
        
    logo_image = tk.PhotoImage(file = 'images/alt_perfoot.png')
    image_width = 80
    image_height = 80
    image_size = logo_image.subsample(int(logo_image.width() / image_width), int(logo_image.height() / image_height))
    logo_label = tk.Label(login_win, image = image_size)
    logo_label.image = image_size
    logo_label.pack(pady = (10, 10))   
    
    tk.Label(login_win, text = 'User Login', font = ('Arial Bold', 15)).pack(pady = 10)
  
    login_username_entry = tk.Entry(login_win, textvariable = log_username)
    login_username_entry.pack(padx = 40, fill = 'x')

    login_password_entry = tk.Entry(login_win, textvariable = log_password, show = '*')
    login_password_entry.pack(padx = 40, pady = (10, 20), fill = 'x')
    
    # prompts the verify entry
    log_in_button = tk.Button(login_win, text = 'Log In', command = lambda: verify_entry(log_username, log_password, login_win), bg = '#1E1E24',fg = 'white')
    log_in_button.pack(padx = 40, fill = 'x')
    white = 'white'
    green= '#1E1E24'
    button_hover(log_in_button, white, green)
    reset_login_entry()

# sign up window
def signup_window():
    signup_win = tk.Toplevel(main)
    window_size(signup_win, 300, 370)
    signup_win.resizable(False, False)
    signup_win.iconbitmap('images/alt_logo.ico')
    signup_win.title('Sign In')
    signup_win.grab_set()
    
    def reset_signin_entry():
        signin_username_entry.delete(0, tk.END)
        signin_email_entry.delete(0, tk.END)
        signin_password_entry.delete(0, tk.END)
        signin_confirmpassword_entry.delete(0, tk.END)
        
        entry_background_text(signin_username_entry, 'Username', False)   
        entry_background_text(signin_email_entry, 'Email', False)
        entry_background_text(signin_password_entry, 'Password (8 or more characters)', True)   
        entry_background_text(signin_confirmpassword_entry, 'Confirm Password', True)

    # sign up window entry error handling
    def verify_entry():
        if username.get() == 'Username':
            showerror('Error', 'Please fill in the username.', parent = signup_win)
        elif email.get() == 'Email':
            showerror('Error', 'Please fill in the email.', parent = signup_win)
        elif password.get() == 'Password (8 or more characters)':
            showerror('Error', 'Please fill in the password.', parent = signup_win)
        elif len(password.get()) < 8:
            showerror('Error', 'Password must be at least 8 characters or more.', parent = signup_win)
        elif con_password.get() == 'Confirm Password':
            showerror('Error', 'Please confirm your password.', parent = signup_win)
        elif password.get() != con_password.get():
            showerror('Error', 'Password does not match.', parent = signup_win)            
        else:
                pfdbcur.execute('SELECT COUNT(*) FROM user WHERE username = %s', (username.get(),))
                usercount = pfdbcur.fetchone()[0]

                pfdbcur.execute('SELECT COUNT(*) FROM user WHERE email = %s', (email.get(),))
                emailcount = pfdbcur.fetchone()[0]
                
                if usercount > 0:
                    showerror('Error', 'The username you\'ve entered already exists', parent = signup_win)
                elif emailcount > 0:
                    showerror('Error', 'The email you\'ve entered already exists', parent = signup_win)
                else:
                    # if all conditions are met the program will insert the user's information into the 'User' table
                    showinfo('Done', f'Welcome {username.get()}! You\'ve succesfully signed up to PerFoot.')

                    usersql = 'INSERT INTO user (username, email, password) VALUES (%s, %s, %s)'
                    userval = (username.get(), email.get(), password.get())
                    pfdbcur.execute(usersql, userval)
                    perfootdb.commit()
                    
                    # prompts the user to log in window
                    login_window()
                    signup_win.destroy()
                
    logo_image = tk.PhotoImage(file = 'images/alt_perfoot.png')
    image_width = 80
    image_height = 80
    image_size = logo_image.subsample(int(logo_image.width() / image_width), int(logo_image.height() / image_height))
    logo_label = tk.Label(signup_win, image = image_size)
    logo_label.image = image_size
    logo_label.pack(pady = (10, 10))   
    
    tk.Label(signup_win, text = 'Sign Up to Perfoot!', font = ('Arial Bold', 12)).pack(pady = 10)

    signin_username_entry = tk.Entry(signup_win, textvariable = username)
    signin_username_entry.pack(padx = 40, fill = 'x')
    
    signin_email_entry = tk.Entry(signup_win, textvariable = email)
    signin_email_entry.pack(padx = 40, pady = 10, fill = 'x')

    signin_password_entry = tk.Entry(signup_win, textvariable = password, show = '*')
    signin_password_entry.pack(padx = 40, fill = 'x')
     
    signin_confirmpassword_entry = tk.Entry(signup_win, textvariable = con_password, show = '*')
    signin_confirmpassword_entry.pack(padx = 40, pady = (10, 20), fill = 'x')

    signin_button = tk.Button(signup_win, text = 'Sign Up', command = verify_entry, bg = '#1E1E24', fg = 'white')
    signin_button.pack(padx = 40, fill = 'x')
    white = 'white'
    green = '#1E1E24'
    
    button_hover(signin_button, white, green)
    reset_signin_entry()

# dashboard of the user
def show_dashboard():
    category_ranking.pack()
    intro.pack_forget()
    dashboard.pack(fill = 'both', expand = True)
    window_size(main, 1280,900)
    main.resizable(False, False)
    main.update()

# error handling for the combobox and entry of subcategories       
def verify(categ_combobox, categ_amount, category):
    global selected
    selected = categ_combobox.get()
    try:
        val = float(categ_amount.get())
        if categ_combobox.get() == '': 
            showerror('Error', 'Please choose a subcategory.')
        elif selected == 'Transportation':
            showerror('Error', 'Please select a subcategory.')
        elif selected == 'Food':
            showerror('Error', 'Please select a subcategory.')
        elif selected == 'Household':
            showerror('Error', 'Please select a subcategory.')    
        else:
            showinfo('Confirmation', f'You\'ve selected \'{selected}\' with the value of {val}.')
            
            if category == 'Transportation':
                pfdbcur.execute('SELECT carbon_emission_per_unit FROM Transportation WHERE transportation_type = %s', (selected,))

            elif category == 'Food':
                pfdbcur.execute('SELECT carbon_emission_per_unit FROM Food WHERE food_type = %s', (selected,))
                
            elif category == 'Household':
                pfdbcur.execute('SELECT carbon_emission_per_unit FROM Household WHERE household_type = %s', (selected,))
                
            fetch = pfdbcur.fetchone()
            if fetch:
                return fetch[0]
            else:
                return None
    except:
        return showerror('Error', 'Please enter an integer.')

# calculates the total carbon emission with the entered value and chosen subcategory carbon emission per unit
def insert(categ_combobox, categ_amount, category):
    global selected
    selected = categ_combobox.get()
    
    # calls the 'verify' function to verify the entered value
    fetched_val = verify(categ_combobox, categ_amount, category)

    try:
        val = float(categ_amount.get())
        deci_amount = decimal.Decimal(str(categ_amount.get()))
        
        # formula for calculating carbon emission
        total_carbon_emission = (fetched_val * deci_amount)
        
        if category == 'Transportation':
            pfdbcur.execute(f'SELECT transportation_id FROM Transportation WHERE transportation_type = %s', (selected,))
            categ_id = pfdbcur.fetchone()
            
            insert = 'INSERT INTO User_Activity (user_id, category, category_id, quantity, carbon_emission) VALUES (%s, %s, %s, %s, %s)'
            values = (loggedon_userid, category, categ_id[0], categ_amount.get(), total_carbon_emission)
            pfdbcur.execute(insert, values)
            perfootdb.commit()
            reset_combobox_selection()

        elif category == 'Food':
            pfdbcur.execute('SELECT food_id FROM Food WHERE food_type = %s', (selected,))
            categ_id = pfdbcur.fetchone()
            
            insert = 'INSERT INTO User_Activity (user_id, category, category_id, quantity, carbon_emission) VALUES (%s, %s, %s, %s, %s)'
            values = (loggedon_userid, category, categ_id[0], categ_amount.get(), total_carbon_emission)
            pfdbcur.execute(insert, values)
            perfootdb.commit()
            reset_combobox_selection()
        elif category == 'Household':
            pfdbcur.execute('SELECT household_id FROM Household WHERE household_type = %s', (selected,))
            categ_id = pfdbcur.fetchone()
            
            insert = 'INSERT INTO User_Activity (user_id, category, category_id, quantity, carbon_emission) VALUES (%s, %s, %s, %s, %s)'
            values = (loggedon_userid, category, categ_id[0], categ_amount.get(), total_carbon_emission)
            pfdbcur.execute(insert, values)
            perfootdb.commit()
            reset_combobox_selection()
            
        showinfo('Activity Recorded', f'Total Carbon Emission: {total_carbon_emission} kgCO₂.')
    except:
        return None

# prompted when a record is clicked from the 'User_Activity' treeview or retrieveall_useracts    
def double_click(click):
    tree = click.widget
    selected = tree.selection()
    
    # packs the update_frame
    def update_quantity():
        update_frame.pack(side = 'top',fill = 'x', padx = 550)
        button_frame.pack_forget()
    
    # overwrites the previous carbon emission for the selected record with the newly entered quantity and selected carbon emission per unit (with error handling)
    def update_quantity_main():
        try:
            val = float(str(entered_quantity.get()))
            decimal_entered_quantity = decimal.Decimal(str(entered_quantity.get()))
            
            pfdbcur.execute('SELECT activity_id FROM User_Activity WHERE activity_timestamp = %s', (timestamp,))
            fetch_activity_id = pfdbcur.fetchone()
            activity_id = fetch_activity_id[0]
            
            pfdbcur.execute('SELECT category, category_id FROM User_Activity WHERE activity_id = %s', (activity_id,))
            fetch_two = pfdbcur.fetchone()
            
            category, category_id = fetch_two
            
            if category == 'Transportation':
                pfdbcur.execute('SELECT carbon_emission_per_unit FROM Transportation WHERE transportation_id = %s', (category_id,))
                fetch = pfdbcur.fetchone()
                
                carbon_emission_per_unit = fetch[0]
                new_quantity = (decimal_entered_quantity * carbon_emission_per_unit)
                pfdbcur.execute('UPDATE User_Activity SET quantity = %s, carbon_emission = %s WHERE activity_id = %s', (decimal_entered_quantity, new_quantity, activity_id))
                perfootdb.commit()

                showinfo('Done', f'The Record\'s quantity was successfully updated to {decimal_entered_quantity} (Total carbon emission was also updated).')
                delete_all_frame.pack(fill = 'x', padx = 20, side = 'bottom')
                category_ranking.pack_forget()
                update_dashboard_treeview.pack_forget()                
            if category == 'Food':
                pfdbcur.execute('SELECT carbon_emission_per_unit FROM Food WHERE food_id = %s', (category_id,))
                fetch = pfdbcur.fetchone()
                
                carbon_emission_per_unit = fetch[0]
                new_quantity = (decimal_entered_quantity * carbon_emission_per_unit)
                pfdbcur.execute('UPDATE User_Activity SET quantity = %s, carbon_emission = %s WHERE activity_id = %s', (decimal_entered_quantity, new_quantity, activity_id))
                perfootdb.commit()

                showinfo('Done', f'The Record\'s quantity was successfully updated to {decimal_entered_quantity} (Total carbon emission was also updated).')
                delete_all_frame.pack(fill = 'x', padx = 20, side = 'bottom')
                category_ranking.pack_forget()
                update_dashboard_treeview.pack_forget()                
            if category == 'Household':
                pfdbcur.execute('SELECT carbon_emission_per_unit FROM Household WHERE household_id = %s', (category_id,))
                fetch = pfdbcur.fetchone()
                
                carbon_emission_per_unit = fetch[0]
                new_quantity = (decimal_entered_quantity * carbon_emission_per_unit)
                pfdbcur.execute('UPDATE User_Activity SET quantity = %s, carbon_emission = %s WHERE activity_id = %s', (decimal_entered_quantity, new_quantity, activity_id))
                perfootdb.commit()

                showinfo('Done', f'The Record\'s quantity was successfully updated to {decimal_entered_quantity} (Total carbon emission was also updated).')
                delete_all_frame.pack(fill = 'x', padx = 20, side = 'bottom')
                category_ranking.pack_forget()
                update_dashboard_treeview.pack_forget()
        except:
            showerror('Error', 'Please enter an integer.')
    
    # deletes the selected record
    def delete_record():
        confirm = askyesno('Confirm', 'Are you sure you want to delete this record?')
        if confirm:
            activity_id = timestamp
            pfdbcur.execute('SELECT activity_id FROM User_Activity WHERE activity_timestamp = %s', (timestamp,))
            fetch = pfdbcur.fetchone()
        
            if fetch:
                activity_id = fetch[0]
                
                pfdbcur.execute('DELETE FROM User_Activity WHERE activity_id = %s', (activity_id,))
                perfootdb.commit()
                showinfo('Done', 'The record has been deleted.')
                dashboard.after(1000, retrieveall_useracts)
                delete_all_frame.pack(fill = 'x', padx = 20, side = 'bottom')
                update_dashboard_treeview.pack_forget()
            else:
                showerror('Error', 'Record not found or already deleted')
        
    if selected:
   
        for widget in update_dashboard_treeview.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()
            if isinstance(widget, tk.Button):
                widget.destroy()
            if isinstance(widget, tk.Frame):
                widget.destroy()
        
        def reset_enter_quantity_entry():
            enter_quantity.delete(0, tk.END)
            entry_background_text(enter_quantity, 'Enter Value')
            
        entered_quantity = tk.StringVar()                
        update_dashboard_treeview.pack(fill = 'x')     
        record_values = tree.item(selected, 'values')
        category, category_id, quantity, carbon_emission, timestamp = record_values
        
        delete_all_frame.pack_forget()
        category_ranking.pack_forget()
        
        detail_frame = tk.Frame(update_dashboard_treeview, bg = '#1E1E24')
        detail_frame.pack(side = 'top')
        
        # lists the information of selected record 
        tk.Label(detail_frame, text = f'Category: {category}', bg = '#1E1E24', fg = 'white').pack(side = 'left', padx = 10)
        tk.Label(detail_frame, text = f'Category ID: {category_id}', bg = '#1E1E24', fg = 'white').pack(side = 'left', padx = 10)
        tk.Label(detail_frame, text = f'Quantity: {quantity}', bg = '#1E1E24', fg = 'white').pack(side = 'left', padx = 10)
        tk.Label(detail_frame, text = f'Carbon Emission: {carbon_emission}', bg = '#1E1E24', fg = 'white').pack(side = 'left', padx = 10)
        tk.Label(detail_frame, text = f'Date/Time: {timestamp}', bg = '#1E1E24', fg = 'white').pack(side = 'left', padx = 10)
        
        #shows the update, delete, and cancel button
        button_frame = tk.Frame(update_dashboard_treeview, bg = '#1E1E24')
        button_frame.pack(side  = 'top', fill = 'x', padx = 550)
        
        update_button = tk.Button(button_frame, text = 'Update Quantity', bg = '#82A37D', fg = 'white', command = update_quantity)
        delete_button = tk.Button(button_frame, text = 'Delete', bg = '#F97362', fg = 'white', command = delete_record)
        cancel_button_again = tk.Button(button_frame, text = 'Cancel', bg = '#F97362', fg = 'white', command = lambda: (delete_all_frame.pack(fill = 'x', padx = 20, side = 'bottom'), update_dashboard_treeview.pack_forget()))
        update_button.pack(fill = 'x', pady = (10, 0))
        delete_button.pack(fill = 'x', pady = 10)
        cancel_button_again.pack(fill = 'x')
        button_hover(update_button, white, green)
        button_hover(delete_button, white, red)
        
        # prompted when the update button was clicked (value entry, confirm, and cancel button)
        update_frame = tk.Frame(update_dashboard_treeview, bg = '#1E1E24')
        
        enter_quantity = tk.Entry(update_frame, textvariable = entered_quantity)
        enter_quantity.pack(fill = 'x', expand = True, pady = 10)
        
        reset_enter_quantity_entry()
        
        # confirm button which prompts the update_quantity_main
        confirm_button = tk.Button(update_frame, text = 'Confirm', bg = '#82A37D', fg = 'white', command = update_quantity_main)
        cancel_button_again_again = tk.Button(update_frame, text = 'Cancel', bg = '#F97362', fg = 'white', command = lambda: (button_frame.pack(fill = 'x', padx = 550), update_frame.pack_forget()))
        confirm_button.pack(fill = 'x', pady = 10)        
        cancel_button_again_again.pack(fill = 'x')
        
        button_hover(confirm_button, white, green)
        button_hover(cancel_button_again, white, red)

# resets the dashboard to its original state         
def hide_logs():
    view_button.pack()
    category_ranking.pack()
    trans_info.pack_forget()
    food_info.pack_forget()
    house_info.pack_forget()
    category.pack_forget()
    cancel_button.pack_forget()
    update_dashboard_treeview.pack_forget()
    dashboard_treeview.pack_forget()
    delete_all_frame.pack_forget()

# prompts the retrieveall_useracts and delete_all_frame        
def treeview():
    delete_all_frame.pack(fill = 'x', padx = 20, side = 'bottom')
    category_ranking.pack_forget()
    trans_frame.pack_forget()
    food_frame.pack_forget()
    house_frame.pack_forget()
    trans_info.pack_forget()
    food_info.pack_forget()
    house_info.pack_forget()
    category.pack_forget()
    cancel_button.pack_forget()
    dashboard_treeview.pack()
    retrieveall_useracts()
    view_button.pack_forget()

# shows the current user's activity logs in treeview from 'User_Activity' table
def retrieveall_useracts():
    for widget in dashboard_treeview.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()
        if isinstance(widget, tk.Button):
            widget.destroy()
        if isinstance(widget, tk.Frame):
            widget.destroy()
    for widget in delete_all_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()
    
    # deletes all the records from 'User_Activity' according to current user_id (loggedon_userid)        
    def delete_all_logs():
        confirm = askyesno('Confirmation', 'This will remove all of your logs.')
        if confirm:
            delete_all = 'DELETE FROM user_activity WHERE user_id = %s'
            pfdbcur.execute(delete_all, (loggedon_userid,))
            perfootdb.commit()
        else:
            return None         
           
    hide_button = tk.Button(dashboard_treeview, text = 'Hide Log(s)', command = lambda: hide_logs(), bg = '#F97362', fg = 'white')
    hide_button.pack(padx = 40, pady = (0, 10), side = 'top')
    button_hover(hide_button, white, red)

    # deletes all of the records of the current user from the table 'User_Activity' 
    delete_button = tk.Button(delete_all_frame, text = 'Delete All', command = lambda: delete_all_logs(), bg = '#F97362', fg = 'white')
    delete_button.pack(padx = 40, pady = (10, 0), side = 'bottom', fill = 'x')
    
    # table 'User_Activity' treeview
    button_hover(delete_button, white, red)
    useract_tree = ttk.Treeview(dashboard_treeview, columns=('Category', 'Category ID', 'Quantity', 'Carbon Emission', 'Timestamp'), show = 'headings')
    useract_tree.pack()
 
    useract_tree.heading('Category', text = 'Category')
    useract_tree.heading('Category ID', text = 'Category ID')
    useract_tree.heading('Quantity', text = 'Quantity')
    useract_tree.heading('Carbon Emission', text = 'Total')
    useract_tree.heading('Timestamp', text ='Date/Time')

    useract_tree.column('Category', width = 150, anchor = 'w') 
    useract_tree.column('Category ID', width = 100, anchor ='center') 
    useract_tree.column('Quantity', width = 100, anchor ='e')  
    useract_tree.column('Carbon Emission', width = 150, anchor = 'e') 
    useract_tree.column('Timestamp', width = 200, anchor = 'center') 
    
    pfdbcur.execute('''
        SELECT ua.category, ua.category_id, ua.quantity, 
               CASE
                   WHEN ua.category = 'Transportation' THEN t.carbon_emission_per_unit * ua.quantity
                   WHEN ua.category = 'Food' THEN f.carbon_emission_per_unit * ua.quantity
                   WHEN ua.category = 'Household' THEN h.carbon_emission_per_unit * ua.quantity
                   ELSE 0
               END AS carbon_emission,
               ua.activity_timestamp
        FROM User_Activity ua
        LEFT JOIN Transportation t ON ua.category = 'Transportation' AND ua.category_id = t.transportation_id
        LEFT JOIN Food f ON ua.category = 'Food' AND ua.category_id = f.food_id
        LEFT JOIN Household h ON ua.category = 'Household' AND ua.category_id = h.household_id
        WHERE ua.user_id = %s
    ''', (loggedon_userid,))
    rows = pfdbcur.fetchall()
    
    for row in rows:
        useract_tree.insert('', 'end', values = row)
    
    dashboard.after(3000, retrieveall_useracts) 
    
    # prompts the option update and delete 
    useract_tree.bind('<Double-1>', lambda click: (double_click(click), delete_button.destroy()))

# subcategories' carbon emissionn per unit in treeview    
def activity_info(category_name, frame):
    for widget in frame.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()
        if isinstance(widget, ttk.Scrollbar):
            widget.destroy()
        if isinstance(widget, tk.Label):
            widget.destroy()
        if isinstance(widget, tk.Frame):
            widget.destroy()
        
    tk.Label(frame, text = 'Carbon Emission Per Unit', bg = '#1E1E24', fg = 'white').pack(pady = 10)
    activity_tree = ttk.Treeview(frame, column = ('ID', 'Subcategory', 'Carbon Emission', 'Unit'), show = 'headings')
    activity_tree.pack(side = 'left', fill = 'x', pady = (0, 30))
    

    activity_tree.heading('ID', text = 'ID')
    activity_tree.heading('Subcategory', text = '    ')
    activity_tree.heading('Carbon Emission', text = 'Carbon Emission')
    activity_tree.heading('Unit', text = 'Unit')
    
    activity_tree.column('ID', width = 50)
    activity_tree.column('Subcategory', width = 250)
    activity_tree.column('Carbon Emission', width = 150)
    activity_tree.column('Unit', width = 75)
    
    pfdbcur.execute(f'SELECT {category_name}_id, {category_name}_type, carbon_emission_per_unit, unit FROM {category_name}')
    rows = pfdbcur.fetchall()
    
    for row in rows:
        activity_tree.insert('', 'end', values = row)
        
    activity_tree_sb = ttk.Scrollbar(frame, orient = 'vertical', command = activity_tree.yview)
    activity_tree_sb.pack(side = 'right', fill = 'y', pady = (0, 30))
    
    activity_tree.configure(yscrollcommand = activity_tree_sb.set)

# automatically updates the user total carbon emission
def total_carbon_emission():
    dashboard.after(1000, total_carbon_emission)  
    pfdbcur.execute('SELECT username FROM user WHERE user_id = %s', (loggedon_userid,))
    user_username = pfdbcur.fetchone()
    
    while user_username is None:
        return None
    else:
        username_dashboard.config(text = f'{user_username[0]}\'s Dashboard', font = ('Arial Bold', 20), bg = '#1E1E24', fg = 'white')
        pfdbcur.execute('SELECT SUM(carbon_emission) FROM User_Activity WHERE user_id = %s', (loggedon_userid,))
        sum_carbonEm = pfdbcur.fetchone()
        
        final = sum_carbonEm[0] if sum_carbonEm[0] is not None else 0
        total_carbon_emission_count.config(text = f'{final} kgCO₂', font = ('Arial Bold', 15), bg = '#1E1E24', fg = 'white')

# packs the category frame
def category_frame():
    category_ranking.pack_forget()
    delete_all_frame.pack_forget()
    trans_frame.pack_forget()
    food_frame.pack_forget()
    house_frame.pack_forget()
    update_dashboard_treeview.pack_forget()
    dashboard_treeview.pack_forget()
    view_button.pack()
    cancel_button.pack(padx = 60, side = 'bottom', fill = 'x')
    category.pack(fill = 'both', expand = True)
    category_buttons.pack(fill = 'both', side = 'top', anchor = 'w', padx = 500)

# shows the chosen category's subcategories
def unpack(first, second, third):
    if first is True:
        trans_frame.pack(side = 'left', fill = 'x', expand = True, padx = (10, 400))
        category_buttons.pack(fill = 'x', side = 'left', expand = True, padx = (400, 10))
        trans_info.pack(side = 'bottom')     
        activity_info('Transportation', trans_info)
        food_frame.pack_forget()
        food_info.pack_forget()
        house_frame.pack_forget()
        house_info.pack_forget()
    else:
        trans_frame.pack_forget()
        trans_info.pack_forget()
        
    if second is True:
        food_frame.pack(side = 'left', fill = 'x', expand = True, padx = (10, 400))
        category_buttons.pack(fill = 'x', side = 'left', expand = True, padx = (400, 10))
        food_info.pack()
        activity_info('Food', food_info)
        trans_frame.pack_forget()
        trans_info.pack_forget()
        house_frame.pack_forget()
        house_info.pack_forget()       
    else:
        food_frame.pack_forget()
        food_info.pack_forget()
    if third is True:
        house_frame.pack(side = 'left', fill = 'x', expand = True, padx = (10, 400))
        category_buttons.pack(fill = 'x', side = 'left', expand = True, padx = (400, 10))
        house_info.pack()
        activity_info('Household', house_info)
        trans_frame.pack_forget()
        trans_info.pack_forget()
        food_frame.pack_forget()
        food_info.pack_forget()
    else:
        house_frame.pack_forget()
        house_info.pack_forget()  

# program's description and log in and sign up buttons       
def introduction():
    window_size(main, 600, 600)
    main.resizable(False, False)
    icon_title(main)
    
    intro.pack(fill = tk.BOTH, expand = True)
    tk.Label(intro, text = 'Welcome to PerFoot!', font = ('Arial Bold', 20), bg = '#1E1E24', fg = 'white').pack(pady = (50,10))

    logo_label = tk.Label(intro, image = image_size, bg = '#1E1E24')
    logo_label.image = image_size
    logo_label.pack(pady = (0, 10))

    tk.Label(intro, text = 'PerFoot is a personal footprint tracker that helps you monitor '
                        'your environmental impact by estimating the carbon footprint '
                        'of your daily activities. The app categorizes your activities into '
                        'Transportation, Food, and Household, providing insights into how each choice '
                        'contributes to your carbon emissions.', wraplength = 500, bg = '#1E1E24', fg = 'white', justify = tk.CENTER).pack(pady = (0, 50))

    # prompts the log in window or sign up window
    login_button = tk.Button(intro, text = 'Log in', command = login_window, bg = '#82A37D', fg = 'white')
    signin_button = tk.Button(intro, text = 'Sign In', command = signup_window, bg = '#82A37D', fg = 'white')

    button_hover(login_button, white, green )
    button_hover(signin_button, white, green)
    login_button.pack(padx = 40, fill = 'x')
    signin_button.pack(padx = 40, pady = 10, fill = 'x')

# logs out the user from the dashboard   
def log_out():
    confirm = askyesno('Exit', 'Are you sure you want to log out?')
    if confirm:
        intro.pack_forget()
        dashboard.pack_forget()
        hide_logs()
        introduction()

# background text for combobox
def combobox_focus_in(combo, background_text):
    if combo.get() == background_text:
        combo.set('')
        combo.config(foreground = 'black')

# removes the background text from combobox        
def combobox_focus_out(combo, background_text):
    if combo.get() == '':
        combo.set(background_text)
        combo.config(foreground = 'gray')

# combines combobox_focus_in and combobox_focus_out, and also resets the entries
def reset_combobox_selection():
    trans_combobox.set('')
    food_combobox.set('')
    house_combobox.set('')
    
    trans_entry.delete(0, tk.END)
    food_entry.delete(0, tk.END)
    house_entry.delete(0, tk.END)
    
    entry_background_text(trans_entry, 'Enter Value')
    entry_background_text(food_entry, 'Enter Value')
    entry_background_text(house_entry, 'Enter Value')

    trans_combobox.bind('<FocusIn>', combobox_focus_in(trans_combobox, 'Transportation'))
    trans_combobox.bind('<FocusOut>', combobox_focus_out(trans_combobox, 'Transportation'))
    
    food_combobox.bind('<FocusIn>', combobox_focus_in(food_combobox, 'Food'))
    food_combobox.bind('<FocusOut>', combobox_focus_out(food_combobox, 'Food'))
    
    house_combobox.bind('<FocusIn>', combobox_focus_in(house_combobox, 'Household'))
    house_combobox.bind('<FocusOus>', combobox_focus_out(house_combobox, 'Household'))

# ranks the category based on total carbon emission from highes to lowest
def category_highest_emission():
    for widget in category_ranking.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()
        if isinstance(widget, tk.Label):
            widget.destroy()
    
    tk.Label(category_ranking, text = 'Category Contributions (Highest to Lowest)', bg = '#1E1E24', fg = 'white').pack(pady = (30, 15))
    category_tree = ttk.Treeview(category_ranking, columns = ('Category', 'Total Emission'), show = 'headings', height = 5)
    category_tree.heading('Category', text = 'Category')
    category_tree.heading('Total Emission', text = 'Total Emission (kgCO₂)')
    category_tree.pack(pady = (0, 100))
    
    # SQL script for ranking Transportation, Food, and Household from highest to lowest
    rank_category = '''
        SELECT 
            category_data.category,
            SUM(category_data.carbon_emission * ua.quantity) AS total_emission
        FROM
            User_Activity AS ua
        JOIN 
            (
                SELECT transportation_id AS category_id, carbon_emission_per_unit AS carbon_emission, 'Transportation' AS category
                FROM Transportation
                UNION ALL
                SELECT food_id AS category_id, carbon_emission_per_unit AS carbon_emission, 'Food' AS category
                FROM Food
                UNION ALL
                SELECT household_id AS category_id, carbon_emission_per_unit AS carbon_emission, 'Household' AS category
                FROM Household
            ) AS category_data
        ON ua.category_id = category_data.category_id
        WHERE ua.user_id = %s 
        AND ua.category = category_data.category  
        GROUP BY category_data.category
        HAVING total_emission > 0 
        ORDER BY total_emission DESC;
    '''

    pfdbcur.execute(rank_category, (loggedon_userid,))
    rows = pfdbcur.fetchall()

    if rows:
        for row in rows:
            category_tree.insert('', 'end', values = row)
    
    dashboard.after(3000, category_highest_emission) 
    
windll.shcore.SetProcessDpiAwareness(1)

# program's database and cursor
perfootdb = mysql.connector.connect(host = 'localhost', user = 'root', database = 'perfootdb')
pfdbcur = perfootdb.cursor()   
main = tk.Tk()

# user's information placeholders and other variables for image
loggedon_userid = None
username =  tk.StringVar()
email = tk.StringVar()
password = tk.StringVar()

con_password = tk.StringVar()
log_username = tk.StringVar()
log_password = tk.StringVar()

white = 'white'
green = '#82A37D'
gray = '#1E1E24'
red = '#F97362'
yellow = '#FFDE70'

image_width = 175
image_height = 175

logo_image = tk.PhotoImage(file = 'images/perfoot.png')
image_size = logo_image.subsample(int(logo_image.width() / image_width), int(logo_image.height() / image_height))

# prompts the introduction page of the program
intro = tk.Frame(main, bg = '#1E1E24')
introduction()

log_out_icon_width = 30
log_out_icon_height = 30
log_out_icon = tk.PhotoImage(file = 'images/log_out.png')
logo_image = tk.PhotoImage(file = 'images/perfoot.png')
log_out_icon_size = log_out_icon.subsample(int(log_out_icon.width() / log_out_icon_width), int(log_out_icon.height() / log_out_icon_height))

# dashboard frame
dashboard = tk.Frame(main, bg = '#1E1E24')

# log out button (prompts the user to the introduction again)
log_out_button = tk.Button(dashboard, command = log_out, image = log_out_icon_size, bg = '#F97362', fg = 'white')
log_out_button.pack(side = 'top', anchor = 'ne', pady = 10, padx = 10)
button_hover(log_out_button, white, red)

# updates the total carbon emission of the dashboard
total_carbon_emission()

# dashboard widgets
username_dashboard = tk.Label(dashboard, text = 'Dashboard', bg = '#1E1E24', fg = 'white')
username_dashboard.pack(pady = (10, 20))

logo_label = tk.Label(dashboard, image = image_size, bg = '#1E1E24')
logo_label.image = image_size
logo_label.pack(pady = (0, 10))

total_carbon_emission_count = tk.Label(dashboard, text = '0 kgCO₂', bg = '#1E1E24', fg = 'white')
total_carbon_emission_count.pack()
total_carbon_emission_label = tk.Label(dashboard, text = 'Total Carbon Emission', bg = '#1E1E24', fg = 'white')
total_carbon_emission_label.pack(pady = (0, 10))

# shows the logs of the current user
view_button = tk.Button(dashboard, text = 'View Log(s)', command = treeview, bg = '#82A37D', fg = 'white')
view_button.pack(padx = 40, side = 'top')
button_hover(view_button, white, green)

# shows the categories total carbon emission ranking
category_ranking = tk.Frame(dashboard, bg = '#1E1E24')
category_highest_emission()

# 'User_Activity' table treeview and delete all button frame
dashboard_treeview = tk.Frame(dashboard, bg = '#1E1E24')
dashboard_treeview.pack()
delete_all_frame = tk.Frame(dashboard, bg = '#1E1E24')
update_dashboard_treeview = tk.Frame(dashboard, bg = '#1E1E24')

# shows the 3 category button: Transportation, Food, and Household
add_button = tk.Button(dashboard, text = '+ Add', command = category_frame, bg = '#82A37D', fg = 'white')
add_button.pack(padx = 60, pady =  10, side = 'bottom', fill = 'x')

# cancels the add button (hides the 3 categories)
cancel_button = tk.Button(dashboard, text = 'Cancel', command = lambda: (trans_info.pack_forget(), food_info.pack_forget(), house_info.pack_forget(), category.pack_forget(), category_ranking.pack(), cancel_button.pack_forget()), bg = '#F97362', fg = 'white')
button_hover(add_button, white, green)
button_hover(cancel_button, white, red)

# category frame
category = tk.Frame(dashboard, bg = '#1E1E24')
category_buttons = tk.Frame(category, bg = '#1E1E24')

# category buttons
tk.Label(category_buttons, text = 'Choose Category', bg = '#1E1E24', fg = 'white').pack(pady = (30, 15))
transportation_button = tk.Button(category_buttons, text = 'Transportation', command = lambda: unpack(True, False, False), bg = '#FFDE70', fg = 'white')
food_button = tk.Button(category_buttons, text = 'Food', command = lambda: unpack(False, True, False), bg = '#FFDE70', fg = 'white')
household_button = tk.Button(category_buttons, text = 'Household', command = lambda: unpack(False, False, True), bg = '#FFDE70', fg = 'white')

transportation_button.pack(fill = 'x', side = 'top', anchor = 'w')
food_button.pack(fill = 'x', side = 'top', anchor = 'w')
household_button.pack(fill = 'x', side = 'top', anchor = 'w')

button_hover(transportation_button, white, yellow)
button_hover(food_button, white, yellow)
button_hover(household_button, white, yellow)

# subcategories frame
trans_frame = tk.Frame(category, bg = '#1E1E24')
food_frame = tk.Frame(category, bg = '#1E1E24')
house_frame = tk.Frame(category, bg = '#1E1E24')

pfdbcur.execute('SELECT transportation_type FROM Transportation')
trans_types = [row[0] for row in pfdbcur.fetchall()]
pfdbcur.execute('SELECT food_type FROM Food')
food_types = [row[0] for row in pfdbcur.fetchall()]
pfdbcur.execute('SELECT household_type FROM Household')
household_types = [row[0] for row in pfdbcur.fetchall()]

# subcategories entered amount (km, L, kg, kWh, and h)
trans_amount = tk.DoubleVar(value = '')
food_amount = tk.DoubleVar(value = '')
house_amount = tk.DoubleVar(value = '')

# transportation subcategory
tk.Label(trans_frame, text = 'Select one', bg = '#1E1E24', fg = 'white').pack(pady = 10)
trans_combobox = ttk.Combobox(trans_frame, values = trans_types, state = 'readonly')
trans_combobox.pack(fill = 'x')

trans_combobox.bind('<<ComboboxSelect>>', verify)

trans_entry = tk.Entry(trans_frame, textvariable = trans_amount)
trans_entry.pack(fill = 'x', pady = 10)

# passes the entered value to 'insert' function
trans_confirm = tk.Button(trans_frame, text = 'Confirm', command = lambda: insert(trans_combobox, trans_amount, 'Transportation'), bg = '#82A37D', fg = 'white')
trans_confirm.pack(fill = 'x', pady = 10)

#food subcategory
tk.Label(food_frame, text = 'Select one', bg = '#1E1E24', fg = 'white').pack(pady = 10)
food_combobox = ttk.Combobox(food_frame, values = food_types, state = 'readonly')
food_combobox.pack(fill = 'x')

food_combobox.bind('<<ComboboxSelect>>', verify)

food_entry = tk.Entry(food_frame, textvariable = food_amount)
food_entry.pack(fill = 'x', pady = 10)

# passes the entered value to 'insert' function
food_confirm = tk.Button(food_frame, text = 'Confirm', command = lambda: insert(food_combobox, food_amount, 'Food'), bg = '#82A37D', fg = 'white')
food_confirm.pack(fill = 'x', pady = 10)

#house subcategory
tk.Label(house_frame, text = 'Select one', bg = '#1E1E24', fg = 'white').pack(pady = 10)
house_combobox = ttk.Combobox(house_frame, values = household_types, state = 'readonly')
house_combobox.pack(fill = 'x')

house_combobox.bind('<<ComboboxSelect>>', verify)

house_entry = tk.Entry(house_frame, textvariable = house_amount)
house_entry.pack(fill = 'x', pady = 10)

# passes the entered value to 'insert' function
house_confirm = tk.Button(house_frame, text = 'Confirm', command = lambda: insert(house_combobox, house_amount, 'Household'), bg = '#82A37D', fg = 'white')
house_confirm.pack(fill = 'x', pady = 10)

button_hover(trans_confirm, white, green)
button_hover(food_confirm, white, green)
button_hover(house_confirm, white, green)

# frames for subcategories' carbon emission per unit
trans_info = tk.Label(dashboard, bg = '#1E1E24')
food_info = tk.Label(dashboard, bg = '#1E1E24')
house_info = tk.Label(dashboard, bg = '#1E1E24')

reset_combobox_selection()
main.mainloop()

'''
Advance Computer Programming - Final Project
IT - 2102
Frankin C. Dela Torre
'''