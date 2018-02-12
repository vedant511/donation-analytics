# Time Complexity = O(n)

# Importing the libraries to be used
import numpy as np


# This method validates the input fields and returns True if all is fine, else False
def validate(cid, name, zip_code, date, amt, other):
    if len(other) > 0:
        return False

    if not len(cid):
        return False

    if not len(name):
        return False

    if not len(amt):
        return False

    if len(zip_code) < 5:
        return False

    if len(date) != 8:
        return False

    return True


# This method calculates the required fields whenever a repeating donor is found
def calculate(cid, year, pin, rep_donors, donor_rec, recip_rec, percentile):
    total_trans = []
    for donor in recip_rec[cid][year]:
        if donor in rep_donors and donor[1] == pin:
            total_trans.extend(recip_rec[cid][year][donor]['transaction_list'])

    out = cid + "|" + pin + "|" + year + "|"

    out += str(np.percentile(sorted(total_trans), percentile, interpolation='nearest'))
    out += "|"

    out += str(sum(total_trans))
    out += "|"

    out += str(len(total_trans))
    out += "\n"

    return out


# This method saves the content in output file
def write_output(out):
    with open("output/repeat_donors.txt", 'a') as f:
        f.write(out)


# This method processes each record from input
def process(inp, percentile, rep_donors, donor_rec, recip_rec):

    fields = inp.split('|')
    cid = fields[0]
    name = fields[7]
    zip_code = fields[10]
    date = fields[13]
    amt = fields[14]
    other = fields[15]

    if validate(cid, name, zip_code, date, amt, other):
        pin = zip_code[:5]
        year = date[-4:]
        if cid not in recip_rec:
            recip_rec[cid] = {year: {(name, pin): {'transaction_list': [int(amt)]}}}
            
        elif year not in recip_rec[cid]:
            recip_rec[cid][year] = {(name, pin): {'transaction_list': [int(amt)]}}
        
        elif (name, pin) not in recip_rec[cid][year]:
            recip_rec[cid][year][(name, pin)] = {'transaction_list': [int(amt)]}
        
        else:
            recip_rec[cid][year][(name, pin)]['transaction_list'].append(int(amt))
                        
        if (name, pin) not in donor_rec:
            donor_rec[(name, pin)] = {year: {cid: {'transaction_list': [int(amt)]}}}

        else:
            rep_donors.append((name, pin))
            if year not in donor_rec[(name, pin)]:
                donor_rec[(name, pin)][year] = {cid: {'transaction_list': [int(amt)]}}

            elif cid not in donor_rec[(name, pin)][year]:
                donor_rec[(name, pin)][year][cid] = {'transaction_list': [int(amt)]}
            
            else:
                donor_rec[(name, pin)][year][cid]['transaction_list'].append(int(amt))

            write_output(calculate(cid, year, pin, rep_donors, donor_rec, recip_rec, percentile))


# Read the percentile and lines for current input chunk. The lines will be processed one at a time.
with open("input/percentile.txt", 'r') as f:
    per = f.read(2)

with open("input/itcont.txt", 'r') as f:
    repeated_donors = []
    record_by_donor = dict()
    record_by_recipient = dict()

    for line in f:
        process(line, per, repeated_donors, record_by_donor, record_by_recipient)
