import  requests
from lxml.html import etree

class GetCityWeather:
    def __init__(self,city):
        self.url = self.search_city(city)
        self.html = None
    # 查询城市,返回城市URL
    def search_city(self,city):
        url  = 'http://www.tianqi.com/tianqi/search'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        response =  requests.get(url,params={'keyword':city}, headers=headers )
        return response.url
    # 获取页面主体
    def get_page(self):
        response = requests.get(self.url)
        if '404' in response.url:
            return   {
                'status':404
        }
        # if :
        print(response.content.decode())
        self.html = etree.HTML(response.content.decode())

        return  self.get_weather()
    def get_weather(self):
        city = self.html.xpath('/html/body/div[5]/div/div[1]/dl/dd[1]/h2')
        date = self.html.xpath('/html/body/div[5]/div/div[1]/dl/dd[2]')
        weather = self.html.xpath("/html/body/div[5]/div/div[1]/dl/dd[3]/span/b")
        temperture = self.html.xpath('/html/body/div[5]/div/div[1]/dl/dd[3]/span/text()')
        humidity = self.html.xpath('/html/body/div[5]/div/div[1]/dl/dd[4]/b[1]')
        wind = self.html.xpath('/html/body/div[5]/div/div[1]/dl/dd[4]/b[2]')
        uv = self.html.xpath('/html/body/div[5]/div/div[1]/dl/dd[4]/b[3]')
        air = self.html.xpath('/html/body/div[5]/div/div[1]/dl/dd[5]/h5')
        pm = self.html.xpath('/html/body/div[5]/div/div[1]/dl/dd[5]/h6')


        return {
            '城市':city[0].text,
            '日期':(date[0].text).replace('\u3000','  '),
            '天气':weather[0].text,
            '温度':temperture[0],
            '湿度':humidity[0].text,
            '风向':wind[0].text,
            '紫外线':uv[0].text,
            '空气质量':air[0].text,
            'PM':pm[0].text,
        }


class GetExpress:
    def __init__(self,text):
        self.text = text
        self.url = 'http://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text={}'.format(self.text)
        self.data = None
        self.follow = ''

    def get_express(self):
        res = requests.get(self.url)
        comCodes = res.json()['auto']
        for comCode in comCodes:
            self.data = self.get_logistics(comCode['comCode'])
            if self.data:
                break
        else:
            if not self.data:
                return '未查询到数据,可能是单号过期或单号输入错误'

        for data in self.data:
            self.follow += data['time'] + '|' + data['context'] + '\n'
        return self.follow

    def get_logistics(self,comCode):

        self.query_url = 'http://www.kuaidi100.com/query?type={}&postid={}'.format(comCode, self.text)
        res = requests.get(self.query_url)
        data = res.json()['data']

        if data:
            return data
        return  None


if __name__ == '__main__':
    express = GetExpress('669474685215')
    print(express.get_express())