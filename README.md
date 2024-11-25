# I. Project Overview

Perfoot: Personal Carbon Footprint Tracker helps users monitor their carbon emissions across three categories: Transportation, Food, and Household. Each category is further divided into subcategories, allowing users to select from various options. The program also supports record deletion and quantity updates. Additionally, the program is not limited to a single user, enabling multiple user profiles to be created. The program was created with Python, Tkinter, and MySQL.

# II. Python Concepts, Libraries, and Database Application

## 1. Python Concepts

- **Functions**:
    - Functions were used to break down the program into smaller, reusable parts, improving code organization and reducing redundancy. This helps keep the program concise and maintainable.

- **Control Structures**:
    - Control statements (like if-else and loops) were used to manage the flow of the program, ensuring it responds appropriately to different user inputs. They also handle logic for validating user data.

- **Error Handling**:
    - The program utilized try-except blocks to handle potential errors, such as invalid user inputs or database issues. This ensures that the program runs smoothly and provides helpful feedback to the user when something goes wrong.

## 2. Libraries

- **Tkinter**:
    - Tkinter was used to create a graphical user interface (GUI), making it easier for users to interact with the program. The GUI includes forms, buttons, and input fields that allow users to track and input their carbon footprint data.

- **MySQL (Database)**:
    - MySQL was used to store user data, including activity logs, categories, subcategories (with carbon emissions per unit), and user activity records. The database also helps manage user authentication, such as in the login and sign-in windows, ensuring a smooth and secure user experience.

# III. SDG and Its Integration into the Project

**SDG 13: Climate Action**  
**Target 13.3**: Improve education, awareness-raising, and human and institutional capacity on climate change mitigation, adaptation, impact reduction, and early warning.

The program helps individuals track their personal carbon footprint, raising awareness about the impact of daily activities on climate change. By increasing users' awareness of their emissions, it encourages more sustainable practices, contributing to climate action.

# IV. Instructions for Running the Program

1. Download the `Perfoot Files.zip`

2. Extract the `Perfoot Files.zip` this file contains:
    - `Perfoot Program` (folder):
       - `perfoot.py`
       - `perfoot.sql`
       - `README.md`
       - `images` folder (which should contain the following files):
           - `alt_logo.ico`
           - `alt_perfoot.png`
           - `log_out.png`
           - `logo.ico`
           - `perfoot.png`
  
3. Open XAMPP and start the MySQL service.

4. Import the SQL database:
    - Open the `perfoot.sql` file and copy the entire script (including one blank space at the bottom).
    - Open Command Prompt and paste the script to create the necessary tables and structure.

5. Run the program:
    - Open the `Perfoot Program` folder in Visual Studio Code (Ctrl+K+O) and run the program.
