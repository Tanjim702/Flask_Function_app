from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)
from sympy import *
x,y,z = symbols('x y z')
init_printing()


@app.route("/",methods=['GET','POST'])
def index():
    return render_template("home.html")

@app.route("/demo",methods=['GET','POST'])
def demo():
    return render_template("demo.html")

@app.route("/result-nth-term",methods=["POST"])   
def result():
    name_of_user = request.form.get("name_of_user") 
    iterable_list = []
    numbers = request.form.get("numbers")
    numbers = numbers.split(',')
    for num in numbers:
        if num != ',':
            iterable_list.append(int(num))  
    main_list = []
    filtered_list = []


    def get_new_list(arr):
        new_list = []
        for num in range(0,len(arr)-1):
            val = arr[num+1]-arr[num]
            new_list.append(val) 
        main_list.insert(len(main_list),new_list)

    def filter_list_from_empty_values(arr):
        for array in arr:
            if len(array) != 0:
                filtered_list.append(array)


    def find_all_lists(arr):
        for num in arr:
            if len(main_list) == 0:
                get_new_list(arr)
            get_new_list(main_list[len(main_list)-1])
        filter_list_from_empty_values(main_list)
        return filtered_list    

    find_all_lists(iterable_list)
    def factorial(num):
        val = 1
        n = num
        while n != 0:
            val = val * n
            n = n -1
        return val  
    def factorial_of_exp(num):
        exp = ''
        n = num
        while n != 0:
            exp = exp + '(x-{n})*'.format(n=n)
            n =n-1
        # sympied = sympify(exp[:-1])
        return  exp[:-1]
    def getFinalExpr():
        expr = '{}'.format(iterable_list[0])
        for arr in filtered_list:
            arrIndex = filtered_list.index(arr)
            deno = factorial(arrIndex+1)
            mult = arr[0]
            if mult>0:
                loopexpr = '(+{0}*'.format(mult)+'{}'.format(factorial_of_exp(arrIndex+1)) + '/{0})'.format(deno)
            else:
                loopexpr = '({0}*'.format(mult)+ '{}'.format(factorial_of_exp(arrIndex+1)) + '/{0})'.format(deno)

            expr = expr + '+({0})'.format(loopexpr)
            # expr = expr[:-1]   
        expr = sympify(expr)
        return expr
            
    last = factor(getFinalExpr())
    expandedform = expand(last)
    #latex format
    latexexpanded = '$${}$$'.format(latex(expandedform))
    finalLast = '$${0}$$'.format(latex(last)) 
    isLong = len(finalLast) > 60
    numbers_with_result = []
    return render_template("result.html",
                            finalExpand = latexexpanded,
                            finalExp = finalLast,
                            name_of_user=name_of_user,
                            numbers = iterable_list,
                            isLong=isLong)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)