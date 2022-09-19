from prometheus_client import Counter, Histogram, MetricsHandler
import requests
import logging

REQUESTS_COUNT = Counter('sample_external_url_up', 'Status request count', ['url'])
RESPONSE_TIMES = Histogram('sample_external_url_response_ms', 'Time spent processing a status page', ['url'])

class HttpHandler(MetricsHandler):
    '''
    Class description...
    '''
    def do_GET(self):
        '''
        Method description...
        '''
        urls = ['https://httpstat.us/200', 'https://httpstat.us/503']
        response_html = "<html><head><title>Status page</title></head><body>{}</body></html>"
        response_body = ""
        for url in urls:
            request_successful = 0
            response = requests.get(url)

            # Set user output to 1 and `increment` successful requests on 200 HTTP status code
            if response.status_code == 200:
                request_successful = 1
                self.inc_metric(REQUESTS_COUNT, url)

            # TODO Most probably we should add another metric and an else condition to count error responses, not in scope of this assessment

            # Set current response in milliseconds for user output and `observe` the respective value (in seconds)
            response_timi_millis = response.elapsed.microseconds/1000.0
            self.obs_metric(RESPONSE_TIMES, url, response.elapsed.total_seconds())

            response_body += self.get_html_response_for_url(url, request_successful, response_timi_millis)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(response_html.format(response_body), "utf-8"))

    def inc_metric(self, metric, url):
        '''
        Method description...
        '''
        try:
            metric.labels(url = url).inc()
        except Exception as e:
            logging.warning(f'Could not emit prometheus inc event. {e}')

    def obs_metric(self, metric, url, value):
        '''
        Method description...
        '''
        try:
            metric.labels(url = url).observe(value)
        except Exception as e:
            logging.warning(f'Could not emit prometheus observe event. {e}')

    def get_html_response_for_url(self, url, request_successful, response_timi_millis):
        '''
        Method description...
        '''
        response = "<p>{}{{url=\"{}\"}} = {}</p>".format(REQUESTS_COUNT.labels(url)._name, url, request_successful)
        response += "<p>{}{{url=\"{}\"}} = {}</p>".format(RESPONSE_TIMES.labels(url)._name, url, response_timi_millis)

        return response

