import requests
import days

aocsession = {'session' : '53616c7465645f5f34e4a9993c93195351cfe429bb5fb3c168e4952524127fb73f629ccec41b8f99319ff7e4e9eabde8d7d87ad1199c7b6b181f592878e499ca'}

day = 19
bUseTestInput = True

if bUseTestInput:
    print("Loading test input from file")
    f = open("testinput.txt", "r")
    input = f.read().splitlines()
    f.close()
else:    
    url = 'https://adventofcode.com/2021/day/' + str(day) + '/input'
    print("Loading input from AoC: " + url)
    response = requests.get(url, cookies = aocsession)
    if response.status_code == 200:
        input = response.text.split('\n')
        input.pop()
    else:
        print("Web request failed! Check if session cookie is valid")
        print(response.status_code)
        print(response.text)

funcname1 = 'day' + str(day) + 'a'
funcname2 = 'day' + str(day) + 'b'
result = getattr(days, funcname1)(input)
print("Puzzle 1 result:", result)
result = getattr(days, funcname2)(input)
print("Puzzle 2 result:", result)
