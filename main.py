from dataclasses import dataclass
from bakery import assert_equal
from drafter import *
import sympy as sp


set_website_title("Derivative/Integral Helper")
set_site_information(
    author="Josie Brement",
    description="Derives and Integrates given functions.",
    sources="",
    planning=["Copy of CS1 Final Project 0_ Pick a Problem.pdf", "Final Project Design Phase.pdf"],
    links=["https://github.com/josiebrement/derivative-and-integral-helper.git"]
)

hide_debug_information()
set_website_framed(False)


@dataclass
class Calculation:
    function: str
    operation: str
    bounds: str
    result: str
    
    
@dataclass
class State:
    function: str
    operation: str
    bounds: str
    result: str
    history: list[Calculation]
    

@route
def index(state: State) -> Page:
    """
        Defines the home page of the program. 
        
        Args:
            state(State): the current state of the program.
            
        Returns:
            Page: a page that prompts user to input a function and have it evaluated,
            connects to the history page, and connects to the User Guidelines page.
    """
    return Page(state, [
        Header("Derivative/Integral Helper"),
        "\n \n Enter your polynomial in terms of x:",
        TextBox("function"),
        Button("Check Function", "is_valid_function"),
        "\n \n",
        Button("History", "history"),
        Button("User Guidelines", "user_guidelines")
        ])

assert_equal(index(State(function='', operation='', bounds='', result='', history=[])),
    Page(State(function='', operation='', bounds='', result='', history=[]), [
        Header('Derivative/Integral Helper'),
        '\n \n Enter your polynomial in terms of x:',
        TextBox('function'),
        Button('Check Function', 'is_valid_function'),
        '\n \n',
        Button('History', 'history'),
        Button('User Guidelines', 'user_guidelines'),
    ]))


@route
def is_valid_function(state: State, function: str) -> Page:
    """
        Checks to make sure the user inputted a polynomial function that can be correctly manipulated by the program.
        
        Args:
            state(State): the current state of the function.
            function(str): the user's inputted polynomial. 
            
        Returns:
            Page: either a page allowing the user to continue to choosing to integrate/derive or an error page.
    """
    state.function = function
    function = function.strip()
    
    numbers = "1234567890"
    previous = ""
    result = True
    letters = "abcdefghijklmnopqrstuvwxyz"
    
    for index in function:
    
        index = index.lower()
        
        if index in numbers:
            if previous == "x":
                result = False
         
        elif index == "x":
            if previous == "x" or previous == "^":
                result =  False
        
        elif index in letters:
            result = False
           
        elif index == "+" or index == "-":
            if previous == "+" or previous == "-" or previous == "^":
                result = False
                
        elif index == "^":
            if previous == "^":
                result = False
                
        elif index == "*":
            if previous not in numbers:
                result = False
                
        previous = index
        
    if result == True:
        return Page(state, [
            Header("Valid Polynomial"),
            "\n \n would you like to derive or integrate your polynomial?",
            Button("Take Derivative", "derivative"),
            Button("Integrate", "integration_information"),
            "\n \n",
            Button("Return Home", "index")
            ])
    
    if result == False:
        return Page(state, [
            Header("Invalid Polynomial"),
            "\n \n The function you entered is invalid. Please look over the User Guidlines and try again.",
            Button("User Guidlines", "user_guidelines"),
            Button("Return Home", "index")
            ])
            
assert_equal(is_valid_function(State(function='2*x^2', operation='derivative', bounds='', result='4*x', history=[]), '2'),
    Page(State(function='2', operation='derivative', bounds='', result='4*x', history=[]), [
        Header('Valid Polynomial'),
        '\n \n would you like to derive or integrate your polynomial?',
        Button('Take Derivative', 'derivative'),
        Button('Integrate', 'integration_information'),
        '\n \n',
        Button('Return Home', 'index'),
    ]))


@route
def derivative(state: State) -> Page:
    """
        Computes the derivative of the inputted function and displays the answer on its own page.
        Updates the state's history and result.
        
        Args:
            state(State): the current state of the program.
            
        Returns:
            Page: a page displaying the derivative and a button to return home. 
    """
    state.operation = "derivative"
    x = sp.symbols("x")
    f = sp.simplify(state.function)
    derivative = sp.diff(f, x)
    
    state.result = str(derivative)
    
    new_calculation = Calculation(
        state.function,
        state.operation,
        state.bounds,
        state.result
        )
    
    state.history.append(new_calculation)
    
    return Page(state, [
        Header("The derivative is: " + str(derivative)),
        Button("Return Home", "index")
        ])

assert_equal(derivative(State(function='2*x^2', operation='', bounds='', result='', history=[])),
    Page(State(function='2*x^2',
          operation='derivative',
          bounds='',
          result='4*x',
          history=[Calculation(function='2*x^2',
                               operation='derivative',
                               bounds='',
                               result='4*x')]), [
        Header('The derivative is: 4*x'),
        Button('Return Home', 'index'),
    ]))


@route
def integration_information(state: State) -> Page:
    """
        Prompts the user to input the desired bounds of integration and connects to the integral page.
        
        Args:
            state(State): the current state of the program.
            
        Returns:
            Page: A page prompting user input and displaying a button to compute the integral once they
            have entered the bounds. 
    """
    state.operation = "integral"
    
    return Page(state, [
        Header("Enter the bounds of your integral:"),
        TextBox("bounds"),
        Button("Integrate", "integral")
        ])

assert_equal(integration_information(State(function='2', operation='derivative', bounds='', result='4*x', history=[])),
    Page(State(function='2', operation='integral', bounds='', result='4*x', history=[]), [
        Header('Enter the bounds of your integral:'),
        TextBox('bounds'),
        Button('Integrate', 'integral'),
    ]))


@route
def integral(state: State, bounds: str) -> Page:
    """
        Computes the integral of a function on the given bounds and displays the answer on it's own page.
        Updates the state's result and history.
        
        Args:
            state(State): the current state of the program.
            bounds(str): 2 user-inputted numbers representing the starting and end values of the integral.
            
        Returns:
            Page: a page with the computed answer and a button to return home. 
        
    """
    state.bounds = bounds
    x = sp.symbols("x")
    f = sp.simplify(state.function)
    bound = state.bounds.split(",")
    a = bound[0]
    b = bound[-1]
    integral = sp.integrate(f, (x, a, b))
    
    state.result = str(integral)
    
    new_calculation = Calculation(
        state.function,
        state.operation,
        state.bounds,
        state.result
        )
    
    state.history.append(new_calculation)
    
    return Page(state, [
        Header("The integral is: " + str(integral)),
        Button("Return Home", "index")
        ])

assert_equal(integral(State(function='2', operation='integral', bounds='', result='', history=[]), '0,10'),
    Page(State(function='2',
          operation='integral',
          bounds='0,10',
          result='20',
          history=[Calculation(function='2',
                               operation='integral',
                               bounds='0,10',
                               result='20')]), [
        Header('The integral is: 20'),
        Button('Return Home', 'index'),
    ]))
        

@route
def history(state: State) -> Page:
    """
        Forms a page that stores the history of each calculation in a drop-down menu. Gives user the option
        to delete or keep each previous calculation. 
        
        Args:
            state(State): the current state of the program.
            
        Returns:
            Page: A page displaying the current history state of the program, with options to delete history
            items or return home. 
            
    """
    options = []
    
    for i, calculation in enumerate(state.history):
        option = (str(i) + ": " + calculation.operation + " of " + calculation.function)
        options.append(option)
        
    return Page(state, [
        Header("Calculation History"),
        SelectBox("calculation", options),
        Button("Delete Selected", "delete_selected"),
        Button("Return Home", "index")
    ])
        
assert_equal(history(State(function='2*x^2', operation='derivative', bounds='', result='4*x', history=[Calculation(function='2*x^2', operation='derivative', bounds='', result='4*x')])),
    Page(State(function='2*x^2',
          operation='derivative',
          bounds='',
          result='4*x',
          history=[Calculation(function='2*x^2',
                               operation='derivative',
                               bounds='',
                               result='4*x')]), [
        Header('Calculation History'),
        SelectBox('calculation', ['0: derivative of 2*x^2'], ''),
        Button('Delete Selected', 'delete_selected'),
        Button('Return Home', 'index'),
    ]))


@route
def delete_selected(state: State, calculation: str) -> Page:
    """
        Identifies the calculation the user wants to delete from history and removes it from the history.
        
        Args:
            state(State): The current state of the program.
            calculation(str): The calculation that the user selects to delete.
        
        Returns:
            Page: the updated history page.

    """
    index = int(calculation.split(":")[0])
    
    if index >= 0 and index < len(state.history):
        state.history.pop(index)
    
    return history(state)

assert_equal(delete_selected(State(function='2*x^2', operation='derivative', bounds='', result='4*x', history=[Calculation(function='2*x^2', operation='derivative', bounds='', result='4*x')]), '0: derivative of 2*x^2'),
    Page(State(function='2*x^2',
          operation='derivative',
          bounds='',
          result='4*x',
          history=[]), [
        Header('Calculation History'),
        SelectBox('calculation', [], ''),
        Button('Delete Selected', 'delete_selected'),
        Button('Return Home', 'index'),
    ]))


@route
def user_guidelines(state: State) -> Page:
    """
        Defines a list of rules and displays a Page of the rules listed in bullets.
        
        Args:
            state(State): the current state of the program.
            
        Returns:
            Page: a page with a bulleted list of rules.
        
    """
    rules = [
        "All inputs must be in terms of x.",
        "All functions must be polynomials.",
        """For coefficients of x, there must be an asterek in between the number and the x.
            (ex: 2*x or 13*x^2)
        """,
        """Powers of x can be denoted as "x^2" or "x**2".
        """,
        """Bounds must be listed in a comma seperated list without spaces(ex: "0,10").
        """,
        "Have fun :)"
    ]
    
    return Page(state, [
        Header("User Guidelines:"),
        BulletedList(rules),
        Button("Return Home", "index")
        ])

assert_equal(user_guidelines(State(function='2*x^2', operation='derivative', bounds='', result='4*x', history=[])),
    Page(State(function='2*x^2',
          operation='derivative',
          bounds='',
          result='4*x',
          history=[]), [
        Header('User Guidelines:'),
        BulletedList(['All inputs must be in terms of x.',
                      'All functions must be polynomials.',
                      'For coefficients of x, there must be an asterek in between the number and the x.\n (ex: 2*x or 13*x^2)\n',
                      'Powers of x can be denoted as "x^2" or "x**2".\n',
                      'Bounds must be listed in a comma seperated list without spaces(ex: "0,10").\n',
                      'Have fun :)']),
        Button('Return Home', 'index'),
    ]))

    
start_server(State("", "", "", "", []))
