def read_csv(file):
    data = file.read().decode("utf-8")
    lines = data.splitlines()
    lines.pop(0)
    output = []

    for line in lines:
        output.append(line.split(';'))
    return output

def form_upload(title):
    return f'''
    <!doctype html>
    <title>{title}</title>
    <h1>{title}</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=csv>
      <input type=submit value=Upload>
    </form>
    '''