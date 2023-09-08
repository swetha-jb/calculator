# CalCulator
---
## Overview

CalCulator is a modern, aesthetic user interface implemented in Python using a customization of the Tkinter library in Python. This application emulates a calculator, enabling users to perform complex algebraic, vector, and calculus computations. It also features capabilities to solve complex word problems using the ChatGPT API as well as graph and solve specified formulas.  

The program utilizes Sympy, NumPy, and SciPy for evaluating symbolic expressions.

## Getting Started
To run the code on your local machine, follow these steps:

**1. Clone the repository:**
   ```bash
   git clone https://github.com/brmattos/CalCulator.git
   ```
**2. Install required dependencies and modules:**
   ```bash
   pip install -r requirements.txt
   ```
**3. Get OpenAI API Key (Optional)**  

The word problem solution feature utilizes the OpenAi API and therefore an api key.  
If you would like to try the feature, you can find that information here: [OpenAI API key](https://platform.openai.com/account/api-keys)  

---
## Features  
### *Calculator Page:*

- The calculator page provides a user-friendly interface for performing various mathematical calculations.
- It supports complex algebraic expressions, derivatives, integrals, and more.
- Users can enter mathematical expressions and obtain calculations instantly.

![image](https://github.com/brmattos/CalCulator/assets/140926908/d176fc7e-9cf0-4c2c-a96d-a955dcc5e781)

- Calculated and made readable result of calculating the above inputted equation: ![image](https://github.com/brmattos/CalCulator/assets/140926908/88d0625a-8308-4195-a5ac-efe16a7137e3)

### *Functions Page:*

- The vector functions page allows users to perform various vector-related calculations.
- Supported operations include addition of vectors, dot products, cross products, projections, determinants, norms of vectors, arc lengths, and derivatives.
- Specific operations / concepts are selected from a drop down, with the entrance field format depending on said selection

![image](https://github.com/brmattos/CalCulator/assets/140926908/e815775b-63be-44b9-a324-39066e5e0824)

### *Graphs Page:*

- The graphs page enables users to visualize mathematical functions by plotting their graphs.
- Users can input functions, and the application generates graphical representations.
- The resulting graph provides a visual representation of the input function as well as a formatted and syntactitally pleasing function declaration

![image](https://github.com/brmattos/CalCulator/assets/140926908/4c9ca7f5-0137-4bcc-87cf-a7ec16e588e5)
![image](https://github.com/brmattos/CalCulator/assets/140926908/04f9d660-488e-43e4-8243-d59dcd023c7b)

### *Solve AI Page:*

- The word problem solver page lets users input complex word problems.
- Utilizes the ChatGPT API to generate solutions and presents answers in an organized format.
- Implements a scrollable textbox to see the reasoning and calculations behind the final calculation by the AI generated solution.

![image](https://github.com/brmattos/CalCulator/assets/140926908/b8307c36-9011-4d4c-94b4-7aafb3075670)
---
