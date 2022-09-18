from prometheus_client import Counter, Histogram, MetricsHandler
import requests
import logging

REQUESTS_COUNT = Counter('sample_external_url_up', 'Status request count', ['url'])
RESPONSE_TIMES = Histogram('sample_external_url_response_ms', 'Time spent processing a status page', ['url'])

# DISCLAIMER
#
# In the assignment description it is mentioned that the service queries 2 URLs
# then also that it will check the respective URLs
# It is not clear whether the service will check all URLs at once or based on some query (in the format of self.path for example)
# Then in the expected output you show results for both URLs, but with different counters
# For the time being the service queries both URLs at once, thus the Counter metric will always increase for both
# If that matters maybe we can elaborate more in an online discussion...

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
            response = requests.get(url)

            # Assignment mentions check if the two urls are up (based on http status code 200),
            # but apparently https://httpstat.us/503 returns 503... as expected!
            if response.status_code not in [ 200, 503 ]:
                # Most probably we would like to implement some error handling here
                # But not in the scope of this home assignment
                return

            response_timi_millis = response.elapsed.microseconds/1000.0
            self.inc_metric(REQUESTS_COUNT, url)
            self.obs_metric(RESPONSE_TIMES, url, response_timi_millis)

            response_body += self.get_html_response_for_url(url, response_timi_millis)

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

    def get_html_response_for_url(self, url, response_timi_millis):
        '''
        Method description...
        '''
        response = "<p>{}{{url=\"{}\"}} = {}</p>".format(REQUESTS_COUNT.labels(url)._name, url, int(REQUESTS_COUNT.labels(url)._value.get()))
        response += "<p>{}{{url=\"{}\"}} = {}</p>".format(RESPONSE_TIMES.labels(url)._name, url, response_timi_millis)

        return response

