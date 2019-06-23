# Translating formulas from text format to CCLITP syntax 
# Operators and clauses are expected to be separated by spaces
# e.g. A and B not AandB, ( A or B ) not (A or B)

#form = input()
#form_l = form.split(" ")
#print(form_l)

# Code inspired from CLAC hw for 15-122 
## Make sure that the "stack" we have only has values of higher precedence 
def prec(x):
    if x == "and":
        return 1
    elif x == "or":
        return 2
    elif x == "imply":
        return 3
    else:
        return 100

def is_precstack(S):
    prestack = True
    tmp = []
    if (S == []):
        return True
    x = S[0]
    S = S[1:]
    y = ""
    tmp = [x] + tmp
    while (S != []):
        x = S[0]
        S = S[1:]
        y = tmp[0]
        tmp = tmp[1:]
        if (prec(x) >= prec(y)):
            prestack = False
        tmp = [y] + tmp
        tmp = [x] + tmp
    while (tmp != []):
        S = [tmp[0]] + S
        tmp = tmp[1:]
    return prestack

## Tranforms a formula_list splitted by spaces to a syntax similar to CLAC programming language
def syntax(form):
    output = []
    output_final = []
    prestack = []
    current = 0
    clause_phase = True
    while (form != []):
        if form[0] == "(":
            current += 1
            form = form[1:]
        elif form[0] == ")":
            current -= 1
            form = form[1:]
        else:
            # If we did not find a paranthese, we know that 
            # we should just apply the rule by priority
            if current < 0:
                raise "Error" 
            # Rule by priority means that the result is directly 
            # added to the final output
            if current == 0:
                output_final = output_final + output
                output = []
                if (clause_phase):
                    x = form[0]
                    form = form[1:]
                    output_final.append(x)
                    clause_phase = False
                else:
                    x = form[0]
                    form = form[1:]
                    prestack = [x] + prestack
                    if (not is_precstack(prestack)):
                        x = prestack[0]
                        prestack = prestack[1:]
                        while (prestack != []):
                            output_final.append(prestack[0])
                            prestack = prestack[1:]
                        prestack = [x] + prestack
                    clause_phase = True
            # Otherwise, we put it in a temporary output that 
            # we then append to the final output
            else:
                if (clause_phase):
                    x = form[0]
                    form = form[1:]
                    output.append(x)
                    clause_phase = False
                    if (form[0] == ")"):
                        while (prestack != []):
                            output.append(prestack[0])
                            prestack = prestack[1:]
                else:
                    x = form[0]
                    form = form[1:]
                    prestack = [x] + prestack
                    if (not is_precstack(prestack)):
                        x = prestack[0]
                        prestack = prestack[1:]
                        while (prestack != []):
                            output.append(prestack[0])
                            prestack = prestack[1:]
                        prestack = [x] + prestack
                    clause_phase = True
    output_final = output_final + output
    while (prestack != []):
        output_final.append(prestack[0])
        prestack = prestack[1:]
    return output_final

def parse_f(form, i = 0):
    if len(form) < i+3:
        return form
    if form[i+2] in ["imply", "and", "or"]:
        current = [form[i], form[i+1], form[i+2]]
        if i > 0:
            return parse_f(form[:i] + [current] + form[i+3:])
        else:
            return parse_f([current] + form[3:])
    else:
        return parse_f(form, i+1)

def translate(form):
    form_l = form.split(" ")
    return parse_f(syntax(form_l))

## TESTING 
print(translate("( ( A imply B ) and B ) imply C"))