import csv
from danmu import get_danmu
from pinglun import get_pinglun

if __name__ == "__main__":
    av_list = []
    f = open("./downloader/av_list")
    line = f.readline()
    while line:
        av_list.append(line.strip('\n'))
        line = f.readline()
    f.close()
    for av in av_list:
        out_path1 = f'./data/av{av}_dm.csv'
        out_path2 = f'./data/av{av}.csv'
        danmu_list = get_danmu(av)
        pinglun_list = get_pinglun(av)
        for danmu in danmu_list:
            with open(out_path1, 'a', encoding='utf-8') as sw:
                sw.write(danmu.join('\n\n'))
        with open(out_path2, 'a', encoding='utf-8') as sw:
            fieldnames = ['author', 'message']
            writer = csv.DictWriter(sw, fieldnames=fieldnames)
            writer.writerows(pinglun_list)
