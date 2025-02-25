import ssl
from urllib.request import Request, urlopen


def getUnsecureContext():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    return ctx

cache = {}

def get_url(url) -> str:

    if url not in cache:
        ssl_context = getUnsecureContext()
        request = Request(url)

        try:
            file = urlopen(request, context=ssl_context)
            data = file.read()
            file.close()
        except BaseException as e:
            raise BaseException(e)

        cache[url] = data.decode("utf-8")

    return cache[url]


def main(url):
    data = get_url(url)
    print(data)
    return data


if __name__ == "__main__":
    main("https://www.fega.gob.es/atom/2024/rec_2024")
