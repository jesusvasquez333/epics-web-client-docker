from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
from io import BytesIO
import epics
import os

counter = 1

def getIOCUpTimeCnt(prefix):
    c = epics.caget(f"{prefix}:upTimeCnt", timeout=0.5)

    if c == None:
        return '<font color="red">Off line</font>'
    else:
        return f'<font color="green">{c}</font>'

app = Flask(__name__)

def getIOCSignalPlot(prefix):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    #xs = range(100)
    #ys = [random.randint(1, 50) for x in xs]

    ys = epics.caget(f'{prefix}:signal', timeout=0.5)

    if ys is not None:
        xs = range(len(ys))
        axis.plot(xs, ys)
        axis.legend([f'{prefix}:signal'])

    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route('/plot1.png')
def plot1():
    return getIOCSignalPlot('ioc1')

@app.route('/plot2.png')
def plot2():
    return getIOCSignalPlot('ioc2')

@app.route('/plot3.png')
def plot3():
    return getIOCSignalPlot('ioc3')

@app.route("/")
def hello():
    global counter
    counter += 1
    return f"""
        <head>
          <title>EPICS Web Client Example</title>
        </head>
        <body>
          <meta http-equiv="refresh" content="5">
          <h1>EPICS Web Client Example using Flask + PyEPICS</h1>
          <h2>IOC Up Time Counters</h2>
          <table>
            <tr>
              <th>IOC prefix</th>
              <th>Up time counter (seconds)</th>
            </tr>
            <tr>
              <th>ioc1</th>
              <th>{getIOCUpTimeCnt('ioc1')}</th>
            </tr>
            <tr>
              <th>ioc2</th>
              <th>{getIOCUpTimeCnt('ioc2')}</th>
            </tr>
            <tr>
              <th>ioc3</th>
              <th>{getIOCUpTimeCnt('ioc3')}</th>
            </tr>
          </table>
          </table>

          <h2>IOC Signals</h2>

          <table>
            <tr>
              <th>ioc1</th>
              <th>ioc2</th>
              <th>ioc3</th>
            </tr>
            <tr>
              <th><img src="/plot1.png" alt="my plot"></th>
              <th><img src="/plot2.png" alt="my plot"></th>
              <th><img src="/plot3.png" alt="my plot"></th>
            </tr>
          </table>

        <p><i>Cotainer ID = {os.uname()[1]}</i></p>
        </body>"""


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
