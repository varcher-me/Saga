from flask import Flask,render_template,request,redirect,url_for
import os

app = Flask(__name__)


def secure_filename(filename):
    _windows_device_files = ('CON', 'AUX', 'COM1', 'COM2', 'COM3', 'COM4', 'LPT1',
                             'LPT2', 'LPT3', 'PRN', 'NUL')
    # if isinstance(filename, str):
    #     from unicodedata import normalize
    #     filename = normalize('NFKD', filename).encode('ascii', 'ignore')
    #     filename = filename.decode('ascii')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')

    # filename = str(_filename_ascii_strip_re.sub('', '_'.join(
    #                filename.split()))).strip('._')

    # on nt a couple of special files are present in each folder.  We
    # have to ensure that the target file is not such a filename.  In
    # this case we prepend an underline
    if os.name == 'nt' and filename and \
       filename.split('.')[0].upper() in _windows_device_files:
        filename = '_' + filename

    return filename


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        print("AAA")
        print(request)
        print(request.files['file'])
        print("BBB")
        f = request.files['file']
        print(f.filename)
        upload_path = os.path.join('d:/temp/init/', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
