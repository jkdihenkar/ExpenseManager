import pygrok
import subprocess

class ImportFromWhatsApp:

    def __init__(self):

        self.not_split_pattern_simple = ' %{GREEDYDATA:ssv_user}\ %{NUMBER:amount}\ to\ %{WORD:to_user}\ %{GREEDYDATA:comment}'
        self.not_split_pattern_boxed_simple = ' %{GREEDYDATA:ssv_user}\ \[%{NUMBER:amount}\]\ to\ %{WORD:to_user}\ %{GREEDYDATA:comment}'
        self.split_pattern = ' %{GREEDYDATA:ssv_user}\ %{NUMBER:amount}/%{NUMBER:num_people}\ to\ %{WORD:to_user}\ %{GREEDYDATA:comment}'

        self.parser_simple = pygrok.Grok(self.not_split_pattern_simple)
        self.parser_boxed_simple = pygrok.Grok(self.not_split_pattern_boxed_simple)
        self.pattern_boxed_simple = pygrok.Grok(self.split_pattern)

    def parseObject(self, line):

        m = self.parser_simple.match(line)

        if m is None or not m == {}:
            print(m)
            print(m['ssv_user'])
            print(m['amount'])
            print(m['to_user'])
            print(m['comment'])
            cmd = './exec group '
            print('Running {}')
        else:
            print("Parse fail")

if __name__ == '__main__':
    p = ImportFromWhatsApp()
    p.parseObject(' parth 10 to hdk for teaAfterNoon')
