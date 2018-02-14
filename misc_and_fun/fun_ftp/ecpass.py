
def ecp(str_fn):
    num_l = 0
    dic_ecp = dict()
    with open(str_fn) as f:
        content = f.readlines()
    content = [x.strip() for x in content] # remove whitespace characters like \n
    for str_lin in content:
        num_l += 1
        lst_lin = [tok.strip() for tok in str_lin.split('#')[0].split(':')]
        if len(lst_lin) == 3: # All valid lines hold 3 tokens
            if lst_lin[0].lower() == 'conn':
                try:
                    int(lst_lin[1])
                    dic_ecp[int(lst_lin[1])] = {'_id_':lst_lin[2]} # dict()
                except:
                    print "ecpass Error: conn lable must be integer! Found {} after 'conn' in line {}".format(lst_lin[1], num_l)
                    continue
            else:
                try:
                    int(lst_lin[0])
                except:
                    print "ecpass Error: conn lable must be integer! Found {} in beginning of line {}".format(lst_lin[0], num_l)
                    continue
                if len(lst_lin[1]) > 0 : # and len(lst_lin[2]) > 0
                    dic_ecp[int(lst_lin[0])][lst_lin[1].strip().lower()] = lst_lin[2]
        ##print lst_lin
    return dic_ecp