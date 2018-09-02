from urllib import request
from bs4 import BeautifulSoup
import re

# headers = {
#     'User-Agent':
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
# }


def isAlphabet(uchar):
    """
        判断是否为英文字母
    """
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


def percentageToFloat(value):
    """
        example: (str)50.2% -> (str)0.502
    """
    value = float(value.replace("%", ""))
    return str(float(value) / 100)


def formatStats(stats):
    size = len(stats)

    if size == 0:
        return stats

    index = 0
    while (index < size):
        if ("%" in stats[index]):
            # 百分数->小数
            stats[index] = percentageToFloat(stats[index])
        index += 1

    index = 0
    while (index < size):
        if ("-" in stats[index]):
            # 5.0-10.2 -> 5.0, 10.2
            # FGM=Free Goal Made( 投篮命中数) FGA=Free Goal Attempt( 投篮尝数次数)
            fgm, fga = stats[index].split("-")
            stats[index] = fgm
            stats.insert(index + 1, fga)
            index += 1
        index += 1

    return stats


# def getHtml(url):
#     global headers
#     page = request.Request(url, headers=headers)
#     return request.urlopen(page).read().decode('utf-8')


def getStatsByUrl(url):

    html = getHtml(url)

    # 分析文本，获取常规赛场均数据
    soup = BeautifulSoup(html, "lxml")

    # 球员姓名
    playerName = soup.find("h2").getText()
    playerName = "".join(
        [each if isAlphabet(each) else "" for each in playerName])

    table = soup.find("table", "players_table bott")

    trs = table.find_all("tr")
    # 如果tr只有两组，证明该球员没有数据，用0填充
    if (len(trs) <= 2):
        playerStats = ["0.0"] * 18
    else:
        tr = table.find_all("tr")[-1]  # 取三组tr中最后一个（赛季平均数据）
        playerStats = [td.getText() for td in tr.find_all("td")]  # 存入数组

    return playerName, playerStats


def getPlayerUrlsByTeamUrl(url):
    html = getHtml(url)
    soup = BeautifulSoup(html, "lxml")
    for each in soup.find_all("div", "x_list"):
        text = str(each.find("a"))
        if "https" in text:
            # 提取连接
            yield re.search('.+href="(.+)" target.+', text).group(1)


def getTeamUrls(url):
    html = getHtml(url)
    soup = BeautifulSoup(html, "lxml")

    for each in soup.find_all("div", "team"):
        text = str(each)
        if "https" in text:
            # 提取连接
            for url in re.findall('.+href="(.+)" target.+', text):
                yield url
