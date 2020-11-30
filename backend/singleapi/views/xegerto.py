# 作者      : pengcheng
# 创建时间  : 2020/11/25 15:51 

import random
from xeger import Xeger



def generateChr():
    #gbk2312对字符的编码采用两个字节相组合, 第一个字节的范围是0xB0 - 0xF7, 第二个字节的范围是0xA1 - 0xFE.在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
    temp='{0:x} {1:x}'.format(random.randint(0xb0, 0xf7), random.randint(0xa1, 0xf9) )
    chr=bytes.fromhex(temp).decode('gb2312')
    return chr


'''
@功能:随机生成指定长度，类型的字符串
@入参：
        num:生成的字符串长度
        length:生成的字符串长度
        category:生成的字符串类型
        pure_num代表纯数字，pure_alph代表纯字母,pure_chr代表纯汉字（当前有局限，生成的汉字是不变的）,num_alph代表数字+字母的组合,num_chr代表数字+汉字的组合,alph_chr代表字母+汉字的组合,num_alph_chr代表字母+汉字+数字的组合
'''
class GenerateStr(object):

    def __init__(self,category,num,length=10):
        self.length=length
        self._cateory=category
        self.num=num
        self._categories = {
            "pure_num": r'[0-9]{%d}'%self.length,
            "pure_alph": r'[a-zA-Z]{%d}'%self.length,
            "num_alph": r'[a-zA-Z0-9]{%d}'%self.length,
            "pure_chr": r'[%s]{%d}'%(generateChr(), self.length),
            "num_chr":r'[0-9%s]{%d}'%(generateChr(), self.length),
            "alph_chr":r'[a-zA-Z%s]{%d}'%(generateChr(), self.length),
            "num_alph_chr":r'[a-zA-Z0-9%s]{%d}'%(generateChr(), self.length)
        }

    def _chooseCategory(self):
        try:
            choose_category=self._categories[self._cateory]
        except KeyError:
            print("sorry,the input is uncorrect!")
            choose_category=r'please rewrite the category'
        return choose_category

    def _generateStr(self):

        gen_str=[0 for _ in range(self.num)]
        str_xeger=Xeger(limit=10)
        str=self._chooseCategory()

        for i in range(0,self.num):
            gen_str[i]=str_xeger.xeger(str)
            print(gen_str[i])
        return gen_str


    def getStr(self):
        result=self._generateStr()
        return result


if __name__=='__main__':
    x=GenerateStr('pure_chr',1,100)        #生成符合字母+数字的组合的字符串，长度为100，共7个
    print(x.getStr())