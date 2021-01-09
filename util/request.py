import requests
from urllib.parse import urlencode
from util.common import *
from util.log import get_logger


class Request(object):
    logger = get_logger()

    def get_request(self, url, data=None, headers=None):
        '''
        get请求
        :param url:
        :param data:
        :param headers:
        :return:
        '''

        data = format_data(data)
        headers = format_data(headers)

        if not url.startswith('http://'):
            url = f"http://{url}"

        try:
            if data is None:
                response = requests.get(url, headers=headers)
                self.logger.info(response.text)
                return response
            else:
                response = requests.get(url, params=data, headers=headers)
                self.logger.info(data)
                self.logger.info(response.text)
                return response

        except requests.RequestException as e:
            print(f'RequestException url: {url}')
            self.logger.error(e)
            print(f"http请求报错:{e}")

    def post_request(self, url, data=None, headers=None, content_type=None):
        '''
        post请求
        :param url:
        :param data:
        :param headers:
        :return:
        '''

        data = format_data(data)
        headers = format_data(headers)

        if not url.startswith("http://"):
            url = f"http://{url}"

        try:
            if data is None:
                response = requests.post(url, headers=headers)
                self.logger.info(response.text)
                return response
            else:
                if content_type == 'json':
                    response = requests.post(url, json=data, headers=headers)
                    self.logger.info(data)
                    self.logger.info(response.text)
                    return response
                else:
                    response = requests.post(url, data=data, headers=headers)
                    self.logger.info(data)
                    self.logger.info(response.text)
                    return response

        except requests.RequestException as e:
            print(f'RequestException url: {url}')
            self.logger.error(e)
            print(f"http请求报错:{e}")

    def delete_request(self, url, data, headers=None):
        '''
        delete请求
        :param url:
        :param data:
        :param headers:
        :return:
        '''

        data = format_data(data)
        headers = format_data(headers)

        if not url.startswith("http://"):
            url = f"http://{url}?{urlencode(data)}"
        else:
            url = f"{url}?{urlencode(data)}"
        try:
            response = requests.delete(url, headers=headers)
            self.logger.info(url)
            self.logger.info(response.text)
            return response

        except requests.RequestException as e:
            print(f'RequestException url: {url}')
            self.logger.error(e)
            print(f"http请求报错:{e}")

    def put_request(self, url, data=None, headers=None):
        '''
        put请求
        :param url:
        :param data:
        :param headers:
        :return:
        '''

        data = format_data(data)
        headers = format_data(headers)

        if not url.startswith("http://"):
            url = f"http://{url}"

        try:
            if data is None:
                response = requests.put(url, headers=headers)
                self.logger.info(response.text)
                return response
            else:
                response = requests.put(url, data=data, headers=headers)
                self.logger.info(data)
                self.logger.info(response.text)
                return response

        except requests.RequestException as e:
            print(f'RequestException url: {url}')
            self.logger.error(e)
            print(f"http请求报错:{e}")

    def patch_request(self, url, data=None, headers=None):
        '''
        put请求
        :param url:
        :param data:
        :param headers:
        :return:
        '''

        data = format_data(data)
        headers = format_data(headers)

        if not url.startswith("http://"):
            url = f"http://{url}"

        try:
            if data is None:
                response = requests.patch(url, headers=headers)
                self.logger.info(response.text)
                return response
            else:
                response = requests.patch(url, data=data, headers=headers)
                self.logger.info(data)
                self.logger.info(response.text)
                return response

        except requests.RequestException as e:
            print(f'RequestException url: {url}')
            self.logger.error(e)
            print(f"http请求报错:{e}")

    def post_request_multipart(self, url, file_name, headers=None, data=None, content_type=None):
        '''
        post上传文件
        :param url:
        :param data:
        :param headers:
        :param file_name:
        :return:
        '''

        data = format_data(data)
        headers = format_data(headers)

        if not url.startswith("http://"):
            url = f"http://{url}"

        try:
            if "." not in file_name:
                file_name, path = get_full_file_name(file_name)
            else:
                file_name, path = check_file_suffix(file_name)

            files = {'file': open(path + file_name, 'rb')}

        except Exception as e:
            self.logger.error(e)
            print(e)
            return

        try:
            if data is None:
                response = requests.post(url, headers=headers, files=files)
                self.logger.info(response.text)
                return response
            else:
                if content_type == 'json':
                    response = requests.post(url, json=data, headers=headers, files=files)
                    self.logger.info(data)
                    self.logger.info(response.text)
                    return response
                else:
                    response = requests.post(url, data=data, headers=headers, files=files)
                    self.logger.info(data)
                    self.logger.info(response.text)
                    return response

        except requests.RequestException as e:
            print(f'RequestException url: {url}')
            self.logger.error(e)
            print(f"http请求报错:{e}")
