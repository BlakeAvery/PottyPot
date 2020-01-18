""" Main file for PottyPot """
from speech import record_audio, speech_detect
from money import send_money
import logging

def main():

    SWEARS = {"heck" : 0.01,
              "fudge": 0.10,
              "darn" : 0.05
             }

    print("Welcome to PottyPot!")
    while True:

        print("-"*25)
        print("Start recording?")
        user_response = input("[y]/n> ")
        if user_response.lower() != "y" or not user_response:
            print("Invalid response")
            break

        file = record_audio(5)
        words = speech_detect(file)

        user_swears = [swear for swear in SWEARS if swear in '\n'.join(words)]
        if user_swears:
            print(f"Uh oh, you said {' '.join(user_swears)}!")

            price = float(0)
            for swear in user_swears:
                price += SWEARS[swear]

            price = str(price)[0:4]
            print(f"That'll be ${price}")
            response = send_money(price)
            print(f"Donated ${price}, thanks for swearing!")



if __name__ == "__main__":
    main()