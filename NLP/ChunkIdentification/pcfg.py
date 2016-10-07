# -*- coding: utf-8 -*-

class PCFG(object):
    def __init__(self, non_ternimal, terminal, rules_prob, start_prob):
        self.non_terminal = non_ternimal
        self.terminal = terminal
        self.rules_prob = rules_prob
        self.start_symbol = start_prob


    def parse_sentence(self, sentence):
        sents = sentence.split()
#         best_path = [[{}]*len(sents)]*len(sents)    # Error!! 共享同一块内存区域!!
        best_path = [[{} for _ in range(len(sents))] for _ in range(len(sents))]

        # initialization
        for i in range(len(sents)):
            for x in self.non_terminal:
                best_path[i][i][x] = {}
                if (sents[i],) in self.rules_prob[x].keys():
                    best_path[i][i][x]['prob'] = self.rules_prob[x][(sents[i],)]
                    best_path[i][i][x]['path'] = {'split':None, 'rule': sents[i]}
                else:
                    best_path[i][i][x]['prob'] = 0
                    best_path[i][i][x]['path'] = {'split':None, 'rule': None}

        # CKY recursive
        for l in range(1, len(sents)):
            for i in range(len(sents)-l):
                j = i + l
                for x in self.non_terminal:
                    tmp_best_x = {'prob':0, 'path':None}
                    for key, value in self.rules_prob[x].iteritems():
                        if key[0] not in self.non_terminal: 
                            break
                        for s in range(i, j):
                            tmp_prob = value * best_path[i][s][key[0]]['prob'] * best_path[s+1][j][key[1]]['prob']
                            if tmp_prob > tmp_best_x['prob']:
                                tmp_best_x['prob'] = tmp_prob
                                tmp_best_x['path'] = {'split': s, 'rule': key}
                    best_path[i][j][x] = tmp_best_x
        self.best_path = best_path

        # parse result
        self._parse_result(0, len(sents)-1, self.start_symbol)
        print "prob = ", self.best_path[0][len(sents)-1][self.start_symbol]['prob']


    def _parse_result(self, left_idx, right_idx, root, ind=0):
        node = self.best_path[left_idx][right_idx][root]
        if node['path']['split'] is not None:
            print '\t'*ind, (root, self.rules_prob[root].get(node['path']['rule']))
            self._parse_result(left_idx, node['path']['split'], node['path']['rule'][0], ind+1)
            self._parse_result(node['path']['split']+1, right_idx, node['path']['rule'][1], ind+1)
        else:
            print '\t'*ind, (root, self.rules_prob[root].get((node['path']['rule'],))), 
            print '--->', node['path']['rule']



def main():
    non_terminal = {'S', 'NP', 'VP', 'PP', 'DT', 'Vi', 'Vt', 'NN', 'IN'}
    start_symbol = 'S'
    terminal = {'sleeps', 'saw', 'man', 'woman', 'dog', 'telescope', 'the', 'with', 'in'}
    rules_prob = {'S': {('NP', 'VP'): 1.0},
                  'VP': {('Vt', 'NP'): 0.8, ('VP', 'PP'): 0.2},
                  'NP': {('DT', 'NN'): 0.8, ('NP', 'PP'): 0.2},
                  'PP': {('IN', 'NP'): 1.0},
                  'Vi': {('sleeps',): 1.0},
                  'Vt': {('saw',): 1.0},
                  'NN': {('man',): 0.1, ('woman',): 0.1,('telescope',): 0.3,('dog',): 0.5},
                  'DT': {('the',): 1.0},
                  'IN': {('with',): 0.6, ('in',): 0.4},
                }
    pcfg = PCFG(non_terminal, terminal, rules_prob, start_symbol)
    sentence = "the man saw the dog with the telescope"
    pcfg.parse_sentence(sentence)


if __name__ == "__main__":
    main()
