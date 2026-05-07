def html_form(result=""):
    return """
    <html>
    <body>
        <h2>Simple Calculator</h2>

        <form method="post">
            Number 1: <input type="text" name="n1"><br><br>
            Number 2: <input type="text" name="n2"><br><br>

            <input type="submit" name="op" value="Add">
            <input type="submit" name="op" value="Subtract">
            <input type="submit" name="op" value="Multiply">
            <input type="submit" name="op" value="Divide">
        </form>

        <h3>Result: {}</h3>
    </body>
    </html>
    """.format(result)


def application(environ, start_response):
    method = environ.get('REQUEST_METHOD', 'GET')

    if method == 'GET':
        response = html_form()

    else:
        size = int(environ.get('CONTENT_LENGTH', 0))
        data = environ['wsgi.input'].read(size).decode()

        params = {}
        for pair in data.split('&'):
            if '=' in pair:
                k, v = pair.split('=')
                params[k] = v

        try:
            n1 = float(params.get('n1', 0))
            n2 = float(params.get('n2', 0))
        except:
            n1, n2 = 0, 0

        op = params.get('op', '')

        if op == "Add":
            result = n1 + n2
        elif op == "Subtract":
            result = n1 - n2
        elif op == "Multiply":
            result = n1 * n2
        elif op == "Divide":
            result = n1 / n2 if n2 != 0 else "Cannot divide by zero"
        else:
            result = "Invalid Operation"

        response = html_form(result)

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [response.encode()]