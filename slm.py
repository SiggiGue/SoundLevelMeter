import tornado.ioloop
import tornado.web
import tornado.websocket
import webbrowser

from tornado.options import define, options, parse_command_line

from pysoundcard import Stream, continue_flag
import numpy as np


sample_rate = 44100
block_length = 2048
tau = 0.1

define("port", default=8888, help='run on the given port', type=int)


class SlmWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")
        self.set_exponential_smoothing_tau(tau=tau)
        self.init_stream(sample_rate=sample_rate,
                         block_length=block_length)
        self.start_stream()

    def on_message(self, message):

        if '#start#' in message:
            self.start_stream()

        if '#stop#' in message:
            self.stop_stream()

        if '#set_tau#' in message:
            msg = message.split()
            print(msg)
            if len(msg)>1:
                tau = float(msg[1])
                self.set_exponential_smoothing_tau(tau)

    def on_close(self):
        print("Websocket is closed")

    def set_exponential_smoothing_tau(self, tau):
        if tau > 0:
            alpha = np.exp(-1.0/(tau*(sample_rate/block_length)))
            self._b0 = 1 - alpha
            self._a1 = -alpha
            print("Tau accepted.")
        else:
            print("Tau '{}' not accepted.".format(tau))


    def init_stream(self, sample_rate, block_length):
        self._psc_sample_rate = sample_rate
        self._psc_block_length = block_length
        self._level = -120

        def callback(in_data, frame_count, time_info, status):
            new_value = self._b0*np.mean(in_data**2)  - self._a1*10**(self._level*0.1)
            self._level = 10*np.log10(new_value)
            self.write_message('{:.1f}'.format(self._level))
            return in_data, continue_flag

        self._psc_stream = Stream(
            callback=callback,
            sample_rate=self._psc_sample_rate,
            block_length=self._psc_block_length,
            output_device=False
        )

    def start_stream(self):
        if not self._psc_stream.is_active():
            print('Start stream')
            self._psc_stream.start()

    def stop_stream(self):
        if self._psc_stream.is_active():
            print('Stop stream')
            self._psc_stream.stop()

app = tornado.web.Application([(r'/', SlmWebSocket),])

if __name__=='__main__':
    parse_command_line()
    app.listen(options.port)
    webbrowser.open_new_tab('slm.html')
    tornado.ioloop.IOLoop.instance().start()
