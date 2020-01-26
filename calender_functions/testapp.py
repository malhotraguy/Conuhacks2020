from flask import Flask, render_template, request, redirect

CASES = ['test1', 'test2', 'test3', 'test4']
app = Flask(__name__,template_folder="app/templates")


@app.route("/")
def template_test():
    return "hello"


@app.route("/Test")
def TestCases():
    return render_template('testcases.html', cases=CASES, title="Test Cases")


@app.route("/info", methods=['POST'])
def getinfo():
    if request.method == 'POST':
        print(request.form)
        test = request.form["checks"]

        return str(test)
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090, debug=True, use_reloader=True)
