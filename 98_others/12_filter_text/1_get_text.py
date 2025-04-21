import re


def filter_text():
  reg_replace1 = re.compile('Dialogue:.+?,,')
  reg_replace2 = re.compile(r'\\N.+\}')
  line_list = []

  with open('filter_text.txt', 'w', encoding='utf-8') as op: 
    with open('./target.ass', 'r', encoding='utf-8') as fp:
      for line in fp:
        line = re.sub(reg_replace1, "", line)
        line = re.sub(reg_replace2, " ", line)
        # print(line)
        op.write(line)
  
if __name__ == '__main__':
  filter_text()
  