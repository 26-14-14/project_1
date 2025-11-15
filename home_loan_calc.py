# Home Loan Calculator - project_1

from flask import Flask, render_template, request, redirect, url_for


def calculate_monthly_payment(principal: float, annual_rate: float, years: float) -> float:
    """ Calculates the fixed monthly mortgage payment using the amortization formula.

    Args:
        principal (float): Total Amount of the loan borrowed (the present value).
        annual_rate (float): Yearly Interest Rate expressed as a decimal (e.g., 0.05 for 5%).
        years (float): Total duration of the loan in years.

    Returns:
        float: Fixed Monthly Payment Amount.
    """

    # 1. Convert annual rate percentage to monthly decimal rate
    monthly_rate = (annual_rate / 100) / 12

    # 2. Calculate total number of payments (months)
    number_of_payments = years * 12

    # Handle the zero interest rate case to prevent division by zero
    if monthly_rate == 0:
        return principal / number_of_payments

    # 3. Apply the standard mortgage formula
    # Factor is r(1+r)^n
    factor = monthly_rate * pow(1 + monthly_rate, number_of_payments)

    # Denominator is (1+r)^n - 1
    denominator = pow(1 + monthly_rate, number_of_payments) - 1

    monthly_payment = principal * (factor / denominator)

    return round(monthly_payment, 2)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """Initialize the result variable.

    Returns:
        str: The HTML content of the main loan calculator page, which includes 
             the form and, optionally, the calculated monthly payment result.
    """
    monthly_payment = None

    if request.method == 'POST':
        try:
            # All lines inside the 'try' block must be indented four spaces (or one tab)
            loan_amount = float(request.form['loan_amount'])
            interest_rate = float(request.form['interest_rate'])
            loan_term_years = int(request.form['loan_term_years'])

            # Basic server-side validation
            if loan_amount <= 0 or interest_rate < 0 or loan_term_years <= 0:
                # Note: This return line is inside the try block
                return render_template('index.html', error="All values must be positive and non-zero.")

            # Calculate the payment
            monthly_payment = calculate_monthly_payment(
                loan_amount,
                interest_rate,
                loan_term_years
            )

        except ValueError:
            # The 'except' statement must be at the SAME indentation level as 'try'
            return render_template('index.html', error="Invalid input. Please enter only numeric values.")
        
      # This return statement is OUTSIDE the 'if' block and handles the GET request,
      # and the final rendering for a successful POST.
    return render_template('index.html', monthly_payment=monthly_payment)
    
if __name__ == '__main__':
    app.run(debug=True)
