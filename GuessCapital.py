import CountryScraper
import random

#gets country from a specified index and returns it 
def pickRandomKey(dictionary):
    randomInt = random.randint(0, len(dictionary) - 1)
    for i, key in enumerate(dictionary.keys()):
        if i == randomInt:
            return key

#appends correct choice in a list (along with some wrong ones)
#then shuffles the list and returns it 
def getChoices(dictionary, correctValue): 
    choices = []
    choices.append(correctValue)

    i = 0
    while i < NUMBER_OF_WRONG_CHOICES: 
        wrongKey = pickRandomKey(dictionary)
        wrongValue = dictionary[wrongKey].get("capital")
        #only unique answers/values should be added to the list
        if wrongValue not in choices: 
            choices.append(wrongValue)
            i += 1

    random.shuffle(choices)
    return choices

#specifies the range of the number 
MIN_NUMBER_OF_QUESTIONS = 5
MAX_NUMBER_OF_QUESTIONS = 100
NUMBER_OF_WRONG_CHOICES = 3

#tell player about the game, how to play it, and how to win it
print("Welcome to Guess the Capital.")
print(f"You will be asked what is the capital of a given country and you have to answer correctly. \nScore as many points as you can to see how well you know your countries.")
#ask user to type "Y" to start (or "Yes")
answerGame = input("Will you play the game? (Type \"Y\" to proceed.) ") 
# answerGame - answer to playing the game
print()

#======================== GAME START =========================
while(answerGame.upper() == 'Y' or answerGame.upper() == 'Yes'):
    #initialise web scraper
    countryScraper = CountryScraper.CountryScraper()
    #get countries from scraper
    countries = countryScraper.getCountries()
    #set/reset score and guessedCountries
    score = 0
    guessedCountries = [] #keep track of countries already asked about

    #ask user about how many questions would they like to be asked 
    #should be within the minimum and maximum number of questions
    numberOfQuestions = input(f"How many questions do you want to answer? (minimum of {MIN_NUMBER_OF_QUESTIONS} questions, maximum of {MAX_NUMBER_OF_QUESTIONS} questions): ")

    #prompt user for the number of questions again if input is invalid
    #or out of the minimum or maximum number
    while int(numberOfQuestions) not in range(MIN_NUMBER_OF_QUESTIONS, MAX_NUMBER_OF_QUESTIONS + 1) or not numberOfQuestions.isdigit(): 
        if not numberOfQuestions.isdigit(): 
            print("Invalid input. Try again.")
        else: 
            print("Invalid number of questions. Try again.")
        numberOfQuestions = input(f"How many questions do you want to answer? (minimum of {MIN_NUMBER_OF_QUESTIONS} questions, maximum of {MAX_NUMBER_OF_QUESTIONS} questions): ")

    numberOfQuestions = int(numberOfQuestions) #convert input to int

    for i in range(numberOfQuestions): 
        randomCountry = pickRandomKey(countries)
        #for succeeding rounds, pick a unique country to ask user for the 
        #capital of (not in guessedCountries list)
        while randomCountry in guessedCountries: 
            randomCountry = pickRandomKey(countries)
        
        #after getting a unique country, put it in guessedCountries
        #so that it won't be asked again
        guessedCountries.append(randomCountry)
        #get the correct capital of the country
        #and store it in correctCapital
        correctCapital = countries[randomCountry].get("capital")
        #get 3 other wrong answers and store it in list
        capitals = getChoices(countries, correctCapital)
        print(f"Question {i + 1}: What is the capital of {randomCountry}?")
        for j, capital in enumerate(capitals): 
            print(f"{j + 1} - {capital}")
        print()
        answerRound = input("Type the number of your choice: ")
        #answerRound - answer in one round of the game
        
        #prompt user for input as long as number is not in the choices
        #or if user types non-numeric characters
        while int(answerRound) not in range(1, len(capitals) + 1) or not answerRound.isdigit(): 
            print("Invalid input. Try again.")
            answerRound = input("Type the number of your choice: ")

        #convert answer to int and subtract it by 1 
        #to match it to one of the options in the multiple choice
        indexChoice = int(answerRound) - 1

        #if value of chosen index matches the correct answer
        # add 1 point to the score
        if capitals[indexChoice] == correctCapital: 
            print("Correct! You get a point.")
            score += 1 
        else: #otherwise, tell user correct answer
            print(f"The correct answer is {correctCapital}.")

        #also tell user their total score
        print(f"You have {score} point(s).")
        print()

    #once all questions have been answered, tell user their score
    #and compare it to the number of questions they wanted to be asked
    #then ask user if they want to play again
    #they must enter "Y" (or "Yes") to do so 
    print(f"Game over. You got {score} out of {numberOfQuestions} points.")
    answerGame = input("Play again? (Type \"Y\" to proceed.) ") 
    print()
